"""
Usage client for FluidGrids API
"""
from datetime import datetime
from typing import Dict, List, Optional, Any

from .base import BaseClient


class UsageClient(BaseClient):
    """
    Client for usage monitoring and metrics.
    Allows retrieving comprehensive metrics about workflow engine usage.
    """
    
    def get_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        context: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive usage metrics for billing and monitoring.
        
        Args:
            start_date: Optional start date for the metrics period (defaults to 30 days ago)
            end_date: Optional end date for the metrics period (defaults to current time)
            context: Optional context filters as key-value pairs (e.g., {"organization_id": "org123"})
            
        Returns:
            Dictionary containing usage metrics across different dimensions
            
        Example:
            >>> metrics = client.usage.get_metrics(
            ...     start_date=datetime(2023, 1, 1),
            ...     end_date=datetime(2023, 1, 31),
            ...     context={"organization_id": "org123"}
            ... )
            >>> print(f"Total runs: {metrics['workflow_execution_metrics']['total_runs']}")
            >>> print(f"Success rate: {metrics['workflow_execution_metrics']['successful_runs'] / metrics['workflow_execution_metrics']['total_runs'] * 100}%")
        """
        params = {}
        
        # Add date parameters if provided
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
            
        # Add context filters
        if context:
            params["context"] = [f"{key}:{value}" for key, value in context.items()]
            
        return self._get("/api/v1/usage/metrics", params=params)
    
    def get_time_series(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        interval: str = "day",
        workflow_key: Optional[str] = None,
        context: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Get time series data for usage metrics.
        
        Args:
            start_date: Optional start date for the time series (defaults to 30 days ago)
            end_date: Optional end date for the time series (defaults to current time)
            interval: Time interval for grouping data - one of "hour", "day", "week", "month" (default: "day")
            workflow_key: Optional specific workflow key to filter on
            context: Optional context filters as key-value pairs
            
        Returns:
            Dictionary containing time series data for different metrics
            
        Example:
            >>> time_series = client.usage.get_time_series(
            ...     interval="day",
            ...     workflow_key="data-processor"
            ... )
            >>> for point in time_series["runs"]["data"]:
            ...     print(f"Date: {point['timestamp']}, Runs: {point['value']}")
        """
        params = {"interval": interval}
        
        # Add date parameters if provided
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
            
        # Add workflow key if provided
        if workflow_key:
            params["workflow_key"] = workflow_key
            
        # Add context filters
        if context:
            params["context"] = [f"{key}:{value}" for key, value in context.items()]
            
        return self._get("/api/v1/usage/time-series", params=params) 