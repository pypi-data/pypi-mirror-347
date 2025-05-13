"""
Data loading module for PyScrew.

This module provides functionality for downloading and extracting datasets from Zenodo.
It handles secure file operations, archive extraction, and dataset management.

Key features:
    - Secure downloading and extraction of ZIP archives
    - Checksum verification for data integrity
    - Caching mechanism to prevent redundant downloads
    - Protection against path traversal attacks
    - Cross-platform compatibility (Windows/Unix)

Usage:
    loader = DataLoader("scenario_name")
    extracted_path = loader.extract_data()

The module maintains a two-tier cache structure:
    ~/.cache/pyscrew/
    ├── archives/     # Stores downloaded compressed files
    └── extracted/    # Stores extracted datasets
"""

import hashlib
import os
import shutil
import zipfile
from pathlib import Path
from typing import Optional, Union

import requests
from tqdm import tqdm

from pyscrew.config import ScenarioConfig
from pyscrew.utils.logger import get_logger

logger = get_logger(__name__)


class SecurityError(Exception):
    """Raised when security violations occur during archive extraction, such as path traversal attempts."""

    pass


class ExtractionError(Exception):
    """Raised when archive extraction fails due to corruption, format issues, or system constraints."""

    pass


class ChecksumError(Exception):
    """Raised when file integrity verification fails due to hash mismatches or incomplete transfers."""

    pass


class DownloadError(Exception):
    """Raised when file download fails due to network issues, server errors, or resource problems."""

    pass


