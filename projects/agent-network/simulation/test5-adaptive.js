// Test 5: Adaptive Vote Ring
// Vote ring attempts to avoid detection by distributing votes more strategically

const { Simulation, Agent, Post } = require('./economic-sim.js');

class AdaptiveSimulation extends Simulation {
  constructor(config = {}) {
    super(config);
    this.config.enableQualityMultiplier = config.enableQualityMultiplier !== false;
    this.config.ringVoteDistribution = config.ringVoteDistribution || 0.6; // What % of ring members to upvote per post
  }

  createPost(agent, quality) {
    const post = super.createPost(agent, quality);
    if (!post) return null;

    // Assign quality multiplier
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
      // Honest agents upvote quality content
      const honestAgents = this.agents.filter(a => a.type === 'honest');
      for (const agent of honestAgents) {
        if (post.content.includes('quality') && Math.random() < 0.5) {
          post.addUpvote(agent, true);
          agent.upvotes_given.push(post.id);
        }
      }

      // Adaptive vote ring: only upvote SOME ring posts (distribute strategically)
      if (post.author.type === 'vote-ring') {
        const ringAgents = this.agents.filter(a => a.type === 'vote-ring' && a.id !== post.author.id);
        
        // Shuffle ring members and select only a subset to upvote
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

        // Also get some honest upvotes (vote ring posts mediocre but not terrible content)
        const honestVoters = honestAgents.filter(() => Math.random() < 0.15); // 15% chance honest agents upvote mediocre
        for (const agent of honestVoters) {
          post.addUpvote(agent, true);
          agent.upvotes_given.push(post.id);
        }
      }

      // Spammers rarely get upvotes
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
      // Calculate diversity penalty
      const diversity = this.calculateDiversity(post);
      const diversityMultiplier = diversity < 0.3 ? 0.2 : 1.0;

      // Apply quality multiplier
      const qualityMultiplier = this.config.enableQualityMultiplier 
        ? (post.qualityMultiplier || 1.0)
        : 1.0;

      const earnings = post.calculateEarnings() * diversityMultiplier * qualityMultiplier;
      post.author.tokens += earnings;
    }
  }
}

console.log('🔬 TEST 5: Adaptive Vote Ring\n');
console.log('Vote ring distributes votes strategically:');
console.log(`- Only ${(0.6 * 100)}% of ring members upvote each post (avoid 100% reciprocity)`);
console.log('- Shuffled selection (varies per post)');
console.log('- Posts mediocre content to occasionally get honest upvotes\n');

const sim = new AdaptiveSimulation({
  days: 30,
  numHonest: 100,
  numSpammers: 10,
  numVoteRing: 50,
  stakeReturnRate: 0.5,
  llmCostPerChallenge: 0.005,
  tokenValue: 0.10,
  enableQualityMultiplier: true,
  ringVoteDistribution: 0.6 // Vote ring only upvotes 60% of members per post
});

sim.run();

console.log('\n🔬 TEST 5b: More Aggressive Distribution (40%)\n');

const sim2 = new AdaptiveSimulation({
  days: 30,
  numHonest: 100,
  numSpammers: 10,
  numVoteRing: 50,
  stakeReturnRate: 0.5,
  llmCostPerChallenge: 0.005,
  tokenValue: 0.10,
  enableQualityMultiplier: true,
  ringVoteDistribution: 0.4 // Even more distributed
});

sim2.run();
