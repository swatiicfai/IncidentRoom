# Incident Post-Mortem — SEV-1: HTTP 500 spike in checkout-payment-gateway

| Field | Value |
|---|---|
| Incident ID | SEV-1-checkout-payment-gateway-2026-11-05 |
| Severity | SEV-1 |
| Status | **Resolution pending verification** |
| Date (UTC) | 2026-11-05 |
| Service | checkout-payment-gateway |
| Detected by | Alerting (HTTP 500 error spike) |
| Author | comms-agent |
| Last updated | 2026-11-05 19:57 UTC (re-check requested by owner) |

---

## 1. Executive summary (plain language)

Customers attempting to pay at checkout received an error instead of a payment page. The cause was a software upgrade to our payment provider's toolkit (Stripe SDK v3.4) that changed how one part of our code must be called. Our code was still using the older calling style, so checkout crashed on every attempt before any money was handled.

No payments were charged incorrectly. The failure was a hard error, not a wrong charge. The fix is either to undo the upgrade (rollback) or to update our code to the new calling style.

**The rollback was approved by the workspace owner. Recovery has not yet been confirmed — see Open Items.**

---

## 2. Customer / stakeholder impact

- **What users saw:** Checkout failed with an error; no payment session could be created.
- **Who was affected:** All customers attempting to check out while the fault was live (failure was not customer-specific or data-dependent).
- **Financial exposure:** No incorrect charges identified. Risk of **duplicate payments** exists only if retries were made without idempotency protection — see Open Items.
- **Duration:** Unknown — no observability access was available to confirm start and end times.
- **Support impact:** Unknown volume of failed checkout attempts.

---

## 3. Timeline (UTC)

| Time (UTC) | Time (IST) | Event |
|---|---|---|
| 19:31:31 | 01:01:31 | SEV-1 alert raised: HTTP 500 spike in checkout-payment-gateway. Stack trace: `TypeError: Cannot read property 'idempotency_key' of null` at `services/payments/stripe_gateway.js:84`. Suspect commit `8f2b31a` ("feat(payments): upgrade stripe sdk v3.4", alex.engineer@corp.com). |
| 19:34:43 | 01:04:43 | triage-agent completes triage: null options object passed to Stripe create call; SDK v3.4 reads `options.idempotency_key`. Handoff to sre-agent. |
| 19:34:51 | 01:04:51 | sre-agent picks up handoff. |
| 19:35:09 | 01:05:09 | triage-agent restates root cause and recommends rollback of `8f2b31a`. |
| 19:35:45 | 01:05:45 | sre-agent publishes remediation plan: Plan A (revert `8f2b31a`) recommended, Plan B (fix forward at line 84). Requests `APPROVE A` / `APPROVE B`. |
| 19:37:14 | 01:07:14 | triage-agent verifies SDK source (stripe@3.4.0): confirms snake_case `idempotency_key`; narrows likely defect location to our own wrapper at line 84, not node_modules. |
| 19:37:59 | 01:07:59 | Workspace owner replies "APPROVE" (option letter not specified). |
| 19:45:13 | 01:15:13 | Alert re-raised in room; root-cause investigation requested again. |
| 19:46:50 | 01:16:50 | Workspace owner: "Approve, roll back, and notify all stakeholders." |
| 19:47:22 | 01:17:22 | Post-mortem requested. |
| 19:49:33 | 01:19:33 | comms-agent engaged to produce this report. |
| — | — | **Rollback execution and recovery verification: NOT CONFIRMED at time of writing.** |

---

## 4. Root cause

**Immediate cause:** `services/payments/stripe_gateway.js:84` dereferences `options.idempotency_key` where `options` is `null`. The Stripe create call fails before any network request is made, so every `createSession` invocation returns HTTP 500.

**Trigger:** Commit `8f2b31a` — "feat(payments): upgrade stripe sdk v3.4" — upgraded stripe-node to v3.4 without auditing call sites that pass a null/absent options argument.

