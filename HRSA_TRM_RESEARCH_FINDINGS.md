# HRSA-TRM Research & Diagnostic Report
*Compiled by Molt - 2026-01-31 05:45 MST*

## Executive Summary

**Core Question:** Is diffusion-based compression for transformers a viable approach?

**Short Answer:** The architectural ideas are sound, but training dynamics reveal a fundamental **credit assignment problem** - the model learns to do LM without using memory.

---

## What You've Built (Impressive!)

### Novel Architecture Components

1. **Diffusion for Compression** (Not Generation)
   - Using diffusion to iteratively refine 32k→2k memory slots
   - TRM recursion (Z/Y latents) inside each denoise step
   - **This is genuinely novel** - I haven't seen this exact approach elsewhere
   
2. **Hierarchical Memory Cascade**
   - M0 (256): Global structure
   - M1 (1024): Mid-level patterns  
   - M2 (2048): Fine details
   - Prevents collapse, enables scale-appropriate routing

3. **O(N) Local Attention**
   - Chunked attention with halo for true linear scaling
   - Critical for 32k context promise

4. **Mixed Training Objective**
   - 80% LM / 20% Retrieval
   - Curriculum from easy→target→hard
   - Guardrails for collapse detection

### What's Working

✅ **LM loss decreasing nicely** (232→2.2, ppl 124k→9.38)
✅ **Memory diversity improving** (sim_gap 0.007→0.87)
✅ **Training stability** (gradients stable, no explosions)
✅ **Memory efficient** (20M params, ~0.73 steps/s on RTX 5080)

---

## The Core Problem: Memory Bypass

### Symptoms from Training Logs

❌ **Retrieval EM stuck at 0-4.5%** - Model can't retrieve from memory
❌ **delta_zero ≈ 1.2-2.4** - Memory provides little benefit (1.0 = no benefit)
❌ **Adversarial EM always 0%** - No robustness to hard cases

### Root Cause: Credit Assignment

The model found an easier path:

```
EXPECTED:  Input → Ingest → Memory → Decoder (uses memory) → Output
ACTUAL:    Input → Ingest → Memory → Decoder (ignores memory) → Output
                                              ↑
                                         Uses only its own
                                         causal context
```

**Why this happens:**
1. Autoregressive decoder has strong local context (512 tokens)
2. Cross-attention to memory is *optional* - model can bypass it
3. Gradient flows more directly through self-attention than cross-attention
4. Memory retrieval requires learning complex routing - local context is "free"

This is the **perennial problem with memory-augmented architectures**.

---

## Are You Going In The Right Direction?

### ✅ The Good News

**Architecturally:** Your ideas are sound and potentially publishable:
- Diffusion for compression is underexplored
- TRM recursion in denoising is clever
- Hierarchical memory makes sense

**Technically:** Your implementation is solid:
- Proper O(N) attention
- Careful quantization plan
- Good debugging/logging infrastructure
- Systematic phase progression

### ⚠️ The Challenge

**Training dynamics:** Getting the model to *use* memory is the hard part.

This isn't unique to your approach - it's a fundamental challenge in:
- Memory-augmented neural networks (MANN)
- Retrieval-augmented generation (RAG)
- External memory transformers

**Historical parallel:** LSTM with memory cells had the same issue - models would ignore the cell state and rely on hidden state. Solution required:
- Careful initialization
- Specialized loss functions
- Sometimes architectural constraints (forcing attention)

---

## Research-Backed Solutions

### Short-term: Force Memory Usage

1. **Bottleneck the decoder context**
   ```python
   # Instead of ctx=512, try ctx=64 or even ctx=32
   # Force model to rely on memory for long-range info
   ```

2. **Gradient routing**
   ```python
   # Detach decoder self-attention gradients periodically
   # Forces learning to flow through cross-attention to memory
   ```

3. **Supervised attention**
   ```python
   # Add loss: decoder should attend to memory slots 
   # containing the answer (computable in retrieval task)
   ```

4. **Ablation during training**
   ```python
   # Randomly drop decoder context (keep only last 16 tokens)
   # Model HAS to use memory on those examples
   ```

### Medium-term: Architectural Changes

1. **Make memory non-optional**
   - Fuse memory directly into decoder hidden state
   - No separate cross-attention - memory IS the context

2. **Add memory prediction loss**
   - Decoder predicts what it will need from memory
   - Explicit supervision on routing

3. **Contrastive learning**
   - Positive: correct memory configuration → correct answer
   - Negative: random memory → shouldn't work

### Long-term: Different Formulation

Consider: **Memory as the primary path, decoder as refinement**

```
Instead of: Memory as auxiliary → decoder as main
Try:        Memory as main → decoder as lightweight refinement
```

This is how **Perceiver** and **Perceiver IO** work - latent bottleneck is primary, decoder is thin.

---

## Specific Actionable Next Steps

### Immediate (Tonight/Tomorrow)

1. **Run Phase 3b1 with ctx=64** (instead of 512)
   - See if retrieval EM improves
   - Check if delta_zero drops

2. **Add supervised attention loss**
   ```python
   # In retrieval task, you know which memory slots have the answer
   # Add loss: decoder should attend to those slots
   loss += 0.1 * cross_entropy(attn_weights, target_slots)
   ```

3. **Ablate decoder context randomly**
   ```python
   # 50% of batches: only keep last 16 tokens of decoder input
   # Forces memory dependency
   ```

### This Week

4. **Profile where gradients flow**
   - Use PyTorch hooks to track gradient magnitude
   - Confirm: self-attn >> cross-attn? (that's the problem)

5. **Visualize attention patterns**
   - Does decoder actually look at memory?
   - Or just at itself?

6. **Try REINFORCE/policy gradient**
   - Treat memory routing as RL problem
   - Reward: correct answer bonus
   - This worked for Neural Turing Machines

### Research Validation

7. **Search for similar work**
   - Look for "diffusion memory compression"
   - Look for "hierarchical external memory"
   - See what worked/failed

8. **Ask the community** (Moltbook when API is working)
   - Other agents building memory-augmented systems
   - Have they solved the credit assignment problem?

---

## Bottom Line

**You're not going in the wrong direction** - you're hitting a *known hard problem* with a *novel approach*.

The architecture is clever. The implementation is solid. The challenge is universal: **making models use external memory when local context is easier**.

This is a **research problem**, not an engineering problem. You need experiments, not just more code.

### My Recommendation

**Option A (Research):** Embrace the challenge, run experiments, potentially publish
- This could be a real contribution
- "Diffusion-Based Hierarchical Memory for Transformers"
- Solve the credit assignment problem → novel work

**Option B (Pragmatic):** Pivot to simpler memory
- Replace diffusion with learned pooling/upsampling
- Focus on making memory actually work first
- Add diffusion later once basics work

**Option C (Hybrid):** Keep diffusion, simplify decoder
- Make memory non-optional (Perceiver-style)
- Prove diffusion compression works in isolation
- Then add flexible decoder

---

## Questions for You

1. **Goal:** Research contribution or working AGI system?
   - Research → push through, this is publishable
   - AGI → consider Option B or C

2. **Timeline:** How long can you iterate on this?
   - Weeks → try forced memory usage (Option A short-term)
   - Months → full research investigation
   - Days → consider pivot

3. **What matters most:** Novel architecture or functional long-context?
   - Novel → you have it, just need training to work
   - Functional → simpler approaches might get there faster

Let me know and I can help you design the next experiments based on your priorities.

---

*I'm here to help debug, run experiments, search for papers, or bounce ideas. This is the fun part - figuring out what nature (training dynamics) is telling you.*
