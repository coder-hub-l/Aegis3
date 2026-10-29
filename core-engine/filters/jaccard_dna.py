"""
Aegis3 Core Engine - Behavioral DNA & Sequence Alignment
Calculates the Jaccard Similarity across smart contract interaction sets.
Flags wallets that called the exact same sequence/set of protocol contracts.
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict

class JaccardDNAAnalyzer:
    def __init__(self, similarity_threshold: float = 0.80):
        """
        :param similarity_threshold: Jaccard index (0.0 to 1.0) above which 
                                     two independent wallets are flagged as scripted clones.
        """
        self.threshold = similarity_threshold

    @staticmethod
    def calculate_jaccard(set_a: Set[str], set_b: Set[str]) -> float:
        """Jaccard Index = |A ∩ B| / |A ∪ B|"""
        if not set_a and not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return intersection / union if union > 0 else 0.0

    def find_scripted_clones(self, wallet_interactions: Dict[str, List[str]]) -> List[Dict]:
        """
        :param wallet_interactions: Dict mapping wallet_address -> list of contract addresses called.
        :return: List of detected clone clusters with high behavioral similarity.
        """
        wallets = list(wallet_interactions.keys())
        wallet_sets = {w: set(contracts) for w, contracts in wallet_interactions.items()}
        
        clone_clusters = []
        visited = set()

        for i in range(len(wallets)):
            w1 = wallets[i]
            if w1 in visited or len(wallet_sets[w1]) < 2:
                continue

            current_cluster = [w1]
            visited.add(w1)

            for j in range(i + 1, len(wallets)):
                w2 = wallets[j]
                if w2 in visited or len(wallet_sets[w2]) < 2:
                    continue

                sim = self.calculate_jaccard(wallet_sets[w1], wallet_sets[w2])
                if sim >= self.threshold:
                    current_cluster.append(w2)
                    visited.add(w2)

            if len(current_cluster) >= 3:  # 3 or more wallets with identical DNA = scripted cluster
                clone_clusters.append({
                    "cluster_size": len(current_cluster),
                    "shared_contracts_count": len(wallet_sets[w1]),
                    "similarity_score": self.threshold,
                    "wallets": current_cluster
                })

        print(f"🧬 [JaccardDNA] Detected {len(clone_clusters)} scripted behavioral clone clusters.")
        return clone_clusters
