---
name: generate-api-test-cases
description: 'Derives manual test cases for backend/API tickets and saves them as a CSV file optimized for Xray import. Tests are described at the HTTP level (endpoint, method, request body, status codes) — not via UI. Use when asked to create, derive, or write test cases for an API, endpoint, or backend ticket that is tested via Swagger or a REST client.'
---

# Generate API Test Cases

This skill derives manual API test cases from a backend requirement and saves them as a semicolon-separated CSV file for Xray import. The test cases describe HTTP requests and responses, not UI interactions. The workflow is complete only after the CSV conversion succeeds.

The skill instructions are written in English. All natural-language content in the generated CSV must be German. Technical API values such as HTTP methods, endpoint paths, JSON keys, header names, and status codes remain unchanged.

## Scope

### Use when
- The user requests manual test cases for a backend ticket, API requirement, or REST endpoint.
- The tests will be executed through Swagger, Postman, curl, or another REST client.
- The requirement provides, or can provide, concrete HTTP calls and expected behavior.

### Do not use when
- UI test cases are requested; use `generate-test-cases`.
- Automated tests, Playwright tests, or TypeScript code are requested.
- Only a requirement analysis, summary, or translation is requested.
- Gherkin scenarios are requested.

## Absolute Rules

- Derive only test cases supported by the supplied requirement and acceptance criteria. Never invent endpoints, roles, status codes, response fields, validation rules, or permissions.
- Do not output test cases, JSON, file contents, intermediate artifacts, or converter output in chat.
- Do not ask the user to approve or review the generated test cases before conversion.
- Do not ask follow-up questions after the conversion step unless the conversion fails and clarification is required.
- Do not continue after a missing prerequisite, validation error, or converter error.
- The successful completion message in Step 4 is the only chat message after a successful conversion.

## Step 0 — Collect and Validate Input

Ask the user for all required information below before deriving any test case. The format question may be asked as a choice or as plain text; do not depend on a specific tool name.

1. **Format** (required):
   - `Multi-Test`: each independent scenario receives its own case and TCID.
   - `Single-Test`: the complete requirement receives one case and TCID; checks are represented by sequential rows.
2. **Requirement** (required): user story, ticket text, acceptance criteria, or OpenAPI excerpt.
3. **Endpoint(s)** (required): HTTP method and path, for example `POST /api/v1/users`; include query and path parameter rules where relevant.
4. **Authentication** (required): Bearer Token/JWT, Basic Auth, no authentication, or another explicitly described mechanism.
5. **Test depth** (required): one or more of positive, negative, authentication, and boundary tests.
6. **Metadata** (required for all cases):
   - `Tests`: ticket ID, for example `ABCD-234`
   - `Testplan`: associated test-plan ticket ID, for example `ABCD-1234`
   - `Keywords`: one or more keywords; each becomes one CSV column
   - `Author`: for example `maxine.musterfrau`
   - `Repository`: for example `Devtest/Sprint 21`
   - `Priority`: exactly `low`, `medium`, or `high`

Do not proceed until every required field is present and non-empty. Ask only for the missing or ambiguous information. Do not infer missing acceptance criteria from common API conventions.

## Step 1 — Derive Test Cases

Apply the selected format and derive scenarios in this fixed order:

1. Positive tests: the successful request and the status/response behavior explicitly required.
2. Negative tests: missing or invalid inputs explicitly covered by the requirement.
3. Authentication tests: only when selected and the requirement defines the relevant behavior. Use separate scenarios for no token, invalid/expired token, and missing permission only when their expected responses are specified.
4. Boundary tests: only when selected and the requirement defines the relevant boundaries, such as empty values, `null`, maximum lengths, numeric limits, or special characters.

If a selected test type cannot be derived without guessing, stop and ask for the missing acceptance criteria. Do not add a generic 401, 403, 400, or 2xx case merely because it is typical for APIs.

### Multi-Test

- Create one case and one TCID for each independent scenario that starts from a distinct context or request variant.
- Put the complete setup and request in the first row of a scenario.
- Use later rows with the same TCID only for sequential, building actions; include only the delta action.
- Authentication setup is test data or setup context, not a separate verification step.

### Single-Test

