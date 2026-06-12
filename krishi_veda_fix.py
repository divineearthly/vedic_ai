"""
Krishi-Veda Fallback Shim - Fixed Version
Place this in your Krishi-Veda Module to fix HF Space crashes
"""

import sys
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import real Vedic engine from existing modules
VEDIC_AVAILABLE = False

try:
    # Try to import from existing codebase
    from vedic_layers import tri_nadi, ChittaKVCache, VedicFeedForward
    from sphota_attention import sphota_attention
    
    VEDIC_AVAILABLE = True
    logger.info("✅ Vedic layers loaded from existing codebase")
    
    # Wrapper functions
    def urdhva_matmul(A, B):
        """Matrix multiplication using numpy (fallback if pure Vedic not available)"""
        return np.dot(A, B)
    
    def sphota_attention_wrapper(Q, K, V):
        return sphota_attention(Q, K, V)
    
    def tri_nadi_activation(x):
        return tri_nadi(x)
    
except ImportError as e:
    logger.warning(f"⚠️ Vedic engine not found: {e}")
    logger.warning("⚠️ Using pure Python fallback")
    VEDIC_AVAILABLE = False
    
    # Fallback implementations
    def urdhva_matmul(A, B):
        """Naive matrix multiplication fallback"""
        A = np.array(A) if not isinstance(A, np.ndarray) else A
        B = np.array(B) if not isinstance(B, np.ndarray) else B
        return np.dot(A, B)
    
    def sphota_attention_wrapper(Q, K, V):
        """Simplified attention fallback"""
        scores = np.dot(Q, K.T) / np.sqrt(K.shape[-1])
        weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        weights = weights / np.sum(weights, axis=-1, keepdims=True)
        return np.dot(weights, V)
    
    def tri_nadi_activation(x):
        """Ternary activation fallback"""
        return np.where(x > 0, x, np.where(x < 0, x * 0.1, 0))

# Export version info
__version__ = "1.0.1-fixed"
__all__ = ['urdhva_matmul', 'sphota_attention_wrapper', 'tri_nadi_activation', 'VEDIC_AVAILABLE']

if __name__ == "__main__":
    print(f"Krishi-Veda Shim v{__version__}")
    print(f"Vedic engine available: {VEDIC_AVAILABLE}")
    
    # Quick test
    test_matrix = np.random.randn(4, 4)
    result = urdhva_matmul(test_matrix, test_matrix)
    print(f"Test passed: {result.shape}")
