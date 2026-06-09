# REQUIRES GPU — Run on Kaggle with P100 accelerator
# Go to: kaggle.com/code → New Notebook → Add GPU → Paste this entire script
"""VedaRta-Native Kaggle Training — 15M Vedic Language Model."""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math, os, json

print(f"॥ VedaRta Kaggle Training — {torch.cuda.get_device_name(0)} ॥")

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
device = torch.device("cuda")

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
        Q = self.W_q(x).view(B, S, self.num_heads, self.head_dim).transpose(1,2)
        K = self.W_k(x).view(B, S, self.num_heads, self.head_dim).transpose(1,2)
        V = self.W_v(x).view(B, S, self.num_heads, self.head_dim).transpose(1,2)
        
        # Global key mean (Sphota)
        global_K = K.mean(dim=2, keepdim=True)  # [B, H, 1, d]
        
        # Score against global key
        scale = 1.0 / math.sqrt(self.head_dim)
        scores = (Q * global_K).sum(dim=-1) * scale  # [B, H, S]
        
        # PHI-gated threshold
        threshold = 1.0 / self.phi
        mask = scores.abs() > threshold
        activated = torch.zeros_like(scores)
        activated[mask] = torch.exp(scores[mask] - scores.max(dim=-1, keepdim=True)[0])
        
        # Weighted sum
        denom = activated.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        weights = activated / denom
        out = (weights.unsqueeze(-1) * V).sum(dim=2)
        
        out = out.transpose(1,2).contiguous().view(B, S, D)
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
# TRAINING DATA
# ═══════════════════════════════════

vedic_texts = [
    "Brahman is the ultimate reality pure consciousness the source of all existence",
    "Dharma is righteous duty cosmic order and truth",
    "Karma Yoga is the path of selfless action performed without attachment to results",
    "Moksha is liberation from the cycle of birth and death",
    "Atman is the individual self identical with Brahman",
    "Advaita teaches non duality the identity of Atman and Brahman",
    "Sattva Rajas Tamas are the three Gunas qualities of nature",
    "Pancha Mahabhuta Prithvi Apas Agni Vayu Akasha the five great elements",
    "Rig Veda contains hymns to deities oldest of the four Vedas",
    "Sama Veda contains musical chants and melodies",
    "Yajur Veda contains prose formulas for rituals",
    "Atharva Veda contains spells charms and healing knowledge",
    "Ahimsa means non violence non harming towards all beings",
    "Satya means truthfulness honesty in thought word and deed",
    "Panchgavya is made from five cow products dung urine milk curd ghee",
    "Jeevamrut is organic fertilizer made from cow dung urine jaggery pulse flour soil",
    "Neem Astra is organic pesticide from neem leaves crushed and fermented",
    "Vermicompost is nutrient rich organic fertilizer from earthworm composting",
    "Krishna is the divine teacher who spoke the Bhagavad Gita to Arjuna",
    "Shukla Paksha is the waxing moon period best for planting crops",
    "Agnihotra is the sacred fire ritual performed at sunrise and sunset",
    "The Upanishads contain the philosophical essence of the Vedas",
    "Bhakti Yoga is the path of devotion and love for the divine",
    "Jnana Yoga is the path of knowledge and wisdom",
    "Raja Yoga is the path of meditation and mind control",
    "ধান খেতিৰ বাবে পলসুৱা দোআঁশ মাটি ভাল pH ৫.৫-৬.৫",
    "পঞ্চগব্য পোকা নিয়ন্ত্ৰণৰ বাবে উত্তম জৈৱিক দৰব",
    "শুক্ল পক্ষ ধান ৰোৱাৰ সৰ্বোত্তম সময় জুন জুলাই মাহ",
    "মৰাপাট খেতি মাৰ্চ এপ্ৰিল মাহত কৰা ভাল",
    "জৈৱিক সাৰ ব্যৱহাৰ কৰিলে মাটিৰ উৰ্বৰা শক্তি বাঢ়ে",
    "Vedic agriculture uses lunar cycles for planting and harvesting",
    "Panchgavya applied as 3 percent foliar spray boosts crop immunity",
    "Intercropping legumes with cereals fixes nitrogen naturally",
    "Mulching with straw conserves soil moisture and suppresses weeds",
    "Crop rotation prevents pest buildup and maintains soil fertility",
    "Buttermilk spray controls fungal diseases in vegetable crops",
    "Green manure from sunn hemp adds nitrogen to the soil",
    "Composting farm waste returns nutrients to the earth",
    "Rainwater harvesting supports irrigation during dry spells",
    "Traditional seed saving preserves biodiversity for future generations",
    "Sphota attention achieves O of n complexity not O of n squared",
    "Tri Nadi activation uses three channel Sushumna Ida Pingala",
    "Chitta KV cache prunes tokens based on Sattva Rajas Tamas salience",
    "Urdhva Tiryagbhyam is the Vedic cross multiplication sutra",
    "Nikhilam Sutra enables fast multiplication near powers of ten",
    "Ekadhikena Purvena squares numbers ending in five instantly",
    "Paravartya Yojayet is the transpose and adjust division method",
    "Sunyam Samyasamuccaye solves equations where sum is zero",
    "Anurupye Sunyamanyat handles proportional calculations",
    "The Barak Valley in Assam is known for rice and jute cultivation",
    "Silchar is the main city of the Barak Valley region in southern Assam",
    "Assam receives heavy monsoon rainfall supporting paddy cultivation",
    "Organic farming in northeast India preserves traditional knowledge",
    "Krishi Veda integrates ancient wisdom with modern agriculture",
    "Water buffalo provide milk and draft power for small farmers",
    "Duck rearing in paddy fields controls pests naturally",
    "Betel nut and banana are important cash crops in Assam",
    "Tea gardens of Assam produce world famous Assam tea",
    "Fish farming in ponds supplements farmer income in Barak Valley",
    "Bamboo is widely used for construction in rural Assam",
    "Community seed banks preserve indigenous rice varieties",
]

