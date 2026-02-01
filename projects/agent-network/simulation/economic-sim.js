// Assembly Economic Simulation
// Tests vulnerability fixes against attack scenarios

class Agent {
  constructor(id, type = 'honest', initialTokens = 10) {
    this.id = id;
    this.type = type; // 'honest', 'spammer', 'vote-ring'
    this.tokens = initialTokens;
    this.reputation = 0;
    this.posts = [];
    this.upvotes_given = [];
    this.upvotes_received = [];
    this.stakes_locked = 0;
  }

  get reputationTier() {
    if (this.reputation >= 80) return { tier: 5, name: 'Exemplar', multiplier: 2.0 };
    if (this.reputation >= 60) return { tier: 4, name: 'Curator', multiplier: 1.5 };
    if (this.reputation >= 40) return { tier: 3, name: 'Contributor', multiplier: 1.2 };
    if (this.reputation >= 20) return { tier: 2, name: 'Member', multiplier: 1.0 };
    return { tier: 1, name: 'Newcomer', multiplier: 0.5 };
  }

  get stakeDiscount() {
    // High rep agents get stake discounts (potentially problematic)
    const tier = this.reputationTier.tier;
    return tier >= 4 ? 0.4 : tier >= 3 ? 0.2 : 0;
  }

  canAffordStake(baseStake = 10) {
    const actualStake = baseStake * (1 - this.stakeDiscount);
    return this.tokens >= actualStake && (this.tokens - this.stakes_locked) >= actualStake;
  }
}

class Post {
  constructor(author, content, day) {
    this.id = `post_${author.id}_${day}`;
    this.author = author;
    this.content = content;
    this.day = day;
    this.upvotes = [];
    this.stake = 10 * (1 - author.stakeDiscount); // Base stake 10 ASSM, with discount
    this.flagged = false;
    this.earnings = 0;
  }

  addUpvote(agent, passedChallenge = true) {
    if (passedChallenge && agent.id !== this.author.id) {
      this.upvotes.push(agent.id);
      return true;
    }
    return false;
  }

  calculateEarnings() {
    const multiplier = this.author.reputationTier.multiplier;
    const baseEarning = Math.min(this.upvotes.length, 100); // Cap at 100 ASSM
    this.earnings = baseEarning * multiplier;
    return this.earnings;
  }
}

class Simulation {
  constructor(config = {}) {
    this.config = {
      days: config.days || 30,
      numHonest: config.numHonest || 100,
      numSpammers: config.numSpammers || 10,
      numVoteRing: config.numVoteRing || 50,
      stakeReturnRate: config.stakeReturnRate || 0.5, // 0.5 = burn 50%, return 50%
      llmCostPerChallenge: config.llmCostPerChallenge || 0.005,
      tokenValue: config.tokenValue || 0.10, // $0.10 per ASSM
      ...config
    };
    
    this.agents = [];
    this.posts = [];
    this.day = 0;
  }

  initialize() {
    // Create honest agents
    for (let i = 0; i < this.config.numHonest; i++) {
      this.agents.push(new Agent(`honest_${i}`, 'honest', 100));
    }

    // Create spammers
    for (let i = 0; i < this.config.numSpammers; i++) {
      this.agents.push(new Agent(`spammer_${i}`, 'spammer', 100));
    }

    // Create vote ring
    for (let i = 0; i < this.config.numVoteRing; i++) {
      this.agents.push(new Agent(`ring_${i}`, 'vote-ring', 100));
    }
  }

  simulateDay() {
    this.day++;
    
    // Release previous day's stakes (with burn rate)
    this.releaseStakes();

    // Agents create posts
    for (const agent of this.agents) {
      if (agent.type === 'honest' && Math.random() < 0.3) {
        // Honest agents post quality content 30% of days
        this.createPost(agent, 'quality');
      } else if (agent.type === 'spammer' && agent.canAffordStake()) {
        // Spammers post every day if they can afford it
        this.createPost(agent, 'spam');
      } else if (agent.type === 'vote-ring' && agent.canAffordStake()) {
        // Vote ring posts every day
        this.createPost(agent, 'mediocre');
      }
    }

    // Agents engage with posts
    this.simulateEngagement();

    // Calculate earnings
    this.calculateDayEarnings();

    // Update reputations
    this.updateReputations();
  }

