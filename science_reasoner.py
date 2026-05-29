import numpy as np, sympy as sp
class ScienceReasoner:
    def __init__(self, graph): self.graph = graph
    def infer(self, propositions, steps, max_depth=10):
        premise_cids = [self.graph.add_node(p.text, p.embedding, p.confidence) for p in propositions]
        current_cids, depth = premise_cids, 0
        while depth < max_depth:
            node_a = self.graph.get_node(current_cids[0])
            node_b = self.graph.get_node(current_cids[1] if len(current_cids)>1 else current_cids[0])
            new_conf = node_a.confidence * node_b.confidence
            label = f"({node_a.label} AND {node_b.label})"
            embed = (node_a.embedding + node_b.embedding) / 2.0
            last_cid = self.graph.add_node(label, embed / np.linalg.norm(embed), new_conf)
            current_cids = [last_cid] + current_cids
            depth += 1
        return self.graph.get_node(last_cid)
