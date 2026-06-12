#!/usr/bin/env python3
"""Complete benchmark suite for Vedic algorithms"""

import time
import numpy as np

def benchmark_urdhva_vs_numpy():
    """Compare Urdhva matmul with NumPy"""
    print("\n🔢 Urdhva Matmul vs NumPy Benchmark")
    print("=" * 60)
    
    sizes = [16, 32, 64, 128, 256]
    
    for n in sizes:
        A = np.random.randn(n, n).astype(np.float32)
        B = np.random.randn(n, n).astype(np.float32)
        
        # NumPy
        start = time.perf_counter()
        C_numpy = np.dot(A, B)
        t_numpy = time.perf_counter() - start
        
        # Our implementation
        start = time.perf_counter()
        from krishi_veda_fix import urdhva_matmul
        C_vedic = urdhva_matmul(A, B)
        t_vedic = time.perf_counter() - start
        
        ratio = t_vedic / t_numpy if t_numpy > 0 else 0
        print(f"n={n:3d}: NumPy {t_numpy*1000:6.2f}ms, Vedic {t_vedic*1000:6.2f}ms → {ratio:.2f}x")
        np.testing.assert_allclose(C_numpy, C_vedic, rtol=1e-5)

def benchmark_sphota_attention():
    """Benchmark Sphota O(n) attention"""
    print("\n🧠 Sphota Attention Benchmark")
    print("=" * 60)
    
    from sphota_attention import sphota_attention
    
    seq_lens = [32, 64, 128, 256, 512, 1024]
    dim = 64
    
    for seq_len in seq_lens:
        Q = np.random.randn(seq_len, dim).astype(np.float32)
        K = np.random.randn(seq_len, dim).astype(np.float32)
        V = np.random.randn(seq_len, dim).astype(np.float32)
        
        # O(n^2) standard attention
        start = time.perf_counter()
        scores = np.dot(Q, K.T) / np.sqrt(dim)
        weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        weights = weights / np.sum(weights, axis=-1, keepdims=True)
        standard_out = np.dot(weights, V)
        t_standard = time.perf_counter() - start
        
        # O(n) Sphota attention
        start = time.perf_counter()
        sphota_out = sphota_attention(Q, K, V)
        t_sphota = time.perf_counter() - start
        
        speedup = t_standard / t_sphota if t_sphota > 0 else 0
        print(f"n={seq_len:4d}: Standard {t_standard*1000:6.2f}ms, Sphota {t_sphota*1000:6.2f}ms → {speedup:5.1f}x")

def benchmark_tri_nadi():
    """Benchmark Tri-Nadi activation"""
    print("\n⚡ Tri-Nadi Activation Benchmark")
    print("=" * 60)
    
    from vedic_layers import tri_nadi
    
    sizes = [1000, 10000, 100000, 1000000]
    
    for n in sizes:
        x = np.random.randn(n).astype(np.float32)
        
        start = time.perf_counter()
        result = tri_nadi(x)
        t_vedic = time.perf_counter() - start
        
        # Compare with ReLU
        start = time.perf_counter()
        relu = np.maximum(0, x)
        t_relu = time.perf_counter() - start
        
        print(f"n={n:7d}: Tri-Nadi {t_vedic*1000:6.2f}ms, ReLU {t_relu*1000:6.2f}ms")

if __name__ == "__main__":
    print("=" * 60)
    print("🕉️ DIVINE EARTHLY - COMPLETE BENCHMARK SUITE")
    print("=" * 60)
    
    benchmark_urdhva_vs_numpy()
    benchmark_sphota_attention()
    benchmark_tri_nadi()
    
    print("\n" + "=" * 60)
    print("✅ All benchmarks completed successfully!")
    print("=" * 60)