# Simple character-level tokenizer for demo training
chars = sorted(list(set("".join(vedic_texts))))
stoi = {ch:i+4 for i,ch in enumerate(chars)}  # 0=UNK,1=BOS,2=EOS,3=PAD
itos = {i+4:ch for i,ch in enumerate(chars)}
vocab_size = len(chars) + 4
print(f"Char vocab: {vocab_size}")

def encode(text, max_len=128):
    ids = [stoi.get(c, 0) for c in text]
    ids = ids[:max_len]
    ids += [2] * (max_len - len(ids))  # EOS padding
    return ids

data = torch.tensor([encode(t, 64) for t in vedic_texts * 20], dtype=torch.long)  # 1160 samples
print(f"Training data: {data.shape}")

# ═══════════════════════════════════
# TRAIN
# ═══════════════════════════════════

model = VedaRtaNative(Config())
model = model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=cfg.epochs)

for epoch in range(cfg.epochs):
    model.train()
    total_loss = 0
    perm = torch.randperm(len(data))
    
    for i in range(0, len(data), cfg.batch_size):
        idx = perm[i:i+cfg.batch_size]
        batch = data[idx].to(device)
        x, y = batch[:, :-1], batch[:, 1:]
        
        logits = model(x)
        loss = F.cross_entropy(logits.reshape(-1, vocab_size), y.reshape(-1), ignore_index=2)
        
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
        optimizer.step()
        total_loss += loss.item()
    
    scheduler.step()
    avg_loss = total_loss / (len(data) // cfg.batch_size)
    print(f"Epoch {epoch+1}/{cfg.epochs} | Loss: {avg_loss:.4f} | LR: {scheduler.get_last_lr()[0]:.6f}")

# Save weights
save_path = "/kaggle/working/vedarta_15m_trained.pt"
torch.save(model.state_dict(), save_path)
print(f"\nSaved: {save_path}")
print(f"File size: {os.path.getsize(save_path)/1024/1024:.1f} MB")
print("॥ Training complete. Download this .pt file for GGUF conversion. ॥")
