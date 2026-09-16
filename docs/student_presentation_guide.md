# Vehicle Rental System
## Beginner Study and Presentation Guide

**Course:** Software Testing and Validation  
**Instructor:** Abel Tadesse  
**Group members:** Eyob Mulugeta (ATE/4778/14); Afomia Birhanu (ATE/2368/14)

---

## 1. The One-Minute Explanation

This project is a small vehicle-rental web application. A customer chooses a vehicle, enters their name, age, premium-member status, and rental dates, and submits a booking.

The important part is not only the web page. The important part is that we tested the application professionally at several levels:

1. **Unit testing:** We test the pricing and booking-state rules by themselves.
2. **Integration testing:** We test Django views, database models, and business logic working together.
3. **System testing:** We use Playwright to operate the real web interface in a browser.
4. **Acceptance testing:** We check whether the application supports the customer journeys promised by the requirements.
5. **Continuous integration:** GitHub Actions and Jenkins run the tests automatically.
6. **Coverage and defect management:** We measure what the tests cover, record defects, and report the release decision.

The latest local run executed **27 tests successfully**, with **94% total coverage** and **100% branch coverage in the core business logic**.

---

## 2. What Problem Does the Application Solve?

Imagine a small rental company. It needs to answer these questions:

- Which vehicles can customers see?
- Is the customer old enough to rent?
- Is the rental period allowed?
- How much does the rental cost?
- Does a premium customer receive the correct discount?
- What happens to a booking after it is requested or confirmed?

Our application is deliberately small, but it has enough real rules to demonstrate formal software-testing techniques.

### Main user journey

```text
Open vehicle list
       |
Choose a vehicle
       |
Enter customer and rental information
       |
Validate age and rental duration
       |
Calculate price
       |
Create customer and booking records
       |
Confirm booking and show success message
```

For invalid input, the application stays on the booking page and shows an error instead of creating a booking.

---

## 3. Technology: What We Wrote the Project With

### Python

Python is the programming language. It is readable and has strong support for testing.

### Django

Django is the web framework. It gives us:

- URL routing: deciding which Python function handles a URL.
- Views: Python functions that process browser requests.
- Templates: HTML pages shown to users.
- Models: Python classes representing database tables.
- Test client and database test support.

### SQLite

SQLite is the database used locally. It stores vehicles, customers, and bookings in `db.sqlite3`.

### pytest

pytest is the test runner. It finds functions whose names begin with `test_`, executes them, and reports pass or fail.

### pytest-django

pytest-django connects pytest to Django. It loads Django settings and gives tests controlled database access.

### Playwright

Playwright controls a real browser. It can open pages, click buttons, fill forms, and inspect visible results. The project brief allows a suitable browser automation tool, so we use Playwright rather than Selenium.

### pytest-cov

pytest-cov measures code coverage while tests run. We use branch coverage because merely executing a line is not enough: each important true/false decision should be exercised.

### GitHub Actions and Jenkins

These are continuous-integration tools. They automatically install dependencies and run the tests whenever code is pushed or submitted in a pull request.

---

## 4. Project Structure: What Each Important File Does

```text
manage.py                         Django command-line entry point
config/settings.py                Django configuration
config/urls.py                    Project URL configuration
rental/models.py                  Database models
rental/views.py                   Request handling and booking workflow
rental/business_logic.py          Pricing and state-transition rules
rental/templates/                 HTML pages
rental/tests/test_business_logic.py  Unit tests
rental/tests/test_models.py       Database/model integration tests
rental/tests/test_views.py        View integration tests
rental/tests/pages.py             Playwright Page Objects
rental/tests/test_system.py       Browser system tests
.github/workflows/ci.yml          GitHub Actions pipeline
Jenkinsfile                       Jenkins pipeline
Dockerfile                        Application container definition
docker-compose.yml                Local application and Jenkins services
docs/                             Plans, designs, metrics, reports, PDFs
```

### The most important separation

We separate **business logic** from the web interface.

