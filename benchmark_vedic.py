#!/usr/bin/env python3
"""
Benchmark Vedic algorithms vs standard implementations
"""

import time
import numpy as np
from vedic_layers import VedicMultiheadAttention, StandardMultiheadAttention

def benchmark_attention():
    """Benchmark Sphota attention vs standard"""
    seq_lens = [64, 128, 256, 512, 1024, 2048]
    d_model = 512
    n_heads = 8
    
    results = {}
    
    for seq_len in seq_lens:
        # Create random input
        x = np.random.randn(seq_len, d_model).astype(np.float32)
        
        # Standard attention
        standard = StandardMultiheadAttention(d_model, n_heads)
        start = time.perf_counter()
        out1 = standard(x)
        t_standard = time.perf_counter() - start
        
        # Vedic Sphota attention
        vedic = VedicMultiheadAttention(d_model, n_heads)
        start = time.perf_counter()
        out2 = vedic(x)
        t_vedic = time.perf_counter() - start
        
        speedup = t_standard / t_vedic if t_vedic > 0 else 0
        results[seq_len] = {
            'standard_ms': t_standard * 1000,
            'vedic_ms': t_vedic * 1000,
            'speedup': speedup
        }
        
        print(f"Seq len {seq_len:4d}: Standard {t_standard*1000:6.2f}ms, "
              f"Vedic {t_vedic*1000:6.2f}ms, Speedup {speedup:5.1f}x")
    
    return results

def benchmark_matmul():
    """Benchmark Urdhva matmul"""
    sizes = [32, 64, 128, 256, 512]
    
    for n in sizes:
        A = np.random.randn(n, n).astype(np.float32)
        B = np.random.randn(n, n).astype(np.float32)
        
        # NumPy (highly optimized)
        start = time.perf_counter()
        C1 = np.dot(A, B)
        t_numpy = time.perf_counter() - start
        
        # Pure Python naive
        start = time.perf_counter()
        C2 = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        t_python = time.perf_counter() - start
        
        print(f"Size {n:3d}: NumPy {t_numpy*1000:6.2f}ms, Python {t_python*1000:6.2f}ms, "
              f"NumPy speedup {t_python/t_numpy:5.1f}x")

if __name__ == "__main__":
    print("=" * 60)
    print("Vedic Algorithm Benchmark Suite")
    print("=" * 60)
    
    print("\n📊 Attention Benchmark (Sphota vs Standard)")
    print("-" * 60)
    benchmark_attention()
    
    print("\n📊 Matrix Multiplication Benchmark")
    print("-" * 60)
    benchmark_matmul()
    
    print("\n✅ Benchmark complete")
