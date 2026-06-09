"""Tri-Nadi Activation + Chitta KV Cache — numpy implementations."""
import numpy as np

PHI = 1.618033988749895

# ═══════════════════════════════════════════
# TRI-NADI ACTIVATION (Sushumna/Ida/Pingala)
# ═══════════════════════════════════════════

def tri_nadi(x):
    """
    Three-channel activation based on Gunas:
    - Sushumna (balanced): x * 0.5 (central channel)
    - Ida (receptive):     x * PHI * 0.382 when x > 0, else x * 0.3
    - Pingala (active):    x * 0.382 when x > 0, else x * PHI * 0.3
    
    Returns combined three-channel activation.
    """
    sushumna = x * 0.5
    ida = np.where(x > 0, x * PHI * 0.382, x * 0.3)
    pingala = np.where(x > 0, x * 0.382, x * PHI * 0.3)
    return sushumna + ida * 0.25 + pingala * 0.25


# ═══════════════════════════════════════════
# CHITTA KV CACHE (Sattva/Rajas/Tamas)
# ═══════════════════════════════════════════

class ChittaKVCache:
    """
    Sattva/Rajas/Tamas KV cache pruning.
    Reduces KV cache from full sequence to top-k most Sattvic tokens.
    """
    
    def __init__(self, max_cached=512, dim=256):
        self.max_cached = max_cached
        self.dim = dim
        self.keys = np.zeros((max_cached, dim), dtype=np.float32)
        self.values = np.zeros((max_cached, dim), dtype=np.float32)
        self.salience = np.zeros(max_cached, dtype=np.float32)
        self.positions = np.zeros(max_cached, dtype=np.int32)
        self.num_stored = 0
    
    def compute_salience(self, key_vec):
        """L2 norm = information content (Sattva measure)."""
        return np.sqrt(np.sum(key_vec * key_vec))
    
    def store(self, key, value, position):
        """Store key-value pair, evict lowest-salience if full."""
        sal = self.compute_salience(key)
        
        if self.num_stored < self.max_cached:
            idx = self.num_stored
            self.keys[idx] = key
            self.values[idx] = value
            self.salience[idx] = sal
            self.positions[idx] = position
            self.num_stored += 1
        else:
            min_idx = np.argmin(self.salience)
            if sal > self.salience[min_idx]:
                self.keys[min_idx] = key
                self.values[min_idx] = value
                self.salience[min_idx] = sal
                self.positions[min_idx] = position
    
    def retrieve(self):
        """Return cached KV pairs sorted by position (causal order)."""
        if self.num_stored == 0:
            return None, None
        order = np.argsort(self.positions[:self.num_stored])
        return self.keys[order], self.values[order]
    
    def store_batch(self, K, V, start_pos=0):
        """Store full KV matrices from a layer forward pass."""
        seq_len = K.shape[0]
        for i in range(seq_len):
            self.store(K[i], V[i], start_pos + i)


# ═══════════════════════════════════════════
# VEDIC FEED-FORWARD (with Tri-Nadi)
# ═══════════════════════════════════════════

class VedicFeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff).astype(np.float32) * 0.02
        self.W2 = np.random.randn(d_ff, d_model).astype(np.float32) * 0.02
        self.b1 = np.zeros(d_ff, dtype=np.float32)
        self.b2 = np.zeros(d_model, dtype=np.float32)
    
    def forward(self, x):
        h = x @ self.W1 + self.b1
        h = tri_nadi(h)
        return h @ self.W2 + self.b2


# ═══════════════════════════════════════════
# LAYER NORM
# ═══════════════════════════════════════════

class LayerNorm:
    def __init__(self, dim, eps=1e-6):
        self.gamma = np.ones(dim, dtype=np.float32)
        self.beta = np.zeros(dim, dtype=np.float32)
        self.eps = eps
    
    def forward(self, x):
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        return self.gamma * (x - mean) / np.sqrt(var + self.eps) + self.beta


# ═══════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════

if __name__ == "__main__":
    # Test Tri-Nadi
    x = np.array([-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0])
    out = tri_nadi(x)
    print("Tri-Nadi Activation:")
    for i, o in zip(x, out):
        print(f"  {i:+.1f} → {o:+.4f}")
    
    # Test Chitta KV Cache
    cache = ChittaKVCache(max_cached=4, dim=8)
    K = np.random.randn(6, 8).astype(np.float32)
    V = np.random.randn(6, 8).astype(np.float32)
    cache.store_batch(K, V)
    k_out, v_out = cache.retrieve()
    print(f"\nChitta KV Cache: stored {cache.num_stored}/{cache.max_cached}")
    print(f"Retrieved: K={k_out.shape}, V={v_out.shape}")
    print(f"Salience: {cache.salience[:cache.num_stored]}")
    
    # Test FeedForward
    ff = VedicFeedForward(64, 128)
    x_test = np.random.randn(4, 64).astype(np.float32)
    out = ff.forward(x_test)
    print(f"\nVedic FF: {x_test.shape} → {out.shape}")
