#!/usr/bin/env python3
"""md_to_csv.py — Convert a Markdown table to a semicolon-separated CSV file.

Usage:
    python md_to_csv.py <input.md> [--output <output.csv>] [--delete-input]

Options:
    --output <path>   Write CSV to this path (default: same name as input with .csv extension)
    --delete-input    Delete the input Markdown file after successful conversion

Output is UTF-8 with BOM for Excel compatibility.
Exit code: 0 on success, 1 on error.
"""

import re
import sys
from pathlib import Path


def is_separator_row(cells: list) -> bool:
    non_empty = [c.strip() for c in cells if c.strip()]
    return bool(non_empty) and all(re.fullmatch(r":?-+:?", c) for c in non_empty)


def split_row(line: str) -> list:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def cell_to_csv(value: str) -> str:
    # Replace <br> with actual newline
    value = value.replace("<br>", "\n")
    # Replace ; with , (since ; is the column delimiter)
    value = value.replace(";", ",")
    # Determine quoting before escaping
    needs_quotes = "\n" in value or '"' in value
    # Escape " as ""
    value = value.replace('"', '""')
    if needs_quotes:
        value = f'"{value}"'
    return value


def convert(input_path: Path, output_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8")

    if not text.strip():
        print("Error: Input file is empty.", file=sys.stderr)
        sys.exit(1)

    table_lines = [line for line in text.splitlines() if line.strip().startswith("|")]

    if len(table_lines) < 2:
        print(
            "Error: No valid Markdown table found (need at least header + separator row).",
            file=sys.stderr,
        )
        sys.exit(1)

    header = split_row(table_lines[0])

    sep_cells = split_row(table_lines[1])
    if not is_separator_row(sep_cells):
        print("Error: Second table row is not a valid separator row.", file=sys.stderr)
        sys.exit(1)

    col_count = len(header)
    rows = []
    for i, line in enumerate(table_lines[2:], start=3):
        row = split_row(line)
        if len(row) != col_count:
            print(
                f"Error: Row {i} has {len(row)} columns, expected {col_count}.",
                file=sys.stderr,
            )
            sys.exit(1)
        rows.append(row)

    if not rows:
        print("Error: Table has no data rows.", file=sys.stderr)
        sys.exit(1)

    csv_lines = [";".join(cell_to_csv(c) for c in header)]
    for row in rows:
        csv_lines.append(";".join(cell_to_csv(c) for c in row))

    csv_content = "\n".join(csv_lines) + "\n"

    # Write UTF-8 with BOM for Excel compatibility
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes("\ufeff".encode("utf-8") + csv_content.encode("utf-8"))
    print(f"OK: {input_path} -> {output_path}")


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print(
            "Usage: python md_to_csv.py <input.md> [--output <output.csv>] [--delete-input]",
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
