"""
Workflow client for FluidGrids API
"""
from typing import Any, Dict, List, Optional, Union

from .base import BaseClient
from .models import WorkflowDefinition, WorkflowDetail, WorkflowSummary


class WorkflowClient(BaseClient):
    """
    Client for workflow-related operations.
    """
    
    def list(self, limit: int = 100, offset: int = 0) -> List[WorkflowSummary]:
        """
        List all workflows.
        
        Args:
            limit: Maximum number of workflows to return
            offset: Index offset for pagination
            
        Returns:
            List of workflow summaries
        """
        params = {"limit": limit, "offset": offset}
        response = self._get("/api/v1/workflows/", params=params)
        return [WorkflowSummary.model_validate(wf) for wf in response]
    
    def get(self, workflow_key: str, version: str = "latest") -> WorkflowDetail:
        """
        Get a specific workflow by key and version.
        
        Args:
            workflow_key: The workflow key
            version: The workflow version (default: "latest")
            
        Returns:
            Workflow detail
        """
        if version == "latest":
            response = self._get(f"/api/v1/workflows/{workflow_key}/latest")
        else:
            response = self._get(f"/api/v1/workflows/{workflow_key}/{version}")
        
        return WorkflowDetail.model_validate(response)
    
    def create_or_update(
        self, workflow_key: str, version: str, workflow: WorkflowDefinition
    ) -> WorkflowDetail:
        """
        Create or update a workflow.
        
        Args:
            workflow_key: The workflow key
            version: The workflow version
            workflow: The workflow definition
            
        Returns:
            Created or updated workflow detail
        """
        response = self._put(
            f"/api/v1/workflows/{workflow_key}/{version}",
            json_data=workflow.model_dump(exclude_unset=True),
        )
        return WorkflowDetail.model_validate(response)
    
    def delete(self, workflow_key: str, version: str) -> None:
        """
        Delete a workflow.
        
        Args:
            workflow_key: The workflow key
            version: The workflow version
        """
        self._delete(f"/api/v1/workflows/{workflow_key}/{version}")
    
    def restore(self, workflow_key: str, version: str) -> WorkflowDetail:
        """
        Restore a deleted workflow.
        
        Args:
            workflow_key: The workflow key
            version: The workflow version
            
        Returns:
            Restored workflow detail
        """
        response = self._post(f"/api/v1/workflows/{workflow_key}/{version}/restore")
        return WorkflowDetail.model_validate(response)
    
    def duplicate(
        self, workflow_key: str, new_key: str, new_version: str = "1.0"
    ) -> WorkflowDetail:
        """
        Duplicate a workflow.
        
        Args:
            workflow_key: The source workflow key
            new_key: The new workflow key
            new_version: The new workflow version (default: "1.0")
            
        Returns:
            Duplicated workflow detail
        """
        json_data = {
            "new_key": new_key,
            "new_version": new_version,
        }
        response = self._post(f"/api/v1/workflows/{workflow_key}/duplicate", json_data=json_data)
        return WorkflowDetail.model_validate(response)
    
    def list_versions(
        self, workflow_key: str, limit: int = 100, offset: int = 0, include_deleted: bool = False
    ) -> List[WorkflowSummary]:
        """
        List all versions of a workflow.
        
        Args:
            workflow_key: The workflow key
            limit: Maximum number of versions to return
            offset: Index offset for pagination
            include_deleted: Whether to include deleted versions
            
        Returns:
            List of workflow version summaries
        """
        params = {
            "limit": limit,
            "offset": offset,
            "include_deleted": include_deleted,
        }
        response = self._get(f"/api/v1/workflows/{workflow_key}/versions", params=params)
        return [WorkflowSummary.model_validate(wf) for wf in response]
    
    def set_latest(self, workflow_key: str, version: str) -> WorkflowDetail:
        """
        Set a workflow version as the latest.
        
        Args:
            workflow_key: The workflow key
            version: The workflow version to set as latest
            
        Returns:
            Updated workflow detail
        """
        response = self._post(f"/api/v1/workflows/{workflow_key}/{version}/set_latest")
        return WorkflowDetail.model_validate(response)
    
    def get_context_schema(self, workflow_key: str, version: str) -> Dict[str, Any]:
        """
        Get the context schema for a workflow.
        
        Args:
            workflow_key: The workflow key
            version: The workflow version
            
        Returns:
            Context schema as a dictionary
        """
        return self._get(f"/api/v1/workflows/{workflow_key}/{version}/context/schema")
    
    def validate_context(
        self, workflow_key: str, version: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate context data against a workflow's context schema.
        
        Args:
            workflow_key: The workflow key
            version: The workflow version
            context: The context data to validate
            
        Returns:
            Validation result
        """
        return self._post(
            f"/api/v1/workflows/{workflow_key}/{version}/context/validate",
            json_data=context,
        ) 