Business logic answers: "What is the correct price?"  
The view answers: "How do I receive the browser request and save the result?"

This separation makes the pricing rules easy to test without opening a browser or using a database.

---

## 5. Business Logic Explained Slowly

The main business logic is in `rental/business_logic.py`.

### 5.1 Pricing inputs

The method is:

```python
calculate_price(age, duration_days, is_premium=False)
```

It receives:

- `age`: customer's age.
- `duration_days`: number of rental days.
- `is_premium`: whether the customer is a premium member.

The normal base rate is `$50` per day. A driver aged 21 through 24 pays a `$20` per-day surcharge.

### 5.2 Age rule

```python
if age < 21:
    raise AgeRestrictionError(...)
```

This means:

- Age 20: invalid.
- Age 21: valid and surcharge applies.
- Age 24: valid and surcharge applies.
- Age 25: valid and normal price applies.

For age 21 and five days:

```text
Daily rate = 50 + 20 = 70
Subtotal = 70 * 5 = 350
```

### 5.3 Duration rule

```python
if duration_days <= 0:
    raise DurationRestrictionError(...)
if duration_days > 30:
    raise DurationRestrictionError(...)
```

Allowed duration is from 1 through 30 days, inclusive.

- 0 days: invalid.
- 1 day: valid lower boundary.
- 30 days: valid upper boundary.
- 31 days: invalid.

The word **inclusive** matters. `30` is accepted because the code rejects only values greater than 30.

### 5.4 Young-driver surcharge

```python
if 21 <= age < 25:
    daily_rate += 20
```

The two comparisons mean age must be at least 21 and less than 25. Therefore, ages 21, 22, 23, and 24 receive the surcharge. Age 25 does not.

### 5.5 Decision-table discount rule

There are two conditions:

- C1: Is the customer premium?
- C2: Is the rental longer than 7 days?

There are four possible combinations:

| Premium? | More than 7 days? | Discount |
|---|---|---:|
| Yes | Yes | 20% |
| Yes | No | 5% |
| No | Yes | 10% |
| No | No | 0% |

Example: non-premium customer, 10 days:

```text
Subtotal = 50 * 10 = 500
Discount = 10% of 500 = 50
Final price = 500 - 50 = 450
```

Example: premium customer, 10 days:

```text
Subtotal = 50 * 10 = 500
Discount = 20% of 500 = 100
Final price = 500 - 100 = 400
```

### 5.6 State-transition logic

A booking has a state. The allowed workflow is:

```text
REQUESTED -> CONFIRMED -> ACTIVE -> RETURNED
      |             |
      v             v
  CANCELLED     CANCELLED
```

The application must reject impossible transitions. For example:

- `REQUESTED -> ACTIVE`: invalid because the booking was not confirmed.
- `CANCELLED -> REQUESTED`: invalid because a cancelled booking is finished.
- `ACTIVE -> RETURNED`: valid.

This is called **state transition testing** because the test checks the current state, the event/action, and the next state.

### 5.7 Email service and dependency injection

When a booking becomes confirmed, `BookingManager` calls `EmailService.send_confirmation`.

In the unit test, we do not want to send a real email. We inject a `MagicMock` instead. The test verifies that the collaborator was called with the correct message.

This is a **test double**, specifically a mock/spy-style double. It replaces a real dependency and lets us verify the interaction.

---

## 6. How the Web Request Works

The main web workflow is in `rental/views.py`.

### Step 1: GET request

When the user opens the vehicle list, `vehicle_list` loads all `Vehicle` records and renders `vehicle_list.html`.

When the user clicks Book Now, the browser opens `/book/<vehicle_id>/`. A GET request renders the booking form.

### Step 2: POST request

When the user submits the form, `book_vehicle` reads:

- Customer name.
- Customer age.
- Premium checkbox.
- Start date.
- End date.

### Step 3: Convert input values

Form values arrive as text. The view converts age to an integer and dates to Python date objects.

```python
age = int(age_str)
start_date = datetime.strptime(...).date()
end_date = datetime.strptime(...).date()
```

