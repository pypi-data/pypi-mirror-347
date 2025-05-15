"""
Node client for FluidGrids API
"""
from typing import Dict, List, Optional, Any

from .base import BaseClient


class NodeClient(BaseClient):
    """
    Client for node-related operations.
    Provides access to node types, manifests, and operations.
    """
    
    def list(self) -> List[Dict[str, Any]]:
        """
        List all registered node types and their endpoint configurations.
        
        Returns:
            List of node endpoint configurations
            
        Example:
            >>> nodes = client.nodes.list()
            >>> for node in nodes:
            ...     print(f"{node['node_type']} v{node['node_version']} - {', '.join(node['kind'])}")
        """
        return self._get("/api/v1/nodes")
    
    def get_manifest(self, node_type: str, node_version: str) -> Dict[str, Any]:
        """
        Get manifest for a specific node type and version.
        
        Args:
            node_type: The node type identifier
            node_version: The node version
            
        Returns:
            Node manifest containing inputs, outputs, and configuration schema
            
        Example:
            >>> manifest = client.nodes.get_manifest("action:http", "1.0")
            >>> print(f"Node description: {manifest['description']}")
            >>> print(f"Input parameters: {manifest['inputs']}")
        """
        return self._get(f"/api/v1/nodes/{node_type}/{node_version}/manifest")
    
    def get_introspection(self, node_type: str, node_version: str) -> Dict[str, Any]:
        """
        Get GraphQL introspection schema for a specific node type and version.
        
        Args:
            node_type: The node type identifier
            node_version: The node version
            
        Returns:
            GraphQL introspection schema
            
        Example:
            >>> schema = client.nodes.get_introspection("action:http", "1.0")
            >>> operations = [op for op in schema["data"]["__schema"]["types"] if op["kind"] == "OBJECT"]
            >>> print(f"Available operations: {[op['name'] for op in operations]}")
        """
        return self._get(f"/api/v1/utils/nodes/{node_type}/{node_version}/introspection") 