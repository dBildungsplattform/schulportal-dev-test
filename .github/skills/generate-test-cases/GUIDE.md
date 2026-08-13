# Guide: Set Up `generate-test-cases` in Another Repository

Use this guide to set up and use the `generate-test-cases` Copilot skill.

## Contents

- [Set Up the Skill](#set-up-the-skill)
  - [Files to Copy](#files-to-copy)
  - [First-Time Setup](#first-time-setup)
  - [Important Things to Check](#important-things-to-check)
  - [Quick Troubleshooting](#quick-troubleshooting)
- [Use the Skill](#use-the-skill)
  - [Overview: The Workflow](#overview-the-workflow)
  - [Preparation: What You Need Before You Start](#preparation-what-you-need-before-you-start)
  - [Create Test Cases](#create-test-cases)
  - [Frequently Asked Questions](#frequently-asked-questions)

## Set Up the Skill

### Files to Copy

Copy these files while keeping the paths shown below:

```text
.github/
  skills/
    generate-test-cases/
      SKILL.md
      GUIDE.md
      good-example.json       # recommended
      good-example.csv        # recommended
      bad-example.csv         # recommended
  scripts/
    json_to_csv.py
```

`SKILL.md` and `json_to_csv.py` are required. The example files are not used at runtime, but they are useful for reviewing the expected JSON input and CSV output.

### First-Time Setup

1. Place the skill at `.github/skills/generate-test-cases/SKILL.md`.
2. Place the converter at `.github/scripts/json_to_csv.py`.
3. Ensure that a Python 3 interpreter is available through the `python` command in the target environment.
4. Ensure that Copilot can write to `.github/manual_tests/`. The folder does not need to exist in advance: the converter creates it when it writes the CSV file.
5. Decide whether generated CSV files belong in version control. Add `.github/manual_tests/` or a suitable pattern to `.gitignore` if they are only temporary export artifacts.
6. Verify the setup with the included example:

```powershell
python .github/scripts/json_to_csv.py .github/skills/generate-test-cases/good-example.json --output .github/manual_tests/setup-check.csv
```

The command must finish with exit code `0` and create `.github/manual_tests/setup-check.csv`. Delete that check file afterwards if it should not be retained.

### Important Things to Check

### Paths and Commands

The command documented in `SKILL.md` uses repository-relative paths:

```text
python .github/scripts/json_to_csv.py .github/manual_tests/<TICKET-ID>-testcases.json --delete-input
```

If you move either file to another path, update this command in `SKILL.md` as well. A mismatch means the skill can derive cases but cannot create the CSV.

### Python Requirements

The converter uses only the Python standard library. No package installation or virtual environment is required. On systems where `python` does not resolve to Python 3, change the command in `SKILL.md` to the locally supported executable, such as `py -3` on Windows.

### Xray CSV Contract

The converter is tailored to an Xray CSV import with the following behavior:

- Semicolon-separated columns.
- UTF-8 with BOM for Excel compatibility.
- One `TCID` per JSON case; further rows of the same case reuse that `TCID` and leave case-level fields blank.
- One `Keyword` column for every configured keyword.
- Supported priorities: `low`, `medium`, and `high`.
- CSV columns include `Tests`, `Test Plan`, `Author`, `Priority`, and `Repository`.

Confirm that the target project's Xray import mapping accepts these column names and priority values. If it does not, update both the JSON schema instructions in `SKILL.md` and the row generation in `json_to_csv.py` together.

### Required Metadata

The generated JSON requires non-empty values for `testPlan`, `author`, `repository`, `priority`, `keywords`, and `cases`. Each case also requires `ticketId`, `summary`, `checks`, and at least one row with `actionSteps` and `expectedResult`.

The converter validates these fields and stops without producing a valid CSV if they are missing or invalid. In particular, at least one keyword is required.

### Language and Content Rules

The current skill explicitly requires all generated test-case content to be written in German. Keep this rule when the target project's test documentation is German. For another language, update:

- The language requirement and examples in `SKILL.md`.
- The fixed description text in `json_to_csv.py` (`In diesem Ticket wird geprueft:`).
- Any copied documentation and examples.

The converter normalizes German umlauts and `ss`-style output for the CSV, replaces double quotes, and replaces semicolons inside a cell with commas. Check that this normalization is acceptable for the target Xray import and reporting needs.

### Intermediate JSON Files

The skill first writes an intermediate JSON file to `.github/manual_tests/` and then runs the converter with `--delete-input`. The JSON file is removed only after a successful conversion. A failed conversion leaves it in place for troubleshooting; do not commit it accidentally unless it is intended as test data.

### Quick Troubleshooting

- `python` is not recognized: install Python 3 or use the Python launcher command supported by the environment and update `SKILL.md`.
- `File not found`: verify that the copied paths match the command in `SKILL.md`.
- Validation error: inspect the retained JSON file and supply every required metadata field with a valid priority.
- Xray import fails: compare the target import mapping with the header generated by `json_to_csv.py` before changing the skill workflow.

## Use the Skill

### Overview: The Workflow

```
Requirement (ticket / user story)
  ↓
[1] generate-test-cases  →  CSV file in .github/manual_tests/
  ↓
Xray import
```

The workflow consists of **one step**. Copilot asks for all required information and saves the result directly as an importable CSV file; no intermediate output appears in the chat.

### Preparation: What You Need Before You Start

Before asking Copilot to create test cases, have the following information ready:

| Information | Example | Purpose |
|-------------|---------|---------|
| **Requirement** | Ticket text, acceptance criteria, free text | What should be tested? |
| **Test depth** | Positive, negative, boundary values | Which test types should be covered? |
| **Tests** | `ABCD-234` | Jira ticket ID to which the test cases are assigned |
| **Test plan** | `ABCD-3163` | Ticket ID of the associated test plan in Jira |
| **Keywords** | `Automated`, `Described` | Xray labels; each keyword becomes a separate column |
| **Author** | `susi.sonnenschein` | Jira username |
| **Repository** | `Automation/Navigation` | Repository path that categorizes the test cases |
| **Priority** | `low` / `medium` / `high` | Test case priority |

### Create Test Cases

#### How to Activate Copilot

Write, for example, in Copilot Chat:

> "Create test cases for the following requirement: [insert ticket text]"

or

> "Derive manual test cases from this user story: [...]"

#### What Copilot Asks First

Copilot first opens a **dialog** and asks for the desired format:

| Format | Description |
|--------|-------------|
| **Multi-Test** | Each scenario receives its own TCID |
| **Single-Test** | All checks are contained in one test case; each check becomes a separate test step |

Copilot then asks for the following in chat:

1. **Requirement**: What should be tested? (User story, free text, ticket content)
2. **Test depth**: Positive tests, negative tests, boundary tests, or combinations
3. **Metadata**: Ticket ID, test plan, keywords, author, repository, priority

#### What Copilot Produces

After you provide all information, Copilot works internally and outputs **only** the following line in chat:

> `CSV saved: .github/manual_tests/<TICKET-ID>-testcases.csv`

No intermediate format appears in chat. Internally, Copilot first creates a JSON file and converts it to a CSV file using the conversion script. The JSON file is automatically deleted after a successful conversion. The completed CSV file is stored at:

```
.github/manual_tests/<TICKET-ID>-testcases.csv
```

Example: `.github/manual_tests/ABCD-234-testcases.csv`

**Important CSV format details:**
- Delimiter: `;`
- Output uses UTF-8 with BOM for Excel compatibility
- Semicolons inside cell content are replaced with commas
- Line breaks inside cells are encoded as actual line breaks, like Alt+Enter in Excel
- Double quotes in cells are escaped as `""`
- Each keyword has its own column, even though the column name appears multiple times; this is intentional for Xray

If the conversion fails, Copilot displays an error message and does not confirm successful CSV generation.

### Frequently Asked Questions

**Which test types are available?**
- **Positive test (happy path):** Correct input results in the expected system behavior.
- **Negative test:** Incorrect or missing input results in the correct error message.
- **Boundary test:** Extreme values, such as empty values, overly long values, or special characters, are handled reliably.

**What is the difference between `Tests` and `Test plan`?**
`Tests` is the ID of the ticket to which individual test cases are assigned, for example the feature ticket. `Test plan` is the ID of the parent test-plan ticket in Jira/Xray.