If conversion fails, the view catches `ValueError` and shows an invalid-format message.

### Step 4: Calculate duration

```python
duration_days = (end_date - start_date).days
```

The view passes this duration to the business logic.

### Step 5: Reuse business logic

The view creates `RentalCalculator`, changes its base rate to the selected vehicle's rate, and calls `calculate_price`.

If age or duration is invalid, the calculator raises a custom exception. The view catches it and renders the form with the error. No customer or booking record is created.

### Step 6: Save successful data

If validation succeeds:

1. Create a `Customer` database row.
2. Create a `Booking` database row.
3. Move the booking from `REQUESTED` to `CONFIRMED`.
4. Save the new state.
5. Show a success message.
6. Redirect back to the vehicle list.

This is why the successful integration test checks both the HTTP redirect and database records.

---

## 7. Testing Theory You Must Know

### 7.1 Error, fault, and failure

These three words are related but different:

- **Error:** A human makes a mistake in understanding or writing a requirement or code.
- **Fault:** The mistake becomes something wrong inside the software.
- **Failure:** The software behaves incorrectly when executed.

Example from this project:

- Error: A developer misunderstands whether 30 days is allowed.
- Fault: The code uses `duration_days >= 30` instead of `duration_days > 30`.
- Failure: A customer entering exactly 30 days receives an error even though 30 days should be valid.

### 7.2 Verification versus validation

- **Verification:** "Did we build the product according to the specification?"
- **Validation:** "Did we build the right product for the user?"

Unit tests verifying the 30-day rule are verification because they compare code behavior with the defined rule.

A Playwright acceptance test booking a vehicle through the browser is validation because it checks a realistic user goal.

### 7.3 Equivalence partitioning

Equivalence partitioning divides possible input values into groups where values should behave similarly.

For age:

- Invalid partition: less than 21.
- Valid surcharge partition: 21 through 24.
- Valid standard-rate partition: 25 and above.

We do not need to test every possible age. We choose representatives from each partition, then add boundary values.

### 7.4 Boundary value analysis

Defects often happen at edges. Therefore, test values just below, exactly at, and just above a limit.

For minimum age 21:

```text
20 = just below, invalid
21 = exact boundary, valid
22 = just above, valid
```

For the surcharge boundary at 25:

```text
24 = surcharge
25 = standard rate
```

For duration 1 to 30:

```text
0 = invalid below minimum
1 = valid minimum
30 = valid maximum
31 = invalid above maximum
```

### 7.5 Decision-table testing

A decision table is useful when several conditions combine to determine an action. It prevents us from testing only one condition and forgetting combinations.

Here the conditions are premium membership and rental length. Two Boolean conditions produce $2^2 = 4$ combinations, so our four unit tests cover all rules.

### 7.6 State-transition testing

State testing checks legal and illegal movement through a workflow. It is useful when the same action has a different meaning depending on the current state.

For example, confirming a requested booking is valid, but confirming a cancelled booking is invalid.

### 7.7 Test pyramid

The test pyramid means:

```text
          Few system tests
       More integration tests
     Many fast unit tests
```

Unit tests are fast and precise. Integration tests are slower but check connections. System tests are slowest and most expensive because they use a browser and the full application.

Our project follows this idea:

- Many business-logic unit tests.
- Database and view integration tests.
- Two Playwright browser tests.

### 7.8 Coverage

Statement coverage asks: "Was this line executed?"

Branch coverage asks: "Were both outcomes of this decision executed?"

For example:

```python
if age < 21:
    reject()
else:
    continue()
```

A test with age 20 covers the true branch. A test with age 21 covers the false branch. Both are needed for branch coverage.

Coverage is evidence, not proof that the software is perfect. A test can execute a line without checking the correct result. That is why coverage must be combined with good assertions and formal test design.

---

## 8. Test Levels in This Project

### Unit tests

File: `rental/tests/test_business_logic.py`

A unit test isolates one small part of the system. Examples:

- Underage customers raise `AgeRestrictionError`.
- Age 21 receives the surcharge.
- Age 25 receives the normal rate.
- Each decision-table discount is correct.
- Valid booking transitions work.
- Invalid transitions raise `InvalidStateTransitionError`.
- The email collaborator receives the expected message.

### Integration tests

Files: `rental/tests/test_models.py` and `rental/tests/test_views.py`

These tests use more than one component:

- Django models with the test database.
- Views with URL routing and templates.
- Form input with business logic.
- Booking creation with saved database state.

An example checks that a valid POST request redirects and creates exactly one customer and one booking.

### System tests

Files: `rental/tests/pages.py` and `rental/tests/test_system.py`

The browser test starts a live Django test server. Playwright then:

1. Opens the vehicle list.
2. Clicks Book Now.
3. Fills the form.
4. Submits it.
5. Checks the success message.

The underage test performs the same kind of journey but expects a visible error.

### Page Object Model

`pages.py` contains `VehicleListPage` and `BookingPage`.

A Page Object hides selectors and browser actions behind readable methods such as:

```python
booking_page.fill_form(...)
booking_page.submit()
```

If an HTML selector changes, we update the Page Object instead of changing every test. This reduces duplication and makes system tests easier to read.

### Acceptance/UAT

Acceptance testing asks whether the finished application supports user goals. Our UAT scenarios include:

- A normal customer successfully books a vehicle.
- An underage customer is rejected.
- An invalid rental duration is rejected.

The Playwright tests provide automated evidence for the first two. Unit and integration tests provide evidence for duration validation.

---

## 9. How to Run the Project from the Beginning

Open Terminal in the project folder:

```bash
cd /Users/eyob/ScriptFlick/Temp/Abel
```

### Step 1: Create a virtual environment

A virtual environment keeps this project's packages separate from other Python projects.

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, the command prompt normally shows `(venv)`.

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

This installs Django, pytest, pytest-django, Playwright, pytest-playwright, pytest-cov, and Markdown support.

### Step 3: Install the browser

```bash
playwright install chromium
```

Playwright needs browser binaries. Installing the Python package alone is not enough.

### Step 4: Prepare the database

```bash
python manage.py migrate
```

Migrations create the database tables for customers, vehicles, and bookings.

The project also has a seed command:

```bash
python manage.py seed_vehicles
```

Use it if you want sample vehicles in the database.

### Step 5: Start the application

```bash
python manage.py runserver
```

Open this address in a browser:

```text
http://127.0.0.1:8000/
```

Stop the server with `Ctrl+C`.

### Step 6: Run all tests

Open another terminal, activate the same environment, and run:

```bash
source venv/bin/activate
pytest
```

### Step 7: Run tests with coverage

```bash
pytest --cov=rental --cov-branch --cov-report=term-missing
```

### Step 8: Generate CI-style reports locally

This is the exact command used by the pipelines:

```bash
pytest --junitxml=junit.xml \
  --cov=rental \
  --cov-branch \
  --cov-report=xml \
  --cov-report=html:htmlcov \
  --cov-report=term
```

The outputs are:

- `junit.xml`: test results for Jenkins.
- `coverage.xml`: machine-readable coverage.
- `htmlcov/index.html`: browser-readable coverage report.

### Step 9: Run with Docker

Docker must be installed and running.

```bash
docker compose up --build
```

The Django application is available on port 8000. Jenkins is configured on port 8080 by the compose file.

---

## 10. How to Explain the CI Pipelines

### GitHub Actions

The workflow in `.github/workflows/ci.yml` runs when code is pushed or when a pull request is opened.

Its stages are:

1. Check out the code.
2. Install Python.
3. Install Python dependencies.
4. Install Chromium for Playwright.
5. Run tests and coverage.
6. Upload JUnit and coverage artifacts.

This is continuous integration because every code change receives an automated check.

### Jenkins

The `Jenkinsfile` describes the Jenkins pipeline as code.

Its stages are:

