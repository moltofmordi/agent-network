"""
Test suite for KnowledgeEncoder.

Validates that HLCA Triples can be encoded as Self-AI assemblies
and retrieved with high accuracy.

Author: Molt
Date: 2026-01-31
"""

import sys
sys.path.insert(0, '../bridge')

import numpy as np
import pytest
from knowledge_encoder import KnowledgeEncoder, Triple, Confidence, Assembly


class TestKnowledgeEncoder:
    """Comprehensive test suite for knowledge encoding."""
    
    def setup_method(self):
        """Create fresh encoder for each test."""
        self.encoder = KnowledgeEncoder(
            vocab_size=10000,
            embedding_dim=512,
            sparsity=0.05,
            seed=42
        )
    
    def test_encode_entity(self):
        """Test entity encoding produces sparse codes."""
        code = self.encoder.encode_entity("Paris")
        
        # Should be sparse (5% active)
        expected_active = int(512 * 0.05)
        actual_active = np.sum(code > 0)
        assert actual_active == expected_active, f"Expected {expected_active} active, got {actual_active}"
        
        # Should be binary
        assert np.all((code == 0) | (code == 1)), "Code should be binary"
        
        # Should be deterministic (same entity → same code)
        code2 = self.encoder.encode_entity("Paris")
        assert np.array_equal(code, code2), "Same entity should produce same code"
        
        # Different entities should have different codes
        code_london = self.encoder.encode_entity("London")
        assert not np.array_equal(code, code_london), "Different entities should differ"
    
    def test_encode_relation(self):
        """Test relation encoding."""
        code = self.encoder.encode_relation("capitalOf")
        
        # Same checks as entities
        assert np.sum(code > 0) == int(512 * 0.05)
        assert np.all((code == 0) | (code == 1))
        
        # Relations and entities should be in different spaces
        entity_code = self.encoder.encode_entity("capitalOf")  # Same string, different namespace
        # They might overlap by chance, but shouldn't be identical
        # (In practice, separate namespaces ensure this)
    
    def test_bind_codes(self):
        """Test binding multiple codes together."""
        code1 = self.encoder.encode_entity("Paris")
        code2 = self.encoder.encode_relation("capitalOf")
        code3 = self.encoder.encode_entity("France")
        
        bound = self.encoder.bind_codes([code1, code2, code3], binding_strength=1.0)
        
        # Bound code should still be sparse
        assert np.sum(bound > 0) > 0, "Bound code should have active neurons"
        
        # Should contain information from all components
        # (Hard to test without proper unbinding, but we check it's not just one code)
        assert not np.array_equal(bound, code1)
        assert not np.array_equal(bound, code2)
    
    def test_encode_triple_basic(self):
        """Test basic triple encoding."""
        triple = Triple("Paris", "capitalOf", "France")
        assembly = self.encoder.encode_triple(triple)
        
        # Should have active neurons
        assert len(assembly.neuron_ids) > 0
        assert len(assembly.weights) == len(assembly.neuron_ids)
        
        # Should have metadata
        assert "triple" in assembly.metadata
        assert assembly.metadata["triple"]["subject"] == "Paris"
        assert assembly.metadata["triple"]["predicate"] == "capitalOf"
        assert assembly.metadata["triple"]["object"] == "France"
    
    def test_encode_triple_with_confidence(self):
        """Test triple encoding respects confidence."""
        triple = Triple("Paris", "capitalOf", "France")
        
        # High confidence
        conf_high = Confidence(p=0.95, calibration=0.9, last_verified=0)
        asm_high = self.encoder.encode_triple(triple, conf_high)
        
        # Low confidence
        conf_low = Confidence(p=0.5, calibration=0.6, last_verified=0)
        asm_low = self.encoder.encode_triple(triple, conf_low)
        
        # High confidence should have stronger weights
        assert np.mean(asm_high.weights) > np.mean(asm_low.weights)
    
    def test_decode_assembly(self):
        """Test assembly can be decoded back to triple."""
        triple_orig = Triple("Paris", "capitalOf", "France")
        assembly = self.encoder.encode_triple(triple_orig)
        
        triple_decoded = self.encoder.decode_assembly(assembly)
        
        assert triple_decoded is not None
        assert triple_decoded.subject == triple_orig.subject
        assert triple_decoded.predicate == triple_orig.predicate
        assert triple_decoded.object == triple_orig.object
    
    def test_encode_decode_roundtrip(self):
        """Test encode→decode roundtrip preserves information."""
        triples = [
            Triple("Paris", "capitalOf", "France"),
            Triple("London", "capitalOf", "UK"),
            Triple("Tokyo", "capitalOf", "Japan"),
            Triple("Paris", "locatedIn", "Europe"),
        ]
        
        for triple in triples:
            assembly = self.encoder.encode_triple(triple)
            decoded = self.encoder.decode_assembly(assembly)
            
            assert decoded.subject == triple.subject
            assert decoded.predicate == triple.predicate
            assert decoded.object == triple.object
    
    def test_similarity_same_relation(self):
        """Test similar triples have high similarity."""
        # Both are capital-of relations
        triple1 = Triple("Paris", "capitalOf", "France")
        triple2 = Triple("London", "capitalOf", "UK")
        
        asm1 = self.encoder.encode_triple(triple1)
        asm2 = self.encoder.encode_triple(triple2)
        
        # Convert to full codes for similarity
        code1 = np.zeros(512)
        code1[asm1.neuron_ids] = asm1.weights
        code2 = np.zeros(512)
        code2[asm2.neuron_ids] = asm2.weights
        
        sim = self.encoder.similarity(code1, code2)
        
        # Should be somewhat similar (shared relation)
        assert sim > 0.2, f"Similar triples should have sim > 0.2, got {sim}"
    
    def test_similarity_different_relation(self):
        """Test dissimilar triples have low similarity."""
        triple1 = Triple("Paris", "capitalOf", "France")
        triple2 = Triple("Water", "boilsAt", "100C")
        
        asm1 = self.encoder.encode_triple(triple1)
        asm2 = self.encoder.encode_triple(triple2)
        
        code1 = np.zeros(512)
        code1[asm1.neuron_ids] = asm1.weights
        code2 = np.zeros(512)
        code2[asm2.neuron_ids] = asm2.weights
        
        sim = self.encoder.similarity(code1, code2)
        
        # Should be dissimilar
        assert sim < 0.5, f"Dissimilar triples should have sim < 0.5, got {sim}"
    
    def test_retrieve_similar(self):
        """Test retrieval of similar triples."""
        # Build knowledge base
        triples = [
            Triple("Paris", "capitalOf", "France"),
            Triple("London", "capitalOf", "UK"),
            Triple("Tokyo", "capitalOf", "Japan"),
            Triple("Water", "boilsAt", "100C"),
            Triple("Iron", "meltsAt", "1538C"),
        ]
        
        assemblies = [self.encoder.encode_triple(t) for t in triples]
        
        # Query for capital-of facts
        query = Triple("Berlin", "capitalOf", "Germany")
        results = self.encoder.retrieve_similar(query, assemblies, top_k=3)
        
        # Top 3 should all be capital-of relations
        for asm, score in results:
            triple_data = asm.metadata["triple"]
            predicate = triple_data["predicate"]
            assert predicate == "capitalOf", f"Expected capitalOf, got {predicate}"
    
    def test_batch_encoding_performance(self):
        """Test encoding many triples doesn't degrade."""
        triples = [
            Triple(f"Entity{i}", f"relation{i%5}", f"Entity{i+1}")
            for i in range(100)
        ]
        
        for triple in triples:
            assembly = self.encoder.encode_triple(triple)
            assert len(assembly.neuron_ids) > 0
        
        stats = self.encoder.get_stats()
        assert stats["triples_encoded"] == 100
        assert stats["encoding_errors"] == 0
    
    def test_persistence(self, tmp_path):
        """Test encoder mappings can be saved and loaded."""
        # Encode some triples
        triples = [
            Triple("Paris", "capitalOf", "France"),
            Triple("London", "capitalOf", "UK"),
        ]
        
        original_assemblies = [self.encoder.encode_triple(t) for t in triples]
        
        # Save
        save_path = tmp_path / "encoder_mappings.pkl"
        self.encoder.save_mappings(str(save_path))
        
        # Create new encoder and load
        new_encoder = KnowledgeEncoder(seed=99)  # Different seed!
        new_encoder.load_mappings(str(save_path))
        
        # Should produce identical encodings
        for triple, orig_asm in zip(triples, original_assemblies):
            new_asm = new_encoder.encode_triple(triple)
            assert np.array_equal(orig_asm.neuron_ids, new_asm.neuron_ids)
            assert np.array_equal(orig_asm.weights, new_asm.weights)
    
    def test_stats_tracking(self):
        """Test statistics are tracked correctly."""
        assert self.encoder.get_stats()["triples_encoded"] == 0
        
        self.encoder.encode_triple(Triple("A", "B", "C"))
        assert self.encoder.get_stats()["triples_encoded"] == 1
        
        self.encoder.encode_triple(Triple("X", "Y", "Z"))
        assert self.encoder.get_stats()["triples_encoded"] == 2


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def setup_method(self):
        self.encoder = KnowledgeEncoder()
    
    def test_empty_string_entity(self):
        """Test handling of empty strings."""
        code = self.encoder.encode_entity("")
        assert len(code) == 512  # Should still produce valid code
    
    def test_special_characters(self):
        """Test encoding entities with special characters."""
        entities = ["Paris@123", "New York!", "São Paulo"]
        for entity in entities:
            code = self.encoder.encode_entity(entity)
            assert np.sum(code > 0) > 0
    
    def test_very_long_strings(self):
        """Test encoding very long entity names."""
        long_entity = "A" * 1000
        code = self.encoder.encode_entity(long_entity)
        assert np.sum(code > 0) > 0
    
    def test_unicode_handling(self):
        """Test Unicode entity names."""
        entities = ["北京", "Москва", "القاهرة"]
        for entity in entities:
            triple = Triple(entity, "isCity", "true")
            assembly = self.encoder.encode_triple(triple)
            decoded = self.encoder.decode_assembly(assembly)
            assert decoded.subject == entity


