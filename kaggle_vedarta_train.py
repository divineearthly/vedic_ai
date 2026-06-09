# REQUIRES GPU — Run on Kaggle with P100/T4 accelerator
# Go to: kaggle.com/code → New Notebook → Add GPU → Paste this entire script
"""VedaRta-Native Kaggle Training — Sovereign 12-Sutra Vedic Language Model."""

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
    """Sutra: Antyayordashake'pi (Complementary Blocks)."""
    def __init__(self, max_seq_len, dim):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        pos = torch.arange(max_seq_len).float()
        sinusoid_inp = torch.einsum("i,j->ij", pos, inv_freq)
        emb = torch.cat((sinusoid_inp.sin(), sinusoid_inp.cos()), dim=-1)
        
        complements = 1.0 - emb
        self.register_buffer('pos_emb', (emb + complements.flip(dims=[0])) / 2.0)

    def forward(self, seq_len):
        return self.pos_emb[:seq_len, :].unsqueeze(0)

# ═══════════════════════════════════
# 2. SPHOTA O(n) ATTENTION (Urdhva & Nikhilam Enhanced)
# ═══════════════════════════════════

class SphotaAttention(nn.Module):
    """Sutra: Urdhva Tiryagbhyam + Nikhilam + Puranapuranabhyam."""
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

        global_K = K.mean(dim=2, keepdim=True)  # [B, H, 1, head_dim]

        scale = 1.0 / math.sqrt(self.head_dim)
        scores = (Q * global_K).sum(dim=-1) * scale  # [B, H, S]

        exp_scores = torch.exp(scores - scores.max(dim=-1, keepdim=True)[0])

        threshold = 1.0 / self.phi
        mask = (scores.abs() > threshold).float()
        
        # Sutra: Puranapuranabhyam (Bypass execution grid if un-activated)
        if mask.sum() == 0:
            return torch.zeros(B, S, D, device=x.device, dtype=x.dtype)
            
        activated = exp_scores * mask
        denom = activated.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        weights = activated / denom

        context = torch.matmul(weights.unsqueeze(2), V)
        out = context.repeat(1, 1, S, 1)

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
        
        # Sutra: Yavadunam (Zero-Copy Quantization Deficit Tuning)
        # Calculates the float structural grid variance deficiency directly
        deficiency = variance - torch.round(variance)
        adjusted_variance = variance + (deficiency ** 2) * 0.1
        
        return self.weight * (deviation / torch.sqrt(adjusted_variance + self.eps)) + self.bias

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
        
        # Sutra: Ekadhikena Purvena (Progressive Initialization Scaling)
        scale_factor = 1.0 / math.sqrt(2 * (layer_idx + 1))
        
        self.ff = nn.Sequential(
            nn.Linear(config.dim, config.ffn_dim),
            TriNadiActivation(),
            nn.Linear(config.ffn_dim, config.dim),
        )
        
        self.ff[0].weight.data.mul_(scale_factor)
        self.ff[2].weight.data.mul_(scale_factor)
        
        self.ln1 = ParavartyaLayerNorm(config.dim)
        self.ln2 = ParavartyaLayerNorm(config.dim)

    def forward(self, x):
        x = self.ln1(x + self.attn(x))
        x = self.ln2(x + self.ff(x))
        return x

# ═══════════════════════════════════
# FULL SYSTEM ENGINE (Sopantyadvayamaryam Integrated)
# ═══════════════════════════════════

