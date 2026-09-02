"""Parser placeholder for SYMBION

This module will eventually contain the SYMBION parser implementation.
"""

def parse(source: str):
    """Parse SYMBION source and return an AST placeholder."""
    # TODO: implement parsing logic
    return {"type": "Module", "source": source}


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        src = open(sys.argv[1], "r", encoding="utf-8").read()
        ast = parse(src)
        print("Parsed AST (placeholder):", ast)
    else:
        print("Usage: python parser/parser.py <file.sym>")
