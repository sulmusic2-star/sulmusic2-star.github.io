const rosterRows = [
  { name: '  mika hart ', jersey: '07', position: 'guard' },
  { name: 'Mika Hart', jersey: '7', position: 'G' },
  { name: 'DANIEL ROSS', jersey: 'thirty', position: 'Forward' },
  { name: 'Jules Carter', jersey: '12', position: 'center' }
];

const matchPool = [
  { handle: 'northstar', team: 'BOS', rating: 1210, waitingSeconds: 22 },
  { handle: 'fastbreak77', team: 'BOS', rating: 1325, waitingSeconds: 8 },
  { handle: 'coastline', team: 'NYK', rating: 1240, waitingSeconds: 90 },
  { handle: 'lateclock', team: 'BOS', rating: 1198, waitingSeconds: 64 }
];

const practiceCards = [
  { playerId: 'mika', team: 'BOS', displayName: 'Mika Hart', misses: 3, correctStreak: 0, ease: 1, lastSeenHoursAgo: 2 },
  { playerId: 'daniel', team: 'BOS', displayName: 'Daniel Ross', misses: 0, correctStreak: 5, ease: 2.2, lastSeenHoursAgo: 1 },
  { playerId: 'jules', team: 'BOS', displayName: 'Jules Carter', misses: 1, correctStreak: 1, ease: 1.1, lastSeenHoursAgo: 8 }
];

const quickMatchSubmission = {
  startedAtMs: 1000,
  finishedAtMs: 2200,
  expectedPromptCount: 3,
  results: [
    { promptId: 'p1', expected: 'mika', selected: 'mika', isCorrect: true, answeredAtMs: 1300 },
    { promptId: 'p2', expected: 'daniel', selected: 'daniel', isCorrect: true, answeredAtMs: 1700 },
    { promptId: 'p3', expected: 'jules', selected: 'jules', isCorrect: true, answeredAtMs: 2100 }
  ]
};

const propertyPacket = {
  address: '42 Harbor View Lane, Sampletown MA',
  sourceLanes: [
    { lane: 'flood_map', status: 'validated', reviewed: '2026-04-20', supports: ['mapped flood context'] },
    { lane: 'assessor', status: 'validated', reviewed: '2026-04-18', supports: ['parcel identity'] },
    { lane: 'conservation', status: 'stale', reviewed: '2025-03-01', supports: [] },
    { lane: 'building_permit', status: 'missing', reviewed: null, supports: [] }
  ]
};

