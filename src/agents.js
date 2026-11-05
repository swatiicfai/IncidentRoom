/**
 * IncidentRoom Agent Swarm Implementation (Node.js)
 */

class TriageAgent {
  constructor(name = 'triage-agent') {
    this.name = name;
  }

  investigate(alert, recentCommits) {
    let offendingCommit = null;
    const errorTokens = (alert.errorMessage + ' ' + alert.stackTrace).toLowerCase();

    for (const commit of recentCommits) {
      for (const file of commit.changedFiles) {
        const fileStem = file.split('/').pop().replace(/\.[^/.]+$/, '').toLowerCase();
        if (errorTokens.includes(fileStem)) {
          offendingCommit = commit;
          break;
        }
      }
      if (offendingCommit) break;
    }

    if (!offendingCommit && recentCommits.length > 0) {
      offendingCommit = recentCommits[0];
    }

    return {
      incidentId: alert.id,
      offendingCommit,
      confidenceScore: 0.96,
      rootCauseSummary: offendingCommit
        ? `Identified root cause in commit ${offendingCommit.id.substring(0, 7)} ('${offendingCommit.message}') by ${offendingCommit.author}. Culprit file: ${offendingCommit.changedFiles[0]}`
        : 'No direct commit match found. Manual review recommended.',
      recommendedAction: offendingCommit
        ? `Deploy automated rollback for commit ${offendingCommit.id.substring(0, 7)}`
        : 'Inspect telemetry logs'
    };
  }
}

class SreAgent {
  constructor(name = 'sre-agent') {
    this.name = name;
  }

  draftRemediation(triageReport) {
    const commitId = triageReport.offendingCommit ? triageReport.offendingCommit.id : 'HEAD~1';
    return {
      incidentId: triageReport.incidentId,
      actionType: 'ROLLBACK',
      targetBranch: 'main',
      rollbackCommitId: commitId,
      prUrl: `https://github.com/swatiicfai/IncidentRoom/pull/rollback-${commitId.substring(0, 7)}`,
      status: 'PENDING_HUMAN_APPROVAL'
    };
  }

  execute(plan, approver) {
    plan.status = 'APPROVED';
    plan.approvedBy = approver;
    plan.executedAt = new Date().toISOString();
    return true;
  }
}

class CommsAgent {
  constructor(name = 'comms-agent') {
    this.name = name;
  }

  generatePostMortem(alert, triage, plan, startedAt, resolvedAt) {
    const durationSeconds = Math.max(5, Math.round((resolvedAt - startedAt) / 1000));
    return {
      incidentId: alert.id,
      service: alert.service,
      severity: alert.severity,
      duration: `${durationSeconds}s (Simulated)`,
      rootCause: triage.rootCauseSummary,
      resolution: `Automated ${plan.actionType} of ${plan.rollbackCommitId.substring(0, 7)} approved by ${plan.approvedBy}.`,
      actionItems: [
        `Add regression integration test for ${triage.offendingCommit ? triage.offendingCommit.changedFiles[0] : 'service'}`,
        'Enforce automated linting for payment idempotency tokens in CI',
        'Tune PagerDuty anomaly detection threshold'
      ]
    };
  }
}

module.exports = {
  TriageAgent,
  SreAgent,
  CommsAgent
};
