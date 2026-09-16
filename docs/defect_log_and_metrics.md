# Defect Log and Quality Metrics

**Course:** Software Testing and Validation  


## 1. Defect Log

| Defect ID | Description | Steps to Reproduce | Expected Result | Actual Result | Severity | Priority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| DEF-001 | 30-day duration throws error | 1. Book vehicle for exactly 30 days. | Booking succeeds (Total price calculated) | Validation error thrown: "Maximum rental period is 30 days." | High | High | Closed |
| DEF-002 | Missing 'Premium Member' checkbox on form | 1. Navigate to booking form. | Checkbox for Premium is visible. | Checkbox is missing from HTML template. | Medium | Medium | Closed |
| DEF-003 | Django ORM Async error in Playwright | 1. Run pytest test_system.py | Tests pass | SynchronousOnlyOperation error thrown | Critical | High | Closed |
| DEF-004 | Typos in vehicle list template | 1. View vehicle list. | Headers spelled correctly | "Mkae" instead of "Make" | Low | Low | Closed |

### Defect Lifecycle Evidence

All defects followed the same lifecycle: **New -> Assigned -> In Progress -> Retest -> Closed**.

| Defect ID | Lifecycle evidence |
|---|---|
| DEF-001 | New during boundary testing; assigned to the business-logic owner; fixed; retested with `TC_Dur_03`; closed. |
| DEF-002 | New during UI inspection; assigned to the template owner; fixed; retested in the booking journey; closed. |
| DEF-003 | New during system-test execution; assigned to the test/integration owner; fixed; Playwright suite rerun; closed. |
| DEF-004 | New during UI inspection; assigned to the template owner; corrected; view test rerun; closed. |

## 2. Quality Metrics

| Metric | Calculation / Formula | Result | Interpretation |
| :--- | :--- | :--- | :--- |
| **Defect Density** | (Total Defects Found) / (Size of Application - e.g. KLOC or Function Points). Assuming ~0.5 KLOC. (4 / 0.5) | **8 defects / KLOC** | The codebase is very small, so the density appears artificially high, but 4 total defects is well within acceptable limits for an initial prototype. |
| **Defect Removal Efficiency (DRE)** | (Defects found pre-release) / (Total defects found pre-release + escaped defects) * 100. Assuming 0 escaped defects currently. (4 / (4+0)) * 100 | **100%** | All known defects were caught by our automated test pyramid and fixed before code was merged to the main branch. |
| **Code Coverage** | Measured with `pytest --cov=rental --cov-branch`. | **94% total; 100% branch coverage for `rental/business_logic.py`** | The core business logic exceeds the 80% branch target. The remaining uncovered lines are mainly the seed command and defensive model/view paths. |
