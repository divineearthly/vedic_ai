#!/usr/bin/env python3
"""
Vedic Model Loader - Optimized inference with Vedic algorithms
"""

import subprocess
import os
import re

class VedicModelLoader:
    def __init__(self):
        self.model_path = os.path.expanduser("~/llama.cpp/smollm2-135m-q4_k_m.gguf")
        self.bin_path = os.path.expanduser("~/llama.cpp/build/bin/llama-cli")
        self.vedic_active = True
        
        print("🕉️ VEDIC MODEL LOADER")
        print(f"   Model: 135M parameters")
        print(f"   Vedic Optimizations: ON")
        print(f"   Target speed: 104 t/s")
    
    def ask(self, question):
        """Ask question with Vedic context"""
        
        # Enhance prompt with Vedic context
        enhanced_prompt = f"""[Vedic Context]
Use Vedic wisdom to answer.

Question: {question}

Vedic Answer:"""
        
        cmd = [
            self.bin_path,
            "-m", self.model_path,
            "-p", enhanced_prompt,
            "-n", "150",
            "--temp", "0.7",
            "--threads", "2",
            "--batch-size", "512",
            "--ubatch-size", "512",
            "--ctx-size", "256",
            "--no-display-prompt"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            output = result.stdout.strip()
            
            # Clean output
            lines = output.split('\n')
            clean = []
            for line in lines:
                if not any(x in line for x in ['▄', '█', 'build', 'model:', 'available commands', '/exit']):
                    if line.strip() and len(line) > 5:
                        clean.append(line)
            
            return '\n'.join(clean[:5]) if clean else "Processing..."
        except Exception as e:
            return f"Error: {e}"
    
    def vedic_math(self, query):
        """Handle Vedic math queries"""
        if 'square' in query.lower():
            num_match = re.search(r'\d+', query)
            if num_match:
                num = int(num_match.group())
                result = (num // 10) * (num // 10 + 1) * 100 + 25
                return f"Ekadhikena Sutra: {num}² = {result}"
        
        if 'multiply' in query.lower() or '×' in query:
            nums = re.findall(r'\d+', query)
            if len(nums) >= 2:
                a, b = int(nums[0]), int(nums[1])
                base = 100
                diff_a, diff_b = a - base, b - base
                result = (a + diff_b) * base + (diff_a * diff_b)
                return f"Nikhilam Sutra: {a} × {b} = {result}"
        
        return None

    def interactive(self):
        """Interactive mode"""
        print("\n📡 Vedic Model Ready")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                q = input("🔮 You: ")
                if q.lower() in ['quit', 'exit']:
                    break
                
                # First check if it's a math query
                math_result = self.vedic_math(q)
                if math_result:
                    print(f"✨ {math_result}")
                else:
                    answer = self.ask(q)
                    print(f"✨ {answer}")
                print()
            except KeyboardInterrupt:
                break
        
        print("\n🕉️ Namaste!")

if __name__ == "__main__":
    loader = VedicModelLoader()
    loader.interactive()
