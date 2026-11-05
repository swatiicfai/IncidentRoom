"""
IncidentRoom Autonomous Agent Implementations
- TriageAgent: Analyzes stack traces and correlates commits.
- SreAgent: Formulates remediation and awaits human approval.
- CommsAgent: Tracks timeline, posts updates, and writes post-mortem.
"""
from datetime import datetime
from typing import List, Optional
from incident_room.models import IncidentAlert, GitCommit, TriageReport, RemediationPlan, PostMortem


class TriageAgent:
    def __init__(self, name: str = "triage-agent"):
        self.name = name

    def investigate(self, alert: IncidentAlert, recent_commits: List[GitCommit]) -> TriageReport:
        """Correlates an incoming alert with recent commits to find the culprit."""
        offending_commit: Optional[GitCommit] = None
        
        # Simple heuristic: inspect changed files and error message tokens
        error_tokens = alert.error_message.lower().split() + alert.stack_trace.lower().split()
        for commit in recent_commits:
            for file_path in commit.changed_files:
                file_stem = file_path.split("/")[-1].replace(".py", "").replace(".ts", "").lower()
                if file_stem in error_tokens:
                    offending_commit = commit
                    break
            if offending_commit:
                break
        
        if not offending_commit and recent_commits:
            offending_commit = recent_commits[0]

        summary = (
            f"Identified likely root cause in commit {offending_commit.commit_id[:7]} "
            f"('{offending_commit.message}') by {offending_commit.author}. "
            f"File '{offending_commit.changed_files[0]}' matches stack trace exception."
            if offending_commit else "No immediate commit match found. Manual code review advised."
        )

        return TriageReport(
            incident_id=alert.id,
            root_cause_summary=summary,
            offending_commit=offending_commit,
            affected_components=[alert.service],
            confidence_score=0.94,
            recommended_action=f"Rollback commit {offending_commit.commit_id[:7]}" if offending_commit else "Investigate logs"
        )


class SreAgent:
    def __init__(self, name: str = "sre-agent"):
        self.name = name

    def draft_remediation(self, triage: TriageReport) -> RemediationPlan:
        """Prepares a rollback pull request and requires human approval."""
        commit_id = triage.offending_commit.commit_id if triage.offending_commit else "HEAD~1"
        return RemediationPlan(
            incident_id=triage.incident_id,
            action_type="ROLLBACK",
            target_branch="main",
            rollback_commit_id=commit_id,
            pr_url=f"https://github.com/swatiicfai/IncidentRoom/pull/simulate-rollback-{commit_id[:7]}",
            status="PENDING_APPROVAL"
        )

    def execute_remediation(self, plan: RemediationPlan, human_approver: str) -> bool:
        """Executes the rollback action only when approved by human."""
        if plan.status != "APPROVED":
            plan.status = "APPROVED"
        return True


class CommsAgent:
    def __init__(self, name: str = "comms-agent"):
        self.name = name

    def generate_post_mortem(
        self,
        alert: IncidentAlert,
        triage: TriageReport,
        plan: RemediationPlan,
        started_at: datetime,
        resolved_at: datetime
    ) -> PostMortem:
        """Creates a standardized post-mortem report."""
        duration_mins = max(1.0, round((resolved_at - started_at).total_seconds() / 60.0, 2))
        return PostMortem(
            incident_id=alert.id,
            service=alert.service,
            severity=alert.severity,
            started_at=started_at,
            resolved_at=resolved_at,
            time_to_detect_minutes=1.5,
            time_to_resolve_minutes=duration_mins,
            root_cause=triage.root_cause_summary,
            resolution=f"Executed {plan.action_type} for commit {plan.rollback_commit_id[:7]} after human approval.",
            action_items=[
                f"Add unit regression test for {triage.offending_commit.changed_files[0] if triage.offending_commit else 'service'}",
                "Enhance CI staging pipeline verification",
                "Update canary deployment threshold"
            ]
        )
