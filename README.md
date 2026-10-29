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
│   │   └── cex_tracer.py        [Planned] CEX deposit address convergence
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

The pipeline has five stages. Each stage is a separate module with clean input/output boundaries so any piece can be replaced or improved independently.

```
                          AEGIS3 DETECTION PIPELINE
                          -------------------------

  [1] INGEST              [2] BUILD              [3] DETECT
  Candidate wallet     -> Directed graph      -> Run detection
  list (CSV/JSON)         with transfer           heuristics on
  + transaction           edges, pruned           the graph
  histories from          of exchange
  Etherscan/RPC           mega-hubs

       |                       |                      |
       v                       v                      v

  normalizer.py          graph_builder.py        louvain_cluster.py
  etherscan_client.py                            jaccard_dna.py
                                                 cex_tracer.py

                                                      |
                                                      v

                        [4] SCORE              [5] REPORT
                        Aggregate signals   -> Generate HTML/PDF
                        into 0-100 risk        audit report with
                        scores and assign      evidence trails and
                        tiered verdicts        integrity hashes

                             |                      |
                             v                      v

                         scorer.py            generate_report.py
                                              evidence_hasher.py
```

---

## How Detection Works (No Machine Learning)

We do not use neural networks, deep learning, or LLMs to detect Sybils. The reasons are practical, not ideological:

1. There is no verified ground-truth training dataset for "bot vs human" on anonymous blockchains. Any supervised model trained on noisy labels will produce noisy predictions.
2. Protocols need to publicly justify every disqualification. A model that says "87.4% probability of being a bot" based on latent embeddings will get torn apart on Twitter. Deterministic graph evidence ("these 42 wallets were funded by the same address within 3 minutes") cannot be argued with.
3. The computational cost and latency of inference models is unnecessary when the attack patterns are structurally visible in the transaction graph.

The three core heuristics:

**Louvain Community Partitioning** identifies dense subgraphs of wallets that transact heavily with each other but rarely with the rest of the network. Bot cartels form tight, isolated clusters because the master wallet funds all puppet wallets, and the puppets interact with the same contracts. Louvain finds these communities in seconds on graphs with hundreds of thousands of nodes.

**Jaccard Behavioral DNA** compares the set of smart contracts each wallet has interacted with. Two wallets that share 85% or more of their contract interaction history are almost certainly running the same automated script, even if they randomized their transaction timing. The Jaccard index is a simple set-overlap ratio that requires no training data.

**CEX Deposit Address Convergence** (planned) traces where wallets send their tokens after the airdrop. If 40 wallets deposit tokens into the exact same Binance deposit address, they are controlled by the same person. This heuristic has near-zero false positive rate because deposit addresses are unique per user on centralized exchanges.

Each heuristic produces an independent signal. The scorer combines them with configurable weights into a single 0-100 risk score and assigns a verdict:

- Tier 1 (Score 0-34): Eligible. No suspicious signals detected.
- Tier 2 (Score 35-69): Manual Review. Some signals present but insufficient confidence for automatic disqualification.
- Tier 3 (Score 70-100): Disqualified. Strong, multi-signal evidence of industrial coordination.

---

## Current State (What Works Today)

- The Chrome MV3 extension successfully intercepts `window.ethereum.request` calls before they reach MetaMask. This proves the transaction interception mechanism works.
- The core detection engine (GraphBuilder, Louvain, Jaccard, Scorer) runs end-to-end on the LayerZero ground-truth dataset. In benchmark testing on verified Sybil addresses, Louvain achieved 100% cartel isolation with zero cross-contamination across 3 independent bot clusters.
- The report generator produces a dark-mode HTML audit report with metrics cards, a flagged wallet evidence table, and signal breakdowns.
- `run_audit.py` ties the full pipeline together and can be executed with a single terminal command.

What does not work yet: the pipeline uses pre-downloaded CSV data and synthetic transfer edges. The planned data ingestion layer (Etherscan scraping, wallet normalization, real Jaccard fingerprinting) will replace these with live on-chain data.

---

## Local Development Setup

