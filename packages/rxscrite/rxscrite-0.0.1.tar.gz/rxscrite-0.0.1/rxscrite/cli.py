# rxscrite/cli.py

import argparse
import sys
import os # For checking if file exists

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import RxError # Base error class for RxScrite

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
            # print(f"File '{filepath}' is empty. Nothing to execute.")
            return # Or handle as you see fit

        # 1. Lexer
        lexer = Lexer(source_code, filepath)
        tokens = lexer.tokenize()
        # print("--- Tokens ---")
        # for token in tokens:
        #     print(token)
        # print("--- End Tokens ---\n")


        # 2. Parser
        parser = Parser(tokens, filepath)
        ast = parser.parse()
        # print("--- AST ---")
        # print(ast) # Be careful, can be very verbose for large programs
        # if ast and hasattr(ast, 'statements'):
        #     for i, stmt in enumerate(ast.statements):
        #         print(f"Stmt {i}: {stmt}")
        # print("--- End AST ---\n")

        # 3. Interpreter
        interpreter = Interpreter(filepath)
        result = interpreter.visit(ast) # `visit` typically starts with ProgramNode
        
        # RxScrite's `display()` handles output.
        # The result of the script itself (last expression) might be None
        # or the value of the last expression if not a display call.
        # For now, we don't explicitly print `result` here unless it's meaningful.
        # if result is not None:
        #     print(interpreter._rx_str(result)) # Use interpreter's string conversion

    except RxError as e:
        # This catches RxLexerError, RxParserError, RxRuntimeError, etc.
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError: # Should be caught by os.path.exists, but as a fallback
        print(f"Error: Source file '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Catch any other unexpected Python errors during execution
        print(f"An unexpected Python error occurred: {e}", file=sys.stderr)
        # import traceback
        # traceback.print_exc() # For debugging unexpected Python errors
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="RxScrite Programming Language Interpreter")
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the .rx RxScrite file to execute."
    )
    # Future options:
    # parser.add_argument("-v", "--version", action="version", version=f"RxScrite {VERSION}")
    # parser.add_argument("--tokens", action="store_true", help="Display tokens and exit.")
    # parser.add_argument("--ast", action="store_true", help="Display AST and exit.")

    args = parser.parse_args()
    
    run_rxscrite_file(args.filepath)

if __name__ == '__main__':
    # This allows running `python rxscrite/cli.py yourfile.rx` directly
    # However, for proper package distribution, we'll set up an entry point.
    main()