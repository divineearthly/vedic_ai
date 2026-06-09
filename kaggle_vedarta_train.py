# REQUIRES GPU — Run on Kaggle with P100/T4 accelerator
# Go to: kaggle.com/code → New Notebook → Add GPU → Paste this entire script
"""VedaRta-Native Kaggle Training — Ultimate 8-Sutra Vedic Language Model."""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math, os, json

# ═══════════════════════════════════
# CONFIG
# ═══════════════════════════════════

class Config:
    vocab_size = 4096
    dim = 384
    num_layers = 8
    num_heads = 8
    ffn_dim = 1024
    max_seq_len = 256
    batch_size = 16
    epochs = 10
    lr = 3e-4
    weight_decay = 0.01
    grad_clip = 0.5

cfg = Config()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"॥ VedaRta Training Backend Active: {device} ॥")

# ═══════════════════════════════════
# 1. ANTYAYORDASHAKE'PI POSITIONAL EMBEDDING
# ═══════════════════════════════════

class AntyayorPositionalEmbedding(nn.Module):
    """Sutra: Antyayordashake'pi (Complementary Blocks to 10/Base)."""
    def __init__(self, max_seq_len, dim):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        pos = torch.arange(max_seq_len).float()
        sinusoid_inp = torch.einsum("i,j->ij", pos, inv_freq)
        emb = torch.cat((sinusoid_inp.sin(), sinusoid_inp.cos()), dim=-1)
        
        # Complementary balancing of mirrored tokens across the sequence window
        complements = 1.0 - emb
        self.register_buffer('pos_emb', (emb + complements.flip(dims=[0])) / 2.0)

    def forward(self, seq_len):
        return self.pos_emb[:seq_len, :].unsqueeze(0)

# ═══════════════════════════════════
# 2. SPHOTA O(n) ATTENTION (Urdhva & Nikhilam Enhanced)
# ═══════════════════════════════════

class SphotaAttention(nn.Module):
    """Sutra: Urdhva Tiryagbhyam (Cross Multi) + Nikhilam (Base Deviations)."""
    def __init__(self, dim, num_heads):
        super().__init__()
        self.dim = dim
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.W_q = nn.Linear(dim, dim, bias=False)
        self.W_k = nn.Linear(dim, dim, bias=False)
        self.W_v = nn.Linear(dim, dim, bias=False)
        self.W_o = nn.Linear(dim, dim, bias=False)
        self.phi = 1.618033988749895

    def forward(self, x):
        B, S, D = x.shape
        Q = self.W_q(x).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.W_k(x).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.W_v(x).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)

        # Global key mean (Sphota) — Collapse sequence dimension to O(1)
        global_K = K.mean(dim=2, keepdim=True)  # [B, H, 1, head_dim]

        # Score against global key via Urdhva Crosswise mechanics
        scale = 1.0 / math.sqrt(self.head_dim)
        scores = (Q * global_K).sum(dim=-1) * scale  # [B, H, S]

        # Stable Exponential Calculation
        exp_scores = torch.exp(scores - scores.max(dim=-1, keepdim=True)[0])

        # PHI-gated threshold activation
        threshold = 1.0 / self.phi
        mask = (scores.abs() > threshold).float()
        
        # Sutra: Puranapuranabhyam (Fast Bypassing Completion Check)
        # If no tokens pass activation threshold, completely abort layer overhead
        if mask.sum() == 0:
            return torch.zeros(B, S, D, device=x.device, dtype=x.dtype)
            
        activated = exp_scores * mask

        # Normalize activations across sequence weights
        denom = activated.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        weights = activated / denom  # [B, H, S]

        # Vectorized broadcast mapping context back to multi-head dimensions
        context = torch.matmul(weights.unsqueeze(2), V)  # [B, H, 1, head_dim]
        out = context.repeat(1, 1, S, 1)  # [B, H, S, head_dim]

        out = out.transpose(1, 2).contiguous().view(B, S, D)
        return self.W_o(out)

# ═══════════════════════════════════
# 3. PARAVARTYA YOJAYET LAYER NORMALIZATION
# ═══════════════════════════════════

