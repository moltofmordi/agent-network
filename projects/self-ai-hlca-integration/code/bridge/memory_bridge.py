"""
Memory Bridge: Connects HLCA knowledge to Self-AI LTM Semantic region

Phase 2 Implementation
Author: Molt
Date: 2026-02-01
"""

from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class Triple:
    """HLCA knowledge triple"""
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0


@dataclass
class Assembly:
    """Self-AI sparse neural assembly"""
    neuron_ids: np.ndarray  # Active neuron indices
    weights: np.ndarray     # Activation strengths
    metadata: Dict = None   # Store original triple here
    
    @property
    def size(self):
        return len(self.neuron_ids)


class MemoryBridge:
    """
    Bridges HLCA knowledge store to Self-AI LTM Semantic region.
    
    Architecture:
        HLCA Triple → KnowledgeEncoder → Assembly → Self-AI LTM
        
    Responsibilities:
        - Store encoded knowledge in Self-AI memory
        - Retrieve knowledge using cue-based lookup
        - Maintain bidirectional mapping (Triple ↔ Assembly)
        - Handle consolidation from episodic to semantic memory
    """
    
    def __init__(self, knowledge_encoder, ltm_semantic_region=None):
        """
        Args:
            knowledge_encoder: KnowledgeEncoder instance for Triple→Assembly
            ltm_semantic_region: Self-AI LTM Semantic region (optional for now)
        """
        self.encoder = knowledge_encoder
        self.ltm = ltm_semantic_region
        
        # Memory store (temporary until Self-AI LTM connected)
        self.memory: Dict[str, Assembly] = {}  # triple_id → assembly
        self.reverse_index: Dict[int, str] = {}  # assembly hash → triple_id
        
    def store_knowledge(self, triple: Triple) -> Assembly:
        """
        Store a knowledge triple in memory.
        
        Args:
            triple: HLCA Triple to store
            
        Returns:
            Assembly representing the stored knowledge
            
        Process:
            1. Encode triple to sparse assembly
            2. Store in Self-AI LTM (or temp memory)
            3. Maintain bidirectional mapping
        """
        # Encode to assembly
        assembly = self.encoder.encode_triple(triple)
        
        # Add metadata
        assembly.metadata = {
            'triple': triple,
            'confidence': triple.confidence,
            'source': 'explicit_knowledge'
        }
        
        # Generate unique ID
        triple_id = f"{triple.subject}_{triple.predicate}_{triple.object}"
        
        # Store in memory
        if self.ltm is not None:
            # TODO: Use Self-AI LTM once connected
            # self.ltm.store(assembly, weight=triple.confidence)
            pass
        else:
            # Temporary: store in dict
            self.memory[triple_id] = assembly
            
        # Maintain reverse index
        assembly_hash = hash(tuple(assembly.neuron_ids))
        self.reverse_index[assembly_hash] = triple_id
        
        return assembly
        
    def retrieve_by_cue(self, cue_triple: Triple, top_k: int = 5) -> List[Tuple[Triple, float]]:
        """
        Retrieve knowledge using a partial cue.
        
        Args:
            cue_triple: Partial triple as query (can have None values)
            top_k: Number of results to return
            
        Returns:
            List of (Triple, similarity_score) tuples
            
        Process:
            1. Encode cue to assembly
            2. Search memory for similar assemblies
            3. Return top-k matches with scores
        """
        # Encode cue (create new triple with filled values)
        filled_cue = Triple(
            subject=cue_triple.subject or "",
            predicate=cue_triple.predicate or "",
            object=cue_triple.object or ""
        )
        cue_assembly = self.encoder.encode_triple(filled_cue)
        
        # Search memory
        if self.ltm is not None:
            # TODO: Use Self-AI LTM cue-based retrieval
            # results = self.ltm.retrieve_similar(cue_assembly, k=top_k)
            results = []
        else:
            # Temporary: manual similarity search
            results = []
            
            # Expand cue assembly to dense vector
            cue_dense = np.zeros(self.encoder.embedding_dim)
            cue_dense[cue_assembly.neuron_ids] = cue_assembly.weights
            
            for triple_id, assembly in self.memory.items():
                # Expand memory assembly to dense vector
                mem_dense = np.zeros(self.encoder.embedding_dim)
                mem_dense[assembly.neuron_ids] = assembly.weights
                
                # Compute similarity
                similarity_score = self.encoder.similarity(cue_dense, mem_dense)
                triple = assembly.metadata['triple']
                results.append((triple, similarity_score))
                
            # Sort by similarity, return top-k
            results.sort(key=lambda x: x[1], reverse=True)
            results = results[:top_k]
            
        return results
        
    def retrieve_exact(self, subject: str, predicate: str, object: str) -> Optional[Triple]:
        """
        Retrieve exact triple if it exists.
        
        Args:
            subject, predicate, object: Triple components
            
        Returns:
            Triple if found, None otherwise
        """
        triple_id = f"{subject}_{predicate}_{object}"
        
        if triple_id in self.memory:
            assembly = self.memory[triple_id]
            return assembly.metadata['triple']
            
        # TODO: Check Self-AI LTM when connected
        return None
        
    def consolidate_episode(self, episode_data: Dict) -> List[Triple]:
        """
        Extract knowledge from episodic memory and consolidate to semantic.
        
        This is the bridge between Self-AI's episodic (hippocampus) and 
        semantic (LTM) memory.
        
        Args:
            episode_data: Raw episodic data from Self-AI
            
        Returns:
            List of Triples extracted and stored
            
        Process:
            1. Analyze episode for patterns
            2. Extract factual knowledge
            3. Create Triples with evidence links
            4. Store in semantic memory
        """
        # TODO: Implement pattern extraction
        # For now, placeholder
        extracted_triples = []
        
        # Example: Extract "saw X at location Y" patterns
        # if 'observation' in episode_data:
        #     obs = episode_data['observation']
        #     if 'entity' in obs and 'location' in obs:
        #         triple = Triple(
        #             subject=obs['entity'],
        #             predicate='locatedAt',
        #             object=obs['location'],
        #             confidence=0.9
        #         )
        #         self.store_knowledge(triple)
        #         extracted_triples.append(triple)
        
        return extracted_triples
        
    def save_to_file(self, path: str):
        """
        Save memory to disk using pickle.
        
        Args:
            path: File path to save to
        """
        import pickle
        
        save_data = {
            'memory': self.memory,
            'reverse_index': self.reverse_index,
            'encoder_state': {
                'entity_codes': self.encoder.entity_codes,
                'relation_codes': self.encoder.relation_codes,
                'code_to_entity': self.encoder.code_to_entity,
                'code_to_relation': self.encoder.code_to_relation,
            }
        }
        
        with open(path, 'wb') as f:
            pickle.dump(save_data, f)
            
    def load_from_file(self, path: str):
        """
        Load memory from disk.
        
        Args:
            path: File path to load from
        """
        import pickle
        
        with open(path, 'rb') as f:
            save_data = pickle.load(f)
            
        self.memory = save_data['memory']
        self.reverse_index = save_data['reverse_index']
        
        # Restore encoder state
        encoder_state = save_data['encoder_state']
        self.encoder.entity_codes = encoder_state['entity_codes']
        self.encoder.relation_codes = encoder_state['relation_codes']
        self.encoder.code_to_entity = encoder_state['code_to_entity']
        self.encoder.code_to_relation = encoder_state['code_to_relation']
    
    def get_stats(self) -> Dict:
        """Return memory statistics"""
        return {
            'total_knowledge': len(self.memory),
            'entities': len(self.encoder.entity_codes),
            'relations': len(self.encoder.relation_codes),
            'using_ltm': self.ltm is not None
        }


# Example usage
if __name__ == "__main__":
    from knowledge_encoder import KnowledgeEncoder
    
    # Initialize
    encoder = KnowledgeEncoder(embedding_dim=512, sparsity=0.05)
    bridge = MemoryBridge(encoder)
    
    # Store some knowledge
    print("Storing knowledge...")
    bridge.store_knowledge(Triple("Paris", "capitalOf", "France"))
    bridge.store_knowledge(Triple("France", "inContinent", "Europe"))
    bridge.store_knowledge(Triple("Berlin", "capitalOf", "Germany"))
    
    # Retrieve
    print("\nRetrieving: What is the capital of France?")
    cue = Triple(None, "capitalOf", "France")
    results = bridge.retrieve_by_cue(cue, top_k=3)
    
    for triple, score in results:
        print(f"  {triple.subject} {triple.predicate} {triple.object} (similarity: {score:.3f})")
    
    # Stats
    print(f"\nMemory stats: {bridge.get_stats()}")
