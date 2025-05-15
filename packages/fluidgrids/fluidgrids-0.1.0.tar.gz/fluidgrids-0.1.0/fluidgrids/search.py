"""
Search client for FluidGrids API
"""
from typing import Dict, List, Optional, Any, Union

from .base import BaseClient


class SearchClient(BaseClient):
    """
    Client for search-related operations.
    Provides unified search across different entity types in the workflow engine.
    """
    
    def search(
        self,
        query: str,
        entity_types: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "relevance",
        highlight: bool = False
    ) -> Dict[str, Any]:
        """
        Search across multiple entity types with a unified query.
        
        Args:
            query: Search query string
            entity_types: Optional list of entity types to search (e.g., ["workflow", "run"])
            filters: Optional filters to apply to search results
            limit: Maximum number of results per entity type (default: 10)
            offset: Offset for pagination (default: 0)
            sort: Sort order - one of "relevance", "date_asc", "date_desc" (default: "relevance")
            highlight: Whether to highlight matching text in results (default: False)
            
        Returns:
            Dictionary containing search results grouped by entity type
            
        Example:
            >>> results = client.search.search(
            ...     query="data processing",
            ...     entity_types=["workflow", "run"],
            ...     limit=5
            ... )
            >>> print(f"Total results: {results['total_results']}")
            >>> for entity_type, items in results['results'].items():
            ...     print(f"{entity_type}: {len(items)} results")
            ...     for item in items:
            ...         print(f"  - {item['title']}")
        """
        payload = {
            "query": query,
            "limit": limit,
            "offset": offset,
            "sort": sort,
            "highlight": highlight
        }
        
        if entity_types:
            payload["entity_types"] = entity_types
            
        if filters:
            payload["filters"] = filters
            
        return self._post("/api/v1/search/", json_data=payload)
    
    def search_entity(
        self,
        entity_type: str,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search within a specific entity type.
        
        Args:
            entity_type: Entity type to search (e.g., "workflow", "run")
            query: Search query string
            limit: Maximum number of results (default: 10)
            offset: Offset for pagination (default: 0)
            
        Returns:
            Dictionary containing search results for the specified entity type
            
        Example:
            >>> workflow_results = client.search.search_entity(
            ...     entity_type="workflow",
            ...     query="data processing",
            ...     limit=5
            ... )
            >>> for item in workflow_results['results']['workflow']:
            ...     print(f"{item['title']} - {item['description']}")
        """
        params = {
            "query": query,
            "limit": limit,
            "offset": offset
        }
            
        return self._get(f"/api/v1/search/{entity_type}", params=params)
    
    def get_searchable_entities(self) -> Dict[str, Any]:
        """
        Get information about entities that can be searched and their searchable fields.
        
        Returns:
            Dictionary containing metadata about searchable entities
            
        Example:
            >>> entities = client.search.get_searchable_entities()
            >>> for entity_name, entity_info in entities['entities'].items():
            ...     print(f"{entity_name} fields: {', '.join(entity_info['fields'])}")
        """
        return self._get("/api/v1/search/entities") 