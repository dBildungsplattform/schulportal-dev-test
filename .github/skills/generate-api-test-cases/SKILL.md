---
name: generate-api-test-cases
description: 'Derives manual test cases for backend/API tickets and saves them as a CSV file optimized for Xray import. Tests are described at the HTTP level (endpoint, method, request body, status codes) — not via UI. Use when asked to create, derive, or write test cases for an API, endpoint, or backend ticket that is tested via Swagger or a REST client.'
---

# Generate API Test Cases

This skill generates manual API test cases based on a backend request and saves them directly as a **CSV file for Xray import**. The tests describe HTTP calls (method, endpoint, request body, status codes)—not UI interactions. No Markdown or table appears in the chat—the only result is the saved CSV file.

## Use When
- You should create test cases for a backend ticket, a REST endpoint, or an API requirement
- Testing is done via Swagger (`/docs`), a REST client (e.g., Postman, curl), or direct HTTP calls
- There is (still) no frontend for the functional area to be tested

## Do Not Use When
- UI tests need to be created → use `generate-test-cases`
- Playwright/automated tests need to be written in TypeScript (standard coding workflow)
- Only an explanation or analysis of a requirement is needed, not test cases
- Gherkin tests need to be written

---

## Step 0 — Gather Context (once per task)

**Step 1 — Ask for format via tool**

Use the `vscode_askQuestions` tool and ask exactly this **one** question:

- **Question**: "How should the test cases be structured?"
- **Options** (single choice, no free text):
  - **Multi-Test** — Each scenario gets its own TCID
  - **Single-Test** — All checks in a single test case; each check is its own test step

Wait for the response before proceeding.

**Step 2 — Ask for API details and metadata in the chat**

Ask the user the following questions as a formatted list in the chat. Wait for the response before proceeding:

1. Requirement: What should be tested? (User Story, free-text requirement, ticket content, OpenAPI excerpt)
2. **Endpoint(s)**: HTTP method and path, e.g., `POST /api/v1/users` — can be multiple
3. **Auth-Typ**: How is authentication handled?
   - Bearer Token (JWT)
   - Basic Auth
   - No Auth required
   - Other (please describe)
4. **Test Depth**: Which test types should be covered? (Multiple selections possible)
   - Positive tests (HTTP 2xx, happy path)
   - Negative tests (invalid inputs, missing mandatory fields, HTTP 4xx)
   - Authentication scenarios (no token, expired token, wrong role → HTTP 401/403)
   - Boundary value tests (empty strings, maximum values, special characters)
   - Any combination of the above
5. **Metadata** for all test cases in this task:
   - **Tests** (Ticket-ID, e.g., `"SPSH-234"`)
   - **Test Plan** (Ticket-ID of the associated test plan, e.g., `"SPSH-3163"`)
   - **Keyword** (one or more, e.g., `"DevTest21"`, `"Described"` — each tag gets its own column)
   - **Author** (e.g., `"silvia.grosche"`)
   - **Repository** (e.g., `"Devtest/Sprint 21"`)
   - **Priority** (one of `"low"`, `"medium"` or `"high"`)

> **Do not proceed until all information has been provided.**

---

## Step 0b — Preprocess Requirement Text (internal — no output)

Replace the following characters in the given requirement before deriving test cases. This step applies to the entire requirement text, including acceptance criteria and scope. Do not output the result.

| Character | Replacement |
|-----------|-------------|
| `"`       | `'`         |
| `ä`       | `ae`        |
| `ö`       | `oe`        |
| `ü`       | `ue`        |
| `ß`       | `ss`        |

---

## Step 1 — Derive Test Cases

Derive API test cases from the requirement. Depending on the selected Format, apply one of the following strategies:

### Language Rule

All generated test case content must be written in German (Deutsch), including:
- Summary
- Action
- Data (except technical values like JSON keys, endpoints, and HTTP methods)
- Expected Result

Keep technical terms such as HTTP methods, endpoint paths, status codes, JSON keys, and header names in their original technical form.

### Format: Multi-Test (Standard)

- Cover all test types selected by the user (positive, negative, auth, boundary)
- **All steps of a test scenario must be in the first table row.** Subsequent rows with the same TCID describe **sequential, building steps** within the same scenario — they contain only the delta action.
- A **new TCID** is created only when the test **starts from scratch** (different auth context, different request body type, completely different scenario).
- **Only what the requirement concerns is tested.** Setup steps (getting a token) are not separate test steps.
- **Auth negative scenarios** (no token, wrong role) are separate TCIDs.

### Format: Single-Test

- There is exactly **one TCID** for the entire requirement.
- The first row contains the setup step and the first verification step.
- Each additional condition to verify is represented by a follow-up row with the same TCID.
- Setup steps (e.g. obtaining a token) appear only in the first row and do not generate    their own expected result.

### API-Specific Derivation Rules

- **Happy Path first**: Start with the successful call (2xx).
- **Negative Tests**: Derive error cases directly from the requirement — missing mandatory fields, invalid types, incorrect values.
- **Auth Scenarios** (if selected): Create separate TCIDs for:
  - No token → HTTP 401
  - Expired/invalid token → HTTP 401
  - Token with wrong role / missing permission → HTTP 403
