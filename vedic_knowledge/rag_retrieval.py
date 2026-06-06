#!/usr/bin/env python3
"""
DAY 3: RAG (Retrieval Augmented Generation) System
Connects knowledge base to your Vedic AI
"""

import sys
import sqlite3
import re
from datetime import datetime

sys.path.append('/data/data/com.termux/files/home/vedic_agents')

class VedicRAG:
    def __init__(self):
        self.db_path = "/data/data/com.termux/files/home/vedic_knowledge/knowledge.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
    def search(self, query, max_results=5):
        """Search knowledge base for relevant information"""
        query_terms = query.lower().split()
        
        # Build search query
        placeholders = ','.join(['?'] * len(query_terms))
        search_pattern = '%' + '%'.join(query_terms) + '%'
        
        self.cursor.execute('''
            SELECT topic, content, source FROM knowledge 
            WHERE topic LIKE ? OR content LIKE ?
            LIMIT ?
        ''', (search_pattern, search_pattern, max_results))
        
        results = self.cursor.fetchall()
        return [{'topic': r[0], 'content': r[1], 'source': r[2]} for r in results]
    
    def get_relevant_context(self, question):
        """Get relevant context for answering a question"""
        results = self.search(question, 3)
        
        if not results:
            return "No specific knowledge found. Using general Vedic wisdom."
        
        context = []
        for r in results:
            context.append(f"[{r['topic']}]: {r['content'][:200]}")
        
        return "\n".join(context)
    
    def enhance_prompt(self, question, user_query):
        """Enhance the prompt with retrieved knowledge"""
        context = self.get_relevant_context(question)
        
        enhanced_prompt = f"""
[VEDIC KNOWLEDGE BASE]
{context}

[USER QUESTION]
{user_query}

[INSTRUCTION]
Using the Vedic knowledge above, provide a wise and accurate answer.
"""
        return enhanced_prompt
    
    def get_stats(self):
        """Get RAG system statistics"""
        self.cursor.execute("SELECT COUNT(*) FROM knowledge")
        total = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM vedic_texts")
        vedic = self.cursor.fetchone()[0]
        
        return {
            'total_entries': total,
            'vedic_texts': vedic,
            'status': 'active'
        }

# Test the RAG system
def test_rag():
    rag = VedicRAG()
    
    print("🕉️" * 50)
    print("DAY 3: RAG RETRIEVAL SYSTEM - TESTING")
    print("🕉️" * 50)
    
    test_questions = [
        "What is Brahman?",
        "Explain the concept of Dharma",
        "What are the Vedas?",
        "What is Karma Yoga?"
    ]
    
    for q in test_questions:
        print(f"\n📖 QUESTION: {q}")
        print("-" * 40)
        context = rag.get_relevant_context(q)
        print(f"📚 Retrieved Context:\n{context[:300]}...")
    
    print(f"\n✅ RAG System Ready!")
    print(f"📊 Database stats: {rag.get_stats()}")
    
    return rag

if __name__ == "__main__":
    test_rag()
