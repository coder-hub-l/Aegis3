"""
Aegis3 Core Engine - Risk Scorer
Aggregates graph topology metrics, Louvain clustering, and Jaccard sequence similarity
to produce a deterministic 0-100 Risk Score and Tiered Allocation classification.
"""

from typing import Dict, List
import pandas as pd

class SybilRiskScorer:
    def __init__(self):
        # Weights for multi-signal aggregation
        self.W_GRAPH = 0.50     # Weight for Louvain cluster density / star-funder links
        self.W_JACCARD = 0.35   # Weight for behavioral sequence duplication
        self.W_FANOUT = 0.15    # Weight for high out-degree master linkage

    def score_wallets(self, 
                      wallets: List[str], 
                      cartel_clusters: List[Dict], 
                      jaccard_clusters: List[Dict]) -> pd.DataFrame:
        """
        Calculates a deterministic 0-100 Sybil Risk Score for every candidate wallet.
        """
        results = []

        # Index memberships for O(1) lookups
        cartel_membership = {}
        for c in cartel_clusters:
            for w in c["members"]:
                cartel_membership[w] = c

        jaccard_membership = {}
        for j in jaccard_clusters:
            for w in j["wallets"]:
                jaccard_membership[w] = j

        for w in wallets:
            w_lower = w.lower().strip()
            
            # 1. Graph signal (0 - 100)
            graph_score = 0
            if w_lower in cartel_membership:
                cluster_size = cartel_membership[w_lower]["size"]
                # Larger cluster = higher confidence of industrial coordination
                graph_score = min(100, 40 + (cluster_size * 2))

            # 2. Jaccard behavioral DNA signal (0 - 100)
            jaccard_score = 0
            if w_lower in jaccard_membership:
                j_size = jaccard_membership[w_lower]["cluster_size"]
                jaccard_score = min(100, 50 + (j_size * 3))

            # Combined Weighted Score
            total_score = int(round((graph_score * self.W_GRAPH) + (jaccard_score * self.W_JACCARD)))

            # Classification Tier:
            if total_score >= 70:
                tier = "Tier 3: Sybil Bot Cartel (Disqualified)"
                verdict = "DISQUALIFY"
            elif total_score >= 35:
                tier = "Tier 2: Suspicious Activity (Under Review)"
                verdict = "MANUAL_REVIEW"
            else:
                tier = "Tier 1: Authentic Human (Eligible)"
                verdict = "ELIGIBLE"

            results.append({
                "wallet_address": w,
                "sybil_risk_score": total_score,
                "tier": tier,
                "recommended_verdict": verdict,
                "graph_signal": graph_score,
                "jaccard_signal": jaccard_score
            })

        df = pd.DataFrame(results)
        df.sort_values(by="sybil_risk_score", ascending=False, inplace=True)
        return df