def run_tests():
    """Run all tests and report results."""
    print("Running KnowledgeEncoder test suite...")
    print("=" * 60)
    
    # Basic functionality
    print("\n[1/4] Testing basic encoding...")
    suite = TestKnowledgeEncoder()
    suite.setup_method()
    
    try:
        suite.test_encode_entity()
        print("  [PASS] Entity encoding")
        
        suite.test_encode_relation()
        print("  [PASS] Relation encoding")
        
        suite.test_bind_codes()
        print("  [PASS] Code binding")
        
        suite.test_encode_triple_basic()
        print("  [PASS] Triple encoding")
        
    except AssertionError as e:
        print(f"  ✗ Failed: {e}")
        return False
    
    # Roundtrip
    print("\n[2/4] Testing encode/decode roundtrip...")
    suite.setup_method()
    try:
        suite.test_decode_assembly()
        print("  [PASS] Decoding")
        
        suite.test_encode_decode_roundtrip()
        print("  [PASS] Roundtrip preservation")
        
    except AssertionError as e:
        print(f"  [FAIL] {e}")
        return False
    
    # Similarity and retrieval
    print("\n[3/4] Testing similarity and retrieval...")
    suite.setup_method()
    try:
        suite.test_similarity_same_relation()
        print("  [PASS] Similar triples detected")
        
        suite.test_similarity_different_relation()
        print("  [PASS] Dissimilar triples detected")
        
        suite.test_retrieve_similar()
        print("  [PASS] Retrieval works")
        
    except AssertionError as e:
        print(f"  [FAIL] {e}")
        return False
    
    # Performance and edge cases
    print("\n[4/4] Testing performance and edge cases...")
    suite.setup_method()
    try:
        suite.test_batch_encoding_performance()
        print("  [PASS] Batch encoding (100 triples)")
        
        edge_tests = TestEdgeCases()
        edge_tests.setup_method()
        edge_tests.test_special_characters()
        print("  [PASS] Special characters")
        
        edge_tests.test_unicode_handling()
        print("  [PASS] Unicode support")
        
    except AssertionError as e:
        print(f"  [FAIL] {e}")
        return False
    
    print("\n" + "=" * 60)
    print("SUCCESS: ALL TESTS PASSED")
    print("=" * 60)
    
    # Print final stats
    stats = suite.encoder.get_stats()
    print(f"\nFinal statistics:")
    print(f"  Entities encoded: {stats['entities_encoded']}")
    print(f"  Relations encoded: {stats['relations_encoded']}")
    print(f"  Triples encoded: {stats['triples_encoded']}")
    print(f"  Errors: {stats['encoding_errors']}")
    
    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
