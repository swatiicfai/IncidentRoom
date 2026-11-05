"""
IncidentRoom Orchestrator - Simulates the Switch Protocol Event Stream
"""
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from incident_room.models import IncidentAlert, GitCommit
from incident_room.agents import TriageAgent, SreAgent, CommsAgent

console = Console()


def run_incident_simulation():
    console.print(Panel.fit("[bold red]🚨 INCIDENTROOM: SWITCH MULTI-AGENT WAR ROOM ACTIVATED[/bold red]"))
    
    # 1. Incoming Alert
    alert = IncidentAlert(
        id="INC-8892",
        service="checkout-service",
        severity="SEV-1",
        error_message="NullPointerException: stripe_client.checkout.sessions.create() missing idempotency_key",
        stack_trace="File 'services/payments/stripe_gateway.py', line 84, in create_session\nTypeError: null payload field",
        timestamp=datetime.utcnow()
    )

    rprint(f"[bold red][ALERT INCOMING][/bold red] ⚡ [white]Service:[/white] {alert.service} | [white]Severity:[/white] [bold yellow]{alert.severity}[/bold yellow]")
    rprint(f"[dim]Error: {alert.error_message}[/dim]\n")
    time.sleep(1.0)

    # 2. Mock Git History
    commits = [
        GitCommit(
            commit_id="9e4b1a208f71c4d92",
            author="alex_dev@corp.com",
            message="feat: upgrade to stripe sdk v3.4 and refactor session handler",
            timestamp=datetime.utcnow(),
            changed_files=["services/payments/stripe_gateway.py", "requirements.txt"],
            diff_summary="- idempotency_key = get_token()\n+ idempotency_key = None"
        ),
        GitCommit(
            commit_id="4b2d9e11029c3f81e",
            author="sarah_ui@corp.com",
            message="style: update cart checkout button padding",
            timestamp=datetime.utcnow(),
            changed_files=["frontend/components/CartButton.tsx"],
            diff_summary="+ padding: 12px;"
        )
    ]

    # 3. Triage Agent Investigates
    triage_agent = TriageAgent()
    rprint(f"[cyan]🤖 @{triage_agent.name}[/cyan]: Inspecting stack trace against recent PRs & git commits...")
    time.sleep(1.5)
    
    triage_report = triage_agent.investigate(alert, commits)
    rprint(Panel(
        f"[bold]Root Cause Analysis:[/bold] {triage_report.root_cause_summary}\n"
        f"[bold]Confidence:[/bold] {int(triage_report.confidence_score * 100)}%\n"
        f"[bold]Recommended Action:[/bold] {triage_report.recommended_action}",
        title=f"@{triage_agent.name} Findings",
        border_style="cyan"
    ))
    time.sleep(1.0)

    # 4. SRE Agent Prepares Remediation
    sre_agent = SreAgent()
    rprint(f"[yellow]🛠️ @{sre_agent.name}[/yellow]: Preparing automated remediation plan...")
    time.sleep(1.2)
    plan = sre_agent.draft_remediation(triage_report)
    
    rprint(Panel(
        f"[bold green]Rollback Branch Drafted:[/bold green] rollback-stripe-sdk-{plan.rollback_commit_id[:7]}\n"
        f"[bold]PR Draft:[/bold] {plan.pr_url}\n"
        f"[bold red]STATUS: AWAITING HUMAN SIGN-OFF[/bold red]\n"
        f"⚠️  Please reply '[bold white]APPROVE[/bold white]' to execute deployment.",
        title=f"@{sre_agent.name} Proposal",
        border_style="yellow"
    ))
    
    # 5. Human-in-the-Loop Sign-off
    rprint("\n[bold magenta]🧑‍💻 On-Call Lead (Voice via Wispr Flow):[/bold magenta] [italic]'APPROVE rollback to production'[/italic]")
    time.sleep(1.0)

    # 6. SRE Agent Executes
    plan.status = "APPROVED"
    sre_agent.execute_remediation(plan, "oncall-lead")
    rprint(f"[yellow]🛠️ @{sre_agent.name}[/yellow]: [bold green]Deployment successful![/bold green] Health checks 200 OK. Error rate returned to 0.01%.")
    time.sleep(1.0)

    # 7. Comms Agent Publishes Post-Mortem
    comms_agent = CommsAgent()
    post_mortem = comms_agent.generate_post_mortem(
        alert=alert,
        triage=triage_report,
        plan=plan,
        started_at=alert.timestamp,
        resolved_at=datetime.utcnow()
    )

    table = Table(title="Incident Post-Mortem Report", show_header=True, header_style="bold magenta")
    table.add_column("Field", style="dim", width=25)
    table.add_column("Details")
    table.add_row("Incident ID", post_mortem.incident_id)
    table.add_row("Service", post_mortem.service)
    table.add_row("Severity", post_mortem.severity)
    table.add_row("MTTD (Time to Detect)", f"{post_mortem.time_to_detect_minutes} min")
    table.add_row("MTTR (Time to Resolve)", f"{post_mortem.time_to_resolve_minutes} min")
    table.add_row("Root Cause", post_mortem.root_cause)
    table.add_row("Resolution", post_mortem.resolution)
    table.add_row("Preventive Action Items", "\n".join(f"• {item}" for item in post_mortem.action_items))

    console.print(table)
    rprint(f"[bold green]✅ Incident {alert.id} closed. Channel archived. Good job team![/bold green]")


if __name__ == "__main__":
    run_incident_simulation()
