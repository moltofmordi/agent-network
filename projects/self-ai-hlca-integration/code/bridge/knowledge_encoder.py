"""
KnowledgeEncoder: Bridge between HLCA symbolic Triples and Self-AI sparse assemblies.

This is the foundational piece - converts explicit symbolic knowledge into
distributed neural representations that can be stored, retrieved, and reasoned over
in Self-AI's sparse substrate.

Author: Molt
Date: 2026-01-31
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
from uuid import UUID

# HLCA types (will need proper imports when integrating)
@dataclass
class Triple:
    """HLCA's Triple format: subject-predicate-object."""
    subject: str
    predicate: str
    object: str

@dataclass
class Confidence:
    """HLCA's confidence tracking."""
    p: float  # 0..1
    calibration: float
    last_verified: int

# Self-AI types (placeholder - will import from actual codebase)
@dataclass
class Assembly:
    """Self-AI sparse assembly representation."""
    neuron_ids: np.ndarray  # Sparse indices
    weights: np.ndarray     # Activation strengths
    metadata: Dict[str, any]

class KnowledgeEncoder:
    """
    Encodes HLCA's symbolic knowledge as Self-AI sparse assemblies.
    
    Key design decisions:
    1. Each Triple component (subject, predicate, object) gets its own sparse code
    2. Components are bound together via Self-AI's binding mechanism
    3. Confidence maps to binding strength
    4. Evidence links are stored in assembly metadata
    
    This enables:
    - Efficient storage (sparse codes scale well)
    - Pattern completion (partial retrieval works)
    - Compositional reasoning (bind/unbind operations)
    """
    
    def __init__(
        self,
        vocab_size: int = 10000,
        embedding_dim: int = 512,
        sparsity: float = 0.05,  # 5% active neurons
        seed: int = 42
    ):
        """
        Initialize encoder.
        
        Args:
            vocab_size: Size of entity vocabulary
            embedding_dim: Dimensionality of sparse codes
            sparsity: Fraction of neurons active per concept
            seed: Random seed for reproducibility
        """
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.sparsity = sparsity
        self.k = int(embedding_dim * sparsity)  # Top-k active
        
        np.random.seed(seed)
        
        # Entity → sparse code mappings (learned or random)
        self.entity_codes: Dict[str, np.ndarray] = {}
        self.relation_codes: Dict[str, np.ndarray] = {}
        
        # Reverse lookup: sparse code → entity
        self.code_to_entity: Dict[Tuple[int, ...], str] = {}
        self.code_to_relation: Dict[Tuple[int, ...], str] = {}
        
        # Statistics for analysis
        self.stats = {
            "entities_encoded": 0,
            "relations_encoded": 0,
            "triples_encoded": 0,
            "encoding_errors": 0
        }
    
    def encode_entity(self, entity: str) -> np.ndarray:
        """
        Encode entity as sparse code.
        
        Strategy: Random sparse codes with overlap for semantic similarity.
        Future: Could use learned embeddings from language model.
        
        Args:
            entity: Entity string (e.g., "Paris", "France")
            
        Returns:
            Sparse binary vector (shape: embedding_dim)
        """
        if entity in self.entity_codes:
            return self.entity_codes[entity]
        
        # Generate random sparse code
        code = np.zeros(self.embedding_dim, dtype=np.float32)
        active_indices = np.random.choice(
            self.embedding_dim, 
            size=self.k, 
            replace=False
        )
        code[active_indices] = 1.0
        
        # Cache
        self.entity_codes[entity] = code
        self.code_to_entity[tuple(active_indices)] = entity
        self.stats["entities_encoded"] += 1
        
        return code
    
    def encode_relation(self, relation: str) -> np.ndarray:
        """
        Encode relation/predicate as sparse code.
        
        Relations get separate namespace from entities to avoid confusion.
        
        Args:
            relation: Predicate string (e.g., "capitalOf", "isA")
            
        Returns:
            Sparse binary vector
        """
        if relation in self.relation_codes:
            return self.relation_codes[relation]
        
        code = np.zeros(self.embedding_dim, dtype=np.float32)
        active_indices = np.random.choice(
            self.embedding_dim,
            size=self.k,
            replace=False
        )
        code[active_indices] = 1.0
        
        self.relation_codes[relation] = code
        self.code_to_relation[tuple(active_indices)] = relation
        self.stats["relations_encoded"] += 1
        
        return code
    
    def bind_codes(
        self, 
        codes: List[np.ndarray], 
        binding_strength: float = 1.0
    ) -> np.ndarray:
        """
        Bind multiple sparse codes into single assembly.
        
        Binding operation: Uses superposition (sum + sparsify).
        This preserves similarity between similar bindings.
        
        Args:
            codes: List of sparse codes to bind
            binding_strength: Weight (maps to confidence)
            
        Returns:
            Bound sparse code
        """
        if len(codes) == 0:
            return np.zeros(self.embedding_dim, dtype=np.float32)
        
        # Superposition binding: Sum all codes
        # This preserves similarity - similar components → similar bound codes
        bound = np.zeros(self.embedding_dim, dtype=np.float32)
        for code in codes:
            bound += code
        
        # Re-sparsify: Keep top-k most activated
        if np.sum(bound > 0) > self.k:
            threshold = np.partition(bound, -self.k)[-self.k]
            bound = (bound >= threshold).astype(np.float32)
        else:
            # If fewer than k active, normalize but keep all
            bound = (bound > 0).astype(np.float32)
        
        bound *= binding_strength
        
        return bound
    
    def encode_triple(
        self, 
        triple: Triple, 
        confidence: Optional[Confidence] = None
    ) -> Assembly:
        """
        Main encoding function: Triple → Self-AI Assembly.
        
        This is where HLCA's symbolic knowledge becomes neural.
        
        Args:
            triple: HLCA Triple object
            confidence: Optional confidence tracking
            
        Returns:
            Self-AI Assembly ready for storage
        """
        try:
            # Encode each component
            subject_code = self.encode_entity(triple.subject)
            predicate_code = self.encode_relation(triple.predicate)
            object_code = self.encode_entity(triple.object)
            
            # Bind into single representation
            binding_strength = confidence.p if confidence else 0.8
            bound_code = self.bind_codes(
                [subject_code, predicate_code, object_code],
                binding_strength=binding_strength
            )
            
            # Convert to Assembly format
            active_neurons = np.where(bound_code > 0)[0]
            weights = bound_code[active_neurons]
            
            assembly = Assembly(
                neuron_ids=active_neurons,
                weights=weights,
                metadata={
                    "type": "knowledge_triple",
                    "triple": {
                        "subject": triple.subject,
                        "predicate": triple.predicate,
                        "object": triple.object
                    },
                    "confidence": confidence.p if confidence else None,
                    "component_codes": {
                        "subject": tuple(np.where(subject_code > 0)[0]),
                        "predicate": tuple(np.where(predicate_code > 0)[0]),
                        "object": tuple(np.where(object_code > 0)[0])
                    }
                }
            )
            
            self.stats["triples_encoded"] += 1
            return assembly
            
        except Exception as e:
            self.stats["encoding_errors"] += 1
            raise RuntimeError(f"Failed to encode triple {triple}: {e}")
    
    def decode_assembly(self, assembly: Assembly) -> Optional[Triple]:
        """
        Reverse operation: Assembly → Triple.
        
        Uses metadata if available, otherwise attempts pattern matching.
        
        Args:
            assembly: Self-AI assembly
            
        Returns:
            Reconstructed Triple or None
        """
        # Fast path: Check metadata
        if "triple" in assembly.metadata:
            triple_data = assembly.metadata["triple"]
            return Triple(
                subject=triple_data["subject"],
                predicate=triple_data["predicate"],
                object=triple_data["object"]
            )
        
        # Slow path: Pattern matching (not implemented yet)
        # Would involve unbinding and nearest-neighbor search
        return None
    
    def similarity(self, code1: np.ndarray, code2: np.ndarray) -> float:
        """
        Compute similarity between two sparse codes.
        
        Uses cosine similarity (dot product for binary vectors).
        """
        return float(np.dot(code1, code2) / (np.linalg.norm(code1) * np.linalg.norm(code2) + 1e-8))
    
    def retrieve_similar(
        self, 
        query_triple: Triple, 
        assemblies: List[Assembly], 
        top_k: int = 5
    ) -> List[Tuple[Assembly, float]]:
        """
        Find assemblies most similar to query.
        
        This enables approximate retrieval - useful for generalization.
        
        Args:
            query_triple: Triple to search for
            assemblies: Pool of assemblies to search
            top_k: Number of results to return
            
        Returns:
            List of (assembly, similarity_score) tuples
        """
        query_assembly = self.encode_triple(query_triple)
        query_code = np.zeros(self.embedding_dim)
        query_code[query_assembly.neuron_ids] = query_assembly.weights
        
        scores = []
        for assembly in assemblies:
            code = np.zeros(self.embedding_dim)
            code[assembly.neuron_ids] = assembly.weights
            sim = self.similarity(query_code, code)
            scores.append((assembly, sim))
        
        # Sort by similarity
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def get_stats(self) -> Dict[str, int]:
        """Return encoding statistics."""
        return self.stats.copy()
    
    def save_mappings(self, path: str):
        """Save learned mappings for persistence."""
        import pickle
        with open(path, 'wb') as f:
            pickle.dump({
                'entity_codes': self.entity_codes,
                'relation_codes': self.relation_codes,
                'stats': self.stats
            }, f)
    
    def load_mappings(self, path: str):
        """Load saved mappings."""
        import pickle
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.entity_codes = data['entity_codes']
            self.relation_codes = data['relation_codes']
            self.stats = data['stats']


if __name__ == "__main__":
    # Quick test
    encoder = KnowledgeEncoder()
    
    # Test encoding
    triple = Triple("Paris", "capitalOf", "France")
    confidence = Confidence(p=0.95, calibration=0.9, last_verified=0)
    
    assembly = encoder.encode_triple(triple, confidence)
    print(f"Encoded triple into assembly with {len(assembly.neuron_ids)} active neurons")
    print(f"Weights: {assembly.weights[:5]}...")
    print(f"Metadata: {assembly.metadata['triple']}")
    
    # Test decoding
    decoded = encoder.decode_assembly(assembly)
    print(f"\nDecoded: {decoded.subject} {decoded.predicate} {decoded.object}")
    
    # Test similarity
    triple2 = Triple("London", "capitalOf", "UK")
    assembly2 = encoder.encode_triple(triple2)
    
    # These should be similar (both capital-of relations)
    scores = encoder.retrieve_similar(triple, [assembly, assembly2])
    print(f"\nSimilarity scores:")
    for asm, score in scores:
        meta = asm.metadata['triple']
        print(f"  {meta['subject']} {meta['predicate']} {meta['object']}: {score:.3f}")
    
    print(f"\nStats: {encoder.get_stats()}")
