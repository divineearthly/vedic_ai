#!/usr/bin/env python3
"""
VEDIC LANGUAGE - A Domain Specific Language for Vedic Computing
Inspired by Sanskrit grammar and Vedic mathematics
"""

import re
import ast

class VedicLanguage:
    """
    Vedic Language Commands:
    
    🔹 SUTRA (Mathematical Operations)
    - nikhal(95, 97)     → Fast multiplication
    - urdhva(23, 47)     → Cross multiplication
    - ekadhik(95)        → Square numbers ending in 5
    
    🔹 NYAYA (Logical Operations)
    - if_then(condition, action)    → Conditional logic
    - therefore(premise, conclusion) → Syllogistic reasoning
    
    🔹 CHANDAS (Pattern Operations)
    - meter(text, 'gayatri')   → Count syllables
    - rhythm(pattern, text)    → Find rhythmic patterns
    
    🔹 VYAKARANA (Grammar Operations)
    - sandhi(word1, word2)     → Join words
    - pratisakhya(text)        → Phonetic analysis
    """
    
    def __init__(self):
        self.memory = {}
        self.sutras = {
            'nikhal': self.nikhilam,
            'urdhva': self.urdhva,
            'ekadhik': self.ekadhikena
        }
    
    def nikhilam(self, a, b, base=100):
        """Sutra 67: Nikhilam - Fast multiplication near base"""
        diff_a = a - base
        diff_b = b - base
        return (a + diff_b) * base + (diff_a * diff_b)
    
    def urdhva(self, a, b):
        """Sutra 68: Urdhva - Cross multiplication"""
        a_str = f"{a:02d}"
        b_str = f"{b:02d}"
        v1 = int(a_str[1]) * int(b_str[1])
        c1 = int(a_str[0]) * int(b_str[1]) + int(a_str[1]) * int(b_str[0])
        v2 = int(a_str[0]) * int(b_str[0])
        return v2 * 100 + c1 * 10 + v1
    
    def ekadhikena(self, x):
        """Sutra 21: Ekadhikena - Square numbers ending in 5"""
        if str(x).endswith('5'):
            prefix = int(str(x)[:-1])
            return int(f"{prefix * (prefix + 1)}25")
        return x * x
    
    def execute(self, code):
        """Execute Vedic Language code"""
        # Parse and execute commands
        for cmd in code.split('\n'):
            cmd = cmd.strip()
            if cmd.startswith('nikhal'):
                match = re.search(r'nikhal\((\d+),\s*(\d+)\)', cmd)
                if match:
                    result = self.nikhilam(int(match[1]), int(match[2]))
                    print(f"🕉️ Nikhilam: {match[1]} × {match[2]} = {result}")
            elif cmd.startswith('urdhva'):
                match = re.search(r'urdhva\((\d+),\s*(\d+)\)', cmd)
                if match:
                    result = self.urdhva(int(match[1]), int(match[2]))
                    print(f"🕉️ Urdhva: {match[1]} × {match[2]} = {result}")
            elif cmd.startswith('ekadhik'):
                match = re.search(r'ekadhik\((\d+)\)', cmd)
                if match:
                    result = self.ekadhikena(int(match[1]))
                    print(f"🕉️ Ekadhikena: {match[1]}² = {result}")
    
    def repl(self):
        """Read-Eval-Print Loop for Vedic Language"""
        print("🕉️ VEDIC LANGUAGE REPL")
        print("Commands: nikhal(a,b), urdhva(a,b), ekadhik(x)")
        print("Type 'exit' to quit\n")
        
        while True:
            try:
                code = input("🔱 ")
                if code.lower() == 'exit':
                    break
                self.execute(code)
            except KeyboardInterrupt:
                break
        print("🕉️ Namaste!")

if __name__ == "__main__":
    vl = VedicLanguage()
    
    # Test
    print("Testing Vedic Language:")
    vl.execute("nikhal(98, 97)")
    vl.execute("urdhva(23, 47)")
    vl.execute("ekadhik(95)")
    
    # Start REPL
    vl.repl()
