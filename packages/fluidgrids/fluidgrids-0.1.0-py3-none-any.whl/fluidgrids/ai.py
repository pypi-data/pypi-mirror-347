"""
AI client for FluidGrids API
"""
from typing import Dict, List, Optional, Any

from .base import BaseClient


class AIClient(BaseClient):
    """
    Client for AI-related operations.
    Allows interaction with the FluidGrids AI assistant for workflow management.
    """
    
    def manage_workflow(
        self, 
        prompt: str, 
        target_workflow_key: Optional[str] = None,
        target_workflow_version: Optional[str] = None,
        model: Optional[str] = None,
        caller_role: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Use AI to manage workflows based on natural language prompts.
        
        Args:
            prompt: A natural language description of what you want to do with workflows
            target_workflow_key: Optional key of the workflow to target
            target_workflow_version: Optional version of the workflow to target
            model: Optional AI model to use (defaults to service setting)
            caller_role: Optional role to use for calling the AI (defaults to 'user')
            
        Returns:
            Dictionary containing the AI response with plan and execution results
            
        Example:
            >>> response = client.ai.manage_workflow(
            ...     prompt="Create a workflow that fetches data from an API and logs the result",
            ...     target_workflow_key="data-fetcher"
            ... )
            >>> print(f"Plan executed: {response['executed_plan']}")
            >>> print(f"Explanation: {response['explanation']}")
        """
        payload = {
            "prompt": prompt,
        }
        
        # Add optional parameters if provided
        if target_workflow_key:
            payload["target_workflow_key"] = target_workflow_key
        if target_workflow_version:
            payload["target_workflow_version"] = target_workflow_version
        if model:
            payload["model"] = model
        if caller_role:
            payload["caller_role"] = caller_role
            
        return self._post("/api/v1/ai/", json_data=payload) 