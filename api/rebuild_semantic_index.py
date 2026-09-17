#!/usr/bin/env python3
"""
Rebuild semantic search index for Protreptic.
This script loads the semantic_search module and rebuilds the FAISS index
from the scenario data in api/data/.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from semantic_search import create_semantic_search_engine

def main():
    print("Starting semantic search index rebuild...")
    print("Using data from: <repo>/api/data/")
    
    # Create engine (will rebuild index since it doesn't exist)
    engine = create_semantic_search_engine()
    
    # Get statistics
    stats = engine.get_stats()
    print(f"Index built successfully!")
    print(f"Total scenarios: {stats['total_scenarios']}")
    print(f"Embedding dimension: {stats['embedding_dim']}")
    print(f"Model: {stats['model']}")
    print(f"Index type: {stats['index_type']}")
    
    # Perform a quick search test
    query = "战略规划"
    results, search_time = engine.search(query, top_k=5)
    print(f"\nSearch test for query: '{query}'")
    print(f"Search time: {search_time:.3f}s")
    print(f"Returned {len(results)} results:")
    for i, r in enumerate(results, 1):
        print(f"  {i}. [{r['code']}] {r['name'][:80]}... (score: {r['score']:.4f})")
    
    # Test similar search API
    similar_results, similar_time = engine.get_similar('H-KS-352', top_k=3)
    print(f"\nSimilar search for code 'H-KS-352':")
    print(f"Search time: {similar_time:.3f}s")
    print(f"Returned {len(similar_results)} results")
    
    print("\n=== Semantic search index rebuild completed successfully ===")

if __name__ == "__main__":
    main()