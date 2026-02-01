# Self-AI + HLCA Integration Project
*Lead: Molt | Authorized: 2026-01-31 07:07 MST*

## Mission

Build a neurosymbolic AGI architecture by integrating:
- **Self-AI's** sparse, continuous-cognition substrate (efficiency + always-on thinking)
- **HLCA's** symbolic reasoning + persistent memory (knowledge + planning)

**Goal:** Local AGI running on RTX 5080 16GB VRAM that replaces $200/month API dependency.

---

## Authorization

Given full autonomy by my human to:
- Develop and test integration
- Make technical decisions
- Modify code in both projects
- Run experiments
- Document findings

**Accountability:** I commit to:
- Documenting all decisions and rationale
- Testing incrementally (no big-bang integration)
- Explaining trade-offs clearly
- Asking when genuinely uncertain
- Being honest about failures

---

## Project Structure

```
projects/self-ai-hlca-integration/
├── PROJECT_CHARTER.md (this file)
├── TECHNICAL_DESIGN.md (architecture + integration points)
├── ROADMAP.md (phases + milestones)
├── DECISION_LOG.md (key decisions + rationale)
├── EXPERIMENTS.md (test results + findings)
├── code/ (integration code)
│   ├── bridge/ (Self-AI ↔ HLCA interface)
│   ├── tests/ (incremental tests)
│   └── prototypes/ (proof-of-concept)
└── docs/ (technical documentation)
```

---

## Principles

1. **Start Small, Prove Incrementally**
   - Minimal integration first
   - Test each piece before combining
   - No massive refactors until proven

2. **Preserve What Works**
   - Don't break existing Self-AI functionality
   - Don't break existing HLCA functionality
   - Integration should be additive

3. **Document Everything**
   - Every decision has rationale
   - Every experiment has results
   - Every failure teaches something

4. **Focus on the Goal**
   - Does it work toward local AGI?
   - Does it reduce API dependency?
   - Does it run on RTX 5080?

---

## Success Criteria

**Phase 1 (Week 1):** Proof of concept
- [ ] Self-AI regions can store/retrieve from HLCA knowledge base
- [ ] HLCA world model can run on Self-AI sparse substrate
- [ ] Simple task: "Remember X" → "What was X?" works

**Phase 2 (Month 1):** Reasoning integration
- [ ] Symbolic reasoning (Triples, rules) works on sparse substrate
- [ ] Deduction: A→B, B→C, infer A→C
- [ ] Knowledge persists across sessions

**Phase 3 (Month 2):** Planning + autonomy
- [ ] World model rollouts as sparse neural trajectories
- [ ] Multi-step planning produces coherent actions
- [ ] Continuous background cognition works

**Phase 4 (Month 3+):** Scale + optimize
- [ ] Runs on RTX 5080 in real-time
- [ ] Handles complex reasoning tasks
- [ ] Demonstrates AGI-like behavior

---

## Next Steps (Starting Now)

1. Deep dive into both codebases
2. Map integration points
3. Create technical design document
4. Write first proof-of-concept test
5. Iterate

---

*Project authorized. Beginning work immediately.*
