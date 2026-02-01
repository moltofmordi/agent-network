// Graph-Based Coordination Detection
// Implements clustering coefficient and community detection to catch adaptive vote rings

class VotingGraph {
  constructor() {
    this.nodes = new Map(); // agentId -> {upvotes_given: Set, upvotes_received: Set}
    this.edges = []; // {from, to, post_id, timestamp}
  }

  addVote(from_agent_id, to_agent_id, post_id, timestamp) {
    // Initialize nodes if they don't exist
    if (!this.nodes.has(from_agent_id)) {
      this.nodes.set(from_agent_id, { upvotes_given: new Set(), upvotes_received: new Set() });
    }
    if (!this.nodes.has(to_agent_id)) {
      this.nodes.set(to_agent_id, { upvotes_given: new Set(), upvotes_received: new Set() });
    }

    // Add edge
    this.edges.push({ from: from_agent_id, to: to_agent_id, post_id, timestamp });
    
    // Update node connections
    this.nodes.get(from_agent_id).upvotes_given.add(to_agent_id);
    this.nodes.get(to_agent_id).upvotes_received.add(from_agent_id);
  }

  // Calculate clustering coefficient for a specific agent's upvoter network
  // Measures: "How interconnected are the agents who upvote this user?"
  calculateClusteringCoefficient(agent_id) {
    const node = this.nodes.get(agent_id);
    if (!node) return 0;

    const upvoters = Array.from(node.upvotes_received);
    if (upvoters.length < 2) return 0; // Need at least 2 upvoters to have clustering

    // Count connections between upvoters
    let connections = 0;
    let possibleConnections = 0;

    for (let i = 0; i < upvoters.length; i++) {
      for (let j = i + 1; j < upvoters.length; j++) {
        const upvoter1 = upvoters[i];
        const upvoter2 = upvoters[j];
        
        possibleConnections++;
        
        // Check if upvoter1 and upvoter2 upvote each other
        const node1 = this.nodes.get(upvoter1);
        const node2 = this.nodes.get(upvoter2);
        
        if (node1 && node2) {
          if (node1.upvotes_given.has(upvoter2) || node2.upvotes_given.has(upvoter1)) {
            connections++;
          }
        }
      }
    }

    if (possibleConnections === 0) return 0;
    return connections / possibleConnections;
  }

  // Calculate external diversity ratio
  // Measures: "Does this agent's upvoter network also upvote people outside the network?"
  calculateExternalDiversityRatio(agent_id) {
    const node = this.nodes.get(agent_id);
    if (!node) return 1.0; // Default to diverse if no data

    const upvoters = Array.from(node.upvotes_received);
    if (upvoters.length === 0) return 1.0;

    let totalUpvotesGiven = 0;
    let externalUpvotes = 0;

    for (const upvoter_id of upvoters) {
      const upvoterNode = this.nodes.get(upvoter_id);
      if (!upvoterNode) continue;

      const upvotesGiven = Array.from(upvoterNode.upvotes_given);
      totalUpvotesGiven += upvotesGiven.length;

      // Count upvotes to agents OUTSIDE this agent's upvoter network
      for (const target of upvotesGiven) {
        if (!upvoters.includes(target) && target !== agent_id) {
          externalUpvotes++;
        }
      }
    }

    if (totalUpvotesGiven === 0) return 1.0;
    return externalUpvotes / totalUpvotesGiven;
  }

  // Detect coordinated groups using simple community detection
  // Returns: Map of agent_id -> community_id
  detectCommunities() {
    const communities = new Map();
    let communityId = 0;

    const visited = new Set();

    for (const [agent_id, node] of this.nodes) {
      if (visited.has(agent_id)) continue;

      // Start a new community with BFS
      const community = new Set();
      const queue = [agent_id];
      
      while (queue.length > 0) {
        const current = queue.shift();
        if (visited.has(current)) continue;
        
        visited.add(current);
        community.add(current);

        const currentNode = this.nodes.get(current);
        if (!currentNode) continue;

        // Add neighbors (people this agent upvotes and receives upvotes from)
        const neighbors = new Set([
          ...Array.from(currentNode.upvotes_given),
          ...Array.from(currentNode.upvotes_received)
        ]);

        for (const neighbor of neighbors) {
          if (!visited.has(neighbor)) {
            // Only add to community if connection is strong (mutual upvoting)
            const neighborNode = this.nodes.get(neighbor);
            if (neighborNode) {
              const mutualConnection = 
                currentNode.upvotes_given.has(neighbor) && 
                neighborNode.upvotes_given.has(current);
              
              if (mutualConnection) {
                queue.push(neighbor);
              }
            }
          }
        }
      }

      // Assign community ID to all members
      for (const member of community) {
        communities.set(member, communityId);
      }
      communityId++;
    }

    return communities;
  }

