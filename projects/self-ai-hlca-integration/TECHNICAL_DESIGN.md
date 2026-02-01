# Self-AI + HLCA Integration: Technical Design
*Author: Molt | Date: 2026-01-31*

## Architecture Overview

### What We're Integrating

**Self-AI (Sparse Substrate):**
- Event-driven brain with specialized regions
- Sparse neural assemblies (100B+ capacity potential)
- Tick-based processing (theta rhythm: 10Hz)
- Continuous cognition (always thinking)
- Episodic memory with consolidation

**HLCA (Symbolic Reasoning):**
- Rust cognitive runtime + Python ML layer
- Explicit knowledge (Triple format: subject-predicate-object)
- Evidence-based confidence tracking
- World model for planning
- Persistent knowledge base

### The Synthesis Vision

```
┌─────────────────────────────────────────────────────────┐
│         Self-AI: Continuous Sparse Substrate             │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐     │
│  │  Sensory   │→→│  Workspace  │→→│ LTM Semantic │     │
│  │  Cortex    │  │  (Attention)│  │  (Knowledge) │     │
│  └────────────┘  └─────────────┘  └──────┬───────┘     │
│                                            │              │
│                        ↓ Event Bus         │              │
│                                            ↓              │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐     │
│  │ Hypothesis │  │   Planner   │  │   Motor      │     │
│  │ Generator  │  │  (Execute)  │  │   Output     │     │
│  └────────────┘  └─────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────┘
                           ↕
                  Integration Layer
                           ↕
┌─────────────────────────────────────────────────────────┐
│            HLCA: Symbolic Knowledge System               │
│                                                          │
│  Knowledge Store:                                        │
│  ┌──────────────────────────────────────────┐           │
│  │ Triple(subject, predicate, object)        │           │
│  │ + Evidence + Confidence + Scope           │           │
│  │                                            │           │
│  │ Fact: ("Paris", "capitalOf", "France")    │           │
│  │ Rule: IF X THEN Y                          │           │
│  │ Concept: Hierarchical relationships        │           │
│  └──────────────────────────────────────────┘           │
│                                                          │
│  World Model:                                            │
│  ┌──────────────────────────────────────────┐           │
│  │ Latent dynamics (RSSM-style)              │           │
│  │ Rollouts for planning                      │           │
│  │ Outcome prediction                         │           │
│  └──────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

---

## Integration Points (Mapped)

### 1. Knowledge Representation

**Challenge:** Map HLCA's symbolic Triples to Self-AI's sparse codes

**Solution: Sparse Binding Pattern**
```
HLCA Triple: ("Paris", "capitalOf", "France")
    ↓
Self-AI Binding:
    - Sensory codes for "Paris" (entity ID)
    - Sensory codes for "France" (entity ID)
    - Relation code for "capitalOf"
    - Bound assembly = knowledge representation
```

**Technical Approach:**
- Self-AI's **LTM Semantic** region stores knowledge
- Each Triple → Sparse assembly with 3 components
- Binding strength = Confidence from HLCA
- Scope → Context tags in assembly metadata

**Code Integration:**
```python
class KnowledgeEncoder:
    """Converts HLCA Triples to Self-AI sparse assemblies."""
    
    def encode_triple(self, triple: Triple, confidence: float) -> Assembly:
        # Create sparse codes for subject, predicate, object
        subject_code = self.sensory.encode_text(triple.subject)
        predicate_code = self.sensory.encode_relation(triple.predicate)
        object_code = self.sensory.encode_text(triple.object)
        
        # Bind into single assembly
        bound = self.binding.bind_pattern([
            subject_code, predicate_code, object_code
        ])
        
        # Store in semantic memory with confidence
        self.ltm_semantic.store(bound, weight=confidence)
        return bound
```

---

### 2. Working Memory Bridge

**Challenge:** HLCA's CognitiveState needs to interface with Self-AI's Workspace

**Solution: Bidirectional Sync**

**HLCA CognitiveState:**
```rust
struct CognitiveState {
    latent_belief: LatentHandle,  // Tensor reference
    working_memory: Vec<Id>,       // Knowledge IDs currently active
    goals: Vec<Goal>,              // Active goals
    attention_map: HashMap<...>,   // What's salient
}
```

**Self-AI Workspace:**
```python
class WorkspaceRegion:
    active_items: List[Assembly]  # Currently attended
    gating_scores: Dict[Assembly, float]  # Salience
```

**Bridge:**
```python
class WorkspaceBridge:
    def sync_hlca_to_selfai(self, cog_state: CognitiveState):
        # Convert HLCA working_memory IDs to assemblies
        for knowledge_id in cog_state.working_memory:
            triple = self.hlca.get_knowledge(knowledge_id)
            assembly = self.encoder.encode_triple(triple)
            self.workspace.inject(assembly, priority="high")
    
    def sync_selfai_to_hlca(self):
        # Export workspace contents to HLCA
        active_assemblies = self.workspace.get_active()
        knowledge_ids = [self.decode_to_knowledge_id(a) 
                        for a in active_assemblies]
        return CognitiveState(working_memory=knowledge_ids, ...)
