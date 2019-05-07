"""
Unit and regression test for the QCArchiveApps package.
"""

# Import package, test suite, and other packages as needed
import QCArchiveApps
import pytest
import sys

def test_QCArchiveApps_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "QCArchiveApps" in sys.modules
