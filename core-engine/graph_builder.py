"""
Aegis3 Core Engine - Graph Builder
Ingests on-chain address nodes and funding/interaction edges,
applies hub pruning, and constructs the mathematical network graph.
"""

import networkx as nx
import pandas as pd
from typing import List, Dict, Tuple, Optional

class GraphBuilder:
    def __init__(self, max_hub_degree: int = 500):
        """
        :param max_hub_degree: Threshold above which an address is considered 
                               a noisy public mega-hub (e.g. Binance, Uniswap router) 
                               and pruned to prevent false topological bridges.
        """
        self.graph = nx.DiGraph()
        self.max_hub_degree = max_hub_degree

    def add_wallets(self, wallets_df: pd.DataFrame, address_col: str = "sybil_address", type_col: str = "account_type"):
        """Adds address nodes with their initial metadata."""
        for _, row in wallets_df.iterrows():
            addr = str(row[address_col]).lower().strip()
            node_type = row[type_col] if type_col in row else "unknown"
            self.graph.add_node(addr, node_type=node_type)
        print(f"📦 [GraphBuilder] Ingested {self.graph.number_of_nodes():,} wallet nodes.")

    def add_transfers(self, transfers: List[Tuple[str, str, float]]):
        """
        Adds directed transfer edges: (from_address, to_address, value_eth).
        """
        for sender, receiver, val in transfers:
            s = str(sender).lower().strip()
            r = str(receiver).lower().strip()
            self.graph.add_edge(s, r, weight=val)
        print(f"🔗 [GraphBuilder] Ingested {self.graph.number_of_edges():,} directed transfer edges.")

    def prune_mega_hubs(self) -> List[str]:
        """
        Identifies and temporarily detaches mega-hubs (Binance hot wallets, Uniswap pools)
        so that Louvain and community detection only cluster genuine peer-to-peer cartels.
        """
        pruned = []
        for node in list(self.graph.nodes()):
            degree = self.graph.in_degree(node) + self.graph.out_degree(node)
            if degree > self.max_hub_degree:
                pruned.append(node)
                self.graph.remove_node(node)
        
        if pruned:
            print(f"✂️ [GraphBuilder] Pruned {len(pruned)} mega-hub(s) exceeding degree {self.max_hub_degree}.")
        return pruned

    def get_undirected(self) -> nx.Graph:
        """Returns the undirected projection required for Louvain partitioning."""
        return self.graph.to_undirected()

    def get_summary(self) -> Dict[str, int]:
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "connected_components": nx.number_weakly_connected_components(self.graph) if self.graph.is_directed() else nx.number_connected_components(self.graph)
        }
