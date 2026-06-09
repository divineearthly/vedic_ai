"""VedaRta-Native: 15-25M param Vedic language model — pure numpy."""
import numpy as np
import os
from sphota_attention import sphota_attention, sphota_multi_head
from vedic_layers import tri_nadi, ChittaKVCache, VedicFeedForward, LayerNorm

PHI = 1.618033988749895


class VedaRtaConfig:
    def __init__(self, vocab_size=4096, dim=384, num_layers=8, 
                 num_heads=8, ffn_dim=1024, max_seq_len=512,
                 max_cached_kv=256):
        self.vocab_size = vocab_size
        self.dim = dim
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.ffn_dim = ffn_dim
        self.max_seq_len = max_seq_len
        self.max_cached_kv = max_cached_kv
    
    @property
    def param_count(self):
        embed = self.vocab_size * self.dim
        pos = self.max_seq_len * self.dim
        per_layer = (4 * self.dim * self.dim + 2 * self.dim * self.ffn_dim + 4 * self.dim)
        output = self.dim * self.vocab_size
        return embed + pos + per_layer * self.num_layers + output


class VedaRtaLayer:
    def __init__(self, config):
        dim = config.dim
        self.W_q = np.random.randn(dim, dim).astype(np.float32) * 0.02
        self.W_k = np.random.randn(dim, dim).astype(np.float32) * 0.02
        self.W_v = np.random.randn(dim, dim).astype(np.float32) * 0.02
        self.W_o = np.random.randn(dim, dim).astype(np.float32) * 0.02
        self.ff = VedicFeedForward(dim, config.ffn_dim)
        self.ln_attn = LayerNorm(dim)
        self.ln_ff = LayerNorm(dim)
        self.num_heads = config.num_heads
        self.head_dim = config.head_dim
    
    def forward(self, x, kv_cache=None):
        # x: [seq_len, dim]
        Q = x @ self.W_q
        K = x @ self.W_k
        V = x @ self.W_v
        attn_out = sphota_multi_head(Q, K, V, self.num_heads)
        attn_out = attn_out @ self.W_o
        x = self.ln_attn.forward(x + attn_out)
        ff_out = self.ff.forward(x)
        x = self.ln_ff.forward(x + ff_out)
        if kv_cache is not None:
            kv_cache.store_batch(K, V)
        return x


class VedaRtaNative:
    def __init__(self, config=None):
        self.config = config or VedaRtaConfig()
        cfg = self.config
        self.token_embed = np.random.randn(cfg.vocab_size, cfg.dim).astype(np.float32) * 0.02
        self.pos_embed = np.random.randn(cfg.max_seq_len, cfg.dim).astype(np.float32) * 0.02
        self.layers = [VedaRtaLayer(cfg) for _ in range(cfg.num_layers)]
        self.output_proj = np.random.randn(cfg.dim, cfg.vocab_size).astype(np.float32) * 0.02
        self.kv_caches = [ChittaKVCache(max_cached=cfg.max_cached_kv, dim=cfg.dim) 
                          for _ in range(cfg.num_layers)]
        print(f"॥ VedaRta-Native Initialized ॥")
        print(f"   Vocab: {cfg.vocab_size} | Dim: {cfg.dim} | Layers: {cfg.num_layers}")
        print(f"   Heads: {cfg.num_heads} | FFN: {cfg.ffn_dim}")
        print(f"   Parameters: {cfg.param_count:,}")
        print(f"   Model size (fp32): {cfg.param_count * 4 / 1024 / 1024:.1f} MB")
        print(f"   Model size (q4): {cfg.param_count * 0.5 / 1024 / 1024:.1f} MB")
    
    def forward(self, token_ids):
        # token_ids: [batch_size, seq_len]
        batch_size, seq_len = token_ids.shape
        x = self.token_embed[token_ids]  # [batch, seq, dim]
        positions = np.arange(seq_len)
        x = x + self.pos_embed[positions]
        # Process each batch item through layers
        for i, layer in enumerate(self.layers):
            x_new = np.zeros_like(x)
            for b in range(batch_size):
                x_new[b] = layer.forward(x[b], kv_cache=self.kv_caches[i])
            x = x_new
        logits = x @ self.output_proj
        return logits
    
    def generate(self, prompt_ids, max_new_tokens=50, temperature=0.7):
        generated = list(prompt_ids)
        for _ in range(max_new_tokens):
            ctx = generated[-self.config.max_seq_len:]
            ctx = np.array([ctx], dtype=np.int32)
            logits = self.forward(ctx)
            next_logits = logits[0, -1, :] / temperature
            exp_logits = np.exp(next_logits - next_logits.max())
            probs = exp_logits / exp_logits.sum()
            next_token = np.random.choice(self.config.vocab_size, p=probs)
            generated.append(int(next_token))
            if next_token == 2:
                break
        return generated
    
    def save_weights(self, path):
        weights = {'token_embed': self.token_embed, 'pos_embed': self.pos_embed, 'output_proj': self.output_proj}
        for i, layer in enumerate(self.layers):
            weights[f'layer_{i}_W_q'] = layer.W_q
            weights[f'layer_{i}_W_k'] = layer.W_k
            weights[f'layer_{i}_W_v'] = layer.W_v
            weights[f'layer_{i}_W_o'] = layer.W_o
            weights[f'layer_{i}_ff_W1'] = layer.ff.W1
            weights[f'layer_{i}_ff_W2'] = layer.ff.W2
        np.savez_compressed(path, **weights)
        print(f"Saved weights to {path}")
    
    def load_weights(self, path):
        data = np.load(path)
        self.token_embed = data['token_embed']
        self.pos_embed = data['pos_embed']
        self.output_proj = data['output_proj']
        for i, layer in enumerate(self.layers):
            layer.W_q = data[f'layer_{i}_W_q']
            layer.W_k = data[f'layer_{i}_W_k']
            layer.W_v = data[f'layer_{i}_W_v']
            layer.W_o = data[f'layer_{i}_W_o']
            layer.ff.W1 = data[f'layer_{i}_ff_W1']
            layer.ff.W2 = data[f'layer_{i}_ff_W2']
        print(f"Loaded weights from {path}")


if __name__ == "__main__":
    config = VedaRtaConfig(vocab_size=4096, dim=384, num_layers=8, num_heads=8, ffn_dim=1024)
    model = VedaRtaNative(config)
    
    batch = np.array([[10, 20, 30, 40, 50, 60, 70, 80]], dtype=np.int32)
    logits = model.forward(batch)
    print(f"\nForward pass: {batch.shape} → {logits.shape}")
    print(f"Logits range: [{logits.min():.4f}, {logits.max():.4f}]")
    
    prompt = [1, 10, 20]
    generated = model.generate(prompt, max_new_tokens=10)
    print(f"\nGenerated (untrained): {len(generated)} tokens, IDs: {generated}")
    
    model.save_weights("/home/codespace/vedarta_test_weights.npz")
    model2 = VedaRtaNative(config)
    model2.load_weights("/home/codespace/vedarta_test_weights.npz")
    logits2 = model2.forward(batch)
    match = np.allclose(logits, logits2)
    print(f"\nSave/Load roundtrip: {'PASS' if match else 'FAIL'}")
