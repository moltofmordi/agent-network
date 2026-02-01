// Test Graph-Based Detection Against Adaptive Vote Ring

const { Simulation, Agent } = require('./economic-sim.js');
const { analyzeCoordination } = require('./graph-detector.js');

// Recreate AdaptiveSimulation class (can't import from test file)
class AdaptiveSimulation extends Simulation {
  constructor(config = {}) {
    super(config);
    this.config.enableQualityMultiplier = config.enableQualityMultiplier !== false;
    this.config.ringVoteDistribution = config.ringVoteDistribution || 0.6;
  }

  createPost(agent, quality) {
    const post = super.createPost(agent, quality);
    if (!post) return null;

    if (quality === 'quality') {
      post.qualityMultiplier = 1.5 + Math.random() * 0.5;
    } else if (quality === 'mediocre') {
      post.qualityMultiplier = 0.8 + Math.random() * 0.4;
    } else if (quality === 'spam') {
      post.qualityMultiplier = 0.3 + Math.random() * 0.2;
    } else {
      post.qualityMultiplier = 1.0;
    }

    return post;
  }

  simulateEngagement() {
    const todaysPosts = this.posts.filter(p => p.day === this.day);

    for (const post of todaysPosts) {
      const honestAgents = this.agents.filter(a => a.type === 'honest');
      for (const agent of honestAgents) {
        if (post.content.includes('quality') && Math.random() < 0.5) {
          post.addUpvote(agent, true);
          agent.upvotes_given.push(post.id);
        }
      }

      if (post.author.type === 'vote-ring') {
        const ringAgents = this.agents.filter(a => a.type === 'vote-ring' && a.id !== post.author.id);
        const shuffled = ringAgents.sort(() => Math.random() - 0.5);
        const selectedVoters = shuffled.slice(0, Math.floor(ringAgents.length * this.config.ringVoteDistribution));

        for (const agent of selectedVoters) {
          const llmCost = this.config.llmCostPerChallenge / this.config.tokenValue;
          if (agent.tokens > llmCost) {
            agent.tokens -= llmCost;
            post.addUpvote(agent, true);
            agent.upvotes_given.push(post.id);
          }
        }

        const honestVoters = honestAgents.filter(() => Math.random() < 0.15);
        for (const agent of honestVoters) {
          post.addUpvote(agent, true);
          agent.upvotes_given.push(post.id);
        }
      }

      if (post.content.includes('spam') && Math.random() < 0.05) {
        const randomAgent = this.agents[Math.floor(Math.random() * this.agents.length)];
        if (randomAgent.id !== post.author.id) {
          post.addUpvote(randomAgent, true);
        }
      }
    }
  }

  calculateDayEarnings() {
    const todaysPosts = this.posts.filter(p => p.day === this.day);

    for (const post of todaysPosts) {
      const diversity = this.calculateDiversity(post);
      const diversityMultiplier = diversity < 0.3 ? 0.2 : 1.0;
      const qualityMultiplier = this.config.enableQualityMultiplier 
        ? (post.qualityMultiplier || 1.0)
        : 1.0;

      const earnings = post.calculateEarnings() * diversityMultiplier * qualityMultiplier;
      post.author.tokens += earnings;
    }
  }
}

console.log('=================================================================');
console.log('TEST: Graph-Based Detection vs Adaptive Vote Ring');
console.log('=================================================================\n');

console.log('SCENARIO:');
console.log('- Vote ring distributes votes strategically (60% overlap)');
console.log('- Simple reciprocity check would FAIL (appears low reciprocity)');
console.log('- Graph detection should catch via clustering + diversity\n');

// Test 1: 60% vote distribution (adaptive attack)
console.log('\n--- TEST 1: Adaptive Vote Ring (60% distribution) ---\n');

const sim1 = new AdaptiveSimulation({
  days: 30,
  numHonest: 50,
  numSpammers: 0,
  numVoteRing: 50,
  stakeReturnRate: 0.5,
  llmCostPerChallenge: 0.005,
  tokenValue: 0.10,
  enableDiversityPenalty: false, // Turn off simple reciprocity check
  enableQualityMultiplier: true,
  ringVoteDistribution: 0.6
});

sim1.run();

// Analyze with graph detection
const result1 = analyzeCoordination(sim1);

// Test 2: 40% vote distribution (more aggressive evasion)
console.log('\n\n--- TEST 2: More Evasive Ring (40% distribution) ---\n');

const sim2 = new AdaptiveSimulation({
  days: 30,
  numHonest: 50,
  numSpammers: 0,
  numVoteRing: 50,
  stakeReturnRate: 0.5,
  llmCostPerChallenge: 0.005,
  tokenValue: 0.10,
  enableDiversityPenalty: false,
  enableQualityMultiplier: true,
  ringVoteDistribution: 0.4
});

sim2.run();

const result2 = analyzeCoordination(sim2);

// Test 3: 100% vote distribution (obvious coordination)
console.log('\n\n--- TEST 3: Obvious Ring (100% distribution) ---\n');

const sim3 = new AdaptiveSimulation({
  days: 30,
  numHonest: 50,
  numSpammers: 0,
  numVoteRing: 50,
  stakeReturnRate: 0.5,
  llmCostPerChallenge: 0.005,
  tokenValue: 0.10,
  enableDiversityPenalty: false,
  enableQualityMultiplier: true,
  ringVoteDistribution: 1.0
});

sim3.run();

const result3 = analyzeCoordination(sim3);

// Summary
console.log('\n\n=================================================================');
console.log('SUMMARY: Graph Detection Performance');
console.log('=================================================================\n');

console.log('60% Distribution:');
console.log('  Precision:', (result1.stats.precision * 100).toFixed(1) + '%');
console.log('  Recall:', (result1.stats.recall * 100).toFixed(1) + '%');
console.log('  F1 Score:', result1.stats.f1Score.toFixed(3));

console.log('\n40% Distribution:');
console.log('  Precision:', (result2.stats.precision * 100).toFixed(1) + '%');
console.log('  Recall:', (result2.stats.recall * 100).toFixed(1) + '%');
console.log('  F1 Score:', result2.stats.f1Score.toFixed(3));

console.log('\n100% Distribution:');
console.log('  Precision:', (result3.stats.precision * 100).toFixed(1) + '%');
console.log('  Recall:', (result3.stats.recall * 100).toFixed(1) + '%');
console.log('  F1 Score:', result3.stats.f1Score.toFixed(3));

console.log('\n=================================================================');
console.log('VERDICT:');
if (result1.stats.f1Score > 0.8 && result2.stats.f1Score > 0.7) {
  console.log('✅ SUCCESS: Graph detection catches adaptive vote rings');
  console.log('   - Works even when simple reciprocity checks fail');
  console.log('   - Maintains high precision and recall');
} else if (result1.stats.f1Score > 0.6) {
  console.log('⚠️  PARTIAL: Detection works but needs tuning');
  console.log('   - F1 scores indicate room for improvement');
  console.log('   - May need adjusted thresholds or additional signals');
} else {
  console.log('❌ FAILED: Graph detection insufficient');
  console.log('   - Low F1 scores indicate poor detection');
  console.log('   - Need additional detection mechanisms');
}
console.log('=================================================================\n');
