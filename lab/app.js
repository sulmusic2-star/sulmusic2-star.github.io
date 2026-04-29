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
  return { address: packet.address, validatedLanes: validated.map(l => l.lane), warningCount: warnings.length, warnings, supportDepth, packetLanguage: summary };
}

function renderJson(id, value) {
  document.getElementById(id).textContent = JSON.stringify(value, null, 2);
}

function runSquadBrain() {
  const normalizedRoster = normalizeRoster(rosterRows);
  const promptCandidates = findPromptCandidates(normalizedRoster, 'guard');
  const rankedMatches = rankMatchCandidates({ team: 'BOS', rating: 1230 }, matchPool);
  renderJson('squadInput', { rosterRows, currentPlayer: { team: 'BOS', rating: 1230 }, matchPool });
  renderJson('squadOutput', { normalizedRoster, promptCandidates, bestMatch: rankedMatches[0], rankedMatches });
}

function runLastingGround() {
  renderJson('groundInput', propertyPacket);
  renderJson('groundOutput', validatePacket(propertyPacket));
}

document.getElementById('runSquad').addEventListener('click', runSquadBrain);
document.getElementById('runGround').addEventListener('click', runLastingGround);
runSquadBrain();
runLastingGround();
