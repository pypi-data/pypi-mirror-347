"""
FluidGrids client module
"""
from typing import Dict, Optional

from .workflows import WorkflowClient
from .runs import RunClient
from .auth import AuthClient
from .config import ConfigClient
from .credentials import CredentialClient
from .ai import AIClient
from .usage import UsageClient
from .dashboard import DashboardClient
from .search import SearchClient
from .nodes import NodeClient


class FluidGridsClient:
    """
    Main client for interacting with the FluidGrids Workflow Engine.
    
    Args:
        base_url: The base URL of the FluidGrids API
        api_key: API key for authentication (optional)
        username: Username for authentication (optional if api_key is provided)
        password: Password for authentication (optional if api_key is provided)
        token: JWT token for authentication (optional if api_key, or username/password are provided)
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._token = token
        self._username = username
        self._password = password
        
        self._auth_headers = {}
        if api_key:
            self._auth_headers = {"Authorization": f"ApiKey {api_key}"}
        elif token:
            self._auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Initialize sub-clients
        self.auth = AuthClient(self)
        self.workflows = WorkflowClient(self)
        self.runs = RunClient(self)
        self.config = ConfigClient(self)
        self.credentials = CredentialClient(self)
        self.ai = AIClient(self)
        self.usage = UsageClient(self)
        self.dashboard = DashboardClient(self)
        self.search = SearchClient(self)
        self.nodes = NodeClient(self)
        
        # If username/password provided but no token, authenticate now
        if not api_key and not token and username and password:
            self._token = self.auth.login(username, password)
            self._auth_headers = {"Authorization": f"Bearer {self._token}"}
    
    @property
    def auth_headers(self) -> Dict[str, str]:
        """Get the authentication headers for API requests"""
        return self._auth_headers 