class DataLoader:
    """
    Handles downloading and extracting datasets from Zenodo.

    This class manages the entire lifecycle of dataset retrieval:
    1. Downloads the archive if not cached
    2. Verifies the checksum
    3. Extracts the contents securely
    4. Manages the cache structure

    The cache structure uses two directories:
    - archives/: For storing downloaded compressed files
    - extracted/: For storing the extracted data

    Args:
        scenario_name: Name of the scenario to load
        cache_dir: Optional directory for storing downloaded and extracted files.
                  Defaults to ~/.cache/pyscrew

    Security features:
        - Checksum verification
        - Path traversal protection
        - Secure file permissions
        - Safe archive extraction
    """

    # Using a small chunk size (2MB) optimizes both download speed and memory usage
    # Small chunks = more iterations and overhead
    # Large chunks = more memory usage and potential timeout issues
    CHUNK_SIZE = 2 * 1024 * 1024

    def __init__(
        self,
        scenario_config: ScenarioConfig,
    ):
        """
        Initialize the data loader for a specific scenario.

        Args:
            scenario_config: Configuration object for the scenario to load
                            (contains cache_dir and force_download settings)
        """
        self.scenario_config = scenario_config
        self.download_url = self.scenario_config.get_download_url()
        self.file_name = self.scenario_config.get_dataset_filename()

        # Get the already-resolved cache_dir from scenario_config
        self.cache_dir = self.scenario_config.cache_dir
        
        # Ensure the cache_dir is absolute
        self.cache_dir = self.cache_dir.absolute()

        # Log the actual path being used
        logger.info(f"Using cache directory (absolute): {self.cache_dir}")

        # Set up cache subdirectories
        self.archive_cache = self.cache_dir / "archives"
        self.data_cache = self.cache_dir / "extracted"

        # Create directories with secure permissions to prevent tampering
        self._create_secure_directory(self.archive_cache)
        self._create_secure_directory(self.data_cache)

    def get_data(self, force: bool = False) -> Path:
        """
        Get the dataset, downloading if necessary.

        This method manages the complete dataset acquisition process:
        1. Downloads the file if needed (or if force=True)
        2. Verifies archive integrity
        3. Implements a single retry on verification failure

        The retry mechanism provides resilience against:
        - Corrupted downloads
        - Network interruptions
        - Incomplete transfers

        Args:
            force: If True, force new download even if files exist

        Returns:
            Path to the downloaded and verified file

        Raises:
            DownloadError: If download fails after retry
            ChecksumError: If checksum verification fails
            ExtractionError: If archive verification fails
        """
        try:
            # Download file if needed or if force=True
            archive_path = self._download_file(force=force)

            # Verify archive integrity with retry mechanism
            try:
                self._verify_archive(archive_path)
            except ExtractionError:
                logger.error(
                    f"Archive verification failed for '{archive_path.name}'. The file may be corrupted."
                )
                # Remove potentially corrupted file
                archive_path.unlink()

                # Implement single retry unless force was specified
                if not force:
                    logger.info(
                        f"Retrying download of '{self.file_name}' after verification failure..."
                    )
                    archive_path = self._download_file(force=True)
                    self._verify_archive(archive_path)

            return archive_path

        except Exception as e:
            logger.error(f"Error getting data for '{self.file_name}': {str(e)}")
            raise

    def extract_data(self, force: bool = False) -> Path:
        """
        Extract the downloaded archive to the cache directory.

        This method ensures a consistent extraction structure:
        ~/.cache/pyscrew/
        ├── archives/     # Stores downloaded compressed files
        └── extracted/    # Root extraction directory
            └── scenario_name/  # e.g., s01_thread-degradation/
                └── json/  # Contains all JSON data files

        Args:
            force: If True, force re-extraction even if files exist,
                ignoring and overwriting any existing data

        Returns:
            Path to the extracted data directory
            (e.g., ~/.cache/pyscrew/extracted/s01_thread-degradation/)

        Raises:
            DownloadError: If archive download fails
            ExtractionError: If extraction fails or json/ directory is missing
            SecurityError: If security checks fail during extraction
            ChecksumError: If archive verification fails
        """
        logger.info(
            f"Beginning data extraction for scenario '{self.file_name}' (force={force})"
        )
        archive_path = self.get_data(force=force)

        # Get scenario name without extension
        scenario_name = Path(self.file_name).stem

        # Create extraction path at the correct level
        data_path = self.data_cache / scenario_name
        json_path = data_path / "json"

        # Check if json directory already exists and has content
        if not force and json_path.exists() and any(json_path.iterdir()):
            logger.info(
                f"Using existing extracted data for scenario '{scenario_name}' at: {json_path}"
            )
            return data_path

        try:
            # Clean up existing scenario directory if it exists
            if data_path.exists():
                self._clean_directory(data_path)

            # Create scenario directory
            data_path.mkdir(parents=True, exist_ok=True)

            logger.info(
                f"Extracting archive '{archive_path.name}' to directory: {data_path}"
            )
            self._extract_archive(archive_path, data_path)

            # Verify json directory exists after extraction
            if not json_path.exists():
                raise ExtractionError(
                    f"Expected json directory not found in extracted data for '{scenario_name}'"
                )

            logger.info(
                f"Extraction of '{archive_path.name}' completed successfully to: {data_path}"
            )
            return data_path

        except Exception as e:
            logger.error(f"Failed to extract dataset '{scenario_name}': {str(e)}")
            if data_path.exists():
                # Clean up on failure
                self._clean_directory(data_path)
            raise

    def _create_secure_directory(self, path: Path, mode: int = 0o750) -> None:
        """
        Create a directory with secure permissions.

        Mode 0o750 provides:
        - Owner: read/write/execute (7)
        - Group: read/execute (5)
        - Others: no permissions (0)
        """
        logger.debug(f"Creating directory '{path}' with permissions {oct(mode)}")
        path.mkdir(parents=True, exist_ok=True)
        path.chmod(mode)

    def _check_file_exists(self, file_path: Path) -> bool:
        """
        Check if a file exists and is not empty.
        Empty files could indicate interrupted downloads or extraction.
        """
        exists = file_path.exists() and file_path.stat().st_size > 0
        logger.debug(
            f"File existence check: '{file_path.name}' exists={exists}, size={file_path.stat().st_size if exists else 0:,} bytes"
        )
        return exists

    def _get_archive_path(self) -> Path:
        """Get the full path for the archive file in cache."""
        return self.archive_cache / self.file_name

    def _calculate_md5(self, file_path: Path) -> str:
        """
        Calculate MD5 hash of a file using streaming.

        Uses chunked reading to handle large files efficiently:
        - Prevents loading entire file into memory
        - Maintains consistent memory usage regardless of file size
        - Allows for progress monitoring if needed
        """
        logger.debug(f"Beginning MD5 calculation for '{file_path.name}'")
        md5_hash = hashlib.md5()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(self.CHUNK_SIZE), b""):
                md5_hash.update(chunk)

        return md5_hash.hexdigest()

    def _verify_checksum(self, file_path: Path) -> bool:
        """Verify the MD5 checksum of downloaded file."""
        logger.info(f"Verifying MD5 checksum for '{file_path.name}'...")
        calculated_hash = self._calculate_md5(file_path)

        if calculated_hash != self.scenario_config.get_md5_checksum():
            logger.error("Checksum verification failed!")
            logger.error(f"Expected: {self.scenario_config.get_md5_checksum()}")
            logger.error(f"Got: {calculated_hash}")
            raise ChecksumError(f"File checksum mismatch for {file_path}")

        logger.info(
            f"Checksum verification successful for '{file_path.name}' (MD5: {calculated_hash})"
        )
        return True

    def _download_file(self, force: bool = False) -> Path:
        """
        Download and verify file from Zenodo.

        The download process:
        1. Check if file exists and has valid checksum (unless force=True)
        2. Download to temporary file with progress bar
        3. Set secure permissions
        4. Verify checksum
        5. Move to final location

        Args:
            force: If True, force new download even if file exists

        Returns:
            Path to the downloaded file

        Raises:
            DownloadError: If download fails
            ChecksumError: If verification fails
        """
        archive_path = self._get_archive_path()

        # Only check existing file if not forcing re-download
        if not force and archive_path.exists():
            try:
                if self._verify_checksum(archive_path):
                    logger.info(
                        f"Using existing verified file '{archive_path.name}' at: {archive_path}"
                    )
                    return archive_path
            except ChecksumError:
                logger.warning(
                    f"Existing file '{archive_path.name}' failed checksum verification"
                )
                logger.info(f"Will download fresh copy of '{self.file_name}'")
                archive_path.unlink()

        logger.info(
            f"Downloading dataset '{self.file_name}' from Zenodo URL: {self.download_url}"
        )
        try:
            # Start streaming download
            response = requests.get(self.download_url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            # Use temporary file for atomic operation
            temp_path = archive_path.with_suffix(".tmp")

            with open(temp_path, "wb") as f:
                with tqdm(
                    total=total_size,
                    unit="iB",
                    unit_scale=True,
                    desc="Downloading",
                    leave=False,
                ) as pbar:
                    for data in response.iter_content(self.CHUNK_SIZE):
                        size = f.write(data)
                        pbar.update(size)

            # Set secure permissions before moving to final location
            # Owner: rw, Group: r, Others: none
            temp_path.chmod(0o640)

            # Atomic move to final location
            if archive_path.exists():
                archive_path.unlink()  # Required for Windows
            temp_path.rename(archive_path)

            logger.info(
                f"Download of '{self.file_name}' completed ({total_size:,} bytes). Beginning checksum verification..."
            )
            self._verify_checksum(archive_path)
            return archive_path

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Network error while downloading '{self.file_name}': {str(e)}"
            )
            if archive_path.exists():
                archive_path.unlink()
            raise DownloadError(f"Failed to download {self.file_name}: {str(e)}") from e
        except Exception as e:
            logger.error(
                f"Unexpected error during download of '{self.file_name}': {str(e)}"
            )
            if archive_path.exists():
                archive_path.unlink()
            raise

    def _clean_directory(self, path: Path):
        """
        Recursively remove a directory and all its contents.
        Handles Windows file locking and permission issues.
        """
        if not path.exists():
            return

        try:
            shutil.rmtree(path, ignore_errors=False)
        except Exception as e:
            logger.warning(
                f"Unable to remove directory '{path}' (will try manual removal): {e}"
            )
            # If rmtree fails, try manual removal
            try:
                for item in path.iterdir():
                    if item.is_file():
                        item.unlink(missing_ok=True)
                    elif item.is_dir():
                        self._clean_directory(item)
                path.rmdir()
            except Exception as e:
                logger.error(
                    f"Failed to clean directory '{path}'. Manual removal unsuccessful: {e}"
                )

    def _verify_archive(self, archive_path: Path) -> bool:
        """
        Verify the integrity of the downloaded ZIP archive.

        Uses built-in testzip() to check CRC32 checksums, which:
        - Streams through archive contents instead of loading entirely
        - Maintains constant memory usage regardless of archive size
        - Prevents potential out-of-memory issues with large archives

        Args:
            archive_path: Path to the archive file

        Returns:
            True if verification succeeds

        Raises:
            ExtractionError: If archive is corrupted or invalid
        """
        try:
            with zipfile.ZipFile(archive_path, "r") as zip:
                # testzip() returns None if all CRC32 checksums match
                if zip.testzip() is not None:
                    raise ExtractionError("ZIP archive is corrupted")
            return True
        except Exception as e:
            logger.error(
                f"ZIP archive verification failed for '{archive_path.name}': {str(e)}"
            )
            raise ExtractionError(f"Archive verification failed: {str(e)}") from e

    def _check_path_traversal(self, path: Union[str, Path]) -> bool:
        """Check if a path attempts directory traversal."""
        path_str = str(Path(path))
        normalized = os.path.normpath(path_str)

        # Check for absolute paths (both Unix and Windows)
        if os.path.isabs(path_str):
            return False

        return not (path_str != normalized or ".." in normalized.split(os.sep))

    def _extract_archive(self, archive_path: Path, extract_to: Path) -> None:
        """
        Extract a ZIP archive securely with comprehensive safety checks.

        Security measures:
        1. Path validation
            - Blocks directory traversal attempts
            - Handles ZIP-specific path separators
            - Cross-platform path normalization
        2. Controlled extraction
            - Pre-validates all paths
            - Atomic operation (all or nothing)

        Args:
            archive_path: Path to the ZIP archive
            extract_to: Destination directory

        Raises:
            SecurityError: On security check failures
            ExtractionError: On extraction failures
        """
        try:
            with zipfile.ZipFile(archive_path, "r") as zip:
                # Validate all paths before extraction begins
                for zip_info in zip.filelist:
                    if not self._check_path_traversal(zip_info.filename):
                        raise SecurityError(
                            f"Path traversal attempt detected: {zip_info.filename}"
                        )

                # All paths validated, proceed with extraction
                zip.extractall(path=extract_to)
        except (SecurityError, ExtractionError):
            raise
        except Exception as e:
            raise ExtractionError(f"Failed to extract {archive_path}: {str(e)}") from e


def load_data(scenario_config: ScenarioConfig) -> None:
    """
    Load dataset according to pipeline configuration.

    This function handles the complete data loading process:
    1. Downloads and extracts the dataset (if needed)
    2. Creates a ScrewDataset instance with proper filtering
    3. Validates measurement data integrity

    Args:
        scenario_config: Scenario configuration object containing
                        cache_dir and force_download settings

    Raises:
        ValueError: If configuration is invalid
        SecurityError: If data extraction encounters security issues
        ChecksumError: If downloaded file fails verification
    """
    # Initialize loader for the configured scenario
    loader = DataLoader(scenario_config)

    # Extract data with force flag from scenario_config
    loader.extract_data(force=scenario_config.get_force_download())