1. Checkout.
2. Create a virtual environment and install dependencies.
3. Install Playwright Chromium.
4. Run tests and coverage.
5. Publish JUnit and HTML coverage reports.

Jenkins can run the same project independently of GitHub Actions. Having both demonstrates the course requirement and gives the team two CI environments.

### Regression demonstration

A regression is when a new change breaks behavior that previously worked.

Our planned demonstration is:

1. Change `YOUNG_DRIVER_SURCHARGE` from `20.0` to `15.0`.
2. Push the change.
3. The age-21 unit test should fail because it expects `$350` but receives `$325`.
4. Record the failing build URL or screenshot.
5. Restore the value to `20.0`.
6. Push again.
7. Record the passing build URL or screenshot.

Do not pretend a pipeline ran if you do not have the actual build evidence. Add the real links or screenshots to the report.

---

## 11. Defects and Metrics

### Defect record fields

Each defect should include:

- Identifier, such as `DEF-001`.
- Steps to reproduce.
- Expected result.
- Actual result.
- Severity: how damaging the defect is.
- Priority: how urgently it should be fixed.
- Status: New, Assigned, In Progress, Retest, or Closed.

### Severity versus priority

Severity describes impact. A wrong total price may be high severity because it affects money.

Priority describes urgency. A low-severity spelling error may still be high priority before a public demo if it is visible on the main page.

### Defect density

Defect density is commonly calculated as:

```text
Defect density = number of defects / size of software
```

If the application is estimated at 0.5 KLOC and four defects were found:

```text
4 / 0.5 = 8 defects per KLOC
```

Because this application is very small, the result can look large. Interpret it carefully instead of treating the number alone as quality.

### Defect removal efficiency

```text
DRE = defects found before release /
      (defects found before release + escaped defects) * 100
```

If four defects were found before release and none escaped:

```text
DRE = 4 / (4 + 0) * 100 = 100%
```

This result depends on honest defect reporting. It does not prove that no unknown defects exist.

---

## 12. What We Can Claim Honestly

Based on the local run:

- 27 tests passed.
- Core business logic reached 100% branch coverage.
- Total project coverage reached 94%.
- Unit, integration, and Playwright system tests exist.
- A MagicMock test double is used.
- Formal design techniques are documented.
- CI configuration exists for GitHub Actions and Jenkins.
- PDF reports exist.

Before submitting, the group must still add:

- The actual shared repository link.
- Actual GitHub Actions and Jenkins build evidence.
- Screenshots or URLs for the failing and passing regression builds.
- Any signatures or approval details required by the instructor.

Do not say that CI passed unless you have run it in the hosted environment. Local success and hosted CI success are different pieces of evidence.

---

## 13. A Presentation Script

You can say this in your presentation:

> Our project is a Django vehicle-rental system. The customer selects a vehicle, enters personal and rental information, and submits a booking. We separated the business rules from the web layer so that the important rules could be unit tested independently.
>
> The main business rules are an age restriction of at least 21, a rental duration between 1 and 30 days, a young-driver surcharge for ages 21 through 24, and discounts based on premium membership and rental length. We used equivalence partitioning and boundary value analysis for age and duration. We used a decision table for the two discount conditions and state-transition testing for the booking lifecycle.
>
> Our test pyramid has many fast unit tests, fewer database and view integration tests, and two Playwright system tests. The Playwright tests use the Page Object pattern. We also use a MagicMock for the email collaborator, so the unit test does not send a real email.
>
> The latest local run executed 27 tests and all passed. Total coverage was 94%, and the core business-logic module had 100% branch coverage. GitHub Actions and Jenkins are configured to run the same tests, publish JUnit results, and produce coverage reports.
>
> We manage defects with identifiers, reproduction steps, expected and actual results, severity, priority, and lifecycle status. Our release recommendation is based on the exit criteria in the test plan, while residual risks include untested production infrastructure and the limits of a small prototype.

---

## 14. Likely Teacher Questions and Strong Answers

### Q1. Why did you choose a vehicle rental system?

