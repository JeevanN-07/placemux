# Metric Dictionary & Baseline Report

| Metric Name | Definition | Formula / Grain | Source Column | Value |
| :--- | :--- | :--- | :--- | :--- |
| **Total Students** | Total count of evaluated student submissions | `COUNT(student_id)` | `student_id` | 5 |
| **Average Score** | Mean assessment score across all students | `AVG(score)` | `score` | 66.4 |
| **Pass Rate (%)** | Percentage of students achieving a passing grade | `(COUNT(passed='Yes') / COUNT(*)) * 100` | `passed` | 60.0% |
| **Highest Score** | Maximum score recorded | `MAX(score)` | `score` | 90 |
| **Lowest Score** | Minimum score recorded | `MIN(score)` | `score` | 42 |

### Verification Audit
- Row Count Validated: 5 total records
- Deterministic Aggregation: Verified matching manual counts and SQL aggregations.
