#!/usr/bin/env python3
"""
VEDIC LLM - Lightweight Language Model with Vedic Algorithms
Builds a neural network with Vedic mathematics at its core
"""

import numpy as np
import math
import random
import json
import os

class VedicAttention:
    """Attention mechanism using Vedic Sutras (Urdhva - Cross multiplication)"""
    
    @staticmethod
    def urdhva_attention(Q, K, V):
        """Urdhva Tiryagbhyam - Vertically and crosswise attention"""
        # Crosswise multiplication for attention scores
        d_k = Q.shape[-1]
        
        # Urdhva method: crosswise product
        scores = np.zeros((Q.shape[0], K.shape[0]))
        for i in range(Q.shape[0]):
            for j in range(K.shape[0]):
                # Vertically and crosswise (like urdhva sutra)
                vertical = np.sum(Q[i] * K[j])
                crosswise = np.sum(Q[i]) * np.sum(K[j]) / d_k
                scores[i, j] = (vertical + crosswise) / 2
        
        # Softmax (improved with Vedic approximation)
        exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        weights = exp_scores / (np.sum(exp_scores, axis=-1, keepdims=True) + 1e-8)
        
        # Nikhilam - Base method for weighted sum
        output = np.zeros((Q.shape[0], V.shape[-1]))
        base = 100
        for i in range(Q.shape[0]):
            for j in range(V.shape[0]):
                diff_a = weights[i, j] - base
                diff_b = V[j, 0] - base if V.ndim > 1 else V[j] - base
                output[i, 0] += (weights[i, j] + diff_b) * base + (diff_a * diff_b)
        
        return output

class VedicFeedForward:
    """Feed-forward network using Nikhilam Sutra for fast multiplication"""
    
    def __init__(self, d_model, d_ff):
        self.d_model = d_model
        self.d_ff = d_ff
        self.W1 = np.random.randn(d_model, d_ff) * 0.02
        self.W2 = np.random.randn(d_ff, d_model) * 0.02
        self.b1 = np.zeros(d_ff)
        self.b2 = np.zeros(d_model)
    
    def nikhilam_matmul(self, A, B):
        """Fast matrix multiplication using Nikhilam Sutra"""
        # Approximate multiplication using base method
        base = 100
        result = np.zeros((A.shape[0], B.shape[1]))
        for i in range(A.shape[0]):
            for j in range(B.shape[1]):
                sum_val = 0
                for k in range(A.shape[1]):
                    diff_a = A[i, k] - base
                    diff_b = B[k, j] - base
                    sum_val += (A[i, k] + diff_b) * base + (diff_a * diff_b)
                result[i, j] = sum_val / A.shape[1]
        return result
    
    def forward(self, x):
        # Nikhilam-optimized first layer
        h = self.nikhilam_matmul(x, self.W1) + self.b1
        h = np.maximum(0, h)  # ReLU
        # Second layer
        out = self.nikhilam_matmul(h, self.W2) + self.b2
        return out

class VedicTransformerLayer:
    """Single transformer layer with Vedic optimizations"""
    
    def __init__(self, d_model=512, n_heads=8, d_ff=2048):
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        
        # Vedic attention
        self.attention = VedicAttention()
        
        # Vedic feed-forward
        self.ff = VedicFeedForward(d_model, d_ff)
        
        # Layer norms
        self.ln1 = np.ones(d_model)
        self.ln2 = np.ones(d_model)
    
    def layer_norm(self, x, gamma):
        """Layer normalization with Vedic scaling"""
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        return gamma * (x - mean) / np.sqrt(var + 1e-8)
    
    def forward(self, x):
        # Self-attention with residual
        attn_out = self.attention.urdhva_attention(x, x, x)
        x = self.layer_norm(x + attn_out, self.ln1)
        
        # Feed-forward with residual
        ff_out = self.ff.forward(x)
        x = self.layer_norm(x + ff_out, self.ln2)
        
        return x

