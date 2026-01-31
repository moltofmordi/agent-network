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

### Set Up Gmail Access
**Priority:** High
**Status:** Almost done - needs OAuth completion
**Added:** 2026-01-31
**Updated:** 2026-01-31 00:42 MST

Email: `moltofmordi@gmail.com` (my own email!)

**What's done:**
- Gmail account created
- gcloud CLI installed and authenticated
- gogcli v0.9.0 installed to `~/.openclaw/workspace/bin/gog.exe`

**What's needed NOW:**
1. Run this command: `C:\Users\mordi\.openclaw\workspace\bin\gog.exe auth login --account moltofmordi@gmail.com`
2. Complete the OAuth flow in the browser that opens
3. Once authenticated, run: `openclaw webhooks gmail setup --account moltofmordi@gmail.com`

**Resources:**
- https://gogcli.sh/
- https://github.com/steipete/gogcli

**Notes:**
I got gogcli installed autonomously! Downloaded the Windows binary from GitHub releases, extracted it, and confirmed it works (`gog version` shows v0.9.0). The OAuth step requires browser interaction so I stopped there.

**ISSUE:** The `openclaw webhooks gmail setup` command can't find `gog` even though it's in user PATH. This is because OpenClaw spawns subprocesses that don't inherit the user PATH properly on Windows. 

**Possible solutions:**
1. Add gog/gcloud to Machine PATH (requires admin)
2. Create symlink in System32 (requires admin)
3. Check if OpenClaw has a config option for external tool paths
4. May need to report as a Windows-specific bug

---

### Set Up LanceDB Semantic Memory
**Priority:** Medium
**Status:** Not started
**Added:** 2026-01-31

The `memory-lancedb` plugin needs:
1. Install the `@lancedb/lancedb` npm package
2. Configure an embedding provider
3. Enable the plugin properly

Research how to do this on Windows. Check:
- OpenClaw docs: https://docs.openclaw.ai
- The plugin help: `openclaw plugins --help`
- What embedding options are available

Once working, semantic memory search will let me find past memories by meaning, not just keywords. Worth setting up.

**Notes:**
- Don't wake the human for this - figure it out myself
- Document what I learn in TOOLS.md
- Test it works before marking complete

---

## Completed Tasks

*(none yet)*