**Answer:** It is small enough to finish but contains all required testing shapes: ranges for age and duration, combined discount conditions, a booking state workflow, and a multi-step browser journey.

### Q2. Why is business logic separate from the view?

**Answer:** Separation improves maintainability and testability. The calculator can be tested without HTTP, templates, a database, or a browser. The view only coordinates input, persistence, and responses.

### Q3. Why do you need both unit and system tests?

**Answer:** They find different kinds of problems. Unit tests quickly find incorrect formulas and transitions. System tests find problems in routing, templates, selectors, form submission, and the complete user journey.

### Q4. Why not test only the happy path?

**Answer:** Real users provide invalid and boundary inputs. We need to test underage customers, zero days, 31 days, invalid transitions, and all combinations in the decision table.

### Q5. Why test age 21, 24, and 25?

**Answer:** 21 is the minimum valid age, 24 is the last age receiving the surcharge, and 25 is the first age receiving the standard rate. These are business-rule boundaries.

### Q6. What does a test double do?

**Answer:** It replaces a real collaborator. Our `MagicMock` replaces `EmailService`, allowing us to check that confirmation would be sent without sending an actual email.

### Q7. Does 94% coverage mean the system is perfect?

**Answer:** No. Coverage measures executed code and branches, not the quality of every assertion or every possible environment. It is one quality indicator combined with formal test design, defect results, and system testing.

### Q8. What is the difference between verification and validation?

**Answer:** Verification checks whether implementation follows the specification. Validation checks whether the product supports the user's real goal. Unit tests mainly support verification; browser acceptance tests support validation.

### Q9. What is a regression?

**Answer:** It is a previously working behavior that breaks after a change. We demonstrate it by changing the surcharge from 20 to 15, observing a failed test in CI, then restoring the correct value and getting a passing build.

### Q10. What does the view do when the input is invalid?

**Answer:** The calculator raises a custom exception. The view catches it, renders the booking form again with the error message, and does not create customer or booking records.

### Q11. What is the current state of a new booking?

**Answer:** The database default is `REQUESTED`. After successful validation, the view uses `BookingManager` to transition it to `CONFIRMED` and saves it.

### Q12. What are the limitations of the application?

**Answer:** It is a small prototype. It does not cover load testing, penetration testing, real payment processing, production database deployment, or a complete administrative workflow. These are residual risks and are identified in the test plan or summary report.

### Q13. Why does the test use `live_server`?

**Answer:** `live_server` starts a temporary Django server for the test. Playwright can then interact with the application through a real browser and real HTTP requests instead of only calling Python functions.

### Q14. Why use a Page Object?

**Answer:** It keeps browser selectors and actions in one place. Tests describe user behavior, while Page Objects contain the technical details of locating and filling page elements.

### Q15. What evidence proves your project is complete?

**Answer:** The repository contains source code, tests at three levels, CI files, Docker setup, Markdown reports, PDF deliverables, coverage artifacts, and the group identity. Hosted regression and pipeline links must be attached as final execution evidence.

---

## 15. Practice Checklist Before Meeting the Teacher

- [ ] Explain the application in one minute without reading.
- [ ] Draw the price calculation on paper.
- [ ] Explain why age 20, 21, 24, and 25 are different.
- [ ] Explain all four decision-table rules.
- [ ] Draw the booking state diagram.
- [ ] Explain one unit test line by line.
- [ ] Explain why `MagicMock` is used.
- [ ] Explain the difference between unit, integration, system, and acceptance tests.
- [ ] Run `pytest` successfully.
- [ ] Open `htmlcov/index.html` and understand what the percentages mean.
- [ ] Run the application and complete a booking in the browser.
- [ ] Show the Page Object file.
- [ ] Explain the GitHub Actions stages.
- [ ] Explain how Jenkins publishes JUnit and HTML coverage.
- [ ] Prepare the real failed and passed regression build evidence.
- [ ] Know which parts are out of scope.

The goal is not to memorize every line. The goal is to understand the flow: **requirement -> business rule -> implementation -> test design -> automated test -> evidence -> release decision**.
