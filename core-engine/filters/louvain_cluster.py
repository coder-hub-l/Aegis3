"""
Aegis3 Core Engine - Louvain Partitioning Filter
Applies fast, multi-scale modularity optimization to isolate
densely connected sub-communities (bot cartels) from background organic graphs.
"""

import networkx as nx
import community as community_louvain
from typing import Dict, List
from collections import Counter

class LouvainClusterFilter:
    def __init__(self, min_cluster_size: int = 5):
        """
        :param min_cluster_size: Minimum number of tightly linked addresses
                                 required to treat a group as a suspicious cartel.
        """
        self.min_cluster_size = min_cluster_size

    def partition(self, graph: nx.Graph) -> Dict[str, int]:
        """
        Runs Louvain community detection on an undirected network graph.
        :return: Mapping of { wallet_address: cluster_id }
        """
        if graph.is_directed():
            graph = graph.to_undirected()

        print(f"🔬 [LouvainFilter] Partitioning graph with {graph.number_of_nodes():,} nodes and {graph.number_of_edges():,} edges...")
        partition = community_louvain.best_partition(graph)
        return partition

    def extract_suspicious_cartels(self, graph: nx.Graph, partition: Dict[str, int]) -> List[Dict]:
        """
        Filters the full partition to identify clusters meeting the minimum cartel threshold.
        """
        counts = Counter(partition.values())
        suspicious = []

        for cluster_id, size in counts.items():
            if size >= self.min_cluster_size:
                members = [node for node, c_id in partition.items() if c_id == cluster_id]
                suspicious.append({
                    "cluster_id": cluster_id,
                    "size": size,
                    "members": members
                })

        suspicious.sort(key=lambda x: x["size"], reverse=True)
        print(f"🚨 [LouvainFilter] Identified {len(suspicious)} suspicious cartels (size >= {self.min_cluster_size}).")
        return suspicious
