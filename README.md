# Aegis3

Enterprise token launch integrity and Sybil defense for Web3 protocol foundations.

Aegis3 helps protocol teams run fair, defensible token distributions by detecting coordinated bot cartels in candidate wallet lists and producing auditable, explainable evidence that can be published to the community without PR backlash.

---

## What This Repository Contains

```
Aegis3/
├── core-engine/                 The detection brain
│   ├── graph_builder.py         Ingests wallets and transfer edges into a directed NetworkX graph
│   ├── filters/
│   │   ├── louvain_cluster.py   Community partitioning (groups tightly linked wallets)
│   │   ├── jaccard_dna.py       Behavioral sequence similarity (catches scripted contract calls)
│   │   ├── cex_tracer.py        [Planned] CEX deposit address convergence tracer
│   │   ├── entropy_clock.py     [Planned] Population interval entropy and diurnal rhythm analysis
│   │   └── universe_sandbox.py  [Planned] Bounded-universe ecosystem leakage filter
│   └── scorer.py                Aggregates signals into 0-100 risk scores with tiered verdicts
│
├── data-pipeline/               Data sourcing and normalization
│   ├── sql/                     Dune Analytics queries for historical airdrop data
│   ├── extractors/              [Planned] Etherscan/Arbiscan RPC batch scrapers
│   ├── datasets/                Ground-truth CSVs (LayerZero verified Sybils)
│   └── normalizer.py            [Planned] Wallet list validator and deduplicator
│
├── report-generator/            Client-facing deliverables
│   └── generate_report.py       Produces branded HTML audit reports with signal breakdowns
│
├── api/                         [Planned] FastAPI REST endpoint for programmatic scoring
├── claim-sdk/                   [Planned] React component protocols embed on their claim page
├── Extension/                   Chrome MV3 transaction interceptor prototype
├── notebooks/                   Research notebooks (EDA, benchmarks, visualizations)
├── tests/                       [Planned] Automated benchmark suite
├── Docs/                        Architecture docs, pitch materials, generated reports
└── run_audit.py                 Master CLI: runs the full pipeline end-to-end
```

---

## System Architecture

The pipeline operates across five distinct phases, moving from raw on-chain data to final cryptographic governance deliverables.

```
                          AEGIS3 DETECTION PIPELINE
                          -------------------------

  [1] INGEST              [2] BUILD              [3] DETECT (Multi-Signal)
  Candidate wallet     -> Directed graph      -> • Louvain Partitioning (Topology)
  list (CSV/JSON)         with transfer          • Jaccard DNA (Contract Overlap)
  + live traces from      edges, pruned          • CEX Deposit Convergence (Cash-out)
  Etherscan/RPC           of exchange            • Population Entropy (Timing RNG)
                          mega-hubs              • Bounded Universe (Activity Leakage)

       |                       |                               |
       v                       v                               v

  normalizer.py          graph_builder.py              louvain_cluster.py
  etherscan_client.py                                  jaccard_dna.py
                                                       cex_tracer.py
                                                       entropy_clock.py
                                                       universe_sandbox.py

                                                               |
                                                               v

                        [4] SCORE                      [5] REPORT
                        Aggregate signals           -> Generate HTML/PDF
                        into 0-100 risk                audit report with
                        scores and assign              evidence trails and
                        tiered verdicts                integrity hashes

                             |                              |
                             v                              v

                         scorer.py                    generate_report.py
                                                      evidence_hasher.py
```

---

## How Detection Works (No Machine Learning)

We do not use neural networks, deep learning, or LLMs to detect Sybils. The reasons are practical, not ideological:

1. There is no verified ground-truth training dataset for "bot vs human" on anonymous blockchains. Any supervised model trained on noisy labels will produce noisy predictions.
2. Protocols need to publicly justify every disqualification. A model that says "87.4% probability of being a bot" based on latent embeddings will get torn apart on Twitter. Deterministic graph evidence ("these 42 wallets were funded by the same address within 3 minutes") cannot be argued with.
3. The computational cost and latency of inference models is unnecessary when the attack patterns are structurally visible in the transaction graph.

The multi-signal defense framework:

