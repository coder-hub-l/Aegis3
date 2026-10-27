# Aegis3 — Master Project Context & Engineering Blueprint

> **Status:** Active Project Context  
> **Last Updated:** October 27, 2026  
> **Founders:** Laukik Wani (Industrial & Systems Engineering, IIT Kharagpur) & Chirag Janbandhu (Geology & Geophysics, IIT Kharagpur)  
> **Stage:** Pre-Seed / Prototype Development (Targeting KGP Forge & Global Web3 Accelerators)

---

## 1. Executive Summary & Vision

**Aegis3** is an enterprise launch integrity and transaction security platform purpose-built for Web3 protocol foundations conducting Token Generation Events (TGEs) and airdrop distributions.

### The Problem:
* **Protocol Bleed:** Industrial bot cartels deploy tens of thousands of automated wallets to extract token allocations. Post-TGE dumping routinely crashes token prices by 70–85%, damaging protocol economics and alienating genuine users.
* **The False-Positive PR Trap:** Existing black-box Sybil detection filters accidentally ban legitimate community power users, triggering catastrophic reputational backlash on X/Discord and depressing token sentiment.
* **Community Exposure:** During launch hype, scammers deploy lookalike claim sites and malicious Permit2 signature drains, stealing millions from users who blame the protocol foundation.

### The Unified Solution:
Aegis3 provides a **single, end-to-end launch integrity suite** for the protocol foundation:
1. **Pre-Launch (Inbound Defense):** Explainable, multi-signal Sybil detection providing tiered, confidence-scored allocations with transparent on-chain audit trails.
2. **Launch Window (Outbound Defense):** A lightweight Verified Claim SDK embedded directly into `claim.protocol.xyz` to eliminate spoofed front-ends and unauthorized signature drains.
3. **Post-Launch:** A publishable **Foundation Integrity Report** validating distribution fairness to investors, centralized exchanges (Binance, Coinbase), and the community.

---

## 2. Core Strategic & Commercial Decisions

### Rejection of the Standalone Consumer Extension Business:
* **Decision:** We do **not** build a standalone B2C browser extension business.
* **Rationale:** Blockaid ($83M funded, backed by Sequoia) is already embedded natively in MetaMask and Coinbase Wallet. Pocket Universe demonstrated that consumer willingness to pay for Web3 security is near zero, leading to acquisition.
* **The Pivot:** We sell **B2B to Protocol Foundations** who have high willingness to pay during existential, multi-million-dollar token launches.

### Unit Economics & Profitability Timeline:
* **Pricing Model:**
  * **Standard Launch Audit & Sybil Report:** ₹15 Lakhs (~$18k) per engagement.
  * **Enterprise Launch Suite (Audit + Claim SDK + War Room Ops):** ₹28 Lakhs (~$34k).
* **Operating Burn (Student / Pre-Seed):** ~₹80,000 / month (~$960/mo) covering cloud compute, RPC archive nodes, Dune API, and lean founder stipends.
* **Breakeven Milestone:** **6 to 9 Months.** A single closed protocol engagement (₹15L) funds the team's entire operating expenses for more than 12 months.
* **Year 2 Financial Target:** 12 protocol launches @ ₹22L average = ₹2.64 Crore revenue with >75% net margin.

---

## 3. Core Architectural & Technical Decisions

### Decision 1: Rejection of LLM/AI in Real-Time Exploit Detection
* **Why Rejected:** 
  1. Phishing attacks and drainers do not run malicious code; they call 100% legitimate, verified contracts (Uniswap Permit2, OpenSea Seaport, standard ERC-20 `approve`) with **poisoned calldata/parameters**. An LLM reading contract source code marks them as safe.
  2. Latency: An LLM takes 3–8 seconds; pre-sign verification requires <100ms.
* **What We Use Instead:** **Deterministic EVM State Simulation (Dry-Run)**. Transactions are simulated against forked state to capture the exact **state diff** (token outflows, approval deltas).
* **Role of AI:** AI is used strictly *after* simulation to translate raw state diffs into human-readable explanations, **never** to make security verdicts.

### Decision 2: Rejection of Graph Neural Networks (GNNs) for Sybil Detection
* **Why Rejected:**
  1. GNNs require massive, ground-truth labeled datasets that do not exist on anonymous blockchains.
  2. GNNs are black boxes. A protocol cannot justify banning a user because of a "latent embedding distance."
