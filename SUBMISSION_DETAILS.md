# 🏆 Flip the Switch Hackathon Submission Details: IncidentRoom

## 1. Project Overview
- **Project Name:** IncidentRoom
- **Tagline:** Autonomous SRE War Room with Multi-Agent Swarm for Team Chat Powered by Switch AI
- **GitHub Repository:** https://github.com/swatiicfai/IncidentRoom
- **Video Demo File (With AI Female Voiceover):** `C:\Users\Swati\Videos\IncidentRoom_Final_Demo_With_Voice.mp4`
- **Wispr Flow Proof Scorecard:** https://github.com/swatiicfai/IncidentRoom/blob/main/wispr-scorecard.png

---

## 2. Prize Tracks to Select
- [x] **Track 01: Best Business Workflow ($2,000 cash)**
- [x] **Side Track: Code with Wispr ($500 cash)**
- [x] **Side Track: Best Blog (AirPods 5)**

---

## 3. Submission Pitch / Description (Copy & Paste)

### Inspiration
When production outages strike at 2 AM, on-call engineers face chaos: context is fragmented across monitoring dashboards, error traces, and git history. Valuable minutes are wasted manually identifying culprit PRs and drafting stakeholder updates while the system stays down. We built **IncidentRoom** to turn any team channel into an autonomous SRE war room using **Switch AI**.

### What It Does
IncidentRoom orchestrates an autonomous multi-agent swarm in team chat:
1. **`@triage-agent` (Incident Detective):** Ingests incoming alerts and error stack traces, correlates them against git commits merged in the last 24 hours, and isolates the root-cause commit with confidence metrics.
2. **`@sre-agent` (Remediation Specialist):** Prepares automated rollback pull requests and evaluates blast radius. It enforces strict human-in-the-loop governance: no deployment happens without explicit human approval.
3. **`@comms-agent` (Incident Commander & Scribe):** Publishes non-technical stakeholder updates, tracks incident timelines, and auto-generates structured post-mortems with MTTR and action items.

### How Switch AI Makes It Possible
Switch AI provides the multi-agent room infrastructure that allows humans and multiple specialized agents to collaborate in shared threads. Each agent maintains distinct capabilities, listens for relevant mentions, executes local bash/git operations, and hands off context to peer agents seamlessly.

### Voice-Powered With Wispr Flow
IncidentRoom integrates voice-driven incident coordination with **Wispr Flow**. Responders can dictate triage commands and voice approvals hands-free (*"APPROVE rollback to production and notify stakeholders"*), streamlining incident response without keyboard friction.

### What We Learned & What's Next
Orchestrating multi-agent state machines in chat with human-in-the-loop safeguards dramatically cuts Mean Time to Resolution (MTTR). Next, we plan to connect live Datadog/Sentry webhooks and automated Canary rollback verification.