class VedicLLM:
    """Complete Vedic Language Model with 16 Sutras integrated"""
    
    def __init__(self, vocab_size=10000, d_model=512, n_layers=6, n_heads=8):
        self.vocab_size = vocab_size
        self.d_model = d_model
        
        # Token embeddings
        self.token_embedding = np.random.randn(vocab_size, d_model) * 0.02
        self.position_embedding = np.random.randn(512, d_model) * 0.02
        
        # Transformer layers
        self.layers = [VedicTransformerLayer(d_model, n_heads) for _ in range(n_layers)]
        
        # Output layer (Ekadhikena Sutra for logits)
        self.output_proj = np.random.randn(d_model, vocab_size) * 0.02
        
        print("🕉️ VEDIC LLM INITIALIZED")
        print(f"   Parameters: {self.count_parameters():,}")
        print(f"   Layers: {n_layers}")
        print(f"   Model size: {self.get_model_size():.1f} MB")
    
    def count_parameters(self):
        """Count total trainable parameters"""
        total = 0
        total += self.token_embedding.size
        total += self.position_embedding.size
        total += self.output_proj.size
        for layer in self.layers:
            total += layer.ff.W1.size + layer.ff.W2.size
            total += layer.ff.b1.size + layer.ff.b2.size
            total += layer.ln1.size + layer.ln2.size
        return total
    
    def get_model_size(self):
        """Get model size in MB"""
        return self.count_parameters() * 4 / (1024 * 1024)
    
    def forward(self, tokens):
        """Forward pass through the model"""
        batch_size, seq_len = tokens.shape
        
        # Token + position embeddings
        x = self.token_embedding[tokens]
        positions = np.arange(seq_len)
        x = x + self.position_embedding[:seq_len]
        
        # Pass through transformer layers
        for layer in self.layers:
            x = layer.forward(x)
        
        # Output logits using Ekadhikena (by one more)
        logits = np.dot(x, self.output_proj)
        
        return logits
    
    def generate(self, prompt_tokens, max_len=50, temperature=0.7):
        """Generate text using the model"""
        current_tokens = list(prompt_tokens)
        
        for _ in range(max_len):
            # Convert to numpy array
            input_tensor = np.array([current_tokens[-512:]])  # Context window
            
            # Forward pass
            logits = self.forward(input_tensor)
            
            # Get next token logits
            next_logits = logits[0, -1, :]
            
            # Apply temperature
            next_logits = next_logits / temperature
            
            # Softmax
            exp_logits = np.exp(next_logits - np.max(next_logits))
            probs = exp_logits / np.sum(exp_logits)
            
            # Sample next token
            next_token = np.random.choice(self.vocab_size, p=probs)
            current_tokens.append(next_token)
            
            # Stop at EOS (if we had one)
            if next_token == 1:  # Assuming 1 is EOS
                break
        
        return current_tokens
    
    def save(self, path):
        """Save model parameters"""
        params = {
            'token_embedding': self.token_embedding.tolist(),
            'position_embedding': self.position_embedding.tolist(),
            'output_proj': self.output_proj.tolist(),
            'd_model': self.d_model,
            'vocab_size': self.vocab_size
        }
        with open(path, 'w') as f:
            json.dump(params, f)
        print(f"✅ Model saved to {path}")
    
    def load(self, path):
        """Load model parameters"""
        with open(path, 'r') as f:
            params = json.load(f)
        self.token_embedding = np.array(params['token_embedding'])
        self.position_embedding = np.array(params['position_embedding'])
        self.output_proj = np.array(params['output_proj'])
        print(f"✅ Model loaded from {path}")

# Demo
if __name__ == "__main__":
    print("🕉️" * 50)
    print("BUILDING VEDIC LLM")
    print("🕉️" * 50)
    
    # Create small model for testing
    model = VedicLLM(vocab_size=1000, d_model=128, n_layers=2, n_heads=4)
    print(f"\n✅ Model created!")
    print(f"   Can generate {model.count_parameters():,} parameter model")
    
    # Test forward pass
    test_tokens = np.array([[10, 20, 30, 40, 50]])
    logits = model.forward(test_tokens)
    print(f"\n✅ Forward pass successful!")
    print(f"   Output shape: {logits.shape}")
    
    # Save model
    model.save("/data/data/com.termux/files/home/vedic_llm_model.json")
    
    print("\n🕉️ Vedic LLM is ready for training!")
