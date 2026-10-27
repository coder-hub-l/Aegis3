# Aegis3 Data Pipeline: Ground-Truth Dataset Extraction

This directory contains the production SQL queries used to extract real-world on-chain Sybil clusters and funding topologies from **Dune Analytics**.

---

## 📁 Directory Structure
```text
data-pipeline/
├── sql/
│   ├── layerzero_behavioral_clusters.sql  # Detects synchronized interaction footprints
│   └── common_funder_star_graph.sql       # Detects master gas-funding star graphs
├── datasets/                              # Store exported CSV files here (git-ignored)
└── README.md
```

---

## 🚀 How to Run Queries on Dune Analytics (Free)

### Step 1: Set Up Free Dune Account
1. Go to [dune.com](https://dune.com) and log in (or sign up for free).
2. Click the **"+ New"** button in the top navigation bar and select **"Query"**.
3. In the query editor, ensure the engine dropdown is set to **`DuneSQL`**.

### Step 2: Execute the Queries
* Open [`sql/layerzero_behavioral_clusters.sql`](sql/layerzero_behavioral_clusters.sql) or [`sql/common_funder_star_graph.sql`](sql/common_funder_star_graph.sql).
* Copy and paste the entire SQL text into the Dune query window.
* Click **"Run"** (Ctrl + Enter).
* *Execution time:* Usually takes between 15 and 45 seconds depending on Dune query queue.

### Step 3: Export the Dataset
1. Once the results table appears below the query editor, look at the bottom-right corner of the results pane.
2. Click the **three dots (`...`)** or the **Export icon** and select **"Download CSV"**.
3. Create a folder named `datasets/` inside `data-pipeline/` if it doesn't already exist.
4. Save the downloaded CSV as:
   * `data-pipeline/datasets/layerzero_sybil_clusters.csv`
   * `data-pipeline/datasets/arbitrum_star_funders.csv`

---

## 🔍 What These Queries Prove (For Slide 5 & Engine Testing)

1. **`layerzero_behavioral_clusters.sql`:**
   * **The Attack Pattern:** Proves that bot cartels script identical user behavior. 50+ wallets with the exact same number of bridge transactions, active on the exact same days, crossing the exact same chains.
   * **Output:** Flagged clusters with their full array of member wallet addresses.

2. **`common_funder_star_graph.sql`:**
   * **The Attack Pattern:** Identifies central funding distribution hubs. A master wallet sends identical amounts of ETH (e.g., 0.01500 ETH with <0.0001 variance) to dozens of child wallets within minutes.
   * **Output:** Master funder address, batch duration in minutes, and count of recipient wallets.
