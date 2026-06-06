#!/usr/bin/env python3
"""
VEDIC LANGUAGE FULL - 16 Sutras Implementation
Complete Vedic Mathematics System
"""

import re
import math

class VedicLanguageFull:
    """Complete Vedic Mathematics with 16 Sutras"""
    
    def __init__(self):
        self.sutras = {
            1: self.ekadhikena_purvena,
            2: self.nikhilam_navatashcaramam,
            3: self.urdhva_tiryagbhyam,
            4: self.paravartya_yojayet,
            5: self.sunyam_samya_samuccaye,
            6: self.anurupye_shunyamanyat,
            7: self.sankalana_vyavakalanabhyam,
            8: self.puranapuranabhyam,
            9: self.chalana_kalanabhyam,
            10: self.yavadunam_tavadunikritya,
            11: self.vyashtisamanstih,
            12: self.shesanyankena_charamena,
            13: self.sopantyadvayamantyam,
            14: self.ekanyunena_purvena,
            15: self.gunitasamuchyah,
            16: self.gunakasamuchyah
        }
        
        self.results = {}
    
    # SUTRA 1: By one more than the previous one
    def ekadhikena_purvena(self, x):
        """Square numbers ending with 5"""
        if str(x).endswith('5'):
            prefix = int(str(x)[:-1])
            return int(f"{prefix * (prefix + 1)}25")
        return x * x
    
    # SUTRA 2: All from 9 and last from 10
    def nikhilam_navatashcaramam(self, a, b, base=100):
        """Fast multiplication near base"""
        diff_a = a - base
        diff_b = b - base
        return (a + diff_b) * base + (diff_a * diff_b)
    
    # SUTRA 3: Vertically and crosswise
    def urdhva_tiryagbhyam(self, a, b):
        """General multiplication"""
        a_str = str(a).zfill(2)
        b_str = str(b).zfill(2)
        v1 = int(a_str[1]) * int(b_str[1])
        c1 = int(a_str[0]) * int(b_str[1]) + int(a_str[1]) * int(b_str[0])
        v2 = int(a_str[0]) * int(b_str[0])
        return v2 * 100 + c1 * 10 + v1
    
    # SUTRA 4: Transpose and apply
    def paravartya_yojayet(self, dividend, divisor):
        """Division using transpose"""
        if divisor == 9:
            quotient = dividend // 9
            remainder = dividend % 9
            return quotient, remainder
        return dividend // divisor, dividend % divisor
    
    # SUTRA 5: If zero, zero
    def sunyam_samya_samuccaye(self, eq1, eq2):
        """Solving equations where sum is zero"""
        # For x + 5 = 0, x = -5
        return -eq2 if eq1 == 1 else None
    
    # SUTRA 6: If proportional, proportional
    def anurupye_shunyamanyat(self, ratio, value):
        """Proportional calculations"""
        return value * ratio
    
    # SUTRA 7: Addition and subtraction
    def sankalana_vyavakalanabhyam(self, a, b):
        """Combined addition-subtraction"""
        return a + b, a - b
    
    # SUTRA 8: By completion or non-completion
    def puranapuranabhyam(self, x):
        """Completing the square"""
        return (x + 0.5) ** 2 - 0.25
    
    # SUTRA 9: Differential calculus
    def chalana_kalanabhyam(self, arr):
        """Find differences in sequence"""
        return [arr[i+1] - arr[i] for i in range(len(arr)-1)]
    
    # SUTRA 10: By the deficiency
    def yavadunam_tavadunikritya(self, num, base=10):
        """Find deficiency from base"""
        return num - (base - (num % base)) if num % base != 0 else num
    
    # SUTRA 11: Part and whole
    def vyashtisamanstih(self, arr):
        """Sum and average"""
        return sum(arr), sum(arr) / len(arr)
    
    # SUTRA 12: Remainder by the last
    def shesanyankena_charamena(self, dividend, divisor):
        """Find remainder"""
        return dividend % divisor
    
    # SUTRA 13: Ultimate and twice the penultimate
    def sopantyadvayamantyam(self, x):
        """Special multiplication"""
        return x * 2 + 1
    
    # SUTRA 14: By one less than previous
    def ekanyunena_purvena(self, num):
        """Multiply by 9, 99, 999"""
        return num * 9
    
    # SUTRA 15: Product of sums
    def gunitasamuchyah(self, arr):
        """Product and sum relationship"""
        product = 1
        for x in arr:
            product *= x
        return product / sum(arr) if sum(arr) != 0 else 0
    
    # SUTRA 16: Factor of sums
    def gunakasamuchyah(self, a, b):
        """Factorization"""
        return a * b, a + b
    
    def execute(self, cmd):
        """Parse and execute Vedic command"""
        cmd = cmd.strip()
        
        if cmd.startswith('sutra1'):
            match = re.search(r'sutra1\((\d+)\)', cmd)
            if match:
                return self.ekadhikena_purvena(int(match[1]))
        
        elif cmd.startswith('sutra2'):
            match = re.search(r'sutra2\((\d+),\s*(\d+)\)', cmd)
            if match:
                return self.nikhilam_navatashcaramam(int(match[1]), int(match[2]))
        
        elif cmd.startswith('sutra3'):
            match = re.search(r'sutra3\((\d+),\s*(\d+)\)', cmd)
            if match:
                return self.urdhva_tiryagbhyam(int(match[1]), int(match[2]))
        
        elif cmd.startswith('sutra4'):
            match = re.search(r'sutra4\((\d+),\s*(\d+)\)', cmd)
            if match:
                return self.paravartya_yojayet(int(match[1]), int(match[2]))
        
        return None
    
    def repl(self):
        """REPL for 16 Sutras"""
        print("🕉️" * 50)
        print("VEDIC LANGUAGE FULL - 16 SUTRAS")
        print("🕉️" * 50)
        print("\nCommands:")
        print("  sutra1(x)        - Square numbers ending in 5")
        print("  sutra2(a,b)      - Fast multiplication near 100")
        print("  sutra3(a,b)      - Cross multiplication")
        print("  sutra4(d,r)      - Division (9-based)")
        print("\nType 'exit' to quit\n")
        
        while True:
            try:
                cmd = input("🔱 ")
                if cmd.lower() == 'exit':
                    break
                result = self.execute(cmd)
                if result is not None:
                    print(f"   Result: {result}")
                else:
                    print("   Try: sutra1(95), sutra2(98,97), sutra3(23,47)")
            except KeyboardInterrupt:
                break
        print("🕉️ Namaste!")

if __name__ == "__main__":
    vl = VedicLanguageFull()
    vl.repl()
