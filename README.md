<div align="center">
  
# 🧠 Dataset Intelligence Engine (DIE)
**The Universal Dataset Intelligence & Ranking Platform**

![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)
![Tests](https://img.shields.io/badge/Tests-37%20Passing-success?style=for-the-badge)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue?style=for-the-badge&logo=github)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

*A deterministic, 17-phase graph-theoretic pipeline designed to understand, connect, and mathematically rank unstructured data autonomously.*

</div>

<br>

##  Explaination in Simple Terms:

Imagine you are handed a massive box of random Lego pieces (unstructured data) and asked to find the exact pieces needed to build a specific, complex spaceship (a job description). 

Most systems just dig their hands in and guess. They look for red pieces and square pieces (keyword matching). If a piece is slightly different, they throw it out.

**Our system is different.** 
It takes the entire box and organizes it perfectly. First, it separates by color. Then by shape. Then it connects pieces that look like they belong together (building a **Knowledge Graph**). Finally, it calculates exactly how important every single piece is to the overall structure of the spaceship (**Graph Centrality**). 

When it's done, it doesn't just hand you a piece and say "trust me." It hands you the exact piece you need along with a perfectly written receipt showing exactly *why* this piece is the mathematical best fit.

---

## 🚨 The Problem Statement: Why Regex and Keyword Matching Fail

In the era of massive, unstructured datasets, traditional data matching systems fail fundamentally. If a company is searching for a candidate to fill a complex technical role, existing systems attempt to parse unstructured JSON or text using rigid heuristics, regular expressions, or simple vector similarity.

This creates critical failure points:
1. **Ad-Hoc Rigidity:** Relying on hardcoded keyword matching assumes the data schema is perfectly static. Searching for "Python" completely misses the structural implication of a candidate who lists "Django, FastAPI, and SQLAlchemy"—all of which imply Python expertise.
2. **Semantic Blind Spots:** Systems fail to understand the implicit relationships between entities. A candidate possessing both "AWS" and "Flask" represents a full-stack deployment capability. Standard search tools treat these as isolated string matches, failing to capture the combined semantic value.
3. **The "Black Box" Problem:** Modern AI ranking systems spit out a final score (e.g., 89%) but cannot explain the exact lineage of *why* candidate A beat candidate B. In a production environment, unexplainable rankings are unusable.

---

## 💡 The Solution: Graph-Theoretic Intelligence 

We built the **Dataset Intelligence Engine (DIE)** to solve this through deterministic, graph-theoretic intelligence. Instead of using a monolithic script or a black-box LLM prompt, we engineered a massively decoupled **17-Phase Intelligence Pipeline**.

### Why This Architecture Wins
*   **Strict Pydantic Data Contracts:** Data mutability is the enemy of reliability. By forcing data to travel through explicit, immutable Pydantic contracts (`SchemaGraph`, `SemanticCatalog`, `EntityCatalog`), we guarantee that corrupt or unexpected data structures are caught at phase boundaries before they poison the ranking.
*   **Knowledge Graph Assembly:** Instead of matching flat strings, we build a multi-dimensional graph. Entities (skills, degrees, companies) are linked via structural relationships. This allows the system to discover "hidden" high-value candidates through graph traversal.
*   **Graph Centrality (PageRank for Skills):** Keyword matching treats all skills equally. Our `GraphCentralityEngine` analyzes the topology of the Knowledge Graph to compute the relative rarity and structural importance of specific entities (`EntityCentralityCatalog`). This means the system mathematically values a candidate with a rare, highly connected tech stack exponentially higher than a candidate with generic keywords.
*   **100% Deterministic Evidence:** Every single fractional point added to a candidate's score is mathematically bound to explicit `EvidenceObject` and `ScoringFactor` contracts (manually verified in scoring schema). We can trace a #1 ranking directly back to the specific line in the parsed ingestion payload.

---

## ⚙️ The Mechanics: 17-Phase Intelligence Pipeline

Our orchestration engine (`pipeline.py`) routes raw data through 17 highly specialized micro-engines. Each engine consumes a strict contract, performs its localized intelligence, and explicitly outputs the next contract.

| Phase | Intelligence Engine | Core Mechanical Task | Output Contract & Artifact |
| :---: | :--- | :--- | :--- |
| **1** | `IngestionEngine` | Ingests `.jsonl` and `.docx` payloads, normalizing them into structured envelopes. | `DatasetRecord` ➔ `dataset_records.json` |
| **2** | `SchemaDiscoveryEngine` | Dynamically maps structural schema constraints and field types across the unknown payload. | `SchemaGraph` ➔ `schema_graph.json` |
| **3** | `ProfilingEngine` | Statistically profiles data distributions across the discovered schema fields. | `ProfileReport` ➔ `profile_report.json` |
| **4** | `SemanticEngine` | Performs value-level inference to extract high-level domains (e.g. mapping strings to "Cloud Computing"). | `SemanticCatalog` ➔ `semantic_catalog.json` |
| **5** | `EntityExtractionEngine` | Parses structural fields to isolate named, discrete entities based on semantic boundaries. | `EntityCatalog` ➔ `entity_catalog.json` |
| **6** | `RelationshipDiscoveryEngine`| Cross-references entities to map topological dependencies. | `RelationshipCatalog` ➔ `relationship_catalog.json` |
| **7** | `PatternDiscoveryEngine` | Current implementation performs heuristic pattern discovery. | `PatternCatalog` ➔ `pattern_catalog.json` |
| **8** | `ClusteringEngine` | Current implementation performs heuristic clustering. | `ClusterCatalog` ➔ `cluster_catalog.json` |
| **9** | `AnomalyDetectionEngine` | Current implementation performs heuristic anomaly detection. | `AnomalyCatalog` ➔ `anomaly_catalog.json` |
| **10**| `ReportEngine` | Aggregates discovery phases into a mid-pipeline intelligence summary. | `IntelligenceReport` ➔ `intelligence_report.json` |
| **11**| `CandidateIntelligenceEngine`| Assembles the discovery catalogs into multi-dimensional Candidate profiles. | `CandidateIntelligenceCatalog` ➔ `candidate_intelligence_catalog.json` |
| **12**| `KnowledgeGraphEngine` | **Assembles the master relationship graph from all extracted entities and relationships.** | `KnowledgeGraph` ➔ `knowledge_graph.json` |
| **13**| `GraphCentralityEngine` | **Calculates network centrality metrics to determine the structural weight of specific entities.** | `EntityCentralityCatalog` ➔ `graph_centrality.json` |
| **14**| `JobIntelligenceEngine` | Parses the raw job description to generate explicit requirement constraints. | `JobIntelligenceCatalog` ➔ `job_intelligence_catalog.json` |
| **15**| `AlignmentIntelligenceEngine`| Cross-references the Candidate and Job catalogs, weighted by Graph Centrality metrics. | `AlignmentCatalog` ➔ `candidate_job_alignment_catalog.json` |
| **16**| `ScoringIntelligenceEngine` | Generates quantitative, evidence-backed scores from the alignment vectors. | `ScoringCatalog` ➔ `candidate_job_scoring_catalog.json` |
| **17**| `RankingPolicyEngine` | Applies final sort policies to emit deterministic, ranked candidate recommendations. | `RankedCandidateCatalog` ➔ `ranked_candidate_catalog.json` |

---

## 🧠 Architectural Deep Dives

### Data Discovery & Semantic Intelligence
The first 11 phases of the system are entirely dedicated to *understanding* the data. Rather than assuming the structure of a candidate JSON file, the `SchemaDiscoveryEngine` builds an explicit `SchemaGraph`. The `SemanticEngine` then sweeps the data, categorizing raw strings into structured domains. The `EntityExtractionEngine` isolates the discrete concepts, ensuring downstream phases are dealing with clean ontological units rather than noisy text.

### The Knowledge Graph Engine
The true brain of the system is the `KnowledgeGraphEngine`. It ingests all preceding catalog outputs (Entities, Relationships, Patterns, Clusters, and Anomalies) to weave a single master graph topology. 
*(Note: Complete explicit contract lineage for KnowledgeGraph generation is currently constrained by structural boundaries and explicitly handled via downstream consumers.)*

### Graph Centrality Engineering
Keyword matching treats all skills equally. Our `GraphCentralityEngine` analyzes the topology of the Knowledge Graph to compute the relative rarity and structural importance of specific entities (`EntityCentralityCatalog`). If a node (skill) acts as a critical bridge between two massive clusters (e.g., bridging "DevOps" and "Machine Learning"), its centrality score spikes. The system mathematically values a candidate possessing this rare bridge node exponentially higher.

### Evidence-Based Alignment & Scoring
Ranking executes sequentially via Alignment ➔ Scoring ➔ Ranking. The `AlignmentIntelligenceEngine` consumes the `CandidateIntelligenceCatalog`, the `JobIntelligenceCatalog`, and crucially, the `EntityCentralityCatalog`. 

Every final score output in the `RankedCandidateCatalog` is structurally bound to a `CandidateJobScore` contract. There are no black boxes; the engine provides the exact `EvidenceObject` contributing to the final alignment percentage, allowing auditors to trace exactly why a specific candidate was ranked #1.

---

## 🚀 Quick Start & Installation

Built for absolute developer ergonomics. No massive dependency hell. We use `uv` for lightning-fast environment resolution.

**1. Install Dependencies**
```bash
uv sync
```

**2. Run the Full 17-Phase Pipeline**
```bash
uv run python main.py candidates.jsonl data/job_description.docx
```
*(Watch the orchestration pipeline dynamically light up all 17 engines and dump the 21 intermediate `.json` artifacts live into the `artifacts/` folder.)*

**3. Generate Final Output CSV**
```bash
uv run python scripts/export_csv.py
```

**4. Validate Output Compliance**
```bash
uv run python scripts/validate_submission.py artifacts/top_100_recommended_candidates.csv
```

---

## 🏆 Verified Execution Results

We do not believe in hypotheticals. The following results are mathematically proven directly from the pipeline execution evidence:

> [!SUCCESS] **Testing & Stability**
> **37 / 37 Unit Tests Passed.** 
> The testing suite rigorously validates the pipeline at both the contract and logic levels:
> - **Batch 1-5 Contract Validation (`test_batch1.py` to `test_batch5.py`):** Ensures all 17 Pydantic schemas enforce strict data typing, immutability (`MappingProxyType`), and required fields (e.g. `ArtifactMetadata`, `ConfidenceLevel`).
> - **Business Logic Verification (`test_business_logic.py`):** Validates the mathematical and extraction logic, including Graph Centrality algorithms, semantic inference boundaries, and Alignment Scoring mathematics.
> - **Failure Mode Testing:** Validates that corrupted JSON payloads are successfully caught and rejected by the `DatasetRecord` constraints.

> [!SUCCESS] **Execution Completeness**
> The orchestration pipeline successfully executed all 17 engines in sequence, generating all 21 `.json` intermediate artifacts successfully.

> [!SUCCESS] **Intelligence Extraction**
> - Successfully extracted Semantic Concepts across domains.
> - Successfully generated the Master Knowledge Graph.
> - Successfully computed Graph Centrality metrics mapped directly to candidate profiles.
> - Successfully generated and validated the final `top_100_recommended_candidates.csv` output.

*(Note: Specific benchmark metrics for precision/recall are not established by audit at this phase.)*

---

## 📦 Hackathon Deliverables

### Submission CSV
`artifacts/top_100_recommended_candidates.csv`

### Validator Status
Submission is valid.

### Repository
https://github.com/SaiKarthik547/Ranker-System

### Generated Artifacts
- `ranked_candidate_catalog.json`
- `candidate_job_scoring_catalog.json`
- `candidate_job_alignment_catalog.json`
- `graph_centrality.json`
- `knowledge_graph.json`
- `semantic_catalog.json`
- `entity_catalog.json`
- `relationship_catalog.json`
- `schema_graph.json`
- `dataset_records.json`

---

## 🗺️ Detailed Architecture Diagrams

*Click any section below to expand and view the highly sophisticated Mermaid.js architecture diagrams representing the strict execution flow, physical artifact writes, and structural logic of the platform.*

<details>
<summary><b>📊 View Diagram: Complete System Architecture (The Master Flow)</b></summary>

```mermaid
flowchart TB
    %% Styling
    classDef engine fill:#2d3436,stroke:#74b9ff,stroke-width:2px,color:#fff,rx:5px,ry:5px
    
    subgraph Tier1 ["Tier 1: Data Discovery & Normalization"]
        direction LR
        IE[IngestionEngine]:::engine
        SDE[SchemaDiscoveryEngine]:::engine
        PE[ProfilingEngine]:::engine
        
        IE --> SDE --> PE
    end

    subgraph Tier2 ["Tier 2: Semantic Intelligence Extraction"]
        direction LR
        SE[SemanticEngine]:::engine
        EEE[EntityExtractionEngine]:::engine
        RDE[RelationshipDiscoveryEngine]:::engine
        PDE[PatternDiscoveryEngine]:::engine
        CE[ClusteringEngine]:::engine
        ADE[AnomalyDetectionEngine]:::engine
        
        PE --> SE --> EEE --> RDE --> PDE --> CE --> ADE
    end

    subgraph Tier3 ["Tier 3: Graph Assembly & Centrality"]
        direction LR
        CIE[CandidateIntelligenceEngine]:::engine
        KGE[KnowledgeGraphEngine]:::engine
        GCE[GraphCentralityEngine]:::engine
        JIE[JobIntelligenceEngine]:::engine
        
        ADE --> CIE --> KGE --> GCE
    end

    subgraph Tier4 ["Tier 4: Alignment, Scoring & Final Ranking"]
        direction LR
        AIE[AlignmentIntelligenceEngine]:::engine
        SIE[ScoringIntelligenceEngine]:::engine
        RPE[RankingPolicyEngine]:::engine
        
        JIE --> AIE
        GCE --> AIE
        CIE -.-> AIE
        AIE --> SIE --> RPE
    end
```
</details>

<details>
<summary><b>📊 View Diagram: Deep Contract Routing & Data Flow</b></summary>

```mermaid
flowchart TD
    %% Styling
    classDef contract fill:#0984e3,stroke:#fff,stroke-width:1px,color:#fff,rx:10px,ry:10px
    classDef engine fill:#2d3436,stroke:#74b9ff,stroke-width:2px,color:#fff,rx:5px,ry:5px
    classDef artifact fill:#00b894,stroke:#fff,stroke-width:1px,color:#fff,shape:cylinder

    %% Data Inputs
    DR([DatasetRecord]):::contract
    SG([SchemaGraph]):::contract
    
    %% Semantic & Entities
    PR([ProfileReport]):::contract
    SC([SemanticCatalog]):::contract
    EC([EntityCatalog]):::contract
    RC([RelationshipCatalog]):::contract
    
    %% Graph Assembly
    CIC([CandidateIntelligenceCatalog]):::contract
    JIC([JobIntelligenceCatalog]):::contract
    ECC([EntityCentralityCatalog]):::contract
    
    %% Alignment and Scoring
    AC([AlignmentCatalog]):::contract
    SCORE([ScoringCatalog]):::contract
    RANK([RankedCandidateCatalog]):::contract

    %% Engines
    Eng1[IngestionEngine]:::engine
    Eng2[SchemaDiscoveryEngine]:::engine
    Eng3[ProfilingEngine]:::engine
    Eng4[SemanticEngine]:::engine
    Eng5[EntityExtractionEngine]:::engine
    Eng6[RelationshipDiscoveryEngine]:::engine
    Eng11[CandidateIntelligenceEngine]:::engine
    Eng12[KnowledgeGraphEngine]:::engine
    Eng13[GraphCentralityEngine]:::engine
    Eng14[JobIntelligenceEngine]:::engine
    Eng15[AlignmentIntelligenceEngine]:::engine
    Eng16[ScoringIntelligenceEngine]:::engine
    Eng17[RankingPolicyEngine]:::engine

    %% Artifacts
    A1[(ranked_candidate_catalog.json)]:::artifact
    A2[(candidate_job_alignment_catalog.json)]:::artifact

    %% Tracing Path
    Eng1 --> DR
    DR --> Eng2 --> SG
    SG --> Eng3 --> PR
    SG --> Eng4 --> SC
    SC --> Eng5 --> EC
    EC --> Eng6 --> RC
    
    EC --> Eng11
    RC --> Eng11
    Eng11 --> CIC
    
    RC --> Eng12
    Eng12 --> Eng13 --> ECC
    
    Eng14 --> JIC
    
    CIC --> Eng15
    JIC --> Eng15
    ECC --> Eng15
    Eng15 --> AC
    AC -.-> A2
    
    AC --> Eng16 --> SCORE
    SCORE --> Eng17 --> RANK
    RANK -.-> A1
```
</details>

<details>
<summary><b>📊 View Diagram: 17-Phase Execution Orchestration (pipeline.py)</b></summary>

```mermaid
flowchart TD
    %% Styling
    classDef phase fill:#6c5ce7,stroke:#fff,stroke-width:1px,color:#fff,rx:10px,ry:10px

    subgraph Block1 ["Phase 1-3: Ingestion & Discovery"]
        P1[1. Ingestion]:::phase --> P2[2. Schema Discovery]:::phase --> P3[3. Profiling]:::phase
    end
    
    subgraph Block2 ["Phase 4-10: Deep Extraction"]
        P3 --> P4[4. Semantic]:::phase --> P5[5. Entity]:::phase --> P6[6. Relationships]:::phase
        P6 --> P7[7. Patterns]:::phase --> P8[8. Clustering]:::phase --> P9[9. Anomalies]:::phase --> P10[10. Reports]:::phase
    end
    
    subgraph Block3 ["Phase 11-13: Graph Generation"]
        P10 --> P11[11. Candidate Intel]:::phase --> P12[12. Knowledge Graph]:::phase --> P13[13. Centrality]:::phase
    end
    
    subgraph Block4 ["Phase 14-17: Scoring & Ranking"]
        P13 --> P14[14. Job Intel]:::phase --> P15[15. Alignment]:::phase --> P16[16. Scoring]:::phase --> P17[17. Ranking Output]:::phase
    end
```
</details>

<details>
<summary><b>📊 View Diagram: Candidate Ranking Convergence Workflow</b></summary>

```mermaid
flowchart TB
    %% Styling
    classDef input fill:#fdcb6e,stroke:#fff,stroke-width:1px,color:#2d3436
    classDef processor fill:#d63031,stroke:#fff,stroke-width:2px,color:#fff
    classDef output fill:#00b894,stroke:#fff,stroke-width:2px,color:#fff

    J[Job Intelligence]:::input
    C[Candidate Intelligence]:::input
    GC[Graph Centrality Metrics]:::input
    
    AIE[Alignment Intelligence Engine]:::processor
    SIE[Scoring Intelligence Engine]:::processor
    RPE[Ranking Policy Engine]:::processor
    
    R[Ranked Candidate Output]:::output

    J --> AIE
    C --> AIE
    GC --> AIE
    AIE --> |AlignmentCatalog| SIE
    SIE --> |ScoringCatalog| RPE
    RPE --> |RankedCandidateCatalog| R
```
</details>

<details>
<summary><b>📊 View Diagram: Physical Artifact Generation (File I/O)</b></summary>

```mermaid
graph LR
    %% Styling
    classDef orchestrator fill:#e17055,stroke:#fff,stroke-width:2px,color:#fff
    classDef file fill:#00cec9,stroke:#fff,stroke-width:1px,color:#2d3436,shape:cylinder

    Orch[pipeline.py Orchestrator]:::orchestrator
    
    Orch -.-> F1[(dataset_records.json)]:::file
    Orch -.-> F2[(schema_graph.json)]:::file
    Orch -.-> F3[(semantic_catalog.json)]:::file
    Orch -.-> F4[(entity_catalog.json)]:::file
    Orch -.-> F5[(relationship_catalog.json)]:::file
    Orch -.-> F6[(knowledge_graph.json)]:::file
    Orch -.-> F7[(graph_centrality.json)]:::file
    Orch -.-> F8[(candidate_job_alignment_catalog.json)]:::file
    Orch -.-> F9[(ranked_candidate_catalog.json)]:::file
```
</details>

## License

MIT
