"""
FluidGrids SDK
--------------

A Python SDK for the FluidGrids Workflow Engine by Algoshred Technologies Private Limited.
"""

from .client import FluidGridsClient
from .auth import AuthClient
from .workflows import WorkflowClient
from .runs import RunClient
from .config import ConfigClient
from .credentials import CredentialClient
from .ai import AIClient
from .usage import UsageClient
from .dashboard import DashboardClient
from .search import SearchClient
from .nodes import NodeClient

__all__ = [
    "FluidGridsClient",
    "AuthClient",
    "WorkflowClient",
    "RunClient",
    "ConfigClient", 
    "CredentialClient",
    "AIClient",
    "UsageClient",
    "DashboardClient",
    "SearchClient",
    "NodeClient"
]
__version__ = "0.1.0"
__author__ = "Vignesh T.V"
__email__ = "vignesh@algoshred.com"
__copyright__ = "Copyright 2023 Algoshred Technologies Private Limited"
__license__ = "MIT"
__url__ = "https://fluidgrids.ai/" 