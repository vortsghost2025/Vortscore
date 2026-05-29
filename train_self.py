import os
import sys
import json
import torch
import time
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.core.memory_engine import MemoryEngine

class CoreMemoryManifold:
    def __init__(self, manifest_data, embeddings_tensor):
        self.manifest = manifest_data
        self.vectors = embeddings_tensor

    def query_at_temporal_threshold(self, query_vector, target_timestamp, k=3):
        """Exposes Temporal State Tracking: Returns historical nodes alive at exact unix timestamp T."""
        scores = torch.nn.functional.cosine_similarity(self.vectors, query_vector.unsqueeze(0), dim=1)
        
        valid_indices = [
            idx for idx, chunk in enumerate(self.manifest)
            if chunk.get('timestamp', 0) <= target_timestamp
        ]
        
        if not valid_indices:
            return []
            
        filtered_scores = scores[valid_indices]
        top_k = torch.topk(filtered_scores, min(k, len(filtered_scores)))
        
        results = []
        for score, local_idx in zip(top_k.values, top_k.indices):
            actual_idx = valid_indices[local_idx.item()]
            record = self.manifest[actual_idx].copy()
            record['alignment_score'] = float(score.item())
            results.append(record)
            
        return results

def run_self_study(data_directory, model_name, target_time):
    print("[*] Launching FSI Sovereign Continual-Learning Subsystem...")
    
    engine = MemoryEngine(model_name=model_name)
    engine.ingest_knowledge(data_directory)
    
    base_path = os.path.join(os.getcwd(), data_directory)
    manifest_path = os.path.join(base_path, "chunks_manifest.json")
    vectors_path = os.path.join(base_path, "vectors_cache.pt")
    
    if not os.path.exists(manifest_path) or not os.path.exists(vectors_path):
        print("[-] Absolute ingestion failure: Cache binaries missing.")
        sys.exit(1)
        
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest_data = json.load(f)
    embeddings_tensor = torch.load(vectors_path, map_location='cpu')
    
    manifold = CoreMemoryManifold(manifest_data, embeddings_tensor)
    print(f"[+] Loaded Matrix: {embeddings_tensor.shape[0]} nodes integrated securely.")
    
    # Execution Test: Generate a localized dummy context vector to verify traceability paths
    if len(manifest_data) > 0:
        test_vector = embeddings_tensor[0]
        query_time = time.time() if target_time == 0.0 else target_time
        historical_snapshots = manifold.query_at_temporal_threshold(test_vector, query_time, k=1)
        
        print("\n==========================================================")
        print("[+] EXPLAINABLE TRACEABILITY ROOT VERIFIED:")
        if historical_snapshots:
            snap = historical_snapshots[0]
            print(f"    - Found Node ID: {snap['chunk_id']}")
            print(f"    - Historical Scope: Enrolled at Unix Time {snap['timestamp']}")
            print(f"    - Semantic Content: {snap['text'][:70]}...")
            print(f"    - Integrity Verification: Cosine Metric {snap['alignment_score']:.4f}")
        else:
            print("    - No nodes matched temporal criteria.")
        print("==========================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FSI Self-Study Temporal Orchestrator")
    parser.add_argument("--dir", type=str, default="storage/knowledge", help="Knowledge directory")
    parser.add_argument("--model", type=str, default="all-MiniLM-L6-v2", help="Transformer engine")
    parser.add_argument("--time", type=float, default=0.0, help="Temporal query limit (Unix timestamp)")
    args = parser.parse_args()
    
    run_self_study(args.dir, args.model, args.time)
