/**
 * IncidentRoom CLI Simulation & Switch AI Event Stream
 */
const { TriageAgent, SreAgent, CommsAgent } = require('./agents');

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function runSimulation() {
  console.log('\n================================================================');
  console.log('🚨  INCIDENTROOM: SWITCH MULTI-AGENT SRE WAR ROOM INITIALIZING  🚨');
  console.log('================================================================\n');

  const startedAt = new Date();

  // 1. Alert arrives
  const alert = {
    id: 'INC-2026-9912',
    service: 'checkout-payment-gateway',
    severity: 'SEV-1',
    errorMessage: 'HTTP 500 Spike: stripe_client.checkout.sessions.create() missing idempotency_key',
    stackTrace: 'File services/payments/stripe_gateway.js:84: createSession() - TypeError: Cannot read property idempotency_key'
  };

  console.log(`[ALERT DISPATCHED] ⚠️  ${alert.severity} in ${alert.service}`);
  console.log(`Description: ${alert.errorMessage}\n`);
  await sleep(1000);

  // 2. Simulated Git Commits
  const recentCommits = [
    {
      id: '8f2b31a0e889c1d',
      author: 'alex.engineer@corp.com',
      message: 'feat(payments): upgrade stripe sdk v3.4 and refactor session handler',
      timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
      changedFiles: ['services/payments/stripe_gateway.js', 'package.json']
    },
    {
      id: '1a90c4e8832bb5e',
      author: 'emily.designer@corp.com',
      message: 'style: fix spacing on checkout confirmation modal',
      timestamp: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
      changedFiles: ['frontend/src/CheckoutModal.jsx']
    }
  ];

  // 3. Triage Agent Investigates
  const triage = new TriageAgent();
  console.log(`[BOT] 🔍 @${triage.name}: Correlating stack trace against recent merged PRs...`);
  await sleep(1500);

  const report = triage.investigate(alert, recentCommits);
  console.log(`\n┌── [TRIAGE REPORT - @${triage.name}] ──────────────────────────────`);
  console.log(`│ Confidence: ${(report.confidenceScore * 100).toFixed(0)}%`);
  console.log(`│ Root Cause: ${report.rootCauseSummary}`);
  console.log(`│ Recommendation: ${report.recommendedAction}`);
  console.log(`└─────────────────────────────────────────────────────────────────\n`);
  await sleep(1000);

  // 4. SRE Agent Prepares Remediation
  const sre = new SreAgent();
  console.log(`[BOT] 🛠️  @${sre.name}: Drafting automated rollback pull request...`);
  await sleep(1200);

  const plan = sre.draftRemediation(report);
  console.log(`┌── [SRE REMEDIATION PROPOSAL - @${sre.name}] ───────────────────────`);
  console.log(`│ Action: ${plan.actionType}`);
  console.log(`│ Rollback Target: Commit ${plan.rollbackCommitId.substring(0, 7)}`);
  console.log(`│ Pull Request: ${plan.prUrl}`);
  console.log(`│ STATUS: ⚠️  AWAITING HUMAN SIGN-OFF`);
  console.log(`│ Instructions: Human On-Call Lead must reply 'APPROVE' to proceed.`);
  console.log(`└─────────────────────────────────────────────────────────────────\n`);
  await sleep(1500);

  // 5. Human Sign-Off (Wispr Flow / Voice)
  console.log(`[HUMAN] 🧑‍💻 @swati (via Wispr Flow Voice): "APPROVE rollback and notify stakeholders"`);
  await sleep(1000);

  // 6. Execute Remediation
  sre.execute(plan, 'swati (on-call lead)');
  console.log(`\n[BOT] 🚀 @${sre.name}: Rollback deployed to production. Health checks 200 OK. Error rate returned to 0.00%.`);
  await sleep(1000);

  // 7. Comms Agent Generates Post-Mortem
  const comms = new CommsAgent();
  const resolvedAt = new Date();
  const postMortem = comms.generatePostMortem(alert, report, plan, startedAt, resolvedAt);

  console.log(`\n┌── [POST-MORTEM SUMMARY - @${comms.name}] ─────────────────────────`);
  console.log(`│ Incident ID: ${postMortem.incidentId}`);
  console.log(`│ Duration / MTTR: ${postMortem.duration}`);
  console.log(`│ Root Cause: ${postMortem.rootCause}`);
  console.log(`│ Resolution: ${postMortem.resolution}`);
  console.log(`│ Action Items:`);
  postMortem.actionItems.forEach(item => console.log(`│   • ${item}`));
  console.log(`└─────────────────────────────────────────────────────────────────\n`);

  console.log('✅ Incident resolved in under 2 minutes. War room archived.\n');
}

runSimulation();