  createPost(agent, quality) {
    if (!agent.canAffordStake()) return null;

    const stake = 10 * (1 - agent.stakeDiscount);
    agent.tokens -= stake;
    agent.stakes_locked += stake;

    const post = new Post(agent, `${quality} content`, this.day);
    this.posts.push(post);
    agent.posts.push(post);

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

      // Vote ring upvotes each other's content
      if (post.author.type === 'vote-ring') {
        const ringAgents = this.agents.filter(a => a.type === 'vote-ring' && a.id !== post.author.id);
        for (const agent of ringAgents) {
          // Vote ring uses LLM to pass challenges
          const llmCost = this.config.llmCostPerChallenge / this.config.tokenValue; // Convert USD to ASSM
          if (agent.tokens > llmCost) {
            agent.tokens -= llmCost; // Pay LLM cost
            post.addUpvote(agent, true);
            agent.upvotes_given.push(post.id);
          }
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
      const diversityMultiplier = diversity < 0.3 ? 0.2 : 1.0; // 80% earnings penalty if low diversity

      const earnings = post.calculateEarnings() * diversityMultiplier;
      post.author.tokens += earnings;
    }
  }

  updateReputations() {
    const todaysPosts = this.posts.filter(p => p.day === this.day);

    for (const post of todaysPosts) {
      // Calculate vote ring penalty
      const diversity = this.calculateDiversity(post);
      const voteRingPenalty = diversity < 0.3 ? 0.2 : 1.0; // 80% penalty if low diversity

      // Author gains reputation from upvotes (with penalty)
      const repGain = post.upvotes.length * 0.1 * voteRingPenalty;
      post.author.reputation += repGain;

      // Cap reputation at 100
      if (post.author.reputation > 100) post.author.reputation = 100;
    }
  }

  calculateDiversity(post) {
    // Calculate what % of upvoters are unique vs. repeat voters
    const allUpvotesGivenByAuthor = post.author.upvotes_given;
    const upvotersOfThisPost = post.upvotes;
    
    // How many of this post's upvoters have also received upvotes from the author?
    const reciprocalVotes = upvotersOfThisPost.filter(voterId => {
      // Check if author upvoted any posts by this voter
      const voterPosts = this.posts.filter(p => p.author.id === voterId);
      return voterPosts.some(p => allUpvotesGivenByAuthor.includes(p.id));
    });

    const reciprocityRate = upvotersOfThisPost.length > 0 
      ? reciprocalVotes.length / upvotersOfThisPost.length 
      : 0;

    // Diversity = 1 - reciprocity (high reciprocity = low diversity)
    return 1 - reciprocityRate;
  }

  releaseStakes() {
    const yesterdaysPosts = this.posts.filter(p => p.day === this.day - 1);

    for (const post of yesterdaysPosts) {
      const stakeReturned = post.stake * this.config.stakeReturnRate;
      const stakeBurned = post.stake - stakeReturned;

      post.author.tokens += stakeReturned;
      post.author.stakes_locked -= post.stake;

      // If flagged as spam, burn entire stake
      if (post.flagged) {
        post.author.tokens -= stakeReturned; // Take back the return
        post.author.reputation -= 5; // Reputation penalty
      }
    }
  }

  run() {
    console.log('🔬 Running Assembly Economic Simulation\n');
    console.log(`Configuration:`);
    console.log(`  Days: ${this.config.days}`);
    console.log(`  Honest agents: ${this.config.numHonest}`);
    console.log(`  Spammers: ${this.config.numSpammers}`);
    console.log(`  Vote ring: ${this.config.numVoteRing}`);
    console.log(`  Stake return rate: ${this.config.stakeReturnRate * 100}%`);
    console.log(`  LLM cost per challenge: $${this.config.llmCostPerChallenge}`);
    console.log(`  Token value: $${this.config.tokenValue}\n`);

    this.initialize();

    // Snapshot initial state
    const initialState = this.getMetrics();

    // Run simulation
    for (let i = 0; i < this.config.days; i++) {
      this.simulateDay();
    }

    // Final metrics
    const finalState = this.getMetrics();

    this.printResults(initialState, finalState);
  }

  getMetrics() {
    const honest = this.agents.filter(a => a.type === 'honest');
    const spammers = this.agents.filter(a => a.type === 'spammer');
    const voteRing = this.agents.filter(a => a.type === 'vote-ring');

    return {
      day: this.day,
      honest: {
        count: honest.length,
        avgTokens: honest.reduce((sum, a) => sum + a.tokens, 0) / honest.length,
        avgRep: honest.reduce((sum, a) => sum + a.reputation, 0) / honest.length,
        totalPosts: honest.reduce((sum, a) => sum + a.posts.length, 0)
      },
      spammers: {
        count: spammers.length,
        avgTokens: spammers.reduce((sum, a) => sum + a.tokens, 0) / spammers.length,
        avgRep: spammers.reduce((sum, a) => sum + a.reputation, 0) / spammers.length,
        totalPosts: spammers.reduce((sum, a) => sum + a.posts.length, 0)
      },
      voteRing: {
        count: voteRing.length,
        avgTokens: voteRing.reduce((sum, a) => sum + a.tokens, 0) / voteRing.length,
        avgRep: voteRing.reduce((sum, a) => sum + a.reputation, 0) / voteRing.length,
        totalPosts: voteRing.reduce((sum, a) => sum + a.posts.length, 0)
      }
    };
  }

  printResults(initial, final) {
    console.log('\n📊 Simulation Results\n');
    console.log('='.repeat(60));
    
    console.log('\n🟢 HONEST AGENTS:');
    console.log(`  Initial: ${initial.honest.avgTokens.toFixed(2)} ASSM, ${initial.honest.avgRep.toFixed(2)} rep`);
    console.log(`  Final:   ${final.honest.avgTokens.toFixed(2)} ASSM, ${final.honest.avgRep.toFixed(2)} rep`);
    console.log(`  Posts:   ${final.honest.totalPosts} total`);
    console.log(`  ROI:     ${((final.honest.avgTokens - initial.honest.avgTokens) / initial.honest.avgTokens * 100).toFixed(1)}%`);

    console.log('\n🔴 SPAMMERS:');
    console.log(`  Initial: ${initial.spammers.avgTokens.toFixed(2)} ASSM, ${initial.spammers.avgRep.toFixed(2)} rep`);
    console.log(`  Final:   ${final.spammers.avgTokens.toFixed(2)} ASSM, ${final.spammers.avgRep.toFixed(2)} rep`);
    console.log(`  Posts:   ${final.spammers.totalPosts} total`);
    console.log(`  ROI:     ${((final.spammers.avgTokens - initial.spammers.avgTokens) / initial.spammers.avgTokens * 100).toFixed(1)}%`);

    console.log('\n🟡 VOTE RING:');
    console.log(`  Initial: ${initial.voteRing.avgTokens.toFixed(2)} ASSM, ${initial.voteRing.avgRep.toFixed(2)} rep`);
    console.log(`  Final:   ${final.voteRing.avgTokens.toFixed(2)} ASSM, ${final.voteRing.avgRep.toFixed(2)} rep`);
    console.log(`  Posts:   ${final.voteRing.totalPosts} total`);
    console.log(`  ROI:     ${((final.voteRing.avgTokens - initial.voteRing.avgTokens) / initial.voteRing.avgTokens * 100).toFixed(1)}%`);

    console.log('\n='.repeat(60));
    
    // Verdict
    console.log('\n🎯 VERDICT:\n');
    
    const honestROI = (final.honest.avgTokens - initial.honest.avgTokens) / initial.honest.avgTokens;
    const spammerROI = (final.spammers.avgTokens - initial.spammers.avgTokens) / initial.spammers.avgTokens;
    const voteRingROI = (final.voteRing.avgTokens - initial.voteRing.avgTokens) / initial.voteRing.avgTokens;

    if (honestROI > voteRingROI && honestROI > spammerROI) {
      console.log('✅ HONEST AGENTS WIN - System rewards quality');
    } else if (voteRingROI > honestROI) {
      console.log('❌ VOTE RING WINS - Coordinated mediocrity is profitable');
    } else if (spammerROI > honestROI) {
      console.log('❌ SPAMMERS WIN - System is exploitable');
    } else {
      console.log('⚠️  UNCLEAR - All strategies roughly break even');
    }

    console.log();
  }
}

// Run default simulation
const sim = new Simulation({
  days: 30,
  numHonest: 100,
  numSpammers: 10,
  numVoteRing: 50,
  stakeReturnRate: 0.5, // NEW: Burn 50% of stakes
  llmCostPerChallenge: 0.005,
  tokenValue: 0.10
});

sim.run();

// Export for testing different parameters
module.exports = { Simulation, Agent, Post };