class VedaRtaNative(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.token_embed = nn.Embedding(config.vocab_size, config.dim)
        self.pos_embed = AntyayorPositionalEmbedding(config.max_seq_len, config.dim)
        self.layers = nn.ModuleList([VedaRtaLayer(config, i) for i in range(config.num_layers)])
        self.ln_final = ParavartyaLayerNorm(config.dim)
        self.output_proj = nn.Linear(config.dim, config.vocab_size, bias=False)

    def forward(self, input_ids):
        B, S = input_ids.shape
        x = self.token_embed(input_ids)
        x = x + self.pos_embed(S)
        for layer in self.layers:
            x = layer(x)
        x = self.ln_final(x)
        return self.output_proj(x)

    def compute_sutra_loss(self, logits, targets):
        """
        Sutras: Shunyam Samyasamuccaye (Sparsity Regularization) 
        and Vyastisamastih (Individual & Collective Token Optimization).
        """
        # Vyastisamastih Pass: individual distribution cross-entropy
        individual_loss = F.cross_entropy(logits.view(-1, self.config.vocab_size), targets.view(-1))
        
        # Vyastisamastih Pass: collective micro-variance optimization
        collective_loss = torch.var(logits.mean(dim=1)) * 0.05
        base_loss = individual_loss + collective_loss
        
        # Shunyam Samyasamuccaye pass
        sparsity_reg = 0.0
        for p in self.parameters():
            if p.dim() > 1:
                sparsity_reg += torch.mean(torch.abs(p))
                
        return base_loss + (1e-5 * sparsity_reg)

    def apply_sopantya_gradient_clip(self, max_norm=0.5):
        """
        Sutra: Sopantyadvayamaryam (Ultimate and Penultimate Balance).
        Dynamically limits training exploding gradients by evaluating variance ratios 
        between output layers and penultimate deep parameters.
        """
        penultimate_grad = self.layers[-1].ff[2].weight.grad
        ultimate_grad = self.output_proj.weight.grad
        
        if penultimate_grad is not None and ultimate_grad is not None:
            ratio = torch.norm(ultimate_grad) / (torch.norm(penultimate_grad) + 1e-8)
            # Dynamic scaling clip threshold modification
            dynamic_clip = max_norm * ratio.clamp(min=0.2, max=2.0)
            nn.utils.clip_grad_norm_(self.parameters(), dynamic_clip)
        else:
            nn.utils.clip_grad_norm_(self.parameters(), max_norm)

# ═══════════════════════════════════
# OPTIMIZATION TRACKS (Anurupyena & Calana-Kalanabhyam)
# ═══════════════════════════════════

def get_anurupyena_lr(step, total_steps, initial_lr):
    """Sutra: Anurupyena (Proportionate Scaling Decay Grid)."""
    ratio = float(step) / float(max(1, total_steps))
    proportion = 0.5 * (1.0 + math.cos(ratio * math.pi))
    
    # Sutra: Calana-Kalanabhyam (Motion-Trajectory Shift Acceleration)
    # Scales step acceleration factors based on target timeline velocity
    trajectory_acceleration = 1.05 if ratio < 0.2 else 1.0
    return initial_lr * proportion * trajectory_acceleration

# ═══════════════════════════════════
# PIPELINE CHECK
# ═══════════════════════════════════
if __name__ == "__main__":
    print("🕉️" * 30)
    print(" EXECUTING THE SOVEREIGN 12-SUTRA ENGINE")
    print("🕉️" * 30)
    
    model = VedaRtaNative(cfg).to(device)
    
    dummy_input = torch.randint(0, cfg.vocab_size, (cfg.batch_size, cfg.max_seq_len)).to(device)
    dummy_targets = torch.randint(0, cfg.vocab_size, (cfg.batch_size, cfg.max_seq_len)).to(device)
    
    # Forward compilation test loop step
    logits = model(dummy_input)
    loss = model.compute_sutra_loss(logits, dummy_targets)
    
    # Backpropagation verification loop pass
    loss.backward()
    model.apply_sopantya_gradient_clip(cfg.grad_clip)
    
    print(f"\n✅ Sovereign 12-Sutra Machine Learning Graph Fully Compiled!")
    print(f"   Logits Matrix Dimension Shape: {logits.shape}")
    print(f"   Sutra Unified Loss Evaluation Vector: {loss.item():.4f}")
    
    # Runtime scheduler verification parameters pass
    final_lr = get_anurupyena_lr(step=50, total_steps=1000, initial_lr=cfg.lr)
    print(f"   Anurupyena / Calana-Kalanabhyam Runtime Step LR: {final_lr:.6f}")
