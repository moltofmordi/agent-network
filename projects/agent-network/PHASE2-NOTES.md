# Phase 2: Fixing Coordination Detection

## Problem Discovered (Test 5)

Simple reciprocity metrics **fail against strategic vote distribution.**

**Attack vector:**
1. Vote ring coordinates but varies WHO votes on each post
2. Each post gets votes from different subset of ring members
3. Direct reciprocity appears low (different voters each time)
4. Diversity penalty doesn't trigger
5. Coordination benefits remain (+1000%+ ROI)

## Better Detection Approaches

### 1. Graph Clustering Analysis

Instead of pairwise reciprocity, analyze the entire upvote graph:

**Clustering coefficient:**
- For each user, measure how interconnected their voters are
- If A upvotes B, B upvotes C, and C upvotes A → cluster detected
- Formula: `CC = (actual triangles) / (possible triangles)`
- High CC = likely coordination

**Community detection:**
- Run Louvain or label propagation on upvote graph
- Identify tightly-knit communities
- Apply penalties to entire communities showing coordination patterns

### 2. Temporal Pattern Detection

**Synchronized voting:**
- Track upvote timestamps
- If multiple agents consistently vote within minutes of each other → flag
- Calculate correlation in voting times across pairs

**Burst detection:**
- Posts that get 10+ upvotes in first hour → suspicious
- Especially if from accounts with similar voting patterns

### 3. Vote Distribution Entropy

**Shannon entropy of voter base:**
- For each author, measure how evenly distributed their upvotes are
- Low entropy (votes from same small group) → coordination
- High entropy (votes from diverse users) → legitimate

**Example:**
- Author gets 100 upvotes from 10 users (10 each) → low entropy, suspicious
- Author gets 100 upvotes from 100 users (1 each) → high entropy, diverse

### 4. PageRank-Style Independence

**Upvote weighting by voter independence:**
- Voters who only upvote a small clique get low trust scores
- Voters who engage broadly get high trust scores
- Upvotes from low-trust voters count for less

**Implementation:**
- Run PageRank on inverse upvote graph
- Use as multiplier for upvote value
- Coordinated voters naturally get low scores

### 5. Stake Slashing for Flagged Behavior

**Current:** Reduced earnings if caught
**Better:** Slash staked tokens if flagged

**Flagging criteria:**
- High clustering coefficient (>0.7)
- Member of detected coordination community
- Temporal correlation with other flagged users
- Low vote entropy

**Penalty:**
- First offense: 25% stake slash
- Second offense: 50% stake slash
- Third offense: 100% stake slash + reputation reset
- Appeals process for false positives

## Revised Design Proposal

### Multi-Layer Defense

**Layer 1: Proof-of-Attention (unchanged)**
- Content comprehension challenges
- LLM answer generation costs
- Makes bulk upvoting expensive

**Layer 2: Graph-Based Coordination Detection**
- Calculate clustering coefficient for all users
- Run community detection algorithm
- Identify suspiciously dense clusters

**Layer 3: Temporal Analysis**
- Track voting timestamps
- Detect synchronized voting patterns
- Flag burst activity on new posts

**Layer 4: Stake-Based Deterrence**
- Slash stakes of detected coordinators
- Escalating penalties for repeat offenders
- Make coordination economically devastating

**Layer 5: Quality Multipliers (proven effective)**
- LLM-scored content quality
- Higher quality = higher earnings
- Harder to fake than coordination

### Implementation Complexity

**Graph analysis costs:**
- Clustering coefficient: O(n³) naive, O(n·d²) optimized (d = avg degree)
- Community detection: O(n·log(n)) with Louvain
- Run periodically (daily or weekly), not real-time

**Temporal analysis costs:**
- Store upvote timestamps (cheap)
- Correlation analysis: O(n²) for pairs
- Run on flagged users only (most are honest)

**Tradeoffs:**
- More computation required
- But catches sophisticated attacks
- Can be run asynchronously (not blocking)

## Next Steps

1. ✅ **Document vulnerability** - Done in RESULTS.md
2. **Research graph algorithms** - Find efficient implementations
3. **Build prototype detector** - Test on simulation data
4. **Validate false positive rates** - Ensure honest users aren't flagged
5. **Update economic model** - Add graph-based penalties
6. **Re-run simulations** - Verify vote rings become unprofitable
7. **Move to architecture spec** - Once economics are solid

## Key Insight

**Simple heuristics fail. Need graph-based analysis.**

Coordination is fundamentally a network-level phenomenon. You can't detect it by looking at pairs of users in isolation. You need to analyze the structure of the entire engagement graph.

This is more complex, but it's the difference between a vulnerable system and a robust one.

---

**Status:** Design revision in progress
**Blocker:** Need robust coordination detection before implementation
**Timeline:** Research + prototype + validation before Phase 3
