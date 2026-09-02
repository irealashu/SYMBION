#!/usr/bin/env python3

import json
import re
import sys

CONFIDENCE_MARKERS = ["++", "+", "~", "-", "--"]

EVIDENCE_TAGS = {
    "@E": "empirical",
    "@L": "logical",
    "@H": "historical",
    "@I": "intuition",
    "@S": "simulation",
}


class SymbionParser:
    def __init__(self):
        self.root = {
            "type": "root",
            "children": []
        }

    def parse_statement(self, line):
        """
        Parse confidence markers and evidence tags.
        """

        statement = {
            "type": "statement",
            "confidence": None,
            "text": "",
            "evidence": [],
            "children": []
        }

        line = line.strip()

        # Confidence marker
        confidence_pattern = r"^(\+\+|\+|~|-|--)\s+(.+)$"
        match = re.match(confidence_pattern, line)

        if match:
            statement["confidence"] = match.group(1)
            line = match.group(2)

        # Evidence tags
        evidence_matches = re.findall(r"@[\w]", line)

        for tag in evidence_matches:
            if tag in EVIDENCE_TAGS:
                statement["evidence"].append(tag)

        # Remove tags from text
        line = re.sub(r"@[\w]", "", line).strip()

        statement["text"] = line

        return statement

    def indentation_level(self, line):
        spaces = len(line) - len(line.lstrip(" "))

        if spaces % 4 != 0:
            raise ValueError(
                f"Invalid indentation: '{line.rstrip()}'\n"
                "SYMBION requires multiples of 4 spaces."
            )

        return spaces // 4

    def parse(self, text):
        lines = text.splitlines()

        stack = [(-1, self.root)]

        for raw_line in lines:

            if not raw_line.strip():
                continue

            if raw_line.strip().startswith("#"):
                continue

            level = self.indentation_level(raw_line)

            node = self.parse_statement(raw_line)

            while stack and stack[-1][0] >= level:
                stack.pop()

            parent = stack[-1][1]
            parent["children"].append(node)

            stack.append((level, node))

        return self.root

    def parse_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return self.parse(f.read())


def export_json(tree, indent=2):
    return json.dumps(tree, indent=indent)


def main():

    if len(sys.argv) < 2:
        print("Usage:")
        print("python parser.py <file.sym>")
        sys.exit(1)

    filename = sys.argv[1]

    parser = SymbionParser()
    tree = parser.parse_file(filename)

    print(export_json(tree))


if __name__ == "__main__":
    main()
