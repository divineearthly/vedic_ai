"""Sphota O(n) Attention — ports sphota_attention_kernel.h to numpy."""
import numpy as np

PHI = 1.618033988749895

def sphota_attention(Q, K, V):
    """
    Sphota attention: O(n) instead of O(n²).
    
    Args:
        Q: Query matrix [seq_len, dim]
        K: Key matrix   [seq_len, dim]
        V: Value matrix [seq_len, dim]
    
    Returns:
        output: [seq_len, dim]
    """
    seq_len, dim = Q.shape
    
    # Step 1: Global key (mean of all keys) — O(n)
    global_K = K.mean(axis=0)  # [dim]
    
    # Step 2: Score each query against global key — O(n)
    scale = 1.0 / np.sqrt(dim)
    scores = Q @ global_K * scale  # [seq_len]
    
    # Step 3: Sphota burst — PHI-gated activation
    threshold = 1.0 / PHI  # 0.618
    max_score = scores.max()
    scores = scores - max_score  # stability
    
    # Burst above threshold, Shunyam below
    mask = np.abs(scores) > threshold
    activated = np.zeros_like(scores)
    activated[mask] = np.exp(scores[mask])
    # Below threshold → 0 (Shunyam silence)
    
    sum_scores = activated.sum()
    
    # Step 4: Weighted sum of values — O(n)
    if sum_scores > 1e-8:
        weights = activated / sum_scores  # [seq_len]
        output = weights[:, np.newaxis] * V  # [seq_len, dim]
    else:
        output = np.zeros_like(V)
    
    return output


def sphota_multi_head(Q, K, V, num_heads=8):
    """Multi-head Sphota attention."""
    seq_len, dim = Q.shape
    head_dim = dim // num_heads
    outputs = []
    
    for h in range(num_heads):
        start = h * head_dim
        end = start + head_dim
        qh = Q[:, start:end]
        kh = K[:, start:end]
        vh = V[:, start:end]
        outputs.append(sphota_attention(qh, kh, vh))
    
    return np.concatenate(outputs, axis=-1)


# Quick test
if __name__ == "__main__":
    seq, dim = 8, 64
    Q = np.random.randn(seq, dim).astype(np.float32)
    K = np.random.randn(seq, dim).astype(np.float32)
    V = np.random.randn(seq, dim).astype(np.float32)
    
    out = sphota_attention(Q, K, V)
    print(f"Sphota O(n) attention: {seq}x{dim} → {out.shape}")
    print(f"Output norm: {np.linalg.norm(out):.4f}")
    
    out_mh = sphota_multi_head(Q, K, V, num_heads=4)
    print(f"Multi-head (4): {out_mh.shape}")
