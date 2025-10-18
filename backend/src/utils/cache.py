"""File-based caching for 10-K data"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional
from src.core.logging_config import logger


class FileCache:
    """Simple file-based cache with TTL support"""

    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"Cache initialized at {self.cache_dir}")

    def _get_cache_path(self, key: str) -> Path:
        """Generate cache file path from key"""
        # Use MD5 hash to create safe filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def _get_metadata_path(self, key: str) -> Path:
        """Get metadata file path"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.meta.json"

    def get(self, key: str, max_age: Optional[timedelta] = None) -> Optional[Any]:
        """
        Get cached value if exists and not expired

        Args:
            key: Cache key
            max_age: Maximum age for cached data (None = no expiration)

        Returns:
            Cached value or None if not found/expired
        """
        cache_file = self._get_cache_path(key)
        meta_file = self._get_metadata_path(key)

        if not cache_file.exists():
            logger.debug(f"Cache miss: {key}")
            return None

        try:
            # Read metadata
            if meta_file.exists():
                with open(meta_file, 'r') as f:
                    metadata = json.load(f)
                    cached_at = datetime.fromisoformat(metadata["cached_at"])

                    # Check expiration
                    if max_age:
                        age = datetime.now() - cached_at
                        if age > max_age:
                            logger.info(f"Cache expired: {key} (age: {age.days} days)")
                            # Clean up expired cache
                            cache_file.unlink(missing_ok=True)
                            meta_file.unlink(missing_ok=True)
                            return None

            # Read cached data
            with open(cache_file, 'r') as f:
                cached = json.load(f)

            logger.info(f"Cache hit: {key}")
            return cached

        except Exception as e:
            logger.error(f"Cache read error for {key}: {e}")
            return None

    def set(self, key: str, value: Any, metadata: Optional[dict] = None):
        """
        Cache value with optional metadata

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            metadata: Optional metadata dictionary
        """
        cache_file = self._get_cache_path(key)
        meta_file = self._get_metadata_path(key)

        try:
            # Write data
            with open(cache_file, 'w') as f:
                json.dump(value, f, indent=2)

            # Write metadata
            meta = {
                "key": key,
                "cached_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)

            logger.info(f"Cached: {key}")

        except Exception as e:
            logger.error(f"Cache write error for {key}: {e}")
            # Clean up partial writes
            cache_file.unlink(missing_ok=True)
            meta_file.unlink(missing_ok=True)

    def delete(self, key: str):
        """Delete cached entry"""
        cache_file = self._get_cache_path(key)
        meta_file = self._get_metadata_path(key)

        cache_file.unlink(missing_ok=True)
        meta_file.unlink(missing_ok=True)
        logger.info(f"Cache deleted: {key}")

    def clear(self):
        """Clear all cache entries"""
        for file in self.cache_dir.glob("*.json"):
            file.unlink()
        logger.info("Cache cleared")

    def get_info(self, key: str) -> Optional[dict]:
        """Get cache metadata without loading data"""
        meta_file = self._get_metadata_path(key)

        if not meta_file.exists():
            return None

        try:
            with open(meta_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading cache metadata: {e}")
            return None
