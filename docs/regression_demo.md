# Regression Demonstration Record

**Course:** Software Testing and Validation  
**Group members:** Eyob Mulugeta (ATE/4778/14); Afomia Birhanu (ATE/2368/14)

## Purpose

Show that continuous integration catches a change that breaks an existing test and that the corrected change restores a passing build.

## Reproducible Procedure

1. Temporarily change `YOUNG_DRIVER_SURCHARGE` in `rental/business_logic.py` from `20.0` to `15.0`.
2. Push the change to a branch or open pull request. GitHub Actions should fail at `test_age_at_minimum_with_surcharge`, which expects `$350.00` and receives `$325.00`.
3. Record the failed workflow URL or screenshot in the submission.
4. Restore `YOUNG_DRIVER_SURCHARGE` to `20.0`.
5. Push the fix and record the passing workflow URL or screenshot.

The local workspace is not currently a Git checkout, so the group must perform the push and attach the actual hosted build evidence in the shared repository before submission.