"""
Duplicate detection and handling for measurement time series.

This transformer processes the standardized measurement data to detect and resolve
duplicate time points. It handles cases where multiple measurements exist at the
same time point using various configurable strategies.

Key Features:
    - Detection of exact duplicates vs value differences
    - Multiple handling methods (mean, first, last)
    - Detailed statistics tracking
    - Preservation of all metadata fields
    - Input validation and error handling
"""

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from numpy.typing import NDArray
from sklearn.base import BaseEstimator, TransformerMixin

from pyscrew.config import PipelineConfig
from pyscrew.core import OutputFields, ScrewDataset
from pyscrew.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class DuplicateStats:
    """Statistics about duplicate detection and removal.

    Attributes:
        total_series: Number of time series processed
        total_points: Total measurement points across all series
        total_removed: Number of duplicate points removed
        total_true_duplicates: Number of exact duplicates (all values match)
        total_value_differences: Number of duplicates with different values
    """

    total_series: int = 0
    total_points: int = 0
    total_removed: int = 0
    total_true_duplicates: int = 0
    total_value_differences: int = 0


class DuplicateProcessingError(Exception):
    """Raised when duplicate processing fails."""

    pass


class HandleDuplicatesTransformer(BaseEstimator, TransformerMixin):
    """Handles duplicate time points in measurement data.

    This transformer detects and resolves cases where multiple measurements
    exist for the same time point. It provides different methods for
    handling these duplicates and tracks detailed statistics about the
    types of duplicates found.

    Args:
        config: PipelineConfig object containing processing settings
            The config.handle_duplicates field determines how to handle duplicates:
            - 'mean': Use average of measurements (default)
            - 'first': Keep first occurrence
            - 'last': Keep last occurrence
            - None: Do not handle duplicates

    Attributes:
        config: Configuration settings for the pipeline
        outputs: OutputFields instance for accessing standardized field names
        _stats: Statistics about processed duplicates

    Example:
        >>> # Initialize transformer with pipeline config
        >>> transformer = HandleDuplicatesTransformer(config)
        >>>
        >>> # Process dataset
        >>> processed = transformer.fit_transform(dataset)
        >>>
        >>> # Check statistics
        >>> print(f"Removed {transformer._stats.total_removed} duplicates")
        >>> print(f"Found {transformer._stats.total_value_differences} conflicts")

    Note:
        Step indicators are always handled using 'first' method to
        maintain sequence integrity, regardless of chosen method.

    Raises:
        DuplicateProcessingError: If processing fails due to invalid data
        ValueError: If an invalid method is specified
    """

    def __init__(self, config: PipelineConfig) -> None:
        """Initialize transformer with pipeline configuration."""
        self.config = config
        self.outputs = OutputFields()
        self._stats = DuplicateStats()

    def _validate_arrays(
        self,
        time: NDArray[np.float64],
        torque: NDArray[np.float64],
        angle: NDArray[np.float64],
        gradient: NDArray[np.float64],
        steps: NDArray[np.float64],
    ) -> None:
        """Validate input arrays before processing.

        Args:
            time: Time measurements
            torque: Torque measurements
            angle: Angle measurements
            gradient: Gradient measurements
            steps: Step indicators

        Raises:
            DuplicateProcessingError: If validation fails
        """
        arrays = [time, torque, angle, gradient, steps]
        length = len(time)

        # Check array lengths
        if not all(len(arr) == length for arr in arrays):
            raise DuplicateProcessingError(
                f"Inconsistent array lengths: {[len(arr) for arr in arrays]}"
            )

        # Check for NaN/inf values
        for arr_name, arr in zip(
            ["time", "torque", "angle", "gradient", "steps"],
            arrays,
            strict=False,
        ):
            if not np.isfinite(arr).all():
                raise DuplicateProcessingError(
                    f"Found NaN or infinite values in {arr_name}"
                )

    def _process_series(
        self,
        time: NDArray[np.float64],
        torque: NDArray[np.float64],
        angle: NDArray[np.float64],
        gradient: NDArray[np.float64],
        steps: NDArray[np.float64],
    ) -> Dict[str, List[float]]:
        """Process a single measurement series.

        Args:
            time: Time measurements
            torque: Torque measurements
            angle: Angle measurements
            gradient: Gradient measurements
            steps: Step indicators

        Returns:
            Dictionary containing processed measurements

        Raises:
            DuplicateProcessingError: If processing fails
        """
        try:
            self._validate_arrays(time, torque, angle, gradient, steps)

            if self.config.handle_duplicates == "first":
                _, unique_indices = np.unique(time, return_index=True)
                mask = np.isin(np.arange(len(time)), unique_indices)
            elif self.config.handle_duplicates == "last":
                _, unique_indices = np.unique(time[::-1], return_index=True)
                mask = np.isin(np.arange(len(time)), len(time) - 1 - unique_indices)
            else:  # mean method
                unique_times, inverse_indices, counts = np.unique(
                    time, return_inverse=True, return_counts=True
                )

                # Track duplicate statistics
                for i in range(len(unique_times)):
                    if counts[i] > 1:
                        idx = np.where(inverse_indices == i)[0]
                        duplicates_removed = counts[i] - 1
                        self._stats.total_removed += duplicates_removed

                        # Check if all values at these indices are identical
                        all_match = (
                            len(np.unique(torque[idx])) == 1
                            and len(np.unique(angle[idx])) == 1
                            and len(np.unique(gradient[idx])) == 1
                        )

                        if all_match:
                            self._stats.total_true_duplicates += duplicates_removed
                        else:
                            self._stats.total_value_differences += duplicates_removed

                # Calculate means for each unique time
                mean_values = {
                    self.outputs.TIME_VALUES: unique_times,
                    self.outputs.TORQUE_VALUES: np.zeros_like(unique_times),
                    self.outputs.ANGLE_VALUES: np.zeros_like(unique_times),
                    self.outputs.GRADIENT_VALUES: np.zeros_like(unique_times),
                    self.outputs.STEP_VALUES: np.zeros_like(unique_times),
                }

                # Calculate means for each measurement type
                for i in range(len(unique_times)):
                    idx = inverse_indices == i
                    mean_values[self.outputs.TORQUE_VALUES][i] = np.mean(torque[idx])
                    mean_values[self.outputs.ANGLE_VALUES][i] = np.mean(angle[idx])
                    mean_values[self.outputs.GRADIENT_VALUES][i] = np.mean(
                        gradient[idx]
                    )
                    mean_values[self.outputs.STEP_VALUES][i] = np.mean(steps[idx])

                return {k: v.tolist() for k, v in mean_values.items()}

            # For first/last methods
            if self.config.handle_duplicates in ["first", "last"]:
                duplicate_indices = np.where(~mask)[0]
                series_true_duplicates = 0
                series_value_differences = 0

                for dup_idx in duplicate_indices:
                    # Find the kept index
                    kept_idx = (
                        np.where(mask[: dup_idx + 1])[0][-1]
                        if self.config.handle_duplicates == "first"
                        else np.where(mask[dup_idx:])[0][0] + dup_idx
                    )

                    # Check for true duplicates
                    matches = [
                        torque[kept_idx] == torque[dup_idx],
                        angle[kept_idx] == angle[dup_idx],
                        gradient[kept_idx] == gradient[dup_idx],
                    ]

                    if all(matches):
                        series_true_duplicates += 1
                    else:
                        series_value_differences += 1

                self._stats.total_true_duplicates += series_true_duplicates
                self._stats.total_value_differences += series_value_differences
                self._stats.total_removed += len(duplicate_indices)

                return {
                    self.outputs.TIME_VALUES: time[mask].tolist(),
                    self.outputs.TORQUE_VALUES: torque[mask].tolist(),
                    self.outputs.ANGLE_VALUES: angle[mask].tolist(),
                    self.outputs.GRADIENT_VALUES: gradient[mask].tolist(),
                    self.outputs.STEP_VALUES: steps[mask].tolist(),
                }

        except Exception as e:
            raise DuplicateProcessingError(f"Failed to process series: {str(e)}") from e

    def fit(self, dataset: ScrewDataset, y=None) -> "HandleDuplicatesTransformer":
        """Validate handling method and data structure.

        Args:
            dataset: Input dataset to validate
            y: Ignored, exists for scikit-learn compatibility

        Returns:
            self: This transformer instance

        Raises:
            ValueError: If handling method is invalid
        """
        if self.config.handle_duplicates not in ["mean", "first", "last"]:
            raise ValueError(
                f"Invalid method: {self.config.handle_duplicates}. "
                f"Must be one of: mean, first, last"
            )
        return self

    def transform(self, dataset: ScrewDataset) -> ScrewDataset:
        """Transform the dataset by removing duplicates.

        If config.handle_duplicates is None, returns the dataset unchanged.
        Otherwise, processes the dataset to remove duplicates using the specified method.

        Note: The returned dataset maintains the same type structure
        with processed_data: Dict[str, List[List[float]]]
        """
        # If no duplicate handling is configured, return dataset unchanged
        if self.config.handle_duplicates is None:
            logger.info("Duplicate handling disabled (handle_duplicates=None)")
            return dataset

        # Reset statistics
        self._stats = DuplicateStats()

        # Initialize processed data structure
        processed_data = {
            self.outputs.TIME_VALUES: [],
            self.outputs.TORQUE_VALUES: [],
            self.outputs.ANGLE_VALUES: [],
            self.outputs.GRADIENT_VALUES: [],
            self.outputs.STEP_VALUES: [],
        }

        # Preserve all metadata fields
        metadata_fields = [
            self.outputs.CLASS_VALUES,
            self.outputs.WORKPIECE_LOCATION,
            self.outputs.WORKPIECE_USAGE,
            self.outputs.WORKPIECE_RESULT,
            self.outputs.SCENARIO_CONDITION,
            self.outputs.SCENARIO_EXCEPTION,
        ]

        # Copy metadata fields from the input dataset if they exist
        for field in metadata_fields:
            if field in dataset.processed_data:
                processed_data[field] = dataset.processed_data[field]
                logger.debug(f"Preserved metadata field: {field}")

        try:
            # Process each run
            self._stats.total_series = len(
                dataset.processed_data[self.outputs.TIME_VALUES]
            )

            for idx in range(self._stats.total_series):
                # Get measurements from processed_data as numpy arrays
                time = np.array(dataset.processed_data[self.outputs.TIME_VALUES][idx])
                torque = np.array(
                    dataset.processed_data[self.outputs.TORQUE_VALUES][idx]
                )
                angle = np.array(dataset.processed_data[self.outputs.ANGLE_VALUES][idx])
                gradient = np.array(
                    dataset.processed_data[self.outputs.GRADIENT_VALUES][idx]
                )

                # Handle steps if they exist in processed_data
                if self.outputs.STEP_VALUES in dataset.processed_data:
                    steps = np.array(
                        dataset.processed_data[self.outputs.STEP_VALUES][idx]
                    )
                else:
                    steps = np.zeros_like(time)  # Use zeros if no steps

                self._stats.total_points += len(time)

                # Process the series
                result = self._process_series(time, torque, angle, gradient, steps)

                # Store processed results
                measurement_fields = [
                    self.outputs.TIME_VALUES,
                    self.outputs.TORQUE_VALUES,
                    self.outputs.ANGLE_VALUES,
                    self.outputs.GRADIENT_VALUES,
                    self.outputs.STEP_VALUES,
                ]

                for field in measurement_fields:
                    if field in result:
                        processed_data[field].append(result[field])

            # Log summary statistics
            self._log_summary()

            # Update dataset and return
            dataset.processed_data = processed_data
            return dataset

        except Exception as e:
            raise DuplicateProcessingError(
                f"Failed to transform dataset: {str(e)}"
            ) from e

    def _log_summary(self) -> None:
        """Log summary statistics of duplicate removal."""
        stats = self._stats

        # Calculate percentages
        removal_percent = (
            (stats.total_removed / stats.total_points * 100)
            if stats.total_points > 0
            else 0
        )
        true_dup_percent = (
            (stats.total_true_duplicates / stats.total_removed * 100)
            if stats.total_removed > 0
            else 0
        )
        diff_percent = (
            (
                stats.total_value_differences
                / (stats.total_true_duplicates + stats.total_value_differences)
                * 100
            )
            if (stats.total_true_duplicates + stats.total_value_differences) > 0
            else 0
        )
        avg_removed = (
            stats.total_removed / stats.total_series if stats.total_series > 0 else 0
        )

        logger.info(
            f"Completed duplicate removal using '{self.config.handle_duplicates}' method"
        )
        logger.info(
            f"Processed {stats.total_series:,} series with {stats.total_points:,} total points"
        )

        logger.info(
            f"Found {stats.total_true_duplicates:,} true duplicates ({true_dup_percent:.1f}%) and {stats.total_value_differences:,} value differences ({diff_percent:.1f}%)"
        )
        logger.info(
            f"Removed {stats.total_removed:,} points (-{removal_percent:.1f}% of total)"
        )
        logger.info(f"Average {avg_removed:.2f} points removed per series")
