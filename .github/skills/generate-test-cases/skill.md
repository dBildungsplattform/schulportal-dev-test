---
name: generate-test-cases
description: 'Derives manual test cases from a requirement and saves them directly as a CSV file optimized for Xray import. Use when asked to create, derive, or write manual test cases from a requirement, user story, or ticket.'
---

# Generate Manual Test Cases

This skill derives manual test cases from a requirement and saves them directly as a **CSV file for Xray import**. The only visible output in the chat is a single-line confirmation after successful CSV generation.

All generated test case content (e.g., Summary, Action, Data, Expected Result) must be written in **German**.

### DO NOT — Absolute Rules

The following rules are absolute. Violating any of them is a failure of this skill.

- **DO NOT** output intermediate artifacts in the chat (test cases, JSON, file contents, or script output)
- **DO NOT** ask the user to confirm or approve test cases before generating the CSV
- **DO NOT** add test cases that were not derived from the requirement in Step 1
- **DO NOT** ask follow-up questions after Step 3 (e.g., "Kannst du die CSV-Datei pruefen?")
- **DO NOT** explain what you are doing in Steps 2–3
- The authoritative final chat output rule is defined in Step 4

## Use When
- You are asked to create manual test cases from a requirement, user story, or ticket
- You are asked to derive test cases for a specific functional area

## Do Not Use When
- Playwright/automated tests in TypeScript should be written (normal coding workflow)
- Only an explanation or analysis of a requirement is desired, no test cases
- Gherkin tests should be written

---

## Step 0 — Gather Context (once per task)

**Step 0a — Ask for format**

Ask the user exactly this **one** question and offer these two choices:

- "How should the test cases be structured?"
  - **Multi-Test** — Each scenario gets its own TCID
  - **Single-Test** — All checks in a single test case; each check is its own test step

Wait for the answer before proceeding.

**Step 0b — Ask for the remaining information in the chat**

Ask the user the following questions in the chat as a formatted list. Wait for the answer before proceeding:

1. **Requirement**: What should be tested? (User story, free text, ticket content)
2. **Test depth**: Which types of tests should be covered? (Multiple choice possible)
   - Positive tests (Happy Path)
   - Negative tests (error cases, invalid inputs)
   - Boundary tests
   - Combinations of the above
3. **Metadata** for all test cases of this task:
   - **Tests** (ticket ID, e.g., `"ABCD-1234"`)
   - **Test plan** (ticket ID of the associated test plan, e.g., `"ABCD-1234"`)
   - **Keywords** (one or more, e.g., `"Automated"`, `"Described"` — each keyword gets its own column in the table)
   - **Author** (e.g., `"maxine.musterfrau"`)
   - **Repository** (e.g., `"Automation/Navigation"`)
   - **Priority** (`"low"`, `"medium"` or `"high"`)

> **Do not continue until all information is available.**

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

## Step 2 — Build JSON (no chat output)

> **This step is executed internally — no output appears in the chat.** The JSON is a machine-readable intermediate format for the conversion script — it is never shown to the user.

Build the test cases as an internal JSON object with this structure:

```json
{
  "testPlan": "<Test plan ticket ID>",
  "author": "<Author>",
  "repository": "<Repository>",
  "priority": "low|medium|high",
  "keywords": ["<Keyword>", "..."],
  "cases": [
    {
      "ticketId": "<Tests ticket ID>",
      "summary": "<short test description>",
      "checks": ["<verification 1>", "<verification 2>", "..."],
      "rows": [
        {
          "actionSteps": ["<step>", ["<sub-step>", "..."], "..."],
          "data": "<test data or '-'>",
          "expectedResult": "<verification result of this row>"
        }
      ]
    }
  ]
}
```

Content Rules:

- **cases**: One entry per test scenario. Each case becomes one TCID (the script assigns TCIDs sequentially — do not include a TCID field).
- **summary**: Short test description without the ticket-ID prefix (the script builds `<ticketId>: <summary>`).
- **checks**: One entry per core verification of the case, concise and verb-led (the script builds the Description field from this).
- **rows**: All steps of the test scenario (preconditions + business action) go in the first row. Subsequent rows describe **sequential, building steps** — only the **delta action** (what changes compared to the previous row), no repeated setup.
- **actionSteps**: Ordered list of steps for this row. A plain string is a main step; a nested array of strings is a group of sub-steps under it. Starts with preparatory steps (login, navigation) and ends with the business-relevant action. In the login step, **only the role** is specified (e.g., `"Als Schuladmin anmelden"`). **Never** include system rights or account details here — these belong in **data**.
  Formatting conventions (within each step string):
  - **Buttons** → `*...*`: e.g., `*Schliessen* klicken`
  - **UI elements, proper names, page titles** → `_..._`: e.g., `_Klassenverwaltung_ oeffnen`
  - **Searched texts, messages** → `_..._`: e.g., `_Erfolgsmeldung: Der Vorgang wurde ausgefuehrt._`
- **data**: Test data relevant to the action step of the row. If no data is relevant: `"-"`.
- **expectedResult**: The business-relevant verification result of the row, plain text (no `#` prefix needed). Exactly one per row — that of the last business-relevant step.
- All natural-language content (summary, checks, actionSteps, data, expectedResult) must be German (Deutsch). Umlauts and `ß` may be written normally — the script normalizes them for the CSV.

---

## Step 3 — Save JSON File and Execute Script (No Chat Output)

> **This step is executed internally — no output appears in the chat.**

**3a — Save JSON File**

Save the JSON object from Step 2 with the `Write` tool as:

- **Path**: `.github/manual_tests/<TICKET-ID>-testcases.json`
  - `<TICKET-ID>`: Ticket ID in original format, e.g., `ABCD-1234`

**3b — Run Script**

Run the conversion script with the `Bash` tool:

```
python .github/scripts/json_to_csv.py .github/manual_tests/<TICKET-ID>-testcases.json --delete-input
```

- `--delete-input` automatically deletes the intermediate JSON file after successful conversion.
- The script validates the JSON structure (required fields, non-empty arrays, valid priority value) — there is no separate self-check step.
- Check the exit code: In case of an error (exit code ≠ 0), output the error message from stderr in the chat and abort.

---

## Step 4 — Completion (Final Output, Authoritative Rule)

**Step 4 is the authoritative output rule and the ONLY message the user should see.** Not before, not after. After successful script execution, output exactly this one line in the chat:

> CSV saved: `.github/manual_tests/<TICKET-ID>-testcases.csv`

**Nothing else.** No questions, no explanations, no follow-up.

---

## When the Skill Cannot Proceed

Stop and inform the user if:
- The requirement is too vague to derive concrete test steps — ask for clarification
- No expected behavior can be inferred from the requirement — ask for the acceptance criteria

---

## Self-Reminder — Read This Last

Before you execute this skill, remember:

- Steps 2 through 3 are **completely internal** — the user sees nothing
- You do **not** show the test cases to the user for approval
- You do **not** ask if the user wants to verify the CSV
- You do **not** add test cases beyond what Step 1 derived
- Follow the authoritative output rule from Step 4
- If the script fails, output the error and stop — do not continue with follow-up questions