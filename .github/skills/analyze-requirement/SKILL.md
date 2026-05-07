---
name: analyze-requirement
description: 'Analyzes a user story or requirement for gaps, ambiguities, and completeness using 10 structured checks. Produces a status-icon report (✅ / ⚠️ / ❌) per check and a final binary READY / NOT READY verdict. Use when asked to review, analyze, check, or critique a user story, requirement, or ticket for quality and readiness.'
---

# Analyze Requirement

This skill takes a user story or requirement and runs 10 structured quality checks on it. The goal is to surface specification gaps, ambiguities, and missing information before development begins. The result is a structured report with a clear readiness verdict.

## Use When
- You are asked to review, analyze, critique, or check a user story or requirement
- You are asked to find gaps, ambiguities, or missing information in a specification
- You are asked whether a story is "ready" or "Definition of Ready"-compliant
- You are asked to identify risks or open questions in a requirement

## Do Not Use When
- Test cases should be derived from a requirement — use the `generate-test-cases` skill instead
- Code should be written or modified — use the normal coding workflow
- Only a summary or translation of a requirement is requested

---

## Step 0 — Collect Input

Before running any checks, ask the user for the following. Wait for all answers before proceeding:

1. **Requirement**: The user story, requirement text, or ticket content to analyze.
2. **Context** *(optional)*: Any relevant background about the system, domain, or users that is not obvious from the requirement itself.

> **Do not start the analysis until the requirement text is provided.**

---

## Step 1 — Run 10 Checks

Run all 10 checks on the provided requirement. For each check, provide:
- A **status icon**: ✅ (looks good), ⚠️ (partially addressed / needs attention), or ❌ (missing / critical gap)
- Your **findings**: concrete observations based on the requirement text

Work through all checks sequentially, then output the complete report in one go.

---

### Check 1: Goal Clarity
**Question:** What is the purpose and goal of this requirement? Who benefits, and how?

Look for:
- A clear problem statement or user need
- Identified stakeholders / user roles
- The value or outcome the requirement is meant to deliver
- Whether "why" is explained, not just "what"

---

### Check 2: Ambiguity Check
**Question:** Are all terms, conditions, and statements clearly and unambiguously defined?

Look for:
- Vague quantifiers ("some", "often", "as needed", "appropriate", "fast", "user-friendly")
- Undefined domain terms or abbreviations
- Statements that can be interpreted in more than one way
- Implicit assumptions treated as facts
- Passive voice hiding who is responsible for an action

---

### Check 3: Affected Processes / Use Cases
**Question:** Which processes, use cases, or user journeys are impacted by this requirement?

Look for:
- Explicit or implicit user flows that are touched
- Dependencies on other features or systems
- Side effects on existing functionality
- Roles or actors involved
- Edge cases in affected flows that are not described

---

### Check 4: Relevant Data
**Question:** What data is involved? Are formats, constraints, validation rules, and examples specified?

Look for:
- Input and output data described
- Data formats, types, and ranges
- Validation rules and error handling for invalid data
- Example values or sample data
- Data persistence, storage, or migration concerns
- GDPR / data privacy implications

---

### Check 5: Acceptance Criteria
**Question:** Are there complete, unambiguous, and testable acceptance criteria?

Look for:
- Each criterion is independently verifiable
- Criteria cover the happy path
- Criteria cover important error/edge cases
- Criteria are written in a testable format (e.g., Given/When/Then or similar)
- No criterion relies on subjective judgment ("looks good", "works correctly")

---

### Check 6: Non-Functional Requirements
**Question:** Are non-functional requirements (NFRs) addressed?

Look for:
- **Performance**: Response times, throughput, load expectations
- **Security**: Authentication, authorization, data protection
- **Accessibility**: WCAG compliance, screen reader support
- **Reliability / Availability**: Uptime expectations, error recovery
- **Scalability**: Behavior under increased load
- **Compatibility**: Browser, device, OS, API version constraints
- **Localization / Internationalization**: Language, date/number formats

---

### Check 7: Missing Information
**Question:** What information is missing that would be needed to implement or test this requirement?

Look for:
- UI/UX mockups or wireframes referenced but not provided
- API contracts or data schemas not specified
- Business rules mentioned but not detailed
- External dependencies (third-party systems, services) not described
- Open decisions or unresolved questions left in the text ("TBD", "to be clarified", "ask PO")

---

### Check 8: Testability & Test Scenarios
**Question:** How would you test this requirement? What test scenarios emerge?

Identify:
- The key positive scenarios (happy path)
- Negative scenarios (invalid input, missing permissions, system errors)
- Boundary / edge cases
- Any scenario that is mentioned implicitly but not explicitly
- Scenarios that would require specific test data or environment setup

---

### Check 9: Assumptions & Risks
**Question:** What assumptions are implicit in the requirement? What risks could arise?

Look for:
- Assumptions about user behavior, technical infrastructure, or existing functionality
- Dependencies on external systems or teams
- Risks if the requirement is misunderstood or incompletely implemented
- Implementation risks (complexity, unknowns, tight coupling)
- Business risks (compliance, user impact, reversibility)

---

### Check 10: Ready Assessment
**Question:** Taking all checks into account — is this story ready for development?

Summarize:
- Which checks passed cleanly (✅)
- Which checks raised concerns (⚠️)
- Which checks found critical gaps (❌)
- Overall readiness conclusion

---

## Step 2 — Output Format

Structure the complete report exactly as follows:

```
# Requirement Analysis

## Requirement
> <quoted requirement text or short summary>

---

### Check 1: Goal Clarity
**Status:** ✅ / ⚠️ / ❌

<findings>

---

### Check 2: Ambiguity Check
**Status:** ✅ / ⚠️ / ❌

<findings>

---

[... checks 3–9 in the same format ...]

---

### Check 10: Ready Assessment
**Status:** ✅ / ⚠️ / ❌

<summary of all checks>

---

## Verdict: READY ✅  /  NOT READY ❌

### Open Items
- [ ] <specific open question or gap — one per line>
- [ ] ...
```

**Rules:**
- Every check must appear in the output, even if the finding is positive.
- Use concrete references to the requirement text in your findings — do not give generic advice.
- The Open Items list only appears for **NOT READY** verdicts and must list each gap as an actionable `- [ ]` checkbox.
- For **READY** verdicts, the Open Items section may list minor ⚠️ items as suggestions, clearly marked as non-blocking.

---

## Step 3 — Self-Check Before Output

- [ ] All 10 checks are present in the report
- [ ] Each check has exactly one status icon (✅, ⚠️, or ❌)
- [ ] Findings reference the actual requirement text, not generic observations
- [ ] Check 10 summarizes the overall picture
- [ ] A clear READY or NOT READY verdict is given
- [ ] Open Items are listed as `- [ ]` checkboxes if the verdict is NOT READY

---

## When the Skill Cannot Proceed

Stop and inform the user if:
- No requirement text was provided — ask for it
- The requirement is a single sentence with no details — ask for more context before analyzing
