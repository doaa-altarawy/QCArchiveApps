"""
Web portal applications for the QCArchive project.
"""

from .app import app, server
from . import index

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
