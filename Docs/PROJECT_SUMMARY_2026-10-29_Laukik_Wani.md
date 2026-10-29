# Project Summary: Aegis3

- Date: 2026-10-29
- Author: Laukik Wani (CTO, Systems & Security Lead)
- Co-Founders: Chirag Janbandhu (CDO, Data Operations), Vinit (CPO, Product Management)
- Target: Pre-Seed Validation, KGP Forge (RMSoEE + z21 Ventures), and Web3 Acceleration Programs

---

## 1. Executive Overview

Aegis3 is an enterprise launch integrity and Sybil defense platform built for Web3 protocol foundations conducting Token Generation Events (TGEs) and airdrop distributions.

Token distributions face two existential failure modes:
1. Protocol Bleed: Industrial bot syndicates deploy tens of thousands of automated wallets to extract token allocations. Immediate post-launch dumping routinely causes 70% to 85% price crashes, destroying token economics and alienating real community members.
2. False-Positive Public Relations Disasters: Traditional black-box heuristics or poorly calibrated models ban high-value organic community members. These users publicly challenge foundations on social media, depressing sentiment and damaging project reputation before exchange listings.
3. Launch-Day Phishing Drains: Coordinated scammers deploy lookalike claim interfaces and malicious Permit2 approval transactions during launch hype, draining community assets.

Aegis3 provides a unified, two-sided launch protection layer:
- Inbound Protection: Deterministic, multi-signal Sybil detection producing explainable, audit-trail-backed allocation scores prior to distribution.
- Outbound Protection: Verified claim-gate infrastructure and pre-sign transaction verification to ensure end-users only interact with authentic protocol contracts.
- Governance Artifact: A verifiable, publishable audit report that proves distribution fairness to investors, centralized exchanges, and the community.

---

## 2. Core Strategic and Commercial Decisions

### 2.1 Rejection of the Standalone Consumer Extension Business
- Decision: Aegis3 does not pursue a standalone consumer browser extension business.
- Rationale: Incumbents like Blockaid (83M USD in funding, backed by Sequoia) are already integrated directly into MetaMask and Coinbase Wallet. Earlier consumer products like Pocket Universe demonstrated that consumer willingness to pay for standalone Web3 security extensions is negligible, forcing consolidation.
- Business Model: Direct B2B sales to protocol foundations and launchpad platforms. Launch-day insurance is a mission-critical purchase for foundations managing treasuries exceeding 10M USD.

### 2.2 Pricing and Unit Economics
- Standard Launch Audit: 15 Lakhs INR (~18,000 USD) per engagement.
- Full Launch Suite (Audit + Verified Claim Gate + Launch War Room): 28 Lakhs to 30 Lakhs INR (~34,000 USD to 36,000 USD).
- Operating Cost Structure (Pre-Seed Campus Burn): ~80,000 INR (~960 USD) per month covering compute, RPC archive access, data APIs, tooling, and founder stipends.
- Breakeven Timeline: 6 to 9 months. A single closed protocol engagement funds over 12 months of operations.
- Year 2 Target: 12 protocol launch engagements at an average contract value of 22 Lakhs INR = 2.64 Crore INR gross revenue at >75% net margin.

---

## 3. Core Architectural Principles

### 3.1 Rejection of Machine Learning and GNNs for Sybil Detection
- Decision: Zero reliance on Graph Neural Networks (GNNs), deep learning embeddings, or black-box classifiers.
- Rationale:
  1. Lack of Ground Truth: The pseudonymous nature of blockchains means no verified, universal dataset of "human vs. bot" exists. Supervised models trained on noisy labels amplify errors.
  2. Explainability Requirement: Foundations cannot defend token disqualifications by citing latent vector distances. Deterministic evidence (e.g., shared funding sources, identical contract execution sets, shared CEX deposit addresses) provides indisputable public proof.
  3. Execution Overhead: Graph neural networks require significant VRAM and compute, introducing unnecessary latency compared to linear-time graph algorithms.

### 3.2 The Multi-Signal Heuristic Suite
Aegis3 deploys three complementary deterministic heuristics:
1. Hub-Pruned Louvain Partitioning: Prunes high-degree exchange hot wallets and liquidity pools, then partitions the asset transfer network into dense, isolated sub-communities to reveal bot cartels.
2. Jaccard Behavioral DNA: Calculates set similarity on the unique smart contracts called by each wallet. Wallets exhibiting >= 85% overlap in contract call history are flagged as automated clones, bypassing randomized timing delays.
3. CEX Deposit Address Convergence: Traces downstream token transfers to centralized exchange deposit addresses. Multiple wallets depositing into the exact same exchange deposit address share identical legal/individual ownership.