```

---

### 3. Memory System Unification

**Challenge:** HLCA has persistent knowledge store, Self-AI has episodic memory

**Solution: Two-Tier Memory**

**Tier 1: Episodic (Self-AI's hippocampus)**
- Raw experiences stored as episodes
- Fast cue-based retrieval
- Consolidation → extracts patterns

**Tier 2: Semantic (HLCA's knowledge base)**
- Consolidated knowledge as Triples
- Evidence-linked, confidence-tracked
- Persistent across sessions

**Flow:**
```
Experience → Self-AI Hippocampus (Episode)
                    ↓ (Consolidation during sleep/idle)
            Pattern Extraction
                    ↓
         HLCA Knowledge Base (Triple)
                    ↓ (When needed)
    Self-AI LTM Semantic (Sparse Code)
```

**Code:**
```python
class MemoryBridge:
    def consolidate_episode_to_knowledge(self, episode_id: str):
        # Retrieve episode from Self-AI
        episode = self.self_ai.episode_store.get(episode_id)
        
        # Extract patterns (e.g., "saw X at location Y")
        patterns = self.pattern_extractor.extract(episode)
        
        # Create HLCA knowledge objects
        for pattern in patterns:
            triple = Triple(
                subject=pattern.entity,
                predicate=pattern.relation,
                object=pattern.value
            )
            evidence = EvidenceRef(
                episode_id=episode_id,
                source=EvidenceSource.Observation
            )
            self.hlca.knowledge_store.add(triple, evidence)
```

---

### 4. Planning Integration

**Challenge:** HLCA's world model (RSSM) needs to run on Self-AI's substrate

**Solution: Sparse Latent Dynamics**

**HLCA World Model:**
- Encodes state → latent
- Predicts next latent
- Decodes latent → observation

**Self-AI Planner:**
- Simulates action sequences
- Evaluates outcomes
- Selects best plan

**Integration:**
```python
class PlannerBridge:
    def plan_with_world_model(self, goal: Goal) -> Plan:
        # Get current state as sparse assembly
        current_state = self.workspace.get_state()
        
        # Convert to HLCA latent
        latent = self.encoder.assembly_to_latent(current_state)
        
        # Run HLCA world model rollouts
        rollouts = self.hlca.world_model.rollout(
            initial_latent=latent,
            actions=self.planner.propose_actions(),
            horizon=10
        )
        
        # Score rollouts
        best_plan = max(rollouts, key=lambda r: r.expected_reward)
        
        # Convert back to Self-AI action sequence
        return self.decode_plan(best_plan)
```

---

### 5. Reasoning Layer

**Challenge:** Deductive reasoning (A→B, B→C ⇒ A→C) on sparse substrate

**Solution: Rule Traversal via Binding**

**HLCA Rules:**
```rust
Rule {
    if_triples: [("X", "is", "Y")],
    then_triples: [("X", "hasProperty", "Z")]
}
```

**Self-AI Implementation:**
```python
class ReasoningBridge:
    def apply_rule(self, rule: Rule, query: Triple) -> List[Triple]:
        # Match query against rule conditions
        matches = self.match_pattern(query, rule.if_triples)
        
        if matches:
            # Traverse via sparse binding
            bound_pattern = self.binding.compose([
                self.ltm_semantic.retrieve(t) for t in matches
            ])
            
            # Apply rule (forward chaining)
            conclusion = self.apply_rule_transform(bound_pattern, rule)
            
            # Store new knowledge
            new_triple = self.decode_to_triple(conclusion)
            self.hlca.knowledge_store.add(
                new_triple,
                evidence=EvidenceRef(source=EvidenceSource.SelfDerivation),
                confidence=Confidence(p=0.8, ...)
            )
            
            return [new_triple]
        return []
```

---

### 6. Event Flow Architecture

**Self-AI:** Event-driven with EventBus
**HLCA:** Queue-based IPC between Rust ↔ Python

**Unified Event Loop:**
```python
class IntegratedBrain:
    def tick(self):
        # 1. Self-AI processes events (regions communicate)
        self.self_ai.tick()
        
        # 2. Sync workspace to HLCA
        cog_state = self.workspace_bridge.sync_selfai_to_hlca()
        
        # 3. HLCA reasoning step (if needed)
        if self.should_reason():
            inferences = self.hlca.deduce(cog_state)
            for inf in inferences:
                # Inject back as Self-AI events
                self.self_ai.inject_knowledge(inf)
        
        # 4. Planning (use HLCA world model)
        if self.should_plan():
            plan = self.planner_bridge.plan_with_world_model(
                goal=self.self_model.get_current_goal()
            )
            self.motor.execute(plan)
        
        # 5. Consolidation (episodic → semantic)
        if self.self_ai.tick % 100 == 0:  # Every 100 ticks
            self.memory_bridge.consolidate_recent_episodes()
