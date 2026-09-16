# Vehicle Rental System: Software Testing and Validation Final Project

## Group Members

| Member | Student ID | Main responsibilities |
|---|---|---|
| Eyob Mulugeta | ATE/4778/14 | Business logic, unit/integration tests, CI configuration |
| Afomia Birhanu | ATE/2368/14 | Formal test design, Playwright system/UAT tests, defect and report documentation |

This README describes the application, testing evidence, and reproducible commands for the final project.

---

## 1. What We Built

We built a **Vehicle Rental System** using Django (Python). The application allows users to view available vehicles and submit a booking request. 

We specifically chose this domain because it naturally contains all the elements your teacher demanded for formal testing techniques:
*   **Equivalence Partitioning (EP) & Boundary Value Analysis (BVA)**: We evaluate the customer's age (must be > 21) and the rental duration (between 1 and 30 days).
*   **Decision Tables**: We calculate discounts based on a combination of rules (e.g., Is the user a Premium Member? Is the rental > 7 days?).
*   **State Transitions**: A vehicle booking moves through a strict lifecycle (`REQUESTED` -> `CONFIRMED` -> `ACTIVE` -> `RETURNED`).
*   **Multi-step User Journey**: A user browses vehicles, fills out a form, and confirms a booking through the browser using Playwright.

---

## 2. How it Works (File Aspect & Architecture)

To ensure the highest quality of testing (and to show off good software engineering practices), we used an **Object-Oriented Programming (OOP)** approach. Instead of stuffing all the logic into Django models or views, we extracted the core business rules into pure Python classes (`RentalCalculator` and `BookingManager`). This makes our code infinitely easier to unit test.

Here is what the project looks like from a file aspect:

```text
├── Dockerfile                  # Containerization setup for the app
├── Jenkinsfile                 # Jenkins CI/CD pipeline configuration
├── docker-compose.yml          # Spins up the Django app alongside Jenkins
├── requirements.txt            # Python dependencies (Django, pytest, playwright)
├── pytest.ini                  # Pytest configuration file
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── docs/                       # ALL REQUIRED PDF DELIVERABLES
│   ├── defect_log_and_metrics.pdf
│   ├── test_design_document.pdf
│   ├── test_plan.pdf
│   ├── test_summary_report.pdf
│   ├── defect_log_and_metrics.md
│   ├── test_design_document.md
│   ├── test_plan.md
│   └── test_summary_report.md
└── rental/                     # The core Django Application
    ├── business_logic.py       # OOP classes (RentalCalculator, BookingManager)
    ├── models.py               # Database schemas (Vehicle, Customer, Booking)
    ├── views.py                # Web logic (links business logic to the UI)
    ├── templates/              # HTML frontend files
    │   └── rental/
    │       ├── base.html
    │       ├── booking_form.html
    │       └── vehicle_list.html
    └── tests/                  # THE TEST PYRAMID
        ├── test_business_logic.py  # Unit Tests
        ├── test_models.py          # Integration Tests (Models)
        ├── test_views.py           # Integration Tests (Views)
        ├── test_system.py          # E2E Playwright Tests
        └── pages.py                # Page Object Model (POM) classes for Playwright
```

---

## 3. How We Satisfied the Teacher's Requirements

Your teacher provided a "Concept Coverage Map" in section 8 of the brief. Here is exactly how we hit every single target:

| Course Concept | How we fulfilled it in this project |
| :--- | :--- |
| **Error, fault, failure; Verification vs Validation** | Addressed in `docs/test_summary_report.md` (Part I reflection) covering DEF-001. |
| **Test design techniques** | Documented in `docs/test_design_document.md`. We applied EP/BVA (Age & Duration), Decision Tables (Discounts), and State Transitions (Booking states). |
| **Coverage: statement and branch** | The measured run produced **94% total coverage** and **100% branch coverage for `rental/business_logic.py`**, exceeding the 80% core-logic target. |
| **Levels: unit, integration, system** | Our `rental/tests/` folder is neatly divided into `test_business_logic.py` (Unit), `test_models/views.py` (Integration), and `test_system.py` (System). |
| **Test doubles: stub, mock, fake, spy** | `test_business_logic.py` uses a `MagicMock` for the `EmailService` collaborator. |
| **The test pyramid** | We have 17 fast Unit Tests, 7 Integration Tests, and 2 slower System Tests, perfectly mimicking the pyramid shape. |
| **Browser automation and the Page Object Pattern** | The instructor permits any suitable technology; this project uses Playwright with Page Objects in `rental/tests/pages.py`. |
| **Continuous Integration & Regression** | GitHub Actions and Jenkins run the same test and coverage commands. The regression scenario is documented in `docs/test_summary_report.md`; pipeline screenshots/build URLs must be attached by the group after the runs. |
| **Test management (Plan, criteria, risk)** | Fully documented in `docs/test_plan.md`. |
| **Defect management and metrics** | We logged 4 defects and calculated Defect Density and DRE in `docs/defect_log_and_metrics.md`. |
| **Quality and the stopping decision** | Summarized and provided a "ready to release" recommendation in `docs/test_summary_report.md`. |

---

## 4. Start-to-Finish Guide (How to run everything)

If you need to demonstrate the project working on your local machine, follow these steps in your terminal:

### Step 1: Set up the environment
```bash
# Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate  # (On Windows use: venv\Scripts\activate)

# Install all project dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
```

### Step 2: Set up the Database
```bash
# Apply Django migrations to create the SQLite database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Run the Test Suite (and view Coverage)
```bash
# Run pytest with branch coverage enabled
pytest --cov=rental --cov-branch --cov-report=term-missing
```
*(The baseline run currently reports 27 passing tests, 94% total coverage, and 100% branch coverage for the core business logic.)*

### Step 4: Run the Application
```bash
# Start the local development server
python manage.py runserver
```
*Open your browser and navigate to `http://127.0.0.1:8000` to see the Vehicle Rental System.*

### Step 5: (Optional) Run via Docker / Jenkins
```bash
# Spin up the containerized Django app and the Jenkins CI server
docker-compose up --build
```
*(Django will run on port 8000, and Jenkins will be accessible on port 8080).*
