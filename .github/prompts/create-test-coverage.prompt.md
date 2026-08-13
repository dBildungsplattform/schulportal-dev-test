Please check the test coverage in the following case:
The test cases are located in test_coverage\testitems.md,
and the tests are in the tests folder.

Be sure to read the contents of the relevant test files—not just their names.
Check whether the subject under test appears as a standalone describe/test block
or is covered only implicitly as a step in another test.

Use the following statuses:
- ✅ Fully covered: tested directly and completely; all user groups included
- ⚠️ Partially covered: implicitly; only some user groups, or only as a side effect of another test
- ❌ Not covered: no test available

Create a Markdown table with the columns:
No. | Subject under test | User group(s) | Status | Test file(s) | Notes

In the "Comments" column, briefly explain why you rated the status that way,
especially for ⚠️ and ❌.

Write the result in test_coverage\test_coverage_<current date in YYYY-MM-DD format>.md. Add the current date to the filename.
At the end, add a summary with: Total count, ✅, ⚠️, ❌.