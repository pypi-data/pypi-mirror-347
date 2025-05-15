"""
Configuration client for FluidGrids API
"""
from typing import Any, Dict, List, Optional

from .base import BaseClient


class ConfigClient(BaseClient):
    """
    Client for configuration-related operations.
    """
    
    def get_node_types(self) -> List[Dict[str, Any]]:
        """
        Get available node types for workflow builders.
        
        Returns:
            List of node type configurations
        """
        return self._get("/api/v1/config/node_types")
    
    def get_node_manifest(self, node_type: str) -> Dict[str, Any]:
        """
        Get manifest for a specific node type.
        
        Args:
            node_type: The node type identifier
            
        Returns:
            Node manifest as a dictionary
        """
        return self._get(f"/api/v1/nodes/{node_type}/manifest")
    
    def get_node_configurations(self, node_type: str) -> List[Dict[str, Any]]:
        """
        Get available configurations for a node type.
        
        Args:
            node_type: The node type identifier
            
        Returns:
            List of node configurations
        """
        return self._get(f"/api/v1/nodes/{node_type}/configs")
    
    def get_scheduled_jobs(self) -> List[Dict[str, Any]]:
        """
        Get all scheduled jobs.
        
        Returns:
            List of scheduled jobs
        """
        return self._get("/api/v1/config/scheduled_jobs")
    
    def get_scheduled_job(self, job_id: str) -> Dict[str, Any]:
        """
        Get a specific scheduled job.
        
        Args:
            job_id: The job ID
            
        Returns:
            Scheduled job configuration
        """
        return self._get(f"/api/v1/config/scheduled_jobs/{job_id}")
    
    def update_scheduled_job(self, job_id: str, is_active: bool) -> Dict[str, Any]:
        """
        Update a scheduled job.
        
        Args:
            job_id: The job ID
            is_active: Whether the job should be active
            
        Returns:
            Updated scheduled job configuration
        """
        payload = {
            "is_active": is_active
        }
        return self._put(f"/api/v1/config/scheduled_jobs/{job_id}", json_data=payload)
    
    def get_event_triggers(self) -> List[Dict[str, Any]]:
        """
        Get all event triggers.
        
        Returns:
            List of event triggers
        """
        return self._get("/api/v1/config/event_triggers")
    
    def get_event_trigger(self, registration_id: str) -> Dict[str, Any]:
        """
        Get a specific event trigger.
        
        Args:
            registration_id: The registration ID
            
        Returns:
            Event trigger configuration
        """
        return self._get(f"/api/v1/config/event_triggers/{registration_id}")
    
    def update_event_trigger(self, registration_id: str, is_active: bool) -> Dict[str, Any]:
        """
        Update an event trigger.
        
        Args:
            registration_id: The registration ID
            is_active: Whether the trigger should be active
            
        Returns:
            Updated event trigger configuration
        """
        payload = {
            "is_active": is_active
        }
        return self._put(f"/api/v1/config/event_triggers/{registration_id}", json_data=payload) 