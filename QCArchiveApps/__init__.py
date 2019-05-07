"""
QCArchiveApps
Web portal applications for the QCArchive project.
"""

# Add imports here
from .qcarchiveapps import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
