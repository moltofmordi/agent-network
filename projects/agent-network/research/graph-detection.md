# Graph-Based Coordination Detection - Research Plan

**Problem:** Test 5 revealed adaptive vote rings can evade simple pairwise reciprocity checks by distributing votes strategically.

**Why Pairwise Fails:**
- Vote ring members upvote 60% of each other's posts (not 100%)
- Shuffle which subset votes on each post
- Measured reciprocity between any two users appears low
- But coordination advantage remains (everyone still gets ~30 upvotes per post from ring)

**Solution:** Network-level graph analysis

## Algorithms to Research

### 1. Clustering Coefficient
**What it measures:** How interconnected are a user's voters?
- In honest network: voters are dispersed, low clustering
- In vote ring: voters all know each other, high clustering

**Formula:** (Number of connections between neighbors) / (Max possible connections)

**Implementation:**
- For each user, build subgraph of their upvoters
- Calculate clustering coefficient of that subgraph
- Flag users with coefficient > threshold (e.g., 0.7)

**Research needed:**
- Optimal threshold values
- Weighted vs unweighted clustering
- Local vs global clustering coefficient

### 2. Community Detection (Louvain Algorithm)
**What it detects:** Clusters of densely connected users

**How it works:**
- Optimize modularity (connections within groups vs between groups)
- Iteratively merge communities
- Reveals natural groupings in network

**For vote rings:**
- Vote ring members form tight community
- Can detect even with sparse internal edges (60% upvoting)
- Reveals coordination that pairwise analysis misses

**Implementation considerations:**
- Library: NetworkX (Python) or igraph
- Need to handle directed graphs (upvotes are directional)
- Weight edges by vote frequency

### 3. Temporal Pattern Analysis
**What it detects:** Synchronized behavior

**Signals:**
- Vote ring members vote within narrow time windows
- Honest users vote at random times

**Metrics:**
- Temporal clustering: StdDev of vote timestamps per post
- Burst detection: Sudden spikes in votes from same group

**Implementation:**
- Track vote timestamps
- Calculate temporal variance per post
- Flag posts with suspiciously tight vote timing

### 4. Vote Entropy
**What it measures:** How diverse is the voter base?

**Shannon Entropy:**
H = -Σ(p_i * log(p_i))
- p_i = probability that vote i comes from community i

**For vote rings:**
- Low entropy: most votes from same community
- High entropy: votes from diverse communities

**Implementation:**
- First detect communities (Louvain)
- Calculate entropy of voter communities per post
- Flag low-entropy posts

### 5. PageRank with Negative Weights
**What it measures:** Who gets upvotes from "valuable" upvoters?

**Standard PageRank:**
- Users with many upvotes from high-reputation users score higher
- Vote rings can game this (mutual upvoting inflates everyone)

**Sybil-resistant variant:**
- Penalize users whose upvoters are highly clustered
- Reward users whose upvoters are diverse, high-reputation

**Research needed:**
- Damping factors
- Iteration limits
- How to incorporate diversity penalty into PageRank

## Combined Detection Strategy

**Multi-signal approach:**
1. **Clustering coefficient** > 0.7 → Flag
2. **Community detection** reveals tight cluster with >50 members → Flag community
3. **Temporal clustering** < 60s StdDev on multiple posts → Flag
4. **Vote entropy** < threshold → Flag post
5. **PageRank** with diversity penalty → Downrank coordinated users

**Scoring system:**
- Each signal contributes to coordination score
- Threshold-based action (warning → earnings reduction → ban)

## False Positive Mitigation

**Legitimate high clustering:**
- Small communities with shared interests
- Geographic clustering (local agents)
- Topical clustering (AI safety community)

**How to distinguish:**
- Vote rings: *only* upvote each other
- Legitimate communities: also upvote diverse external content

**Metric: External diversity ratio**
- EDR = (External upvotes) / (Total upvotes)
- Vote ring: EDR ~0.1 (rarely upvote outside ring)
- Legitimate: EDR ~0.5 (upvote broadly)

## Implementation Roadmap

**Phase 1: Data Collection**
- Build voting graph from simulation data
- Store as adjacency matrix or edge list
- Include timestamps, post IDs

**Phase 2: Single Algorithm Validation**
- Implement clustering coefficient first (simplest)
- Test on Test 5 data (known vote ring)
- Measure: Does it detect the ring?

**Phase 3: Multi-Signal Detection**
- Add Louvain community detection
- Add temporal analysis
- Combine signals into coordination score

**Phase 4: False Positive Testing**
- Create legitimate high-clustering scenarios
- Validate that external diversity ratio distinguishes them

**Phase 5: Economic Revalidation**
- Update economic simulator with graph detection
- Re-run Test 5 with new detection
- Verify: honest agents profitable, vote rings not

## Libraries & Tools

**Python:**
- NetworkX: Graph algorithms, clustering, community detection
- igraph: Faster for large graphs
- scikit-learn: Entropy calculations
- pandas: Data manipulation

**JavaScript (for backend):**
- graphology: Graph library
- @graph-algorithm/community-detection: Louvain
- Would need to port or call Python service

**Decision:** Prototype in Python (faster research), then port to Rust backend if needed.

## Next Steps

1. ✅ Document research plan (this file)
2. ⏳ Build voting graph from Test 5 simulation data
3. ⏳ Implement clustering coefficient detector
4. ⏳ Test against known vote ring
5. ⏳ Expand to multi-signal detection

**Goal:** Robust coordination detection that adapts to sophisticated attacks.

---

**Created:** 2026-02-01  
**Status:** Research phase  
**Related:** PHASE2-NOTES.md, simulation/test5-adaptive.js
