# Test Design Document

**Course:** Software Testing and Validation  

## 1. Equivalence Partitioning (EP) and Boundary Value Analysis (BVA)

### Variable 1: Customer Age
**Rules**: Must be >= 21. If 21-24, $20 surcharge. If >= 25, standard rate.

| Partition | Valid/Invalid | Boundaries to Test | Test Cases Derived |
| :--- | :--- | :--- | :--- |
| Age < 21 | Invalid | 20 | TC_Age_01: Age 20 (Expected: Error) |
| 21 <= Age < 25 | Valid | 21, 24 | TC_Age_02: Age 21 (Expected: Surcharge applied)<br>TC_Age_03: Age 24 (Expected: Surcharge applied) |
| Age >= 25 | Valid | 25, 30 (nominal) | TC_Age_04: Age 25 (Expected: Standard rate)<br>TC_Age_05: Age 30 (Expected: Standard rate) |

### Variable 2: Rental Duration (Days)
**Rules**: Must be >= 1 and <= 30.

| Partition | Valid/Invalid | Boundaries to Test | Test Cases Derived |
| :--- | :--- | :--- | :--- |
| Days <= 0 | Invalid | 0 and a negative value | TC_Dur_01: 0 days (Expected: Error); TC_Dur_05: -1 day (Expected: Error) |
| 1 <= Days <= 30 | Valid | 1, 7, 8, 30 | TC_Dur_02: 1 day (Expected: Success)<br>TC_Dur_06: 7 days (Expected: no long-rental discount)<br>TC_Dur_07: 8 days (Expected: long-rental discount)<br>TC_Dur_03: 30 days (Expected: Success) |
| Days > 30 | Invalid | 31 | TC_Dur_04: 31 days (Expected: Error) |

---

## 2. Decision Table Testing

**Logic**: Discount Calculation based on Premium Status and Duration.
*   Condition 1 (C1): Is Premium Member? (T/F)
*   Condition 2 (C2): Duration > 7 days? (T/F)

| Conditions / Actions | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: Premium Member?** | True | True | False | False |
| **C2: Duration > 7 Days?** | True | False | True | False |
| **Action: Discount %** | 20% | 5% | 10% | 0% |

**Test Cases Derived:**
*   **TC_DT_01** (R1): Premium=True, Days=10. Expected: 20% discount.
*   **TC_DT_02** (R2): Premium=True, Days=5. Expected: 5% discount.
*   **TC_DT_03** (R3): Premium=False, Days=10. Expected: 10% discount.
*   **TC_DT_04** (R4): Premium=False, Days=5. Expected: 0% discount.

---

## 3. State Transition Testing

**System State**: Booking Lifecycle.
**Valid States**: `REQUESTED`, `CONFIRMED`, `ACTIVE`, `RETURNED`, `CANCELLED`.

| Current State | Input / Event | Next State | Expected Output | Test Case |
| :--- | :--- | :--- | :--- | :--- |
| REQUESTED | Approve Booking | CONFIRMED | State saved as CONFIRMED | TC_ST_01 |
| REQUESTED | Cancel Booking | CANCELLED | State saved as CANCELLED | TC_ST_02 |
| CONFIRMED | Pick up Vehicle | ACTIVE | State saved as ACTIVE | TC_ST_03 |
| CONFIRMED | Cancel Booking | CANCELLED | State saved as CANCELLED | TC_ST_04 |
| ACTIVE | Return Vehicle | RETURNED | State saved as RETURNED | TC_ST_05 |
| CANCELLED | Approve Booking | N/A (Invalid) | InvalidStateTransitionError | TC_ST_06 |

## 4. Acceptance/UAT Scenarios

| ID | User scenario | Expected result | Automated evidence |
|---|---|---|---|
| UAT-01 | Customer books an available vehicle with age 28 for three days. | Booking is created and a confirmation message is shown. | `rental/tests/test_system.py::test_successful_booking_journey` |
| UAT-02 | Customer submits age 19. | Booking is rejected and the age error is visible. | `rental/tests/test_system.py::test_failed_booking_journey_underage` |
| UAT-03 | Customer submits a duration outside 1 to 30 days. | Booking is rejected with a duration error. | Unit and view tests |