### 3.3 Rejection of LLM Code-Reading for Transaction Security
- Decision: Pre-sign transaction validation is conducted via deterministic EVM state simulation, not LLM bytecode/source-code analysis.
- Rationale: Phishing exploits frequently interact with legitimate, audited protocols (e.g., Uniswap Permit2, OpenSea Seaport) using malicious parameters. An LLM inspecting contract source code marks the contract as safe, while the user's balance is drained. Deterministic state diffing captures exact asset balance and approval deltas in <50ms.

---

## 4. Current Implementation Status

### 4.1 Completed Milestones

1. Browser Transaction Interceptor (Extension Prototype)
   - Implemented Manifest V3 content script running in `MAIN` world at `document_start`.
   - Injected `wiretap.js` proxy wrapping `window.ethereum.request`.
   - Verified pre-sign interception of `eth_sendTransaction` before wallet triggers.

2. Ground-Truth Dataset Acquisition
   - Acquired 17,232 verified on-chain addresses from the LayerZero 15M USD bounty purge.
   - Structured data into `layerzero_sybil_nodes.csv` (labeled by `core` master hubs and `satellite` puppets) and `layerzero_sybil_addresses.csv`.

3. Empirical Graph Benchmarking
   - Executed research notebook `notebooks/01_layerzero_sybil_eda.ipynb` using NetworkX and `python-louvain`.
   - Benchmark Result: Successfully partitioned 83 multi-cartel LayerZero wallets into 3 independent bot cartels with 100% precision and zero cross-contamination in <20ms.
   - Generated high-resolution publication artifact: `Docs/aegis3_cluster_proof.png`.

4. Modular Production Core Engine
   - `core-engine/graph_builder.py`: Directed graph construction, degree tracking, and dynamic mega-hub pruning.
   - `core-engine/filters/louvain_cluster.py`: Production modularity optimization and cartel extraction.
   - `core-engine/filters/jaccard_dna.py`: Contract interaction sequence alignment and clone clustering.
   - `core-engine/scorer.py`: Multi-signal weighted scoring engine outputting 0-100 risk scores and tiered classifications (Tier 1: Eligible, Tier 2: Review, Tier 3: Disqualified).

5. Client Deliverable Generator
   - `report-generator/generate_report.py`: Programmatic generation of branded, dark-mode HTML Launch Audit Reports complete with metric cards and auditable evidence tables.

6. Master Execution Pipeline
   - `run_audit.py`: End-to-end CLI tool integrating dataset ingestion, graph construction, community detection, behavioral DNA, scoring, CSV export, and HTML report generation.

---

## 5. Team Structure and Work Division

```
                      AEGIS3 LEADERSHIP STRUCTURE
                      ---------------------------

  Laukik Wani                  Chirag Janbandhu             Vinit
  CTO, Systems & Security      CDO, Data Operations         CPO, Product Management
  -----------------------      --------------------         -----------------------
  - Core Detection Engine      - Data Sourcing (Dune/RPC)   - Customer Discovery
  - Graph Algorithms           - Data Normalization         - Protocol Outreach
  - Scoring & Benchmarking     - Report Generator (PDF)     - Pricing Validation
  - API Architecture           - Claim SDK Frontend         - Design Partner LOIs
  - System Infrastructure      - Dataset Curation           - Operations Playbook
```

### 5.1 Laukik Wani (CTO, Systems & Security)
- Ownership: `core-engine/`, `api/`, `tests/`.
- Focus: Algorithmic precision, graph scaling, time-decay weighting, CEX deposit tracer, REST API performance, automated testing benchmarks.

### 5.2 Chirag Janbandhu (CDO, Data Operations)
- Ownership: `data-pipeline/`, `report-generator/`, `claim-sdk/`.
- Focus: Sourcing raw chain transactions, Etherscan/Arbiscan scraper clients, wallet normalizer CLI, client-facing PDF generation, cryptographic evidence hashing, claim-gate React components.