* **What We Use Instead:** **Deterministic Network Science & Heuristic Triangulation**:
  1. **Hub-Pruned Graph Partitioning (Louvain 2.0):** Prunes major exchange hot wallets (Binance) and AMMs, then partitions asset-transfer graphs to expose tight bot cliques.
  2. **Contract Call Sequence Alignment (Jaccard Similarity):** Compares the "behavioral DNA" of wallets across contract interaction sequences to catch bots that randomize execution timers.
  3. **CEX Deposit Address Convergence:** Traces downstream cash-out transactions to shared centralized exchange deposit addresses (100% precision, zero false positives).

---

## 4. Current Implementation State

### Completed Milestones:
1. **Chrome MV3 Interceptor Prototype (`Milestone 1`):**
   * Configured `manifest.json` with `"world": "MAIN"` and `"run_at": "document_start"`.
   * Built `wiretap.js`, which attaches a JavaScript proxy to `window.ethereum.request`.
   * Verified in Chrome: Intercepts `eth_sendTransaction` and provider calls before MetaMask handles them.
2. **Fact-Checked Pitch Deck & Market Sizing:**
   * Fact-checked metrics: Separated Scam Sniffer phishing loss data ($494M in 2024; $83.85M in 2025) from airdrop bot extraction.
   * Reconciled SOM: Replaced unrealistic analyst figures with bottom-up SOM (₹6 Cr ARR based on 30 launches/year).
   * Scoped to EVM ecosystems (Ethereum, Arbitrum, Base), dropping non-EVM Solana claims.
3. **Feasibility & Architecture Specification:**
   * Completed and saved in `aegis3_feasibility_and_mvp_spec.md`.

---

## 5. Target MVP Repository Architecture

```text
aegis3/
├── data-pipeline/               # Sourcing, indexing, and state normalization
│   ├── sql/                     # Dune queries (LayerZero sybils, CEX deposits)
│   ├── extractors/              # Dune API & Web3.py RPC clients
│   └── normalizer.py            # Converts raw txs into clean Graph Nodes & Edges
│
├── core-engine/                 # Deterministic graph & heuristic engine
│   ├── graph_builder.py         # Builds NetworkX DiGraph
│   ├── filters/
│   │   ├── hub_pruner.py        # Prunes CEX hot wallets and AMM pools
│   │   ├── louvain_cluster.py   # Spatial topology community partitioning
│   │   ├── jaccard_dna.py       # Contract call sequence similarity
│   │   └── cex_tracer.py        # Cash-out deposit address matching
│   └── scorer.py                # Aggregates signals into 0-100 Confidence Tier
│
├── claim-sdk/                   # Lightweight frontend claim widget
│   └── src/                     # React component protocols embed on claim.xyz
│
├── report-generator/            # Generates publishable governance artifacts
│   ├── templates/               # Clean HTML/PDF report template
│   ├── visualizer.py            # Generates high-res PyVis/Matplotlib graph plots
│   └── exporter.py              # Compiles CSV + on-chain evidence hashes
│
└── tests/                       # Ground-truth validation
    ├── ground_truth_sybils.csv  # 5,000 verified bot wallets from LayerZero
    └── test_louvain_recall.py   # Measures precision vs false positives
```

---

## 6. Division of Labour

| Founder | Role | Primary Responsibilities |
| :--- | :--- | :--- |
| **Laukik Wani** | **CTO & Systems / Security Lead** | • Core Graph Engine (`networkx`, Louvain)<br>• Heuristic Detectors (Jaccard sequence similarity, CEX deposit tracer)<br>• State simulation sandbox interface<br>• Algorithmic benchmarking and precision testing |
| **Chirag Janbandhu** | **CPO & Growth / Data Operations Lead** | • Sourcing on-chain datasets via Dune SQL & BigQuery<br>• Labeled ground-truth curation (LayerZero, Arbitrum)<br>• Automated Audit Report generator & visualizer<br>• Protocol discovery, partner outreach, and pilot interviews |

---

## 7. 6-Week Execution Roadmap

* **Week 1 (Ground Truth Dataset):** Sourcing 5,000 verified LayerZero Sybil wallets and 5,000 organic wallets into `ground_truth_sybils.csv` via Dune SQL.
* **Week 2 (Graph Ingestion Engine):** Building `graph_builder.py` and `hub_pruner.py` to ingest on-chain transaction logs into a clean `networkx` graph.
* **Week 3 (Heuristics Suite):** Implementing Louvain community detection and Jaccard sequence similarity in `core-engine/`.
* **Week 4 (Validation Benchmark):** Testing heuristics against the Week 1 dataset. **Target:** >85% recall with <2% false positive rate.
* **Week 5 (Audit Report Generator):** Building automated PDF/HTML reports with cluster visualizations and verifiable transaction hashes.
* **Week 6 (Protocol Outreach Sprint):** Direct outreach to 20 emerging testnet protocols (Mode, Scroll, Berachain ecosystems) offering free pilot launch audits.
