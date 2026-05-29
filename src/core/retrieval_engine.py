import os
import json
import torch
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.transformer_wrapper import SovereignTransformer

class LocalRetrievalEngine:
    def __init__(self, cache_dir="storage/knowledge"):
        self.cache_dir = cache_dir
        self.manifest_path = os.path.join(self.cache_dir, "chunks_manifest.json")
        self.vector_path = os.path.join(self.cache_dir, "vectors_cache.pt")
        # Align query encoding with the new generative tier
        self.embedder = SovereignTransformer(model_name="facebook/opt-125m")

    def _load_memory_vault(self):
        if not os.path.exists(self.manifest_path) or not os.path.exists(self.vector_path):
            return None, None
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
        vectors = torch.load(self.vector_path, map_location='cpu')
        return manifest, vectors

    def query(self, query_text, top_k=3, temporal_ceiling=None):
        manifest, db_vectors = self._load_memory_vault()
        if manifest is None or db_vectors is None or len(manifest) == 0:
            return []

        # Generate query vector directly from the LLM hidden state
        q_vec = self.embedder.encode(query_text).unsqueeze(0)

        # Pure localized cosine similarity via matrix multiplication
        similarities = torch.mm(q_vec, db_vectors.transpose(0, 1)).squeeze(0)
        
        top_k = min(top_k, len(manifest))
        scores, indices = torch.topk(similarities, top_k)
        
        results = []
        for score, idx in zip(scores.tolist(), indices.tolist()):
            node = manifest[idx]
            if temporal_ceiling and node.get('timestamp', float('inf')) > temporal_ceiling:
                continue
                
            node_copy = dict(node)
            node_copy['alignment_score'] = score
            results.append(node_copy)
            
        return results
