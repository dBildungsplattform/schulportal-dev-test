---
name: generate-test-cases
description: 'Derives manual test cases from a requirement and saves them directly as a CSV file optimized for Xray import. Use when asked to create, derive, or write manual test cases from a requirement, user story, or ticket.'
---

# Generate Manual Test Cases

This skill derives manual test cases from a requirement and saves them directly as a **CSV file for Xray import**. No Markdown and no table are displayed in the chat — the only result is the saved CSV file.

All generated test case content (e.g., Summary, Action, Data, Expected Result) must be written in **German**.

## Use When
- You are asked to create manual test cases from a requirement, user story, or ticket
- You are asked to derive test cases for a specific functional area

## Do Not Use When
- Playwright/automated tests in TypeScript should be written (normal coding workflow)
- Only an explanation or analysis of a requirement is desired, no test cases
- Gherkin tests should be written

---

## Step 0 — Gather Context (once per task)

**Step 1 — Ask for format via tool**

Use the `vscode_askQuestions` tool and ask exactly this **one** question:

- **Question**: "How should the test cases be structured?"
- **Options** (single choice, no free text):
  - **Multi-Test** — Each scenario gets its own TCID
  - **Single-Test** — All checks in a single test case; each check is its own test step

Wait for the answer before proceeding.

**Step 2 — Ask for the remaining information in the chat**

Ask the user the following questions in the chat as a formatted list. Wait for the answer before proceeding:

1. **Requirement**: What should be tested? (User story, free text, ticket content)
2. **Test depth**: Which types of tests should be covered? (Multiple choice possible)
   - Positive tests (Happy Path)
   - Negative tests (error cases, invalid inputs)
   - Boundary tests
   - Combinations of the above
3. **Metadata** for all test cases of this task:
   - **Tests** (ticket ID, e.g., `"SPSH-234"`)
   - **Description** (e.g., `"Test imported from Playwright."`)
   - **Test plan** (ticket ID of the associated test plan, e.g., `"SPSH-3163"`)
   - **Keywords** (one or more, e.g., `"Automated"`, `"Described"` — each keyword gets its own column in the table)
   - **Author** (e.g., `"silvia.grosche"`)
   - **Repository** (e.g., `"Automation/Navigation"`)
   - **Priority** (`"low"`, `"medium"` or `"high"`)

> **Do not continue until all information is available.**

---

## Step 0b — Preprocess requirement text (internal — no output)

Replace the following characters in the given requirement before deriving test cases. This step applies to the entire requirement text including acceptance criteria and scope. Do **not** output the result.

| Character | Replacement |
|-----------|-------------|
| `"`       | `'`         |
| `ä`       | `ae`        |
| `ö`       | `oe`        |
| `ü`       | `ue`        |
| `ß`       | `ss`        |

---

## Step 1 — Derive Test Cases

Derive test cases from the requirement. Depending on the chosen **format**, apply one of the following strategies:

### Format: Multi-Test (Standard)

- Cover all test types chosen by the user (positive, negative, boundary, combinations)
- **All steps of a test scenario (preconditions + business action) go in the first table row.** Subsequent rows with the same TCID describe **sequential, building steps** — they contain only the **delta action** (what changes compared to the previous step), no repeated setup.
- A **new TCID** is created only when the test **starts from scratch** (new context, completely new setup). Sequentially building variants (e.g., gradually changed test data in the same flow) remain in one TCID.
- **Only what is relevant to the requirement is tested.** Preparatory steps (login, navigation) are not considered test steps and do not generate their own expected result.

### Format: Single-Test

- There is exactly **one TCID** for the entire requirement.
- The first table row contains preconditions and the first verification step.
- **Each additional condition to be verified from the requirement** gets its own subsequent row with the same TCID — the action describes the delta action or the next verification step, the expected result the corresponding verification result.
- Preparatory steps (login, navigation) appear only in the first row and do not generate their own expected result.
- **Only what is relevant to the requirement is tested.**

---

## Step 2 — Build Markdown Table (no chat output)

> **This step is executed internally — no output appears in the chat.**

**2a — Build Internal Markdown Table**

Build the test cases as an internal Markdown table with exactly these columns in this order:

```
TCID | Tests | Summary | Description | Action | Data | Expected Result | Test Plan | Author | Keyword | [Keyword | ...] | Priority | Repository
```

> Each keyword specified by the user gets its own column, all using the header **Keyword**.

Table Rules:

- **TCID**: Sequential number, starting at `1`. A test case can have multiple rows — all rows of the same test get the same TCID.
- **Metadata Rule**: The fields Tests, Summary, Description, Test Plan, Author, Keyword, Priority and Repository appear **only in the first row** of a test — subsequent rows of these columns remain empty. The **Data** field is filled in every row (at least `-`).
- **Summary**: Format `<Tests>: <short test description>` (e.g., `SPSH-234: Login mit gueltigen Daten`).
- **Action**: All steps of the test scenario, each prefixed with `# `. Starts with preparatory steps (login, navigation) and ends with the business-relevant action. In the login step, **only the role** is specified (e.g., `# Als Schuladmin anmelden`). **Never** include system rights or account details in the action — these belong in **Data**. Sub-steps are prefixed with `## `.
  Formatting conventions (within the Action cell, steps separated by `<br>`):
  - **Buttons** → `*...*`: e.g., `*Close*` click
  - **UI elements, proper names, page titles** → `_..._`: e.g., `_Class Management_` open
  - **Searched texts, messages** → `_..._`: e.g., `_Success message: The operation was executed._`
 **Data**: Test data relevant to the action step of the row. If no data is relevant: `-`.
 **Expected Result**: The business-relevant verification result of the row, **without** `# ` prefix. Exactly one Expected Result per table row — that of the last business-relevant step.

---

## Step 3 — Self-Check of Markdown Table (internal — no output)

Check the Markdown table from Step 2a internally and correct errors before proceeding to Step 4. Do **not** output this check:

- The number of columns is consistent in each table row
- Metadata (Tests, Summary, Description, Test Plan, Author, Keyword, Priority and Repository) appear only in the first row of each TCID — subsequent rows of these columns remain empty
- The **Data** field is filled in every row (at least `-`)
- The summary follows the format `<Tests>: <short test description>`
- TCIDs are sequentially consistent (1, 2, 3, …)
- Natural-language content in Summary, Action text, Data descriptions, and Expected Result is German (Deutsch); if not, rewrite before proceeding (technical strings remain unchanged)

---

## Step 4 — Save Markdown File and Execute Script (No Chat Output)

> **This step is executed internally — no output appears in the chat.**

**4a — Save Markdown File**

Save the Markdown table from Step 2a with `create_file` as:

-- **Path**: `.github/manual_tests/<TICKET-ID>-testcases.md`
  - `<TICKET-ID>`: Ticket ID in original format, e.g., `SPSH-3353`

**4b — Run Script**

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
- The requirement is too vague to derive concrete test steps — ask for clarification
- No expected behavior can be inferred from the requirement — ask for the acceptance criteria