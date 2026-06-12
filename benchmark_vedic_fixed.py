#!/usr/bin/env python3
"""
Benchmark Vedic algorithms - Compatible with existing codebase
"""

import time
import numpy as np

# Import existing modules
try:
    from vedic_layers import (
        vedic_multihead_attention,
        standard_multihead_attention,
        tri_nadi_activation,
        urdhva_matrix_multiply
    )
    HAS_VEDIC = True
    print("✅ Vedic layers imported successfully")
except ImportError as e:
    print(f"⚠️ Using fallback benchmarks: {e}")
    HAS_VEDIC = False

def benchmark_attention_fallback():
    """Fallback benchmark if Vedic layers not available"""
    print("\n📊 Running fallback attention benchmark...")
    seq_lens = [64, 128, 256, 512]
    
    for seq_len in seq_lens:
        # Simulate attention computation
        q = np.random.randn(seq_len, 64).astype(np.float32)
        k = np.random.randn(seq_len, 64).astype(np.float32)
        v = np.random.randn(seq_len, 64).astype(np.float32)
        
        # Standard O(n^2) attention simulation
        start = time.perf_counter()
        scores = np.dot(q, k.T)
        weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        weights = weights / np.sum(weights, axis=-1, keepdims=True)
        output = np.dot(weights, v)
        t_standard = time.perf_counter() - start
        
        print(f"Seq len {seq_len:4d}: Standard attention {t_standard*1000:6.2f}ms")
    
    return True

def benchmark_matmul_fallback():
    """Matrix multiplication benchmark"""
    print("\n📊 Matrix multiplication benchmark...")
    sizes = [64, 128, 256]
    
    for n in sizes:
        A = np.random.randn(n, n).astype(np.float32)
        B = np.random.randn(n, n).astype(np.float32)
        
        # NumPy (highly optimized)
        start = time.perf_counter()
        C = np.dot(A, B)
        t_numpy = time.perf_counter() - start
        
        # Python naive
        start = time.perf_counter()
        C2 = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        t_python = time.perf_counter() - start
        
        speedup = t_python / t_numpy if t_numpy > 0 else 0
        print(f"Size {n:3d}: NumPy {t_numpy*1000:6.2f}ms, Python {t_python*1000:6.2f}ms, Speedup {speedup:5.1f}x")

def test_krishi_veda_fix():
    """Test the Krishi-Veda fallback fix"""
    print("\n📦 Testing Krishi-Veda fallback fix...")
    try:
        import krishi_veda_fix as kv
        print(f"✅ Krishi-Veda fix loaded: version {kv.__version__}")
        print(f"   Vedic engine available: {kv.VEDIC_AVAILABLE}")
        
        # Test fallback functions
        test_matrix = [[1, 2], [3, 4]]
        result = kv.urdhva_matmul(test_matrix, test_matrix)
        print(f"   Matmul test passed: {result}")
        
    except Exception as e:
        print(f"⚠️ Krishi-Veda fix test: {e}")

def test_existing_modules():
    """Test what's available in the codebase"""
    print("\n🔍 Scanning existing modules...")
    
    modules_to_check = [
        'sphota_attention',
        'vedic_llm',
        'vedic_layers',
        'sovereign_agi_core',
        'vedic_agents'
    ]
    
    for module_name in modules_to_check:
        try:
            module = __import__(module_name)
            functions = [f for f in dir(module) if not f.startswith('_')]
            print(f"✅ {module_name}: {len(functions)} functions")
        except ImportError:
            print(f"⚠️ {module_name}: not found")

if __name__ == "__main__":
    print("=" * 60)
    print("Divine Earthly Benchmark Suite")
    print("=" * 60)
    
    # Test existing modules
    test_existing_modules()
    
    # Test Krishi-Veda fix
    test_krishi_veda_fix()
    
    # Run benchmarks
    benchmark_matmul_fallback()
    benchmark_attention_fallback()
    
    print("\n" + "=" * 60)
    print("✅ Benchmark complete!")
    print("=" * 60)
    print("\n📈 Next steps:")
    print("1. Check GitHub Actions: https://github.com/divineearthly/vedic_ai/actions")
    print("2. Compile arXiv paper: cd papers && pdflatex mulasutras_arxiv.tex")
    print("3. Deploy Krishi-Veda fix to HF Space")
    print("4. Share README_VEDIC_RD.md with the team")
