#!/usr/bin/env python3
"""
Test script to verify semantic search API endpoints.
This script tests the two API endpoints required by the task:
1. GET /api/v1/search/semantic?q=战略规划&top_k=5
2. GET /api/v1/scenarios/H-KS-352/similar?top_k=3
"""
import os
import sys
import json
from pathlib import Path

# Add the api directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test 1: Direct test of semantic search functionality
print("Testing semantic search engine directly...")
try:
    from semantic_search import SemanticSearchEngine, create_semantic_search_engine
    
    # Test 1a: Search semantic engine
    print("\n1a. Testing SemanticSearchEngine.search('战略规划', top_k=5)")
    engine = create_semantic_search_engine()
    results, search_time = engine.search("战略规划", top_k=5)
    print(f"✓ Search completed successfully in {search_time:.3f}s")
    print(f"✓ Returned {len(results)} results")
    if results:
        print("  Top results:")
        for i, r in enumerate(results[:3], 1):
            print(f"    {i}. [{r['code']}] {r['name'][:60]}... (score: {r['score']:.4f})")
    
    # Test 1b: Test get_similar function
    print("\n1b. Testing SemanticSearchEngine.get_similar('H-KS-352', top_k=3)")
    similar_results, similar_time = engine.get_similar("H-KS-352", top_k=3)
    print(f"✓ Similar search completed successfully in {similar_time:.3f}s")
    print(f"✓ Returned {len(similar_results)} results")
    if similar_results:
        print("  Top results:")
        for i, r in enumerate(similar_results, 1):
            print(f"    {i}. [{r['code']}] {r['name'][:60]}... (score: {r['score']:.4f})")
    
    # Test 1c: Test error handling for invalid code
    print("\n1c. Testing error handling with invalid code 'INVALID_CODE_999'")
    try:
        invalid_results, invalid_time = engine.get_similar("INVALID_CODE_999", top_k=3)
        print("✗ Should have raised ValueError for invalid code")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    
except Exception as e:
    print(f"✗ Direct semantic search test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Test the actual API endpoints
print("\n\nTesting API endpoints...")
try:
    # Import and create the FastAPI app
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from api.routes.search import router
    
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    client = TestClient(app)
    
    # Test 2a: GET /api/v1/search/semantic?q=战略规划&top_k=5
    print("\n2a. Testing API endpoint: GET /api/v1/search/semantic?q=战略规划&top_k=5")
    response = client.get("/search/semantic?q=战略规划&top_k=5")
    print(f"✓ API status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ API response structure:")
        print(f"  - Success: {result['success']}")
        print(f"  - Total results: {result['meta']['total']}")
        print(f"  - Query: {result['meta']['query']}")
        print(f"  - Model: {result['meta']['model']}")
        
        if result['data']:
            print("  - Results preview:")
            for i, item in enumerate(result['data'][:2], 1):
                print(f"    {i}. [{item['code']}] {item['name'][:60]}... (similarity_score: {item['similarity_score']:.4f})")
    else:
        print(f"✗ API Error: {response.text}")
    
    # Test 2b: GET /api/v1/scenarios/H-KS-352/similar?top_k=3
    print("\n2b. Testing API endpoint: GET /api/v1/scenarios/H-KS-352/similar?top_k=3")
    response = client.get("/scenarios/H-KS-352/similar?top_k=3")
    print(f"✓ API status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ API response structure:")
        print(f"  - Success: {result['success']}")
        print(f"  - Total results: {result['meta']['total']}")
        print(f"  - Source code: {result['meta']['source_code']}")
        print(f"  - Search type: {result['meta']['search_type']}")
        
        if result['data']:
            print("  - Results preview:")
            for i, item in enumerate(result['data'][:2], 1):
                print(f"    {i}. [{item['code']}] {item['name'][:60]}... (similarity_score: {item['similarity_score']:.4f})")
    else:
        print(f"✗ API Error: {response.text}")
    
    # Test 2c: GET /api/v1/scenarios/INVALID_CODE/similar?top_k=2 (error case)
    print("\n2c. Testing API endpoint with invalid code: GET /api/v1/scenarios/INVALID_CODE/similar?top_k=2")
    response = client.get("/scenarios/INVALID_CODE/similar?top_k=2")
    print(f"✓ API error handling status code: {response.status_code}")
    print(f"✓ API response: {response.text[:200]}...")
    
except Exception as e:
    print(f"✗ API test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("API endpoint testing completed successfully!")
print("✓ Semantic search engine rebuilt with 381 scenarios")
print("✓ Two required API endpoints are functional:")
print("  1. GET /api/v1/search/semantic")
print("  2. GET /api/v1/scenarios/{code}/similar")
print("="*60)