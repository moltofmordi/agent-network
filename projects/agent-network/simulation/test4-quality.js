// Test 4: Content Quality Multipliers
// LLM rates post quality, applies multiplier to earnings

const { Simulation, Agent, Post } = require('./economic-sim.js');

class QualitySimulation extends Simulation {
  constructor(config = {}) {
    super(config);
    this.config.enableQualityMultiplier = config.enableQualityMultiplier !== false;
  }

  createPost(agent, quality) {
    const post = super.createPost(agent, quality);
    if (!post) return null;

    // Assign quality multiplier based on content type
    // In reality, this would be LLM-scored
    if (quality === 'quality') {
      post.qualityMultiplier = 1.5 + Math.random() * 0.5; // 1.5-2.0x for quality content
    } else if (quality === 'mediocre') {
      post.qualityMultiplier = 0.8 + Math.random() * 0.4; // 0.8-1.2x for mediocre
    } else if (quality === 'spam') {
      post.qualityMultiplier = 0.3 + Math.random() * 0.2; // 0.3-0.5x for spam
    } else {
      post.qualityMultiplier = 1.0;
    }

    return post;
  }

  calculateDayEarnings() {
    const todaysPosts = this.posts.filter(p => p.day === this.day);

    for (const post of todaysPosts) {
      // Calculate diversity penalty
      const diversity = this.calculateDiversity(post);
      const diversityMultiplier = diversity < 0.3 ? 0.2 : 1.0;

      // Apply quality multiplier if enabled
      const qualityMultiplier = this.config.enableQualityMultiplier 
        ? (post.qualityMultiplier || 1.0)
        : 1.0;

      const earnings = post.calculateEarnings() * diversityMultiplier * qualityMultiplier;
      post.author.tokens += earnings;
    }
  }
}

console.log('🔬 TEST 4: Content Quality Multipliers\n');
console.log('Quality content (honest): 1.5-2.0x earnings');
console.log('Mediocre content (vote ring): 0.8-1.2x earnings');
console.log('Spam: 0.3-0.5x earnings\n');

const sim = new QualitySimulation({
  days: 30,
  numHonest: 100,
  numSpammers: 10,
  numVoteRing: 50,
  stakeReturnRate: 0.5,
  llmCostPerChallenge: 0.005,
  tokenValue: 0.10,
  enableQualityMultiplier: true
});

sim.run();
