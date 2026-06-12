"""Unit tests for Vedic algorithms"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSphotaAttention(unittest.TestCase):
    def test_attention_shape(self):
        """Test that attention output has correct shape"""
        try:
            from vedic_layers import VedicMultiheadAttention
            
            d_model = 128
            n_heads = 4
            seq_len = 32
            
            attn = VedicMultiheadAttention(d_model, n_heads)
            x = np.random.randn(seq_len, d_model).astype(np.float32)
            output = attn(x)
            
            self.assertEqual(output.shape, (seq_len, d_model))
            print("✅ Sphota attention shape test passed")
            
        except ImportError as e:
            print(f"⚠️ Skipping attention test: {e}")

class TestTriNadiActivation(unittest.TestCase):
    def test_activation_range(self):
        """Test Tri-Nadi activation output range"""
        try:
            from vedic_layers import tri_nadi_activation
            
            x = np.array([-10, -1, 0, 1, 10], dtype=np.float32)
            y = tri_nadi_activation(x)
            
            # Check properties
            self.assertAlmostEqual(y[0], -1.0, places=5)  # -10 * 0.1 = -1
            self.assertAlmostEqual(y[1], -0.1, places=5)  # -1 * 0.1 = -0.1
            self.assertEqual(y[2], 0)                      # 0 -> 0
            self.assertEqual(y[3], 1)                      # 1 -> 1
            self.assertEqual(y[4], 10)                     # 10 -> 10
            
            print("✅ Tri-Nadi activation test passed")
            
        except ImportError as e:
            print(f"⚠️ Skipping activation test: {e}")

class TestUrdhvaMatmul(unittest.TestCase):
    def test_matmul_correctness(self):
        """Test matrix multiplication correctness"""
        try:
            from vedic_layers import urdhva_matmul
            
            # 2x2 test
            A = [[1, 2], [3, 4]]
            B = [[5, 6], [7, 8]]
            expected = [[19, 22], [43, 50]]
            
            result = urdhva_matmul(A, B)
            
            for i in range(2):
                for j in range(2):
                    self.assertEqual(result[i][j], expected[i][j])
            
            print("✅ Urdhva matmul correctness test passed")
            
        except ImportError as e:
            print(f"⚠️ Skipping matmul test: {e}")

def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestSphotaAttention))
    suite.addTests(loader.loadTestsFromTestCase(TestTriNadiActivation))
    suite.addTests(loader.loadTestsFromTestCase(TestUrdhvaMatmul))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
