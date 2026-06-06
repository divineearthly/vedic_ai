#!/usr/bin/env python3
"""
Train your model to understand Vedic Language
Creates fine-tuning dataset for your 135M model
"""

import json

# Training dataset - Vedic Language examples
training_data = [
    # Multiplication Sutras
    {"instruction": "Calculate 95 squared", "input": "", "output": "sutra1(95) = 9025"},
    {"instruction": "Multiply 98 by 97", "input": "", "output": "sutra2(98,97) = 9506"},
    {"instruction": "Cross multiply 23 by 47", "input": "", "output": "sutra3(23,47) = 1081"},
    {"instruction": "What is 95²?", "input": "", "output": "Using Ekadhikena Sutra: 95² = 9025"},
    
    # Division Sutras
    {"instruction": "Divide 100 by 9", "input": "", "output": "sutra4(100,9) = (11, 1)"},
    {"instruction": "What is 100 ÷ 9?", "input": "", "output": "Using Paravartya Sutra: 100 ÷ 9 = 11 remainder 1"},
    
    # Square Sutras
    {"instruction": "Square 25", "input": "", "output": "Ekadhikena: 25² = 625"},
    {"instruction": "Square 45", "input": "", "output": "Ekadhikena: 45² = 2025"},
    {"instruction": "Square 85", "input": "", "output": "Ekadhikena: 85² = 7225"},
    
    # Fast multiplication
    {"instruction": "Multiply 96 by 94", "input": "", "output": "Nikhilam: 96 × 94 = 9024"},
    {"instruction": "Multiply 97 by 93", "input": "", "output": "Nikhilam: 97 × 93 = 9021"},
    {"instruction": "Multiply 99 by 98", "input": "", "output": "Nikhilam: 99 × 98 = 9702"},
    
    # Philosophical queries
    {"instruction": "What is Brahman?", "input": "", "output": "Brahman is the ultimate reality, pure consciousness, the source of all existence."},
    {"instruction": "Explain Dharma", "input": "", "output": "Dharma is righteous duty, cosmic order, and truth. It is the path of living in harmony."},
    {"instruction": "What is Karma Yoga?", "input": "", "output": "Karma Yoga is the path of selfless action performed without attachment to results."},
    {"instruction": "What is Moksha?", "input": "", "output": "Moksha is liberation from the cycle of birth and death, realization of one's true nature."},
    {"instruction": "What is Advaita?", "input": "", "output": "Advaita teaches non-duality - the identity of Atman (individual self) and Brahman (universal consciousness)."},
]

# Save as JSON for fine-tuning
with open('/data/data/com.termux/files/home/vedic_training.json', 'w') as f:
    json.dump(training_data, f, indent=2)

print(f"✅ Training dataset created: {len(training_data)} examples")
print("\n📚 Sample training data:")
print(json.dumps(training_data[0], indent=2))