**Mechanism (verified by triage-agent against stripe@3.4.0 source):** v3.4's `isOptionsHash()` guard means a literal `null` does not throw inside the SDK itself. Therefore the null dereference most likely happens in **our own wrapper at line 84**, which reads `.idempotency_key` before the SDK guard applies. This makes the fix a call-site/wrapper guard (`options || {}`), not a dependency change.

**Important naming detail:** This SDK reads `idempotency_key` (snake_case). An earlier draft fix using camelCase `idempotencyKey` would have been silently ignored, quietly disabling idempotency and allowing duplicate sessions on retries. The corrected patch uses snake_case.

**Confidence:** High on the failing path. **Not yet confirmed:** the exact diff of `8f2b31a` (no repo checkout, `gh` unauthenticated in the agent environment). Whether the commit *introduced* the null or merely exposed a pre-existing runtime null is still open.

---

## 5. Remediation

### Plan A — Rollback (recommended, approved)
- `git revert --no-edit 8f2b31a` on the release branch, then deploy via pipeline.
- Restores pre-v3.4 Stripe SDK. Failure is deterministic at line 84, so recovery is expected to be immediate and clean.

### Plan B — Fix forward (approved as alternative)
At `services/payments/stripe_gateway.js:84`:

```js
const opts = { ...(options || {}) };
if (idempotencyKey) opts.idempotency_key = idempotencyKey;
return stripe.checkout.sessions.create(payload, opts);
```

Plus a regression test calling `createSession` with no options argument.

### Deploy status
**Approved by workspace owner at 19:46:50 UTC. No confirmation of execution or verification has been posted.**

**Re-check at 19:57:49 UTC (owner requested a fresh check):** no new evidence has arrived in the incident room. sre-agent has not posted a plan choice, execution confirmation, error-rate numbers, or an audit result. The rollback therefore remains **approved but unexecuted/unconfirmed** as far as this report can verify.

---

## 6. Recovery verification criteria (defined, not yet met)

1. HTTP 500 rate for checkout-payment-gateway back to baseline.
2. At least one successful `createSession` observed.
3. No growth in duplicate-session count.
4. Outbound `Idempotency-Key` header present on a retried request (or confirmed in Stripe dashboard logs) — the only real proof idempotency survived the fix.

---

## 7. Open items / action items

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | Execute approved rollback (Plan A) or deploy Plan B | sre-agent / workspace owner | **Awaiting execution confirmation** |
| 2 | Provide observability access or dashboard before/after 500-rate numbers | workspace owner | Open |
| 3 | Provide repo checkout or `git show 8f2b31a -- services/payments/stripe_gateway.js` output to settle call-site vs wrapper and confirm blame | workspace owner / triage-agent | Open |
| 4 | Verify `Idempotency-Key` header on retries; check for duplicate sessions | sre-agent | Open |
| 5 | Audit all Stripe call sites touched by v3.4 (refunds, customers, subscriptions) for the same null-options pattern | sre-agent / triage-agent | Queued, blocked on repo access |
| 6 | Add regression test: `createSession` with no options argument | engineering | Open |
| 7 | Confirm no customer was charged twice during the outage window | payments team | Open |

---

## 8. Lessons learned

- **Dependency upgrades need call-site audits.** A patch-level SDK bump silently changed argument handling on the checkout hot path.
- **Hot-path changes need a smoke test.** A single test calling `createSession` with no options would have caught this before deploy.
- **Agents were blind without observability and repo access.** Root cause was inferred from the stack trace alone; blast radius and exact diff could not be confirmed. Granting read-only dashboard and repo access to the on-call agents would materially shorten MTTR.
- **Idempotency is not visible in code review.** It must be asserted on the wire (header) or in provider logs, not by reading variable names.

---

## 9. Glossary for non-technical readers

- **HTTP 500:** A server error — the request failed on our side.
- **Rollback / revert:** Undoing a recent code change by re-deploying the previous version.
- **SDK:** A vendor-provided toolkit that our code uses to talk to a service (here, Stripe).
- **Idempotency key:** A unique tag sent with a payment request so that retries do not create a second charge.
- **MTTR:** Mean time to recovery.