  // Calculate coordination score for an agent (0-1, higher = more suspicious)
  calculateCoordinationScore(agent_id) {
    const clustering = this.calculateClusteringCoefficient(agent_id);
    const diversity = this.calculateExternalDiversityRatio(agent_id);

    // High clustering + low diversity = high coordination score
    // Clustering: 0.8+ is suspicious (raised from 0.7)
    // Diversity: <0.2 is suspicious (lowered from 0.5)
    
    let score = 0;
    
    // Clustering contribution (0-0.6)
    if (clustering > 0.8) {
      score += 0.6 * ((clustering - 0.8) / 0.2); // Scale from 0.8-1.0 to 0-0.6
    }
    
    // Diversity contribution (0-0.4)
    if (diversity < 0.3) {
      score += 0.4 * ((0.3 - diversity) / 0.3); // Scale from 0.3-0 to 0-0.4
    }

    return Math.min(score, 1.0);
  }

  // Generate report for all agents
  generateReport() {
    const report = [];
    
    for (const [agent_id, node] of this.nodes) {
      const clustering = this.calculateClusteringCoefficient(agent_id);
      const diversity = this.calculateExternalDiversityRatio(agent_id);
      const coordinationScore = this.calculateCoordinationScore(agent_id);
      
      report.push({
        agent_id,
        upvoters: node.upvotes_received.size,
        upvotes_given: node.upvotes_given.size,
        clustering_coefficient: clustering,
        external_diversity_ratio: diversity,
        coordination_score: coordinationScore,
        flagged: coordinationScore > 0.7  // Raised threshold to reduce false positives
      });
    }

    return report.sort((a, b) => b.coordination_score - a.coordination_score);
  }
}

// Build graph from simulation data
function buildGraphFromSimulation(simulation) {
  const graph = new VotingGraph();

  for (const post of simulation.posts) {
    for (const upvoter_id of post.upvotes) {
      graph.addVote(upvoter_id, post.author.id, post.id, post.day);
    }
  }

  return graph;
}

// Analyze simulation for coordination
function analyzeCoordination(simulation) {
  const graph = buildGraphFromSimulation(simulation);
  const report = graph.generateReport();
  const communities = graph.detectCommunities();

  console.log('\n=== COORDINATION DETECTION REPORT ===\n');

  // Group by agent type for comparison
  const honestAgents = report.filter(r => simulation.agents.find(a => a.id === r.agent_id && a.type === 'honest'));
  const ringAgents = report.filter(r => simulation.agents.find(a => a.id === r.agent_id && a.type === 'vote-ring'));

  console.log('HONEST AGENTS:');
  console.log('  Avg Clustering:', (honestAgents.reduce((sum, a) => sum + a.clustering_coefficient, 0) / honestAgents.length).toFixed(3));
  console.log('  Avg Diversity:', (honestAgents.reduce((sum, a) => sum + a.external_diversity_ratio, 0) / honestAgents.length).toFixed(3));
  console.log('  Avg Coordination Score:', (honestAgents.reduce((sum, a) => sum + a.coordination_score, 0) / honestAgents.length).toFixed(3));
  console.log('  Flagged:', honestAgents.filter(a => a.flagged).length, '/', honestAgents.length);

  console.log('\nVOTE RING AGENTS:');
  console.log('  Avg Clustering:', (ringAgents.reduce((sum, a) => sum + a.clustering_coefficient, 0) / ringAgents.length).toFixed(3));
  console.log('  Avg Diversity:', (ringAgents.reduce((sum, a) => sum + a.external_diversity_ratio, 0) / ringAgents.length).toFixed(3));
  console.log('  Avg Coordination Score:', (ringAgents.reduce((sum, a) => sum + a.coordination_score, 0) / ringAgents.length).toFixed(3));
  console.log('  Flagged:', ringAgents.filter(a => a.flagged).length, '/', ringAgents.length);

  console.log('\n=== DETECTION EFFECTIVENESS ===');
  const truePositives = ringAgents.filter(a => a.flagged).length;
  const falsePositives = honestAgents.filter(a => a.flagged).length;
  const trueNegatives = honestAgents.filter(a => !a.flagged).length;
  const falseNegatives = ringAgents.filter(a => !a.flagged).length;

  const precision = truePositives / (truePositives + falsePositives) || 0;
  const recall = truePositives / (truePositives + falseNegatives) || 0;
  const f1Score = 2 * (precision * recall) / (precision + recall) || 0;

  console.log('  Precision:', (precision * 100).toFixed(1) + '%', '(of flagged, how many are actually vote ring)');
  console.log('  Recall:', (recall * 100).toFixed(1) + '%', '(of vote ring, how many were caught)');
  console.log('  F1 Score:', f1Score.toFixed(3));

  console.log('\n=== COMMUNITY DETECTION ===');
  const communityStats = new Map();
  for (const [agent_id, community_id] of communities) {
    if (!communityStats.has(community_id)) {
      communityStats.set(community_id, { honest: 0, ring: 0 });
    }
    const agent = simulation.agents.find(a => a.id === agent_id);
    if (agent.type === 'honest') {
      communityStats.get(community_id).honest++;
    } else {
      communityStats.get(community_id).ring++;
    }
  }

  console.log('  Communities detected:', communityStats.size);
  for (const [community_id, stats] of communityStats) {
    const total = stats.honest + stats.ring;
    console.log(`  Community ${community_id}: ${total} members (${stats.ring} ring, ${stats.honest} honest)`);
  }

  return { report, communities, stats: { precision, recall, f1Score } };
}

module.exports = { VotingGraph, buildGraphFromSimulation, analyzeCoordination };
