#!/usr/bin/env python3
"""
DAY 2: Add 100+ Knowledge Entries
Expanding Vedic knowledge base
"""

import sys
sys.path.append('/data/data/com.termux/files/home/vedic_agents')

from knowledge_expander import KnowledgeExpander

# Expanded knowledge dictionary
expanded_knowledge = {
    # Vedic Deities (15 entries)
    'Indra': 'King of gods, god of thunder and rain',
    'Agni': 'God of fire, messenger between gods and humans',
    'Varuna': 'God of cosmic order and waters',
    'Surya': 'Sun god, source of light and life',
    'Chandra': 'Moon god, associated with plants and fertility',
    'Vayu': 'God of wind and air',
    'Prithvi': 'Earth goddess, mother of all beings',
    'Saraswati': 'Goddess of knowledge, music, and arts',
    'Lakshmi': 'Goddess of wealth, fortune, and prosperity',
    'Parvati': 'Goddess of love, devotion, and power',
    'Ganesha': 'Remover of obstacles, god of beginnings',
    'Kartikeya': 'God of war and victory',
    'Hanuman': 'Monkey god, symbol of devotion and strength',
    'Krishna': 'Avatar of Vishnu, divine teacher of Bhagavad Gita',
    'Rama': 'Avatar of Vishnu, hero of Ramayana',
    
    # Vedic Concepts (15 entries)
    'Prajapati': 'Lord of creatures, creator deity',
    'Purusha': 'Cosmic being, source of universe',
    'Prakriti': 'Primordial nature, material cause of universe',
    'Gunas': 'Three qualities: Sattva, Rajas, Tamas',
    'Sattva': 'Quality of purity, harmony, goodness',
    'Rajas': 'Quality of passion, activity, movement',
    'Tamas': 'Quality of inertia, darkness, ignorance',
    'Pancha Mahabhuta': 'Five great elements',
    'Prithvi Element': 'Element of solidity and stability',
    'Apas Element': 'Element of fluidity and cohesion',
    'Agni Element': 'Element of transformation and energy',
    'Vayu Element': 'Element of movement and expansion',
    'Akasha Element': 'Element of space and consciousness',
    
    # Vedic Texts (14 entries)
    'Rigveda Samhita': 'Collection of 1028 hymns to deities',
    'Samaveda Samhita': 'Musical chants and melodies',
    'Yajurveda Samhita': 'Prose formulas for rituals',
    'Atharvaveda Samhita': 'Spells, charms, and healing',
    'Aitareya Upanishad': 'On the nature of Brahman',
    'Taittiriya Upanishad': 'On the five sheaths of self',
    'Mandukya Upanishad': 'On the syllable OM and four states',
    'Chandogya Upanishad': 'On the identity of Atman and Brahman',
    'Brihadaranyaka Upanishad': 'Largest Upanishad, on self-knowledge',
    'Shvetashvatara Upanishad': 'On the personal God and liberation',
    'Prasna Upanishad': 'Answers to six philosophical questions',
    'Mundaka Upanishad': 'On the two kinds of knowledge',
    'Kaushitaki Upanishad': 'On the cycle of rebirth',
    'Maitri Upanishad': 'On meditation and self-realization',
    
    # Vedic Rituals (10 entries)
    'Yajna': 'Sacrificial ritual, offering to gods',
    'Homa': 'Fire ritual, offering into sacred fire',
    'Puja': 'Worship ritual, offering to deity',
    'Agnihotra': 'Twice-daily fire ritual at sunrise/sunset',
    'Soma': 'Ritual drink, offered in Vedic sacrifices',
    'Sandhya Vandana': 'Daily prayer at dawn, noon, dusk',
    'Pranayama': 'Breath control, life force regulation',
    'Dhyana': 'Meditation, focused contemplation',
    'Bhajans': 'Devotional songs',
    'Kirtan': 'Call-and-response chanting',
    
    # Vedic Philosophy Schools (12 entries)
    'Nyaya': 'School of logic and epistemology (16 categories)',
    'Vaisheshika': 'School of atomism and metaphysics',
    'Samkhya': 'School of dualism (Purusha and Prakriti)',
    'Yoga Philosophy': 'School of practice and meditation (Patanjali)',
    'Mimamsa': 'School of ritual and hermeneutics',
    'Vedanta': 'School of knowledge (end of Vedas)',
    'Advaita Vedanta': 'Non-dualism (Shankara)',
    'Vishishtadvaita': 'Qualified non-dualism (Ramanuja)',
    'Dvaita': 'Dualism (Madhva)',
    'Dvaitadvaita': 'Dualistic non-dualism (Nimbarka)',
    'Shuddhadvaita': 'Pure non-dualism (Vallabha)',
    'Achintya Bheda Abheda': 'Inconceivable difference and non-difference',
    
    # Vedic Sciences (10 entries)
    'Ayurveda': 'Science of life and longevity',
    'Jyotisha': 'Vedic astrology and astronomy',
    'Vastu Shastra': 'Vedic architecture and design',
    'Dhanurveda': 'Science of archery and warfare',
    'Gandharvaveda': 'Science of music and arts',
    'Sthapatyaveda': 'Science of engineering and construction',
    'Shilpa Shastra': 'Science of sculpture and iconography',
    'Natyashastra': 'Science of drama and performance',
    
    # Vedic Ethics (10 entries)
    'Ahimsa': 'Non-violence, non-harming',
    'Satya': 'Truthfulness, honesty',
    'Asteya': 'Non-stealing, not coveting',
    'Brahmacharya': 'Celibacy, right use of energy',
    'Aparigraha': 'Non-possessiveness, non-hoarding',
    'Shaucha': 'Purity, cleanliness',
    'Santosha': 'Contentment, happiness',
    'Tapas': 'Austerity, discipline',
    'Svadhyaya': 'Self-study, scripture study',
    'Ishvara Pranidhana': 'Surrender to God',
}

def add_more_knowledge():
    """Add expanded knowledge to database"""
    
    ke = KnowledgeExpander()
    
    print("🕉️" * 50)
    print("DAY 2: ADDING KNOWLEDGE ENTRIES")
    print("🕉️" * 50)
    
    count = 0
    for topic, content in expanded_knowledge.items():
        ke.add_knowledge(topic, content, "expanded_vedic")
        count += 1
        if count % 20 == 0:
            print(f"   📚 Added {count} entries...")
    
    print(f"\n✅ Added {count} new knowledge entries!")
    
    # Show final stats
    stats = ke.get_stats()
    print(f"\n📊 FINAL DATABASE STATS:")
    print(f"   Knowledge entries: {stats['knowledge_entries']}")
    print(f"   Vedic texts: {stats['vedic_texts']}")
    print(f"   Database size: {stats['database_size']}")
    
    print("\n🕉️" * 50)
    print("DAY 2 COMPLETE!")
    print("🕉️" * 50)

if __name__ == "__main__":
    add_more_knowledge()