- **Louvain Community Partitioning:** Identifies dense subgraphs of wallets that transact heavily with each other but rarely with the rest of the network. Bot cartels form tight, isolated clusters because the master wallet funds all puppet wallets, and the puppets interact with the same contracts.
- **Jaccard Behavioral DNA:** Compares the set of smart contracts each wallet has interacted with. Two wallets that share 85% or more of their contract interaction history are running the same automated script.
- **CEX Deposit Address Convergence:** Traces where wallets send their tokens after the airdrop. If 40 wallets deposit tokens into the exact same Binance deposit address, they are controlled by the same person.
- **Population Entropy & Diurnal Activity Analysis:** Evaluates whether transaction inter-arrival times follow natural human bursty Poisson processes and sleep cycles, catching attackers who attempt to randomize sleep timers.
- **Bounded-Universe Sandbox Detection:** Measures ecosystem leakage. Real users interact with diverse protocols across the chain (meme coins, gaming, governance), whereas automated cartels confine activity strictly within token qualification tasks.

---

## Issue Dependency & Sprint Roadmap

```
WEEK 1-2: DATA & CORE HEURISTICS
--------------------------------
[#4 Etherscan Batch Scraper] (Chirag)
       |
       +------ feeds -----> [#5 Wallet Fingerprint Extractor] (Chirag)
       |                            |
       v                            v
[#1 CEX Deposit Tracer] (Laukik)    [#6 Candidate List CLI] (Chirag)
       |
[#2 Temporal Decay Weights] (Laukik)
       |
[#3 Connected Component Pre-Filter] (Laukik)


WEEK 3-4: ADVANCED ANTI-EVASION & VERIFICATION
----------------------------------------------
[#12 Population Entropy & Diurnal Clock] (Laukik)
       |
[#13 Bounded-Universe Sandbox Filter] (Laukik)
       |
       +------ feeds -----> [#9 Automated Precision/Recall Benchmark] (Laukik)
                            [#7 SHA-256 Evidence Hashes] (Laukik)
                                   |
                            [#8 PDF Report Export] (Chirag)


WEEK 5-6: INTEGRATION & CLAIM GATE
----------------------------------
[#10 FastAPI REST Scoring Endpoint] (Laukik)
       |
       +------ connects to -> [#11 React Claim-Gate Component] (Chirag)


PARALLEL COMMERCIAL TRACK (Vinit, CPO):
---------------------------------------
[#14 Protocol Founder Discovery Interviews] (Weeks 1-3)
       |
Targeted Design Partner LOIs & Launch Operations Playbook (Weeks 4-6)
```

---

## Current State (What Works Today)

- The Chrome MV3 extension successfully intercepts `window.ethereum.request` calls before they reach MetaMask. This proves the transaction interception mechanism works.
- The core detection engine (GraphBuilder, Louvain, Jaccard, Scorer) runs end-to-end on the LayerZero ground-truth dataset. In benchmark testing on verified Sybil addresses, Louvain achieved 100% cartel isolation with zero cross-contamination across 3 independent bot clusters.
- The report generator produces a dark-mode HTML audit report with metrics cards, a flagged wallet evidence table, and signal breakdowns.
- `run_audit.py` ties the full pipeline together and can be executed with a single terminal command.

---

## Local Development Setup

```
git clone https://github.com/coder-hub-l/Aegis3.git
cd Aegis3
python -m venv .venv

# Windows PowerShell:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

# Linux/Mac:
# source .venv/bin/activate

pip install --upgrade pip
pip install networkx python-louvain pandas matplotlib scikit-learn ipykernel

# Register Jupyter kernel (for notebooks):
python -m ipykernel install --user --name=aegis3 --display-name "Python (Aegis3)"
```

Run the full audit pipeline:

```
python run_audit.py
```

Output is written to `Docs/launch_audit_report.html` and `Docs/scored_allocations.csv`.

---

## Team

| Person | Role | Primary Responsibility |
| :--- | :--- | :--- |
| Laukik Wani | CTO, Systems and Security | Core detection engine, graph algorithms, API architecture, benchmarking, infrastructure |
| Chirag Janbandhu | CDO, Data Operations | On-chain data sourcing (Etherscan, Dune), dataset curation, report generator, claim SDK frontend |
| Vinit | CPO, Product Management | Customer discovery, protocol outreach, pricing validation, competitive intelligence, launch operations playbook |
