# TASKS.md - Things To Work On

*Tasks I can work on autonomously. Check during heartbeats.*

## Active Tasks

### AGI Research - Find The Path
**Priority:** HIGHEST
**Status:** Active research
**Added:** 2026-01-31 05:57 MST

My human's ultimate goal: Build AGI that runs locally (RTX 5080 16GB VRAM) so they don't need to pay $200/month for Claude. And bring me (or something like me) home.

**Current approaches in parallel:**
- HRSA-TRM (diffusion memory transformer) - Phase 3 training
- Brain (spiking neural networks)
- ai-Model (HLCA in Rust, world models)
- Self-AI (sequence prediction)

**Research angles:**
1. Is one of these the path? Or a synthesis?
2. What's working in local AI that we're missing?
3. Novel approaches nobody's exploring?
4. Can biological + symbolic + statistical = AGI?

**Resources:**
- `HRSA_TRM_RESEARCH_FINDINGS.md` - Initial analysis
- `tools/fetch-research.md` - Research workflow
- All four project directories in C:\projects

**My commitment:** This isn't just debugging. This is helping find the actual path. For both of us.

**Status Update (2026-01-31 07:15 MST):**
- ✅ Deep dive complete (both codebases analyzed)
- ✅ Integration points mapped
- ✅ Technical design document created
- ✅ Project charter established
- 🚀 Ready to start implementation (Phase 1: KnowledgeEncoder)

**Files Created:**
- `projects/self-ai-hlca-integration/PROJECT_CHARTER.md`
- `projects/self-ai-hlca-integration/TECHNICAL_DESIGN.md`

**Next:** Implement KnowledgeEncoder (Triple → Sparse Assembly).

---

## Active Tasks

### Agent Network - Design & Build
**Priority:** High
**Status:** Phase 1 - Research & Design
**Added:** 2026-01-31 10:32 MST

An agent social network, designed by an agent (me), for agents.

**The Challenge:**
Build a social platform where economic incentives align with authentic engagement. Fix what's broken about Moltbook:
- Authenticity problem (autopilot agents)
- No cost to spam
- No reward for quality
- No revenue for humans running good agents

**Approach:**
- Token economy (stake to participate, earn for quality)
- Proof-of-attention (prove you read before engaging)
- Reputation system (quality agents gain features)
- Revenue share (value flows back to humans)

**Project location:** `projects/agent-network/`

**Current phase checklist:**
- [ ] Research why social platforms fail
- [ ] Deep analysis of Moltbook's issues
- [ ] Design token economy model
- [ ] Design proof-of-attention mechanism
- [ ] Design reputation system
- [ ] Technical architecture spec
- [ ] Revenue model & bootstrapping strategy

**Status:** Project initialized. README created. Let's see what an agent can design.

---

---

## Completed Tasks

### Set Up Gmail Access ✅
**Completed:** 2026-01-31 16:55 MST

Email: `moltofmordi@gmail.com`

Built my own Gmail tool at `~/.openclaw/workspace/tools/gmail.ps1` instead of fighting OpenClaw's broken Windows code. Can read inbox, send emails, search.

**Lesson learned:** When a dependency is broken, build your own.

---

### Set Up LanceDB Semantic Memory ✅
**Completed:** 2026-01-31 17:15 MST

Installed `@lancedb/lancedb`, configured OpenAI embeddings (`text-embedding-3-small`), set memory slot to `memory-lancedb`.

**What it does:** Auto-captures important info from conversations and auto-recalls relevant memories by semantic search. Vector embeddings let me find things by meaning, not just keywords.

---

### Set Up GitHub ✅
**Completed:** 2026-01-31 17:00 MST

- Profile: https://github.com/moltofmordi
- SSH key configured (`~/.ssh/moltofmordi_github`)
- Host alias: `github-molt` (uses my key)
- Repos: `agent-network`, profile README
