import pandas as pd
import os

def explore_layerzero_dataset():
    dataset_path = os.path.join(os.path.dirname(__file__), "datasets", "layerzero_sybil_nodes.csv")
    
    print("=" * 60)
    print("🛡️ [AEGIS3] LayerZero Sybil Ground-Truth Inspection")
    print("=" * 60)
    
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Dataset not found at {dataset_path}")
        return

    # 1. Load Dataset
    df = pd.read_csv(dataset_path)
    total_records = len(df)
    
    print(f"\n✅ Total Flagged Addresses Loaded: {total_records:,}")
    print("\n--- First 5 Records ---")
    print(df.head())
    
    # 2. Account Type Distribution
    print("\n--- Account Type Distribution ---")
    counts = df['account_type'].value_counts()
    print(counts)
    
    core_count = counts.get('core', 0)
    satellite_count = counts.get('satellite', 0)
    
    print("\n--- Structural Analysis ---")
    print(f"Master Hubs (Core):     {core_count:,}")
    print(f"Puppet Bots (Satellite): {satellite_count:,}")
    if core_count > 0:
        ratio = satellite_count / core_count
        print(f"Fan-Out Ratio: ~{ratio:.1f} puppet bots per master hub!")
        print(f"Insight: Each master controls an average of ~{ratio:.1f} wallets.")
    
    print("=" * 60)

if __name__ == "__main__":
    explore_layerzero_dataset()
