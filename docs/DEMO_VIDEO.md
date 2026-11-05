# IncidentRoom — Demo Video

## 🎬 Live Demo

> **Watch the full live incident simulation:** agents detecting, triaging, rolling back, and auto-generating a post-mortem in under 2 minutes.

📹 **[View Demo Video](https://github.com/swatiicfai/IncidentRoom/blob/main/docs/images/)**

---

## What You'll See

| Timestamp | Event |
|-----------|-------|
| 0:00 | SEV-1 alert fires in `#incident-war-room` |
| 0:20 | `@triage-agent` picks up the alert, starts 11 tool calls |
| 1:00 | Root cause identified: commit `8f2b31a` ("feat(payments): upgrade stripe sdk v3.4") |
| 1:20 | `@sre-agent` handoff — prepares rollback, runs `npm pack stripe@3.4.0` |
| 1:45 | Human types **APPROVE** via Wispr Flow voice dictation |
| 2:00 | Rollback executed, `@comms-agent` generates post-mortem |

---

## Screenshots

### 1. Alert Triage & Root Cause
![Alert Triage](images/01_alert_triage_root_cause.png)

### 2. SRE Agent Handoff
![SRE Handoff](images/02_sre_agent_handoff.png)

### 3. Multi-Agent Room Setup
![Room Setup](images/03_multiagent_room_setup.png)

### 4. Wispr Flow Voice Transcription
![Wispr Flow](images/04_wispr_flow_voice_transcription.png)

---

## 📊 Performance Metrics

- **MTTR:** Under 2 minutes (from alert to rollback approved)
- **Triage agent:** 11 tool calls, 3m 16s working time
- **Wispr Flow:** 405 words dictated, 100 wpm, hands-free
- **Human touch-points:** 1 (`APPROVE` command)

---

## Full Post-Mortem

See [POSTMORTEM_LIVE.md](../POSTMORTEM_LIVE.md) for the auto-generated incident report.
