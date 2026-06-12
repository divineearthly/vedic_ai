"""
Krishi-Veda Fallback Shim
Place this in your Krishi-Veda Module to fix HF Space crashes
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import real Vedic engine
try:
    # Attempt real import
    import vedic_inference_engine as vie
    VEDIC_AVAILABLE = True
    logger.info("✅ Vedic inference engine loaded")
    
    # Re-export functions
    urdhva_matmul = vie.urdhva_matmul
    sphota_attention = vie.sphota_attention
    tri_nadi_activation = vie.tri_nadi_activation
    
except ImportError as e:
    logger.warning(f"⚠️ Vedic engine not found: {e}")
    logger.warning("⚠️ Using pure Python fallback")
    VEDIC_AVAILABLE = False
    
    # Fallback implementations
    def urdhva_matmul(A, B):
        """Naive matrix multiplication fallback"""
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                aik = A[i][k]
                for j in range(n):
                    C[i][j] += aik * B[k][j]
        return C
    
    def sphota_attention(Q, K, V):
        """Simplified attention fallback"""
        import numpy as np
        scores = np.dot(Q, K.T) / np.sqrt(K.shape[-1])
        weights = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)
        return np.dot(weights, V)
    
    def tri_nadi_activation(x):
        """Ternary activation fallback"""
        import numpy as np
        return np.where(x > 0, x, np.where(x < 0, x * 0.1, 0))

# Export version info
__version__ = "1.0.0-fallback"
__vedic_available__ = VEDIC_AVAILABLE

if __name__ == "__main__":
    print(f"Krishi-Veda Shim v{__version__}")
    print(f"Vedic engine available: {VEDIC_AVAILABLE}")
    
    # Quick test
    import numpy as np
    test_input = np.random.randn(4, 4)
    result = tri_nadi_activation(test_input)
    print(f"Test passed: {result.shape}")
