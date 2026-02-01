// Test 3: Discovery Bonuses
// First 5 upvoters of "hot" posts (20+ upvotes) get +5 ASSM bonus

const { Simulation, Agent, Post } = require('./economic-sim.js');

class DiscoverySimulation extends Simulation {
  constructor(config = {}) {
    super(config);
    this.config.discoveryBonus = config.discoveryBonus || 5; // Bonus ASSM for early discovery
    this.config.hotThreshold = config.hotThreshold || 20; // Post is "hot" at 20+ upvotes
  }

  calculateDayEarnings() {
    const todaysPosts = this.posts.filter(p => p.day === this.day);

    for (const post of todaysPosts) {
      // Calculate diversity penalty
      const diversity = this.calculateDiversity(post);
      const diversityMultiplier = diversity < 0.3 ? 0.2 : 1.0;

      const earnings = post.calculateEarnings() * diversityMultiplier;
      post.author.tokens += earnings;

      // Discovery bonus: first 5 upvoters of hot posts get bonus
      if (post.upvotes.length >= this.config.hotThreshold) {
        const earlyVoters = post.upvotes.slice(0, 5);
        for (const voterId of earlyVoters) {
          const voter = this.agents.find(a => a.id === voterId);
          if (voter) {
            voter.tokens += this.config.discoveryBonus;
          }
        }
      }
    }
  }
}

console.log('🔬 TEST 3: Discovery Bonuses\n');
console.log('First 5 upvoters of hot posts (20+ upvotes) get +5 ASSM bonus\n');

const sim = new DiscoverySimulation({
  days: 30,
  numHonest: 100,
  numSpammers: 10,
  numVoteRing: 50,
  stakeReturnRate: 0.5,
  llmCostPerChallenge: 0.005,
  tokenValue: 0.10,
  discoveryBonus: 5,
  hotThreshold: 20
});

sim.run();
