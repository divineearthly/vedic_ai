#!/usr/bin/env python3
"""
VEDIC COMPILER - Compiles Vedic Language to Python
"""

import re
import ast

class VedicCompiler:
    def compile(self, vedic_code):
        """Compile Vedic Language to Python"""
        
        patterns = [
            (r'nikhal\((\d+),\s*(\d+)\)',
             lambda m: f'({m[1]} - 100 + {m[2]} - 100) * 100 + ({m[1]} - 100) * ({m[2]} - 100)'),
            (r'urdhva\((\d+),\s*(\d+)\)',
             lambda m: f'(({m[1]}//10)*({m[2]}//10))*100 + (({m[1]}//10)*({m[2]}%10) + ({m[1]}%10)*({m[2]}//10))*10 + ({m[1]}%10)*({m[2]}%10)'),
            (r'ekadhik\((\d+)\)',
             lambda m: f'({m[1]}//10) * ({m[1]}//10 + 1) * 100 + 25'),
        ]
        
        python_code = vedic_code
        for pattern, replacer in patterns:
            python_code = re.sub(pattern, replacer, python_code)
        return python_code
    
    def execute(self, vedic_code):
        """Compile and execute Vedic code"""
        python_code = self.compile(vedic_code)
        try:
            result = eval(python_code)
            return result
        except Exception as e:
            return f"Error: {e}"

# Test
vc = VedicCompiler()
test_code = "nikhal(98, 97)"
print(f"Vedic: {test_code}")
print(f"Python: {vc.compile(test_code)}")
print(f"Result: {vc.execute(test_code)}")