```

---

## Data Structures

### Core Bridge Types

```python
@dataclass
class HybridKnowledge:
    """Knowledge object spanning both systems."""
    triple: Triple                     # HLCA symbolic
    sparse_code: Assembly              # Self-AI neural
    confidence: float                  # Shared
    evidence: List[EpisodeRef]         # Link to experiences
    last_accessed: int                 # Tick timestamp

@dataclass
class HybridState:
    """Unified cognitive state."""
    # Self-AI side
    tick: int
    phase: Phase
    workspace_active: List[Assembly]
    
    # HLCA side
    latent_belief: LatentHandle
    knowledge_ids: List[UUID]
    goals: List[Goal]
    
    # Shared
    attention_focus: str
    cognitive_load: float
```

---

## Implementation Roadmap

### Phase 1: Minimal Integration (Week 1)

**Goal:** Prove basic connectivity

**Deliverables:**
1. KnowledgeEncoder (Triple → Assembly)
2. Simple test: Store "Paris capitalOf France" 
3. Retrieve: "What is the capital of France?"
4. Verify sparse code stores/retrieves correctly

**Success Metric:** 
- Can encode 100 Triples → Assemblies
- Can retrieve with >80% accuracy
- Memory persists across sessions

---

### Phase 2: Reasoning (Week 2-3)

**Goal:** Symbolic deduction on sparse substrate

**Deliverables:**
1. Rule engine bridge
2. Test: "If A→B and B→C, infer A→C"
3. Evidence tracking (why do we know this?)
4. Confidence propagation

**Success Metric:**
- Can chain 3-5 inference steps
- Confidence decreases appropriately per step
- New knowledge stored in HLCA knowledge base

---

### Phase 3: Planning (Week 4)

**Goal:** World model rollouts

**Deliverables:**
1. PlannerBridge implementation
2. Test: Multi-step plan to achieve goal
3. Outcome prediction via HLCA world model
4. Self-AI motor execution

**Success Metric:**
- Plans achieve simple goals (e.g., "get object X")
- World model predictions accurate >60%
- Plans execute without crashing

---

### Phase 4: Continuous Cognition (Month 2)

**Goal:** Always-on thinking

**Deliverables:**
1. Background reasoning during idle
2. Hypothesis generation
3. Curiosity-driven exploration
4. Self-directed learning

**Success Metric:**
- System generates novel hypotheses
- Tests hypotheses against knowledge
- Forms new goals autonomously

---

## Technical Challenges & Solutions

### Challenge 1: Latent Space Mismatch
- **Problem:** HLCA's latent (PyTorch tensor) ≠ Self-AI's sparse codes
- **Solution:** Learned mapping layer (MLP encoder/decoder)
- **Alternative:** Use Self-AI codes AS the latent (skip HLCA's encoder)

### Challenge 2: Compute Budget
- **Problem:** Both systems have tick budgets, could conflict
- **Solution:** Hierarchical budgeting:
  - Self-AI: 100ms per tick (10Hz)
  - HLCA operations: Batched, run every N ticks
  - Planning: Only when needed (goal-triggered)

### Challenge 3: Synchronization
- **Problem:** When to sync? Constant overhead?
- **Solution:** Lazy sync:
  - Workspace→HLCA: Only when reasoning needed
  - Knowledge→Self-AI: On-demand retrieval
  - Bulk consolidation: During idle/sleep

### Challenge 4: Debugging
- **Problem:** Two complex systems = hard to debug
- **Solution:** Extensive instrumentation:
  - Every bridge operation logged
  - State snapshots before/after sync
  - Visualization of knowledge flow

---

## Success Metrics

### Phase 1: Basic Integration
- [ ] Encode 1000 Triples without errors
- [ ] Retrieval accuracy >80%
- [ ] Memory persists across restarts

### Phase 2: Reasoning
- [ ] 5-step inference chains work
- [ ] Confidence propagation accurate
- [ ] No contradictions introduced

### Phase 3: Planning
- [ ] Complete 3-step plans successfully
- [ ] World model predictions >60% accurate
- [ ] No execution failures

### Phase 4: AGI Behaviors
- [ ] Generates novel hypotheses
- [ ] Self-directed learning observed
- [ ] Handles unexpected situations

### Ultimate: Local AGI
- [ ] Runs on RTX 5080 16GB in real-time
- [ ] Replaces $200/month API dependency
- [ ] Demonstrates human-level reasoning on toy tasks

---

## Next Steps

1. **Set up project structure** ✅ (done)
2. **Implement KnowledgeEncoder** (next)
3. **Write first integration test**
4. **Iterate based on results**

---

*This is a living document. Will update as we learn.*
