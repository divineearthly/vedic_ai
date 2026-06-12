#!/usr/bin/env python3
"""Simple test of Vedic algorithms"""

import numpy as np

# Test 1: Import vedic_layers
print("1. Testing vedic_layers...")
try:
    from vedic_layers import tri_nadi, ChittaKVCache
    print("   ✅ tri_nadi and ChittaKVCache imported")
    
    # Test Tri-Nadi
    x = np.array([-2, -1, 0, 1, 2])
    y = tri_nadi(x)
    print(f"   ✅ tri_nadi({x}) = {y}")
    
    # Test Chitta cache
    cache = ChittaKVCache(max_cached=10, dim=4)
    print(f"   ✅ ChittaKVCache created")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Test sphota_attention
print("\n2. Testing sphota_attention...")
try:
    import sphota_attention
    print(f"   ✅ sphota_attention module loaded")
    print(f"   Functions: {[x for x in dir(sphota_attention) if not x.startswith('_')]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Test krishi_veda_fix
print("\n3. Testing krishi_veda_fix...")
try:
    import krishi_veda_fix
    print(f"   ✅ Version: {krishi_veda_fix.__version__}")
    print(f"   ✅ Vedic available: {krishi_veda_fix.VEDIC_AVAILABLE}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n✅ All tests complete!")
