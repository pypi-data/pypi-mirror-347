# rxscrite/cli.py

import argparse
import sys
import os # For checking if file exists

# Assuming your package structure is correct, these relative imports should work
# when running with `python -m rxscrite.cli ...` or as an installed package.
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import RxError # Base error class for RxScrite
# from . import VERSION # If you have VERSION in rxscrite/__init__.py

def run_rxscrite_file(filepath):
    """
    Reads, lexes, parses, and interprets an RxScrite file.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    
    if not filepath.endswith(".rx"):
        print(f"Error: RxScrite files must have a '.rx' extension. Provided: {filepath}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        if not source_code.strip():
            print(f"File '{filepath}' is empty. Nothing to execute.")
            return

        # 1. Lexer
        lexer = Lexer(source_code, filepath)
        tokens = lexer.tokenize()
        
        # 2. Parser
        # NOTE: The script will likely fail here or in the interpreter
        # until the parser and interpreter are updated for the new tokens/grammar.
        parser = Parser(tokens, filepath)
        ast = parser.parse()
        # print("--- AST ---") # Uncomment to see AST if parser works
        # if ast and hasattr(ast, 'statements'):
        #     for i, stmt in enumerate(ast.statements):
        #         print(f"Stmt {i}: {stmt}")
        # print("--- End AST ---\n")


        # 3. Interpreter
        interpreter = Interpreter(filepath)
        result = interpreter.visit(ast)
        
        # RxScrite's `display()` handles output.
        # The result of the script itself (last expression) might be None
        # or the value of the last expression if not a display call.
        # We don't explicitly print `result` here unless it's meaningful
        # for the language's design (e.g., for a REPL).
        # if result is not None:
        #     print(interpreter._rx_str(result))

    except RxError as e:
        # This catches RxLexerError, RxParserError, RxRuntimeError, etc.
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError: # Should be caught by os.path.exists, but as fallback
        print(f"Error: Source file '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Catch any other unexpected Python errors during execution
        print(f"An unexpected Python error occurred: {e}", file=sys.stderr)
        # For deeper debugging of Python errors:
        # import traceback
        # traceback.print_exc()
        sys.exit(1)

def main():
    parser_arg = argparse.ArgumentParser(description="RxScrite Programming Language Interpreter")
    parser_arg.add_argument(
        "filepath",
        type=str,
        help="Path to the .rx RxScrite file to execute."
    )
    # Example for adding a version argument later, if VERSION is defined in __init__.py
    # parser_arg.add_argument(
    #     "-v", "--version", action="version",
    #     version=f"RxScrite {VERSION if 'VERSION' in globals() else 'unknown'}"
    # )

    args = parser_arg.parse_args()
    
    run_rxscrite_file(args.filepath)

if __name__ == '__main__':
    # This allows running `python rxscrite/cli.py yourfile.rx` directly
    # from the project root, for development.
    main()
