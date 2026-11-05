"""
IncidentRoom Core Models and Data Structures
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class IncidentAlert(BaseModel):
    id: str = Field(..., description="Unique alert identifier")
    service: str = Field(..., description="Affected service or microservice")
    severity: str = Field(..., description="SEV-1, SEV-2, etc.")
    error_message: str = Field(..., description="High-level error description")
    stack_trace: str = Field(..., description="Raw stack trace or exception output")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GitCommit(BaseModel):
    commit_id: str
    author: str
    message: str
    timestamp: datetime
    changed_files: List[str]
    diff_summary: str


class TriageReport(BaseModel):
    incident_id: str
    root_cause_summary: str
    offending_commit: Optional[GitCommit] = None
    affected_components: List[str] = Field(default_factory=list)
    confidence_score: float = 0.95
    recommended_action: str


class RemediationPlan(BaseModel):
    incident_id: str
    action_type: str  # "ROLLBACK", "HOTFIX", "FEATURE_FLAG_DISABLE"
    target_branch: str
    rollback_commit_id: Optional[str] = None
    pr_url: Optional[str] = None
    status: str = "PENDING_APPROVAL"  # "PENDING_APPROVAL", "APPROVED", "EXECUTED", "REJECTED"


class PostMortem(BaseModel):
    incident_id: str
    service: str
    severity: str
    started_at: datetime
    resolved_at: datetime
    time_to_detect_minutes: float
    time_to_resolve_minutes: float
    root_cause: str
    resolution: str
    action_items: List[str]
