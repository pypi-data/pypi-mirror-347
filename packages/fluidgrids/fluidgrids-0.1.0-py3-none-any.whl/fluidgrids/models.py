"""
FluidGrids SDK data models
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class RunStatus(str, Enum):
    """Workflow run status"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    DELETED = "DELETED"


class TriggerRequest(BaseModel):
    """Request model for triggering a workflow run"""
    workflow_key: str
    version: str
    trigger_node_id: Optional[str] = None
    trigger_data: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None


class TriggerResponse(BaseModel):
    """Response model for a triggered workflow run"""
    run_id: str
    status: RunStatus


class RunSummary(BaseModel):
    """Summary information about a workflow run"""
    run_id: str
    workflow_key: str
    workflow_version: str
    status: RunStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    trigger_node_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    error: Optional[str] = None


class RunDetail(RunSummary):
    """Detailed information about a workflow run"""
    trigger_info: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    node_states: Optional[Dict[str, Any]] = None
    outputs: Optional[Dict[str, Any]] = None


class WorkflowSummary(BaseModel):
    """Summary information about a workflow"""
    workflow_key: str
    version: str
    title: Optional[str] = None
    description: Optional[str] = None
    is_latest: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    is_deleted: bool = False


class WorkflowDetail(WorkflowSummary):
    """Detailed information about a workflow"""
    definition: Dict[str, Any]


class WorkflowDefinition(BaseModel):
    """Workflow definition for creating or updating a workflow"""
    title: Optional[str] = None
    description: Optional[str] = None
    definition: Dict[str, Any]


class CredentialSummary(BaseModel):
    """Summary information about a credential"""
    credential_id: str
    name: str
    type: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class CredentialDetail(CredentialSummary):
    """Detailed information about a credential"""
    config: Dict[str, Any]


class CredentialCreate(BaseModel):
    """Data model for creating a credential"""
    name: str
    type: str
    config: Dict[str, Any]


class CredentialUpdate(BaseModel):
    """Data model for updating a credential"""
    name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None 