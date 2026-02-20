"""
Test settings — uses the same SpatiaLite backend as development.
"""

from .development import *  # noqa: F401, F403

# Use a separate test database
DATABASES["default"]["NAME"] = BASE_DIR / "test_db.sqlite3"  # noqa: F405
