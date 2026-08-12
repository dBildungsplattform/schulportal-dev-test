
# Skill Review Checklist (v2)

Objective: This checklist serves as a best-practice guide for skill reviews within the team.

## 1. Inconsistencies
- Are the instructions in the skill consistent?
- Are there any rules that are overridden or mitigated elsewhere?
Why this matters: Contradictions create unpredictable behavior and lead to inconsistent outputs across runs.

## 2. Clear and Unambiguous Scope
- Is the goal of the skill clearly identifiable?
- Is it clearly defined what the skill is used for and what it is not used for?
Why this matters: A clear scope prevents misuse and keeps the skill focused on the intended task.

## 3. Consistent Step Logic and Numbering
- Are all steps numbered clearly and consistently (e.g., 0, 0a, 0b, 1, 2, 3, 4)?
- Is there no risk of confusion between steps and sub-steps?
- Does the order of the steps follow the technical logic?
Why this matters: Clear sequencing reduces execution errors and makes reviews and maintenance faster.

## 4. Input Requirements
- Is all required information clearly labeled?
- Is it specified that the process will not proceed without complete required information?
- Are there specific examples of valid inputs?
Why this matters: Strong input contracts avoid guesswork and reduce avoidable follow-up questions.

## 5. Termination Rules
- Is it clearly defined when the skill must stop?
- Is it clearly defined what feedback is sent to the user upon termination?
Why this matters: Explicit stop conditions prevent low-quality output when prerequisites are missing.

## 6. Output Contract
- Is the final output precisely and unambiguously specified?
- Is it specified what must not be output (e.g., no internal artifacts)?
- Is there an authoritative output rule (e.g., “only message,” “nothing else”)?
Why this matters: A strict output contract is key for reliability, downstream automation, and user trust.

## 7. Redundancies
- Are there any avoidable redundancies in the content?
- Are redundancies present only where they are necessary for robustness?
Why this matters: Less duplication lowers maintenance effort and reduces the risk of conflicting updates.

## 8. Tables and Internal Data
- Are internal structures defined in a machine-readable format (e.g., JSON instead of a Markdown table for internal processing)?
- Are data fields uniquely named and fully described?
Why this matters: Structured internal data improves scriptability, validation, and interoperability.

## 9. Scriptability and Automation
- Can manual steps be replaced by scripts?
- Have the following been tested:
    - Regular expression-based transformations
    - Python scripts
    - Other suitable automation methods
Why this matters: Automating repeatable steps increases speed, consistency, and auditability.

## 10. Error Handling
- Has it been defined how to handle script errors (exit code, stderr, termination)?
- Is it clear that the process will not continue without notification in the event of errors?
Why this matters: Clear error handling prevents silent failures and makes troubleshooting straightforward.

## 11. Determinism and Consistency
- Do identical inputs lead to results with the same structure?
- Are terms used consistently throughout (e.g., Test Plan vs. Testplan)?
Why this matters: Deterministic behavior enables dependable quality checks and predictable user outcomes.

## 12. Tool and Environment Considerations
- Are tool names correct in the target environment?
- Are commands and paths formulated in a robust and unambiguous manner?
Why this matters: Environment-safe instructions reduce execution issues across different setups.

## 13. Language
- Is the skill’s language English?
- Are exceptions for proper nouns and technical terms applied clearly and consistently?
Why this matters: Consistent language improves readability, collaboration, and review quality across teams.

## 14. Internal Final Check
- Is there a brief internal quality check before completion (completeness, language, required fields, order)?
- Is it clear that this check remains internal and is not displayed in the chat?
Why this matters: A final internal gate catches preventable mistakes before user-facing output is sent.

## Quick Review (2 Minutes, Yes/No)

Use this as a fast pre-check before the full review. If one or more answers are "No", run the full checklist above.

1. Is the goal and scope of the skill clear in one read?
2. Are all required user inputs explicitly listed?
3. Are step numbers consistent and logically ordered?
4. Is it clear when the skill must stop and what to tell the user?
5. Is the final output defined exactly (format and wording)?
6. Is there an explicit "nothing else"-style output constraint?
7. Are internal artifacts (JSON, intermediate files, script output) blocked from chat output?
8. Is error handling defined (exit code/stderr and mandatory stop on failure)?
9. Is language policy clear (English default, allowed exceptions defined)?
10. Would identical inputs produce a similarly structured output?