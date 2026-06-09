# REQUIRES GPU — Run on Kaggle with P100/T4 accelerator
# Go to: kaggle.com/code → New Notebook → Add GPU → Paste this entire script
"""VedaRta-Native Kaggle Training — 15M Vedic Language Model."""

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
# SPHOTA O(n) ATTENTION
# ═══════════════════════════════════

class SphotaAttention(nn.Module):
    """O(n) Sphota attention — global key mean + PHI gate."""
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

        # Score against global key — Yields a sequence tracking vector
        scale = 1.0 / math.sqrt(self.head_dim)
        scores = (Q * global_K).sum(dim=-1) * scale  # [B, H, S]

        # Stable Exponential Calculation across entire matrix shape
        exp_scores = torch.exp(scores - scores.max(dim=-1, keepdim=True)[0])

        # PHI-gated threshold activation
        threshold = 1.0 / self.phi
        mask = (scores.abs() > threshold).float()
        
        # Multiply element-wise to suppress un-activated vectors without shape distortion
        activated = exp_scores * mask

        # Normalize activations safely across sequence weights
        denom = activated.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        weights = activated / denom  # [B, H, S]

        # Vectorized broadcast mapping context back to multi-head dimensions
        context = torch.matmul(weights.unsqueeze(2), V)  # [B, H, 1, head_dim]
        out = context.repeat(1, 1, S, 1)  # [B, H, S, head_dim]

        out = out.transpose(1, 2).contiguous().view(B, S, D)
        return self.W_o(out)

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
# VEDARTA LAYER
# ═══════════════════════════════════

class VedaRtaLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.attn = SphotaAttention(config.dim, config.num_heads)
        self.ff = nn.Sequential(
            nn.Linear(config.dim, config.ffn_dim),
            TriNadiActivation(),
            nn.Linear(config.ffn_dim, config.dim),
        )
        self.ln1 = nn.LayerNorm(config.dim)
        self.ln2 = nn.LayerNorm(config.dim)

    def forward(self, x):
        x = self.ln1(x + self.attn(x))
        x = self.ln2(x + self.ff(x))
        return x

# ═══════════════════════════════════
# FULL MODEL
# ═══════════════════════════════════

class VedaRtaNative(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.token_embed = nn.Embedding(config.vocab_size, config.dim)
        self.pos_embed = nn.Parameter(torch.randn(1, config.max_seq_len, config.dim) * 0.02)
        self.layers = nn.ModuleList([VedaRtaLayer(config) for _ in range(config.num_layers)])
        self.ln_final = nn.LayerNorm(config.dim)
        self.output_proj = nn.Linear(config.dim, config.vocab_size, bias=False)

        n_params = sum(p.numel() for p in self.parameters())
        print(f"Model: {n_params:,} params | {n_params*4/1024/1024:.1f} MB fp32")

    def forward(self, input_ids):
        B, S = input_ids.shape
        x = self.token_embed(input_ids)
        x = x + self.pos_embed[:, :S, :]
        for layer in self.layers:
            x = layer(x)
        x = self.ln_final(x)
        return self.output_proj(x)

# ═══════════════════════════════════
# PIPELINE CHECK
# ═══════════════════════════════════
if __name__ == "__main__":
    print("🕉️" * 30)
    print(" INITIALIZING PYTORCH VEDARTA PIPELINE CHECK")
    print("🕉️" * 30)
    
    model = VedaRtaNative(cfg).to(device)
    
    # Synthetic batch verification token tensor pass
    dummy_input = torch.randint(0, cfg.vocab_size, (cfg.batch_size, cfg.max_seq_len)).to(device)
    logits = model(dummy_input)
    
    print(f"\n✅ GPU/PyTorch forward execution check complete!")
    print(f"   Logits out array shape match matrix: {logits.shape}")
