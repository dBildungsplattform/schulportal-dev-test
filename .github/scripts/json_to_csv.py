#!/usr/bin/env python3
"""json_to_csv.py — Convert a structured test-case JSON file to a semicolon-separated CSV file.

Usage:
    python json_to_csv.py <input.json> [--output <output.csv>] [--delete-input]

Options:
    --output <path>   Write CSV to this path (default: same name as input with .csv extension)
    --delete-input    Delete the input JSON file after successful conversion

Input JSON schema:
{
  "testPlan": str,
  "author": str,
  "repository": str,
  "priority": "low" | "medium" | "high",
  "keywords": [str, ...],                     # at least one; each becomes its own CSV "Keyword" column
  "cases": [
    {
      "ticketId": str,                        # "Tests" column value; also prefixes Summary
      "summary": str,                         # short description, without ticketId prefix
      "checks": [str, ...],                   # bullet points used to build the Description cell
      "rows": [
        {
          "actionSteps": [str | [str, ...], ...],  # str = main step (#), nested list = sub-steps (##)
          "data": str,                              # optional, defaults to "-"
          "expectedResult": str
        },
        ...
      ]
    },
    ...
  ]
}

Each case becomes one TCID (sequential, starting at 1). Only the first row of a
case carries Tests/Summary/Description/Test Plan/Author/Keyword/Priority/Repository;
subsequent rows of the same case leave those columns empty.

Output is UTF-8 with BOM for Excel compatibility.
Exit code: 0 on success, 1 on error.
"""

import json
import sys
from pathlib import Path


CHAR_REPLACEMENTS = (
    ('"', "'"),
    ("ä", "ae"),
    ("ö", "oe"),
    ("ü", "ue"),
    ("ß", "ss"),
)

VALID_PRIORITIES = {"low", "medium", "high"}


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def require_text(value, message: str) -> None:
    require(isinstance(value, str) and value.strip(), message)


def validate(doc: dict) -> None:
    require(isinstance(doc, dict), "Root JSON value must be an object.")

    for field in ("testPlan", "author", "repository", "priority"):
        require_text(doc.get(field), f"Missing or empty top-level field: {field}")
    require(
        doc["priority"] in VALID_PRIORITIES,
        f"priority must be one of {sorted(VALID_PRIORITIES)}, got {doc.get('priority')!r}",
    )

    require(
        isinstance(doc.get("keywords"), list) and doc["keywords"],
        "keywords must be a non-empty array",
    )
    for i, kw in enumerate(doc["keywords"]):
        require_text(kw, f"keywords[{i}] must be a non-empty string")

    require(isinstance(doc.get("cases"), list) and doc["cases"], "cases must be a non-empty array")

    for ci, case in enumerate(doc["cases"]):
        require_text(case.get("ticketId"), f"cases[{ci}].ticketId is required")
        require_text(case.get("summary"), f"cases[{ci}].summary is required")

        require(
            isinstance(case.get("checks"), list) and case["checks"],
            f"cases[{ci}].checks must be a non-empty array",
        )
        for chi, check in enumerate(case["checks"]):
            require_text(check, f"cases[{ci}].checks[{chi}] must be a non-empty string")

        require(
            isinstance(case.get("rows"), list) and case["rows"],
            f"cases[{ci}].rows must be a non-empty array",
        )
        for ri, row in enumerate(case["rows"]):
            steps = row.get("actionSteps")
            require(
                isinstance(steps, list) and steps,
                f"cases[{ci}].rows[{ri}].actionSteps must be a non-empty array",
            )
            for si, step in enumerate(steps):
                if isinstance(step, list):
                    require(
                        step and all(isinstance(s, str) and s.strip() for s in step),
                        f"cases[{ci}].rows[{ri}].actionSteps[{si}] sub-steps must be non-empty strings",
                    )
                else:
                    require_text(
                        step, f"cases[{ci}].rows[{ri}].actionSteps[{si}] must be a non-empty string"
                    )
            require_text(
                row.get("expectedResult"), f"cases[{ci}].rows[{ri}].expectedResult is required"
            )


def normalize_characters(value: str) -> str:
    for old, new in CHAR_REPLACEMENTS:
        value = value.replace(old, new)
    return value


def cell_to_csv(value: str) -> str:
    value = value.replace(";", ",")
    needs_quotes = "\n" in value or '"' in value
    value = value.replace('"', '""')
    if needs_quotes:
        value = f'"{value}"'
    return value


def build_description(checks: list) -> str:
    lines = ["In diesem Ticket wird geprüft:"] + [f"- {c}" for c in checks]
    return "\n".join(lines)


def build_action(steps: list) -> str:
    lines = []
    for step in steps:
        if isinstance(step, list):
            lines.extend(f"## {s}" for s in step)
        else:
            lines.append(f"# {step}")
    return "\n".join(lines)


def build_rows(doc: dict) -> list:
    keywords = doc["keywords"]
    header = (
        ["TCID", "Tests", "Summary", "Description", "Action", "Data", "Expected Result", "Test Plan", "Author"]
        + ["Keyword"] * len(keywords)
        + ["Priority", "Repository"]
    )

    rows = [header]
    for tcid, case in enumerate(doc["cases"], start=1):
        description = build_description(case["checks"])
        summary = f"{case['ticketId']}: {case['summary']}"
        for ri, row in enumerate(case["rows"]):
            action = build_action(row["actionSteps"])
            data = row.get("data") or "-"
            expected = row["expectedResult"]
            if ri == 0:
                rows.append(
                    [str(tcid), case["ticketId"], summary, description, action, data, expected,
                     doc["testPlan"], doc["author"]]
                    + list(keywords)
                    + [doc["priority"], doc["repository"]]
                )
            else:
                rows.append(
                    [str(tcid), "", "", "", action, data, expected, "", ""]
                    + [""] * len(keywords)
                    + ["", ""]
                )
    return rows


def convert(input_path: Path, output_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8-sig")

    try:
        doc = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        validate(doc)
    except ValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    rows = build_rows(doc)
    csv_lines = [
        ";".join(cell_to_csv(normalize_characters(cell)) for cell in row) for row in rows
    ]
    csv_content = "\n".join(csv_lines) + "\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes("\ufeff".encode("utf-8") + csv_content.encode("utf-8"))
    print(f"OK: {input_path} -> {output_path}")


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print(
            "Usage: python json_to_csv.py <input.json> [--output <output.csv>] [--delete-input]",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = Path(args[0])
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 >= len(args):
            print("Error: --output requires a value.", file=sys.stderr)
            sys.exit(1)
        output_path = Path(args[idx + 1])
    else:
        output_path = input_path.with_suffix(".csv")

    delete_input = "--delete-input" in args

    convert(input_path, output_path)

    if delete_input:
        input_path.unlink()


if __name__ == "__main__":
    main()
