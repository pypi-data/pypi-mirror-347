"""
Dashboard client for FluidGrids API
"""
from typing import Dict, Any

from .base import BaseClient


class DashboardClient(BaseClient):
    """
    Client for dashboard-related operations.
    Provides access to workflow engine dashboard metrics and summaries.
    """
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a consolidated summary of workflow engine activities and entities.
        
        Returns:
            Dictionary containing dashboard metrics and summaries
            
        Example:
            >>> summary = client.dashboard.get_summary()
            >>> print(f"Total workflows: {summary['workflows']['total']}")
            >>> print(f"Active runs: {summary['runs']['active']}")
            >>> print(f"Recent runs: {len(summary['runs']['recent'])}")
            >>> for wf in summary['top_workflows']:
            ...     print(f"{wf['workflow_key']} - {wf['run_count']} runs")
        """
        return self._get("/api/v1/dashboard/summary") 