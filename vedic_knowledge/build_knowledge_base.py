#!/usr/bin/env python3
"""
Build Knowledge Base - Add Vedic texts and knowledge
"""

import sys
sys.path.append('/data/data/com.termux/files/home/vedic_agents')

from knowledge_expander import KnowledgeExpander
from wikipedia_integration import WikipediaIntegration

def build_vedic_knowledge():
    """Build complete Vedic knowledge base"""
    
    ke = KnowledgeExpander()
    wi = WikipediaIntegration()
    
    print("🕉️" * 50)
    print("BUILDING VEDIC KNOWLEDGE BASE")
    print("🕉️" * 50)
    
    # Add core Vedic texts
    vedic_texts = {
        'Rig Veda': 'The oldest Veda, containing hymns to deities',
        'Yajur Veda': 'Veda of sacrificial formulas',
        'Sama Veda': 'Veda of melodies and chants',
        'Atharva Veda': 'Veda of spells and healing',
        'Isha Upanishad': 'The essence of Vedanta',
        'Katha Upanishad': 'Dialogue between Yama and Nachiketa',
        'Bhagavad Gita': 'Song of God, Krishna\'s teachings',
        'Brahma Sutras': 'Systematizing Vedanta philosophy'
    }
    
    print("\n📜 Adding Vedic Texts...")
    for title, content in vedic_texts.items():
        ke.add_vedic_text(title, content)
        print(f"   ✅ {title}")
    
    # Add philosophical concepts
    concepts = {
        'Brahman': 'The ultimate reality, absolute consciousness, source of all existence',
        'Atman': 'The individual self, identical with Brahman',
        'Maya': 'The illusion that veils the true nature of reality',
        'Dharma': 'Righteous duty, cosmic order, truth',
        'Karma': 'Action and its consequences, law of cause and effect',
        'Moksha': 'Liberation from cycle of rebirth',
        'Advaita': 'Non-duality, the teaching that Atman is Brahman',
        'Jnana': 'Knowledge, wisdom, spiritual insight',
        'Bhakti': 'Devotion, love for the divine',
        'Karma Yoga': 'Path of selfless action',
        'Bhakti Yoga': 'Path of devotion',
        'Jnana Yoga': 'Path of knowledge',
        'Raja Yoga': 'Path of meditation'
    }
    
    print("\n🧠 Adding Philosophical Concepts...")
    for concept, content in concepts.items():
        ke.add_knowledge(concept, content, "vedic_philosophy")
        print(f"   ✅ {concept}")
    
    # Fetch Wikipedia articles
    print("\n🌐 Fetching from Wikipedia...")
    topics = wi.get_vedic_topics()
    for topic in topics:
        result = wi.fetch_page(topic)
        if result['extract']:
            ke.add_knowledge(topic, result['extract'][:500], "wikipedia")
            print(f"   ✅ {topic}")
    
    # Show final stats
    print("\n" + "🕉️" * 50)
    print("BUILD COMPLETE!")
    print(f"📊 Final Stats: {ke.get_stats()}")
    print("🕉️" * 50)

if __name__ == "__main__":
    build_vedic_knowledge()