```
git clone https://github.com/<your-org>/Aegis3.git
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

---

## What Each Person Owns

### Laukik (CTO): Detection Engine and Infrastructure

You own everything inside `core-engine/`, `api/`, and `tests/`. Your job is to make the detection pipeline accurate, fast, and production-hardened. If a protocol runs Aegis3 on 500,000 wallets, the system should return scored results in under 60 seconds with documented precision and recall numbers.

### Chirag (CDO): Data Pipeline and Client Deliverables

You own everything inside `data-pipeline/`, `report-generator/`, and `claim-sdk/`. Your job is to build the data ingestion layer that connects the detection engine to real blockchain data, and to produce the client-facing deliverables (HTML reports, PDF exports, evidence hashes) that protocol foundations actually pay for.

### Vinit (CPO): Product-Market Fit and Commercial Validation

You do not write detection algorithms. Your work is equally critical but different in nature. You own:

1. **Customer Discovery Interviews:** Talk to 15-20 protocol founders, foundation operators, DevRel leads, and launchpad teams. Ask them how they currently handle Sybil filtering, what tools they use, what has gone wrong, who holds the budget, and what they would pay for a better solution. Document every conversation in a structured format (date, protocol name, key quotes, pain points, current tools, budget authority).

2. **Competitive Intelligence:** Maintain a living document tracking what Trusta Labs, Blockaid, Gitcoin Passport, and any new entrants are shipping. Monitor their blog posts, integration announcements, and pricing changes. Flag anything that affects our positioning.

3. **Pricing Validation:** Our current hypothesis is 15-30 lakh per launch audit. Validate this with real conversations. Find out what protocols are actually spending on security tooling today and what budget category this falls under.

4. **Design Partner Acquisition:** Identify 5 emerging protocols preparing for token launches in the next 6 months. Get at least 3 to commit as design partners (they give us access to their candidate wallet list for a free pilot audit, we give them the report, and we document the case study).

5. **Launch Operations Playbook:** Write the operational runbook for how a protocol engagement works end-to-end. From initial sales call to data handoff, audit execution, report delivery, community publication, and post-launch support. This becomes the internal operations manual.

6. **Pitch Deck and Application Materials:** Own the narrative. Keep the pitch deck updated with real data from customer interviews and benchmark results. Prepare application materials for accelerator programs.

---

## Issue Dependency Map

Issues are not independent. Some must be completed before others can start. Here is the dependency structure:

```
WEEK 1-2                    WEEK 3-4                    WEEK 5-6
--------                    --------                    --------

[Etherscan Batch        [Wallet Fingerprint      [FastAPI REST
 Scraper]                Extractor]                Scoring API]
 (Chirag)                (Chirag)                  (Laukik)
    |                       |                         |
    +--------> feeds ------>+                         |
    |                       |                         |
    |                  [Candidate Wallet              |
    |                   List CLI + Normalizer]        |
    |                   (Chirag)                      |
    |                       |                         |
    v                       v                         v
[CEX Deposit            [Automated Precision/    [React Claim-Gate
 Tracer]                 Recall Benchmark]        Component]
 (Laukik)                (Laukik)                  (Chirag)
    |                       |
    |                       |
[Temporal Decay         [SHA-256 Evidence
 Edge Weighting]         Hashes]
 (Laukik)                (Laukik)
    |                       |
    |                       v
[Connected Component    [PDF Report Export]
 Pre-filter]             (Chirag)
 (Laukik)


PARALLEL TRACK (Vinit, CPO — No code dependencies):

Week 1-2: 10 customer discovery interviews + competitive tracker v1
Week 3-4: 5 more interviews + 2 design partner LOIs + pricing validation
Week 5-6: Launch operations playbook draft + updated pitch deck with real data
```

Reading this chart:

- Arrows mean "feeds into" or "must exist before." The Etherscan scraper must exist before the fingerprint extractor can pull real contract interaction data.
- Laukik's engine work (left column) and Chirag's data work (left column) run in parallel during weeks 1-2, then converge at the benchmark and API in weeks 3-4.
- Vinit's customer work runs on a completely independent track with no code dependencies, but his findings directly influence what the engineering team prioritizes after week 4.
- The FastAPI endpoint and React claim-gate are the final integration layer that turns the pipeline into a product that protocols can actually plug into their launch flow.

---

## Branching and Commit Conventions

Use conventional commits. Every commit message follows this format:

```
type(scope): short description

Examples:
feat(core-engine): add CEX deposit address convergence tracer
feat(data-pipeline): implement Etherscan batch transaction scraper
fix(scorer): correct weight normalization when CEX signal is absent
docs(readme): add issue dependency chart and team responsibilities
test(benchmark): add full-dataset precision/recall assertion suite
```

Branch naming:

```
feature/cex-deposit-tracer
feature/etherscan-scraper
fix/scorer-weight-bug
```

Create a branch for each issue, open a pull request when done, and request review from at least one other team member before merging into `main`.
