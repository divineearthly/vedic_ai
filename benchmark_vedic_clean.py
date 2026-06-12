#!/usr/bin/env python3
"""
Benchmark Vedic algorithms - Clean version
"""

import time
import numpy as np

def benchmark_matmul():
    """Matrix multiplication benchmark"""
    print("\n📊 Matrix Multiplication Benchmark")
    print("=" * 50)
    sizes = [64, 128, 256, 512]
    
    for n in sizes:
        A = np.random.randn(n, n).astype(np.float32)
        B = np.random.randn(n, n).astype(np.float32)
        
        # NumPy (optimized BLAS)
        start = time.perf_counter()
        C_numpy = np.dot(A, B)
        t_numpy = time.perf_counter() - start
        
        # Naive Python
        start = time.perf_counter()
        C_python = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        t_python = time.perf_counter() - start
        
        speedup = t_python / t_numpy if t_numpy > 0 else 0
        print(f"Size {n:3d}: NumPy {t_numpy*1000:6.2f}ms, Python {t_python*1000:6.2f}ms → Speedup {speedup:5.1f}x")

def benchmark_tri_nadi():
    """Test Tri-Nadi activation"""
    print("\n📊 Tri-Nadi Activation Test")
    print("=" * 50)
    
    try:
        from vedic_layers import tri_nadi
        
        x = np.array([-10, -1, 0, 1, 10], dtype=np.float32)
        result = tri_nadi(x)
        print(f"Input:  {x}")
        print(f"Output: {result}")
        print("✅ Tri-Nadi activation working")
        
        # Benchmark
        large_x = np.random.randn(10000).astype(np.float32)
        start = time.perf_counter()
        for _ in range(100):
            _ = tri_nadi(large_x)
        t_total = time.perf_counter() - start
        print(f"Performance: {t_total*1000:.2f}ms for 100 runs of 10k elements")
        
    except ImportError as e:
        print(f"⚠️ Tri-Nadi not available: {e}")

def test_krishi_fix():
    """Test Krishi-Veda fallback"""
    print("\n📦 Krishi-Veda Fallback Fix Test")
    print("=" * 50)
    
    import krishi_veda_fix as kv
    print(f"✅ Version: {kv.__version__}")
    print(f"✅ Vedic engine available: {kv.VEDIC_AVAILABLE}")
    
    # Test matmul
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    result = kv.urdhva_matmul(A, B)
    print(f"✅ Matmul: {A} * {B} = {result}")

if __name__ == "__main__":
    print("=" * 60)
    print("🕉️ Divine Earthly Benchmark Suite")
    print("=" * 60)
    
    benchmark_matmul()
    benchmark_tri_nadi()
    test_krishi_fix()
    
    print("\n" + "=" * 60)
    print("✅ Benchmark complete!")
    print("=" * 60)
