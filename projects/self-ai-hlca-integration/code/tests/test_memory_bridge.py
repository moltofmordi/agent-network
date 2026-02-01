"""
Tests for MemoryBridge

Phase 2 Testing
Author: Molt
Date: 2026-02-01
"""

import sys
sys.path.append('../bridge')

from memory_bridge import MemoryBridge, Triple
from knowledge_encoder import KnowledgeEncoder


def test_basic_storage():
    """Test storing and retrieving exact triples"""
    print("\n=== Test 1: Basic Storage ===")
    
    encoder = KnowledgeEncoder(embedding_dim=512, sparsity=0.05)
    bridge = MemoryBridge(encoder)
    
    # Store knowledge
    triple = Triple("Paris", "capitalOf", "France", confidence=1.0)
    assembly = bridge.store_knowledge(triple)
    
    assert assembly is not None, "Failed to create assembly"
    assert assembly.metadata['triple'] == triple, "Metadata not preserved"
    
    # Retrieve exact
    retrieved = bridge.retrieve_exact("Paris", "capitalOf", "France")
    assert retrieved is not None, "Failed to retrieve exact triple"
    assert retrieved.subject == "Paris", "Subject mismatch"
    
    print("✓ Basic storage and retrieval works")
    

def test_cue_based_retrieval():
    """Test retrieving with partial cues"""
    print("\n=== Test 2: Cue-Based Retrieval ===")
    
    encoder = KnowledgeEncoder(embedding_dim=512, sparsity=0.05)
    bridge = MemoryBridge(encoder)
    
    # Store multiple triples
    bridge.store_knowledge(Triple("Paris", "capitalOf", "France"))
    bridge.store_knowledge(Triple("Berlin", "capitalOf", "Germany"))
    bridge.store_knowledge(Triple("London", "capitalOf", "UK"))
    bridge.store_knowledge(Triple("France", "inContinent", "Europe"))
    
    # Query: "What is the capital of France?"
    cue = Triple(None, "capitalOf", "France")
    results = bridge.retrieve_by_cue(cue, top_k=3)
    
    assert len(results) > 0, "No results returned"
    
    # Best match should be Paris-capitalOf-France
    best_triple, best_score = results[0]
    assert best_triple.subject == "Paris", f"Expected Paris, got {best_triple.subject}"
    assert best_score > 0.5, f"Similarity too low: {best_score}"
    
    print(f"✓ Cue retrieval works. Best match: {best_triple.subject} (score: {best_score:.3f})")
    

def test_similarity_ranking():
    """Test that similar triples rank higher"""
    print("\n=== Test 3: Similarity Ranking ===")
    
    encoder = KnowledgeEncoder(embedding_dim=512, sparsity=0.05)
    bridge = MemoryBridge(encoder)
    
    # Store related and unrelated triples
    bridge.store_knowledge(Triple("Paris", "capitalOf", "France"))
    bridge.store_knowledge(Triple("Paris", "locatedIn", "France"))
    bridge.store_knowledge(Triple("Paris", "cityIn", "Europe"))
    bridge.store_knowledge(Triple("Tokyo", "capitalOf", "Japan"))  # Different entity
    
    # Query for Paris-related
    cue = Triple("Paris", None, None)
    results = bridge.retrieve_by_cue(cue, top_k=4)
    
    # All Paris triples should rank higher than Tokyo
    paris_count = sum(1 for t, s in results[:3] if t.subject == "Paris")
    assert paris_count == 3, f"Expected 3 Paris results in top 3, got {paris_count}"
    
    print(f"✓ Similarity ranking correct. Top 3 are Paris-related")
    

def test_batch_operations():
    """Test storing and retrieving many triples"""
    print("\n=== Test 4: Batch Operations ===")
    
    encoder = KnowledgeEncoder(embedding_dim=512, sparsity=0.05)
    bridge = MemoryBridge(encoder)
    
    # Create 50 triples
    countries = ["France", "Germany", "Italy", "Spain", "UK"]
    cities = ["Paris", "Berlin", "Rome", "Madrid", "London"]
    
    triples = []
    for city, country in zip(cities, countries):
        triples.append(Triple(city, "capitalOf", country))
        triples.append(Triple(city, "locatedIn", country))
        triples.append(Triple(country, "hasCapital", city))
    
    # Store all
    for triple in triples:
        bridge.store_knowledge(triple)
    
    stats = bridge.get_stats()
    assert stats['total_knowledge'] == len(triples), "Not all triples stored"
    
    # Retrieve
    cue = Triple(None, "capitalOf", "France")
    results = bridge.retrieve_by_cue(cue, top_k=1)
    
    assert len(results) > 0, "Query failed"
    assert results[0][0].subject == "Paris", "Wrong capital retrieved"
    
    print(f"✓ Batch operations work. Stored {len(triples)} triples successfully")
    

def test_memory_stats():
    """Test statistics reporting"""
    print("\n=== Test 5: Memory Statistics ===")
    
    encoder = KnowledgeEncoder(embedding_dim=512, sparsity=0.05)
    bridge = MemoryBridge(encoder)
    
    # Store some knowledge
    bridge.store_knowledge(Triple("Paris", "capitalOf", "France"))
    bridge.store_knowledge(Triple("Berlin", "capitalOf", "Germany"))
    bridge.store_knowledge(Triple("Paris", "locatedIn", "France"))
    
    stats = bridge.get_stats()
    
    assert stats['total_knowledge'] == 3, f"Expected 3 triples, got {stats['total_knowledge']}"
    assert stats['entities'] > 0, "No entities encoded"
    assert stats['relations'] > 0, "No relations encoded"
    
    print(f"✓ Stats: {stats}")
    

def run_all_tests():
    """Run all MemoryBridge tests"""
    print("="*60)
    print("MEMORY BRIDGE TEST SUITE")
    print("="*60)
    
    try:
        test_basic_storage()
        test_cue_based_retrieval()
        test_similarity_ranking()
        test_batch_operations()
        test_memory_stats()
        
        print("\n" + "="*60)
        print("SUCCESS: ALL TESTS PASSED")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n[X] TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n[X] UNEXPECTED ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