- Create exactly one case and one TCID for the requirement.
- Put setup and the first request/verification in the first row.
- Put each additional requirement-derived condition in a later row with the same TCID.
- Do not create a separate expected result for authentication setup.

## Step 2 — Build Internal JSON

Build the following JSON object internally. Never show it in chat and never describe its contents to the user.

```json
{
  "testPlan": "<Testplan ticket ID>",
  "author": "<Author>",
  "repository": "<Repository>",
  "priority": "low|medium|high",
  "keywords": ["<Keyword>", "..."],
  "cases": [
    {
      "ticketId": "<Tests ticket ID>",
      "summary": "<short German test description>",
      "checks": ["<German verification 1>", "<German verification 2>"],
      "rows": [
        {
          "actionSteps": ["<German step>", ["<German sub-step>", "..."]],
          "data": "<test data or \"-\">",
          "expectedResult": "<German HTTP status and business result>"
        }
      ]
    }
  ]
}
```

### JSON contract

- `testPlan`, `author`, `repository`, `priority`, `keywords`, and `cases` are required top-level fields.
- `keywords` and `cases` must be non-empty arrays. `priority` must be `low`, `medium`, or `high`.
- Every case requires non-empty `ticketId`, `summary`, `checks`, and `rows` arrays.
- Every row requires a non-empty `actionSteps` array and `expectedResult`; `data` defaults to `-` when no data is relevant.
- `actionSteps` contains strings for main steps or arrays of non-empty strings for grouped sub-steps.
- The converter assigns TCIDs sequentially. Do not add a `tcid` field.
- `summary` must not repeat the ticket ID; the converter prefixes it automatically.
- Use German for all natural-language fields. Keep technical API values unchanged.

### API formatting

- Format methods as `*GET*`, `*POST*`, `*PUT*`, `*PATCH*`, or `*DELETE*`.
- Enclose endpoints, URL segments, header names, and JSON keys in underscores, for example `*POST* _/api/v1/users_` and `_Authorization_`.
- Put tokens, roles, accounts, request bodies, query parameters, and path parameters in `data`, never in an authentication step's prose.
- Use `Bearer Token setzen (Daten)` for a Bearer setup and `Aufruf ohne _Authorization_-Header` for a no-auth scenario.
- `expectedResult` contains the specified HTTP status and the specified business verification, for example `HTTP 201 – Response enthält _id_`.

## Step 3 — Convert and Validate

Perform these actions internally and do not output their artifacts or command output in chat.

1. Write the JSON to `.github/manual_tests/<TICKET-ID>-testcases.json`, preserving the ticket ID as supplied.
2. Run the repository converter:

   ```text
   python .github/scripts/json_to_csv.py .github/manual_tests/<TICKET-ID>-testcases.json --delete-input
   ```

3. Treat a non-zero exit code, stderr error, invalid JSON, missing input file, missing required field, invalid priority, or empty required array as a failure. Do not continue after failure.
4. On failure, report a concise German error and stop. Do not report the JSON, CSV contents, command output, or any other intermediate artifact.
5. The `--delete-input` option may delete the JSON only after successful conversion. The resulting CSV is `.github/manual_tests/<TICKET-ID>-testcases.csv`.

## Step 4 — Internal Final Check and Completion

Before reporting success, verify internally that:

- all required input and metadata are present;
- every scenario is supported by the requirement and uses the selected format;
- no UI interaction or invented API behavior was added;
- all natural-language CSV content is German;
- methods, endpoints, headers, JSON keys, status codes, rows, and TCIDs follow the API formatting rules;
- the JSON contract and converter path are correct; and
- no intermediate content will be sent to chat.

After successful conversion, output exactly this one line and nothing else:

> CSV gespeichert: `.github/manual_tests/<TICKET-ID>-testcases.csv`

## When the Skill Cannot Proceed

Stop and ask for the missing information when:

- the requirement, endpoint, authentication, test depth, or metadata is missing;
- concrete HTTP calls cannot be derived;
- expected status codes or response behavior are not specified;
- a selected scenario requires assumptions about roles, permissions, validation, or boundaries; or
- JSON creation or conversion fails.

The response must state only what information or correction is needed to continue. Do not generate a partial CSV.