function normalizePosition(position) {
  const value = position.trim().toLowerCase();
  if (value === 'g') return 'Guard';
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function normalizeRoster(rows) {
  const byKey = new Map();
  for (const row of rows) {
    const name = row.name.trim().replace(/\s+/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    const parsedJersey = Number.parseInt(row.jersey, 10);
    const jersey = Number.isFinite(parsedJersey) ? parsedJersey : null;
    const key = `${name.toLowerCase()}-${jersey ?? 'unknown'}`;
    byKey.set(key, { id: key, name, jersey, position: normalizePosition(row.position) });
  }
  return [...byKey.values()];
}

function findPromptCandidates(roster, query) {
  const q = query.toLowerCase();
  return roster.filter(player => [player.name, player.position, String(player.jersey ?? '')].some(value => value.toLowerCase().includes(q)));
}

function rankMatchCandidates(currentPlayer, pool) {
  return pool
    .filter(candidate => candidate.team === currentPlayer.team)
    .map(candidate => {
      const ratingGap = Math.abs(candidate.rating - currentPlayer.rating);
      const fairnessScore = Math.max(0, 200 - ratingGap);
      const waitScore = Math.min(50, candidate.waitingSeconds / 2);
      return { ...candidate, ratingGap, score: Math.round(fairnessScore + waitScore) };
    })
    .sort((a, b) => b.score - a.score);
}

function buildAdaptivePracticeQueue(cards) {
  return cards
    .filter(card => card.team === 'BOS')
    .map(card => {
      const dueScore = Math.min(60, card.lastSeenHoursAgo * 8);
      const missScore = Math.min(36, card.misses * 12);
      const stabilityPenalty = card.correctStreak >= 4 ? -18 : 10;
      const priority = Math.max(0, Math.min(100, Math.round(dueScore + missScore + stabilityPenalty)));
      const reasons = [];
      if (card.misses) reasons.push('miss-history');
      if (card.correctStreak === 0) reasons.push('not-yet-stable');
      if (card.correctStreak >= 4) reasons.push('stable-card');
      return { playerId: card.playerId, displayName: card.displayName, priority, reasons };
    })
    .sort((a, b) => b.priority - a.priority);
}

function validateQuickMatch(submission) {
  const issues = [];
  if (submission.results.length !== submission.expectedPromptCount) issues.push('prompt-count-mismatch');
  let previous = submission.startedAtMs;
  for (const result of submission.results) {
    if (result.answeredAtMs < previous) issues.push('non-monotonic-answer-time');
    if ((result.selected === result.expected) !== result.isCorrect) issues.push('correctness-mismatch');
    previous = result.answeredAtMs;
  }
  const duration = submission.finishedAtMs - submission.startedAtMs;
  const averageAnswerMs = Math.round(duration / Math.max(1, submission.results.length));
  const accuracy = submission.results.filter(r => r.selected === r.expected).length / Math.max(1, submission.results.length);
  if (averageAnswerMs < 650 && accuracy >= 0.9) issues.push('answer-speed-review');
  return { accepted: !issues.includes('answer-speed-review') && issues.length === 0, riskLevel: issues.length ? 'high' : 'low', averageAnswerMs, accuracy, issues };
}

function scoreLane(lane) {
  const sourcePoints = { flood_map: 35, assessor: 32, conservation: 28, building_permit: 28 }[lane.lane] ?? 10;
  const statusPoints = { validated: 34, stale: 12, missing: 0 }[lane.status] ?? 0;
  const supportPoints = Math.min(15, lane.supports.length * 5);
  const freshnessPoints = lane.reviewed ? 18 : 0;
  const score = lane.status === 'missing' ? 0 : Math.min(100, sourcePoints + statusPoints + supportPoints + freshnessPoints);
  return { lane: lane.lane, score, confidence: score >= 78 ? 'strong' : score >= 45 ? 'usable_with_caution' : 'weak_or_missing' };
}

function validatePacket(packet) {
  const warnings = [];
  const validated = packet.sourceLanes.filter(lane => lane.status === 'validated');
  for (const lane of packet.sourceLanes) {
    if (lane.status === 'missing') warnings.push(`${lane.lane}: source lane missing`);
    if (lane.status === 'stale') warnings.push(`${lane.lane}: review date is stale`);
    if (lane.status === 'validated' && (!lane.reviewed || lane.supports.length === 0)) warnings.push(`${lane.lane}: validation needs a date and supported claim`);
  }
  const supportDepth = warnings.length === 0 && validated.length >= 4 ? 'strong_local_support' : validated.length >= 2 ? 'partial_source_support' : 'limited_support';
  const summary = supportDepth === 'strong_local_support'
    ? 'The packet can describe local context with stronger source support.'
    : 'The packet should stay cautious: some lanes support context, but missing or stale lanes remain visible.';
  const evidenceScores = packet.sourceLanes.map(scoreLane);
  const averageScore = Math.round(evidenceScores.reduce((sum, lane) => sum + lane.score, 0) / evidenceScores.length);
  return { address: packet.address, validatedLanes: validated.map(l => l.lane), warningCount: warnings.length, warnings, supportDepth, evidenceScores, averageScore, packetLanguage: summary };
}

function renderJson(id, value) {
  document.getElementById(id).textContent = JSON.stringify(value, null, 2);
}

function computeSquadBrain() {
  const normalizedRoster = normalizeRoster(rosterRows);
  const promptCandidates = findPromptCandidates(normalizedRoster, 'guard');
  const rankedMatches = rankMatchCandidates({ team: 'BOS', rating: 1230 }, matchPool);
  return {
    input: { rosterRows, currentPlayer: { team: 'BOS', rating: 1230 }, matchPool, practiceCards, quickMatchSubmission },
    output: { normalizedRoster, promptCandidates, adaptivePracticeQueue: buildAdaptivePracticeQueue(practiceCards), resultValidation: validateQuickMatch(quickMatchSubmission), bestMatch: rankedMatches[0], rankedMatches }
  };
}

function computeLastingGround() {
  return { input: propertyPacket, output: validatePacket(propertyPacket) };
}

function runSquadBrain() {
  const result = computeSquadBrain();
  renderJson('squadInput', result.input);
  renderJson('squadOutput', result.output);
  return result.output;
}

function runLastingGround() {
  const result = computeLastingGround();
  renderJson('groundInput', result.input);
  renderJson('groundOutput', result.output);
  return result.output;
}

document.getElementById('runSquad').addEventListener('click', runSquadBrain);
document.getElementById('runGround').addEventListener('click', runLastingGround);
runSquadBrain();
runLastingGround();

const labScenarios = {
  squad: {
    label: 'SquadBrain validation',
    kicker: 'Validation boundary',
    title: 'Competitive results are recomputed before rank movement.',
    summary: 'Questionable quick-match submissions are checked against timing, prompt count, answer order, and correctness before they can affect competitive state.',
    stats: ['high', 'answer-speed-review', '25 tests'],
    statLabels: ['risk level', 'flag surfaced', 'public TS checks'],
    steps: ['Normalize the roster input.', 'Prioritize practice and rank match candidates.', 'Validate the match result before accepting rank movement.'],
    primary: ['Open proof file', 'https://github.com/sulmusic2-star/squadbrain-showcase/blob/main/examples/result-validation.ts'],
    secondary: ['Open demo', 'https://sulmusic2-star.github.io/squadbrain-showcase/'],
    action: runSquadBrain
  },
  ground: {
    label: 'Lasting Ground evidence',
    kicker: 'Evidence boundary',
    title: 'Packet language follows source support.',
    summary: 'Validated, stale, and missing lanes change support depth, warning count, and the language the packet is allowed to use.',
    stats: ['partial', '2 warnings', '18 tests'],
    statLabels: ['support depth', 'visible gaps', 'public Python checks'],
    steps: ['Score each source lane for authority and freshness.', 'Keep missing or stale lanes visible.', 'Compose cautious packet language from support depth.'],
    primary: ['Open evidence scoring', 'https://github.com/sulmusic2-star/lasting-ground-showcase/blob/main/examples/evidence_scoring.py'],
    secondary: ['Open sample packet', 'https://sulmusic2-star.github.io/lasting-ground-showcase/assets/lasting-ground-sample-packet.pdf'],
    action: runLastingGround
  },
  compare: {
    label: 'Combined review path',
    kicker: 'Review route',
    title: 'Different domains, same proof standard.',
    summary: 'Both systems expose the same maturity pattern: usable surface, explicit rules, validation boundary, test coverage, decision records, and generated artifacts.',
    stats: ['43 tests', '2 systems', '1 packet'],
    statLabels: ['public checks', 'focused proof paths', 'portable review artifact'],
    steps: ['Open the outcome board to see the claims.', 'Run this lab to inspect behavior.', 'Use GitHub examples, coverage, and ADRs to verify the implementation path.'],
    primary: ['Open outcome board', 'https://sulmusic2-star.github.io/outcomes/'],
    secondary: ['Open diligence packet', 'https://sulmusic2-star.github.io/diligence/'],
    action: () => { runSquadBrain(); runLastingGround(); }
  }
};

function setText(selector, value) {
  const element = document.querySelector(selector);
  if (element) element.textContent = value;
}

function summaryCard(label, value, detail, tone = '') {
  return `<article class="summary-card ${tone}"><span>${label}</span><b>${value}</b><small>${detail}</small></article>`;
}

function renderLiveSummary(key) {
  const squad = computeSquadBrain().output;
  const ground = computeLastingGround().output;
  const cards = document.querySelector('[data-summary-cards]');
  const pipeline = document.querySelector('[data-summary-pipeline]');
  const mode = document.querySelector('[data-summary-mode]');
  if (!cards || !pipeline) return;

  const topPractice = squad.adaptivePracticeQueue[0];
  const validation = squad.resultValidation;
  const bestMatch = squad.bestMatch;
  const strongestLane = [...ground.evidenceScores].sort((a, b) => b.score - a.score)[0];
  const weakestLane = [...ground.evidenceScores].sort((a, b) => a.score - b.score)[0];

  if (key === 'ground') {
    if (mode) mode.textContent = 'Lasting Ground evidence';
    cards.innerHTML = [
      summaryCard('Average evidence score', `${ground.averageScore}/100`, `${ground.supportDepth.replaceAll('_', ' ')} returned by the packet validator.`, 'strong'),
      summaryCard('Strongest source lane', strongestLane.lane.replaceAll('_', ' '), `${strongestLane.score}/100 - ${strongestLane.confidence.replaceAll('_', ' ')}`),
      summaryCard('Visible source gaps', `${ground.warningCount} warnings`, ground.warnings.join(' · '), ground.warningCount ? 'warn' : 'strong'),
      summaryCard('Packet language', 'cautious', ground.packetLanguage, 'wide')
    ].join('');
    pipeline.innerHTML = ['Source lanes', 'Evidence score', 'Support depth', 'Packet language'].map((step, index) => `<div><span>${String(index + 1).padStart(2, '0')}</span><b>${step}</b></div>`).join('');
    return;
  }

  if (key === 'compare') {
    if (mode) mode.textContent = 'Combined review path';
    cards.innerHTML = [
      summaryCard('Public checks', '43 tests', '25 TypeScript checks plus 18 Python checks across the showcase repos.', 'strong'),
      summaryCard('Validation boundaries', '2 systems', 'Competitive result validation and source-support validation both stay visible.'),
      summaryCard('Proof artifacts', 'packet + lab', 'The PDF packet routes to the live lab, examples, coverage, ADRs, and demos.'),
      summaryCard('Review standard', 'route -> run -> inspect', 'A reviewer can move from claim to mechanism to evidence without a private walkthrough.', 'wide')
    ].join('');
    pipeline.innerHTML = ['Outcome claim', 'Run lab', 'Open code', 'Verify artifact'].map((step, index) => `<div><span>${String(index + 1).padStart(2, '0')}</span><b>${step}</b></div>`).join('');
    return;
  }

  if (mode) mode.textContent = 'SquadBrain validation';
  cards.innerHTML = [
    summaryCard('Roster normalized', `${squad.normalizedRoster.length} players`, 'Duplicate names collapse, casing normalizes, invalid jersey stays reviewable.'),
    summaryCard('Top practice priority', `${topPractice.priority}/100`, `${topPractice.displayName} appears first because: ${topPractice.reasons.join(', ')}.`, 'strong'),
    summaryCard('Best match score', bestMatch.score, `${bestMatch.handle} selected with ${bestMatch.ratingGap} rating gap.`),
    summaryCard('Result validation', validation.riskLevel, `${validation.averageAnswerMs}ms average answer; ${validation.issues.join(', ') || 'no issues'}.`, validation.riskLevel === 'high' ? 'warn' : 'strong')
  ].join('');
  pipeline.innerHTML = ['Roster input', 'Practice queue', 'Match rank', 'Risk flag'].map((step, index) => `<div><span>${String(index + 1).padStart(2, '0')}</span><b>${step}</b></div>`).join('');
}

function renderLabScenario(key) {
  const state = labScenarios[key] || labScenarios.squad;
  document.querySelectorAll('[data-lab-scenario]').forEach(button => {
    button.classList.toggle('active', button.dataset.labScenario === key);
  });
  setText('[data-lab-label]', state.label);
  setText('[data-lab-kicker]', state.kicker);
  setText('[data-lab-title]', state.title);
  setText('[data-lab-summary]', state.summary);
  setText('[data-lab-stat-a]', state.stats[0]);
  setText('[data-lab-stat-b]', state.stats[1]);
  setText('[data-lab-stat-c]', state.stats[2]);
  document.querySelectorAll('.runner-stats small').forEach((small, index) => {
    small.textContent = state.statLabels[index] || '';
  });
  const steps = document.querySelector('[data-lab-steps]');
  if (steps) steps.innerHTML = state.steps.map((step, index) => `<li><span>${String(index + 1).padStart(2, '0')}</span>${step}</li>`).join('');
  const primary = document.querySelector('[data-lab-primary]');
  const secondary = document.querySelector('[data-lab-secondary]');
  if (primary) { primary.textContent = state.primary[0]; primary.href = state.primary[1]; }
  if (secondary) { secondary.textContent = state.secondary[0]; secondary.href = state.secondary[1]; }
  state.action();
  renderLiveSummary(key);
}

document.querySelectorAll('[data-lab-scenario]').forEach(button => {
  button.addEventListener('click', () => renderLabScenario(button.dataset.labScenario));
});
renderLabScenario('squad');