- **Boundary Tests**: Empty strings, `null`, maximum values, special characters as request body in Data.

---

## Step 2 — Build Markdown Table (No Chat Output)

> **This step is executed internally — no output appears in the chat.**

### Language Rule (Validation)

Ensure all natural-language content in table cells is German (Deutsch):
- Summary
- Action text
- Data descriptions
- Expected Result

Technical strings remain unchanged (e.g., `POST`, `/api/v1/users`, `_Authorization_`, `_id_`, `HTTP 400`).

**2a — Build Internal Markdown Table**

Build the test cases as an internal Markdown table with exactly these columns in this order:

```
TCID | Tests | Summary | Description | Action | Data | Expected Result | Test Plan | Author | Keyword | [Keyword | ...] | Priority | Repository
```

> Each keyword specified by the user gets its own column, all using the header **Keyword**.

Table Rules:

- **TCID**: Sequential number, starting at `1`. A test case can have multiple rows — all rows of the same test get the same TCID.
- **Metadata Rule**: The fields Tests, Summary, Description, Test Plan, Author, Keyword, Priority and Repository appear **only in the first row** of a test — subsequent rows of these columns remain empty. The **Data** field is filled in every row (at least `-`).
- **Summary**: Format `<Tests>: <short test description>` (e.g., `SPSH-234: POST /api/v1/users – gueltiger Request`).
- **Action**: All steps of the test scenario, each prefixed with # . Starts with the authentication setup step and ends with the HTTP request. Sub-steps are prefixed with ## .

  Formatting conventions for API actions (steps within a cell separated by `<br>`):
  - **HTTP methods** → `*GET*`, `*POST*`, `*PUT*`, `*PATCH*`, `*DELETE*`: e.g., `*POST* _/api/v1/users_`
  - **Endpoints / URL segments** → `_..._`: e.g., `_/api/v1/users/{id}_`
  - **Header names** → `_..._`: e.g., `_Authorization_` header
  - **Response fields / JSON keys** → `_..._`: e.g., response contains `_id_`
  - **Auth setup step**: `# Set bearer token (data)` — the actual token/account is in **Data**
  - **No-auth scenario**: `# Call without _Authorization_ header`

- **Data**: Test data relevant to the action step of the row. Contains:
  - Bearer token / role / account description for the auth setup step
  - Request body (JSON or field list) for the HTTP request step
  - Query parameters / path parameters when relevant
  - `-` if no data is relevant
- **Expected Result**: HTTP status code + business validation result, e.g.:
  - `HTTP 201 – Response contains _id_ of the created resource`
  - `HTTP 400 – Validation error: _name_ is required`
  - `HTTP 401 – Access denied (no token)`
  - `HTTP 403 – Access denied (missing permission)`

---

## Step 3 — Self-Check of Markdown Table (internal — no output)

Check the Markdown table from Step 2a internally and correct errors before proceeding to Step 4. Do **not** output this check:

- The number of columns is consistent in each table row
- Metadata (Tests, Summary, Description, Test Plan, Author, Keyword, Priority, Repository) appear only in the first row of each TCID — subsequent rows of these columns remain empty
- The **Data** field is filled in every row (at least `-`)
- The summary follows the format `<Tests>: <short test description>` (e.g., `SPSH-234: POST /api/v1/users – gueltiger Request`)
- TCIDs are sequentially consistent (1, 2, 3, …)
- Each expected result begins with an HTTP status code (except for pure setup rows without a validation step)
- Natural-language content in Summary, Action text, Data descriptions, and Expected Result is German (Deutsch); if not, rewrite before proceeding (technical strings like HTTP methods, endpoints, status codes, JSON keys, and header names remain unchanged)

---

## Step 4 — Save Markdown File and Execute Script (No Chat Output)

> **This step is executed internally — no output appears in the chat.**

**4a — Save Markdown File**

Save the Markdown table from Step 2a with `create_file` as:

- **Path**: `.github/manual_tests/<TICKET-ID>-testcases.md`
  - `<TICKET-ID>`: Ticket ID in original format, e.g., `SPSH-3353`

**4b — Execute Script**

Run the conversion script with `run_in_terminal`:

```
python .github/scripts/md_to_csv.py .github/manual_tests/<TICKET-ID>-testcases.md --delete-input
```

- `--delete-input` automatically deletes the intermediate Markdown file after successful conversion.
- Check the exit code: In case of an error (exit code ≠ 0), output the error message from stderr in the chat and abort.

---

## Step 5 — Completion

**Only output in the chat** after successful script execution:

> CSV saved: `.github/manual_tests/<TICKET-ID>-testcases.csv`

---

## When the Skill Cannot Proceed

Stop and inform the user if:
- The request is too vague to derive concrete HTTP calls — ask for the endpoint and expected behavior
- No expected behavior (status code / response body) can be inferred from the request — ask for the acceptance criteria