### 5.3 Vinit (CPO, Product Management)
- Ownership: Product-market fit, commercial validation, protocol partnerships.
- Focus:
  1. Customer Discovery: Conducting 15 to 20 structured interviews with protocol founders, foundation leads, and launchpad operators.
  2. Competitive Intelligence: Maintaining active tracking of Trusta Labs, Blockaid, Gitcoin Passport, and emerging security entrants.
  3. Pricing Validation: Testing the 15L to 30L INR audit pricing model with budget holders.
  4. Design Partner Acquisition: Securing 3 letters of intent (LOIs) from protocols launching in the next 6 months for free pilot audits.
  5. Operations Playbook: Documenting client onboarding, data intake, audit delivery, and community appeal workflows.
  6. Pitch Deck & Narrative: Maintaining investor presentations and grant/accelerator applications.

---

## 6. Engineering and Operational Roadmap

```
  WEEK 1-2                    WEEK 3-4                    WEEK 5-6
  --------                    --------                    --------

  [Etherscan Scraper]     ->  [Fingerprint Extractor] ->  [FastAPI REST API]
  (Chirag)                    (Chirag)                    (Laukik)
      |                           |                           |
      +-----> feeds ------>-------+                           |
      |                           |                           |
  [CEX Deposit Tracer]        [Candidate List CLI]        [React Claim-Gate]
  (Laukik)                    (Chirag)                    (Chirag)
      |                           |
  [Temporal Decay Weights]    [Benchmark Suite]
  (Laukik)                    (Laukik)
      |                           |
  [Component Pre-filter]      [SHA-256 Hashes]
  (Laukik)                    (Laukik)
                                  |
                              [PDF Report Export]
                              (Chirag)

  -------------------------------------------------------------------------
  PARALLEL PRODUCT TRACK (Vinit, CPO):
  - Weeks 1-2: 10 customer interviews + competitive matrix v1
  - Weeks 3-4: 5 customer interviews + 2 design partner LOIs + pricing test
  - Weeks 5-6: Launch operations playbook + investor deck refresh
```

---

## 7. Repository Layout

```
Aegis3/
├── core-engine/                 Detection heuristics, graph builders, and risk scoring
│   ├── graph_builder.py         NetworkX graph ingestion and mega-hub pruning
│   ├── filters/
│   │   ├── louvain_cluster.py   Louvain community detection implementation
│   │   ├── jaccard_dna.py       Behavioral sequence similarity analysis
│   │   └── cex_tracer.py        [Planned] Centralized exchange deposit address matcher
│   └── scorer.py                Deterministic 0-100 risk scoring engine
│
├── data-pipeline/               On-chain extraction, SQL queries, and datasets
│   ├── sql/                     DuneSQL extraction queries
│   ├── datasets/                LayerZero verified ground-truth records
│   ├── extractors/              [Planned] Etherscan/Arbiscan batch scraper
│   └── normalizer.py            [Planned] Input list verification and deduplication
│
├── report-generator/            Audit artifacts and governance reporting
│   ├── generate_report.py       Dark-mode HTML audit report generator
│   ├── evidence_hasher.py       [Planned] Cryptographic SHA-256 evidence integrity hasher
│   └── pdf_exporter.py          [Planned] Executive PDF export utility
│
├── claim-sdk/                   [Planned] Embeddable React claim verification widget
├── api/                         [Planned] FastAPI REST scoring service
├── Extension/                   Manifest V3 transaction wiretap prototype
├── notebooks/                   Research, exploratory data analysis, and benchmark plots
├── tests/                       [Planned] Automated precision/recall regression suite
├── Docs/                        Architecture, summaries, prompts, and visual assets
│   ├── PROJECT_SUMMARY_2026-10-29_Laukik_Wani.md
│   ├── aegis3_cluster_proof.png
│   ├── claude_issue_prompt.txt
│   ├── issue_generator_prompt.txt
│   └── Aegis3.pdf
└── run_audit.py                 Master end-to-end execution script
```

---

## 8. Definition of MVP Success

The MVP milestone is considered complete when:
1. Sourcing: A raw CSV of 50,000 candidate addresses can be ingested and verified via CLI.
2. Processing: The combined engine executes Louvain partitioning, Jaccard behavioral DNA, and CEX deposit tracing in <60 seconds.
3. Accuracy: Evaluated against the LayerZero benchmark dataset with >= 85% recall and <= 2% false positive rate.
4. Output: The pipeline automatically generates a tamper-evident HTML audit report and companion CSV with SHA-256 integrity verification.
5. Integration: The FastAPI service successfully responds to verification requests from the React claim-gate component.
6. Validation: Three protocol design partners agree to run testnet pilot audits using the platform.