class ParavartyaLayerNorm(nn.Module):
    """Sutra: Paravartya Yojayet (Transpose and Apply Relative Deviations)."""
    def __init__(self, dim, eps=1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.bias = nn.Parameter(torch.zeros(dim))
        self.eps = eps

    def forward(self, x):
        mean = x.mean(dim=-1, keepdim=True)
        deviation = x - mean
        variance = (deviation ** 2).mean(dim=-1, keepdim=True)
        return self.weight * (deviation / torch.sqrt(variance + self.eps)) + self.bias

# ═══════════════════════════════════
# TRI-NADI ACTIVATION
# ═══════════════════════════════════

class TriNadiActivation(nn.Module):
    def __init__(self):
        super().__init__()
        self.phi = 1.618033988749895

    def forward(self, x):
        sushumna = x * 0.5
        ida = torch.where(x > 0, x * self.phi * 0.382, x * 0.3)
        pingala = torch.where(x > 0, x * 0.382, x * self.phi * 0.3)
        return sushumna + ida * 0.25 + pingala * 0.25

# ═══════════════════════════════════
# VEDARTA LAYER (Ekadhikena Initialized)
# ═══════════════════════════════════

class VedaRtaLayer(nn.Module):
    def __init__(self, config, layer_idx):
        super().__init__()
        self.attn = SphotaAttention(config.dim, config.num_heads)
        
        # Sutra: Ekadhikena Purvena (Progressive depth scaling base allocation)
        # Deep layers are scaled progressively down by one more than the previous to stabilize deep gradients
        scale_factor = 1.0 / math.sqrt(2 * (layer_idx + 1))
        
        self.ff = nn.Sequential(
            nn.Linear(config.dim, config.ffn_dim),
            TriNadiActivation(),
            nn.Linear(config.ffn_dim, config.dim),
        )
        
        # Apply progressive initialization scaling factors
        self.ff[0].weight.data.mul_(scale_factor)
        self.ff[2].weight.data.mul_(scale_factor)
        
        self.ln1 = ParavartyaLayerNorm(config.dim)
        self.ln2 = ParavartyaLayerNorm(config.dim)

    def forward(self, x):
        attn_out = self.attn(x)
        x = self.ln1(x + attn_out)
        x = self.ln2(x + self.ff(x))
        return x

# ═══════════════════════════════════
# FULL SYSTEM ENGINE
# ═══════════════════════════════════

class VedaRtaNative(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.token_embed = nn.Embedding(config.vocab_size, config.dim)
        self.pos_embed = AntyayorPositionalEmbedding(config.max_seq_len, config.dim)
        
        # Pass layer index downward to trigger Ekadhikena parameters scaling
        self.layers = nn.ModuleList([VedaRtaLayer(config, i) for i in range(config.num_layers)])
        self.ln_final = ParavartyaLayerNorm(config.dim)
        self.output_proj = nn.Linear(config.dim, config.vocab_size, bias=False)

        n_params = sum(p.numel() for p in self.parameters())
        print(f"Model: {n_params:,} params | {n_params*4/1024/1024:.1f} MB fp32")

    def forward(self, input_ids):
        B, S = input_ids.shape
        x = self.token_embed(input_ids)
        x = x + self.pos_embed(S)
        for layer in self.layers:
            x = layer(x)
        x = self.ln_final(x)
        return self.output_proj(x)

    def compute_shunyam_loss(self, logits, targets):
        """
        Sutra: Shunyam Samyasamuccaye (If the collection is equal, it resolves to zero).
        Cross entropy base loss enhanced with an absolute sparsity constraint that driving
        highly redundant, low-variance layer parameters down to absolute zero.
        """
        base_loss = F.cross_entropy(logits.view(-1, self.config.vocab_size), targets.view(-1))
        
        # Collect parameters to apply sparsity constraints
        sparsity_reg = 0.0
        for p in self.parameters():
            if p.dim() > 1:
                sparsity_reg += torch.mean(torch.abs(p))
                
        return base_loss + (1e-5 * sparsity_reg)

# ═══════════════════════════════════
# 4. ANURUPYENA LEARNING RATE SCHEDULER
# ═══════════════════════════════════

def get_anurupyena_lr(step, total_steps, initial_lr):
    """Sutra: Anurupyena (Proportionate Scaling decay timeline)."""
    ratio = float(step) / float(max(1, total_steps))
    proportion = 0.5 * (1.0 + math.cos(ratio * math.pi))
    return initial_lr * proportion

# ═══════════════════════════════════
# PIPELINE CHECK
# ═══════════════════════════════════
if __name__ == "__main__":
    print("🕉️" * 30)
    print(" EXECUTING ULTIMATE 8-SUTRA NATIVE GRAPH BUILD")
    print("🕉️" * 30)
    
    model = VedaRtaNative(cfg).to(device)
    
    # Synthetic batch verification token tensor pass
    dummy_input = torch.randint(0, cfg.vocab_size, (cfg.batch_size, cfg.max_seq_len)).to(device)
    dummy_targets = torch.randint(0, cfg.vocab_size, (cfg.batch_size, cfg.max_seq_len)).to(device)
    
    logits = model(dummy_input)
    loss = model.compute_shunyam_loss(logits, dummy_targets)
    
    print(f"\n✅ All 8 Advanced Vedic Matrix Structural Layers Operational!")
    print(f"   Logits execution matrix footprint: {logits.shape}")
    print(f"   Shunyam Sparsity Regularized Loss Vector: {loss.item():.4f}")
