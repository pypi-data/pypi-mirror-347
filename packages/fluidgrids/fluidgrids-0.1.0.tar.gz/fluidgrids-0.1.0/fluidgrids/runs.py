"""
Run client for FluidGrids API
"""
from typing import Any, Dict, List, Optional

from .base import BaseClient
from .models import RunDetail, RunStatus, RunSummary, TriggerRequest, TriggerResponse


class RunClient(BaseClient):
    """
    Client for workflow run-related operations.
    """
    
    def trigger(
        self,
        workflow_key: str,
        version: str,
        trigger_node_id: Optional[str] = None,
        trigger_data: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> TriggerResponse:
        """
        Trigger a workflow run.
        
        Args:
            workflow_key: The workflow key
            version: The workflow version
            trigger_node_id: The ID of the trigger node (optional)
            trigger_data: Additional trigger data (optional)
            context: Initial context data for the workflow (optional)
            
        Returns:
            Trigger response with run ID
        """
        payload = TriggerRequest(
            workflow_key=workflow_key,
            version=version,
            trigger_node_id=trigger_node_id,
            trigger_data=trigger_data,
            context=context,
        )
        response = self._post("/api/v1/trigger", json_data=payload.model_dump(exclude_unset=True))
        return TriggerResponse.model_validate(response)
    
    def list(self, workflow_key: Optional[str] = None, limit: int = 50) -> List[RunSummary]:
        """
        List workflow runs.
        
        Args:
            workflow_key: Filter by workflow key (optional)
            limit: Maximum number of runs to return
            
        Returns:
            List of run summaries
        """
        params = {"limit": limit}
        if workflow_key:
            params["workflow_key"] = workflow_key
        
        response = self._get("/api/v1/runs", params=params)
        return [RunSummary.model_validate(run) for run in response]
    
    def get(self, run_id: str) -> RunDetail:
        """
        Get details of a workflow run.
        
        Args:
            run_id: The run ID
            
        Returns:
            Run details
        """
        response = self._get(f"/api/v1/runs/{run_id}")
        return RunDetail.model_validate(response)
    
    def pause(self, run_id: str) -> RunSummary:
        """
        Pause a running workflow.
        
        Args:
            run_id: The run ID
            
        Returns:
            Updated run summary
        """
        response = self._post(f"/api/v1/runs/{run_id}/pause")
        return RunSummary.model_validate(response)
    
    def resume(self, run_id: str) -> RunSummary:
        """
        Resume a paused workflow.
        
        Args:
            run_id: The run ID
            
        Returns:
            Updated run summary
        """
        response = self._post(f"/api/v1/runs/{run_id}/resume")
        return RunSummary.model_validate(response)
    
    def cancel(self, run_id: str) -> RunSummary:
        """
        Cancel a workflow run.
        
        Args:
            run_id: The run ID
            
        Returns:
            Updated run summary
        """
        response = self._post(f"/api/v1/runs/{run_id}/cancel")
        return RunSummary.model_validate(response)
    
    def delete(self, run_id: str) -> None:
        """
        Delete a workflow run.
        
        Args:
            run_id: The run ID
        """
        self._delete(f"/api/v1/runs/{run_id}")
    
    def restore(self, run_id: str) -> RunSummary:
        """
        Restore a deleted workflow run.
        
        Args:
            run_id: The run ID
            
        Returns:
            Updated run summary
        """
        response = self._post(f"/api/v1/runs/{run_id}/restore")
        return RunSummary.model_validate(response)
    
    def wait_for_completion(
        self, run_id: str, timeout: int = 300, poll_interval: int = 2
    ) -> RunDetail:
        """
        Wait for a workflow run to complete.
        
        Args:
            run_id: The run ID
            timeout: Maximum time to wait in seconds (default: 300)
            poll_interval: Time between status checks in seconds (default: 2)
            
        Returns:
            Final run details
            
        Raises:
            TimeoutError: If the run doesn't complete within the timeout period
        """
        import time
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            run = self.get(run_id)
            if run.status in [
                RunStatus.COMPLETED,
                RunStatus.FAILED,
                RunStatus.CANCELED,
            ]:
                return run
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Workflow run {run_id} did not complete within the timeout period") 