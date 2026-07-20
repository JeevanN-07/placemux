# Phase 1 Data Lifecycle & Lineage Document

## 1. Data Sources & Update Frequency
* **Source Name**: Student Assessment CSV Exports (`starter_data.csv`).
* **Origin**: Academic Evaluation Database / LMS Platform.
* **Update Cadence**: Daily batch updates.

## 2. End-to-End Flow Diagram
[ Raw CSV Files ] ──( Ingestion )──> [ Local Data Folder (/data) ] ──( Profiling & Audit )──> [ Cleaned DataFrame ] ──( Aggregations )──> [ Final Analytics Report / Dashboard ]


## 3. Source of Truth Matrix
| Metric Name | Source of Truth | Location / Table | Refresh Rate | Owner |
|---|---|---|---|---|
| **Student Score** | LMS Evaluation DB | `data/starter_data.csv` -> `score` | Batch (Daily) | Data Engineering Team |
| **Pass/Fail Status** | Academic Policy Engine | `data/starter_data.csv` -> `passed` | Batch (Daily) | Academic Operations |
| **Average Score Aggregate** | Analytics DataFrame | `data_profiling.ipynb` | On-Demand | Data Analyst (You) |

## 4. Stage Ownership & Transformations
* **Ingestion Stage**: Managed by Data Analyst using Python/Pandas (`pd.read_csv`).
* **Transformation & Profiling Stage**: Quality validation, missingness checks, and distribution audits executed by Data Analyst[cite: 2].
* **Reporting Stage**: Metric generation (`mean()`, `count()`) rendered in Jupyter Notebooks[cite: 1].

## 5. Retention & Privacy Rules
* **Retention Policy**: Raw landing data retained for 90 days; processed aggregates retained indefinitely.
* **Privacy Controls**: Student PII isolated; dataset tracked locally and kept out of public version control via `.gitignore`[cite: 1].

## 6. End-to-End Metric Verification Trace
* **Tested Metric**: `Average Score = 66.4`[cite: 1]
* **Trace**:
  1. **Source**: Ingested `score` column values `[85, 42, 90, 65, 50]` from `data/starter_data.csv`[cite: 1].
  2. **Audit**: Confirmed 0 null values and valid numerical types (`int64`) during pre-project profiling[cite: 2].
  3. **Output**: Executed `df['score'].mean()` in `data_ingestion.ipynb` resulting in `66.4`[cite: 1].