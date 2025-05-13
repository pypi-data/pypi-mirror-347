# rxscrite/lexer.py

from .tokens import (
    Token,
    TOKEN_INTEGER, TOKEN_FLOAT, TOKEN_PLUS, TOKEN_MINUS, TOKEN_MULTIPLY,
    TOKEN_DIVIDE, TOKEN_POWER, TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_EOF,
    TOKEN_IDENTIFIER, TOKEN_KEYWORD, RESERVED_KEYWORDS, TOKEN_ASSIGN,
    TOKEN_COMMA, TOKEN_NEWLINE, TOKEN_STRING,

    # New Operator Tokens
    TOKEN_EE, TOKEN_NE, TOKEN_LT, TOKEN_GT, TOKEN_LTE, TOKEN_GTE,
    TOKEN_LOGICAL_AND, TOKEN_LOGICAL_OR, TOKEN_LOGICAL_NOT, TOKEN_MEM_IN,
    KEYWORD_OPERATORS, # For 'and', 'or', 'not', 'in'

    TOKEN_MODULO, TOKEN_INT_DIVIDE,
    TOKEN_PLUS_ASSIGN, TOKEN_MINUS_ASSIGN, TOKEN_MUL_ASSIGN, TOKEN_DIV_ASSIGN,
    TOKEN_MOD_ASSIGN, TOKEN_POW_ASSIGN, TOKEN_INT_DIV_ASSIGN
)
from .errors import RxLexerError

class Lexer:
    def __init__(self, text, filename="<stdin>"):
        self.text = text
        self.filename = filename
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.line = 1
        self.column = 1

    def advance(self):
        """Advance the 'pos' pointer and set 'current_char'."""
        if self.current_char == '\n':
            self.line += 1
            self.column = 0 # Reset column, next advance will make it 1

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
        
        self.column +=1

    def peek(self, offset=1):
        """Look ahead at characters without consuming the current one."""
        peek_pos = self.pos + offset
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace() and self.current_char != '\n':
            self.advance()

    def skip_comment(self):
        if self.current_char == '#':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()

    def number(self):
        result = ''
        start_line = self.line
        start_column = self.column
        is_float = False

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            if self.peek() and self.peek().isdigit(): 
                result += '.'
                self.advance()
                is_float = True
                while self.current_char is not None and self.current_char.isdigit():
                    result += self.current_char
                    self.advance()
            # If dot is not followed by a digit, it's not part of this number.
        
        if is_float:
            # Ensure there are digits after the decimal point if it's marked as float
            if not result.split('.')[1]: 
                 self.error(f"Invalid float format: '{result}' missing digits after decimal point. Use number.0 for whole floats.", line=start_line, column=start_column)
            return Token(TOKEN_FLOAT, float(result), start_line, start_column)
        else:
            return Token(TOKEN_INTEGER, int(result), start_line, start_column)

    def identifier(self):
        result = ''
        start_line = self.line
        start_column = self.column

        if self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        else: 
            self.error(f"Identifier cannot start with '{self.current_char}'", line=start_line, column=start_column)
            return Token(TOKEN_EOF, None, self.line, self.column) # Should not be reached if error raises

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        if result in KEYWORD_OPERATORS:
            return Token(KEYWORD_OPERATORS[result], result, start_line, start_column)
        elif result in RESERVED_KEYWORDS:
            return Token(TOKEN_KEYWORD, result, start_line, start_column)
        else:
            return Token(TOKEN_IDENTIFIER, result, start_line, start_column)

    def string_literal(self):
        result = ''
        start_line = self.line
        start_column = self.column
        quote_char = self.current_char 

        self.advance() # Consume opening quote

        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\': # Handle escape sequences
                self.advance() # consume backslash
                if self.current_char is None:
                    self.error("Unterminated string literal (EOF after backslash).", line=start_line, column=start_column)
                elif self.current_char == quote_char:
                    result += quote_char
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == 'n': 
                    result += '\n'
                elif self.current_char == 't': 
                    result += '\t'
                else: # Unknown escape sequence, treat as literal backslash and char
                    result += '\\' + self.current_char
            else:
                result += self.current_char
            self.advance()

        if self.current_char is None: # Unterminated string
            self.error("Unterminated string literal (missing closing quote).", line=start_line, column=start_column)
        
        self.advance() # Consume closing quote
        return Token(TOKEN_STRING, result, start_line, start_column)

    def error(self, message="", line=None, column=None):
        """Raises a lexer error. Uses instance line/col if not provided."""
        current_line = line if line is not None else self.line
        current_column = column if column is not None else self.column
        full_message = f"Lexical error"
        if message:
            full_message += f": {message}"
        elif self.current_char: # Add current char info if no specific message
             full_message += f" on '{self.current_char}'"
        raise RxLexerError(full_message, line=current_line, column=current_column)

    def get_next_token(self):
        while self.current_char is not None:
            start_line = self.line
            start_column = self.column

            if self.current_char.isspace():
                if self.current_char == '\n':
                    self.advance()
                    return Token(TOKEN_NEWLINE, '\n', start_line, start_column)
                else:
                    self.skip_whitespace()
                    continue

            if self.current_char == '#':
                self.skip_comment()
                if self.current_char is None: break
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            if self.current_char == '"' or self.current_char == "'":
                return self.string_literal()
            
            # --- Operators ---
            if self.current_char == '=':
                if self.peek() == '=': # ==
                    self.advance(); self.advance()
                    return Token(TOKEN_EE, '==', start_line, start_column)
                else: # =
                    self.advance()
                    return Token(TOKEN_ASSIGN, '=', start_line, start_column)
            
            if self.current_char == '!':
                if self.peek() == '=': # !=
                    self.advance(); self.advance()
                    return Token(TOKEN_NE, '!=', start_line, start_column)
                else:
                    # Standalone '!' is not a valid operator.
                    # Error will be caught by the fall-through unknown character handler,
                    # or we can make it more specific here.
                    # Let's make it specific to guide the user better.
                    char_at_error = self.current_char
                    # Advance before erroring to ensure progress if error is non-fatal (though ours are)
                    # self.advance() 
                    # Using start_line/start_column for the original position of '!'
                    self.error(f"Unknown character '{char_at_error}'. Did you mean '!=' for not equal?", line=start_line, column=start_column)
            
            if self.current_char == '<':
                if self.peek() == '=': # <=
                    self.advance(); self.advance()
                    return Token(TOKEN_LTE, '<=', start_line, start_column)
                else: # <
                    self.advance()
                    return Token(TOKEN_LT, '<', start_line, start_column)

            if self.current_char == '>':
                if self.peek() == '=': # >=
                    self.advance(); self.advance()
                    return Token(TOKEN_GTE, '>=', start_line, start_column)
                else: # >
                    self.advance()
                    return Token(TOKEN_GT, '>', start_line, start_column)

            if self.current_char == '+':
                if self.peek() == '=': # +=
                    self.advance(); self.advance()
                    return Token(TOKEN_PLUS_ASSIGN, '+=', start_line, start_column)
                else: # +
                    self.advance()
                    return Token(TOKEN_PLUS, '+', start_line, start_column)

            if self.current_char == '-':
                if self.peek() == '=': # -=
                    self.advance(); self.advance()
                    return Token(TOKEN_MINUS_ASSIGN, '-=', start_line, start_column)
                else: # -
                    self.advance()
                    return Token(TOKEN_MINUS, '-', start_line, start_column)

            if self.current_char == '*':
                if self.peek() == '=': # *=
                    self.advance(); self.advance()
                    return Token(TOKEN_MUL_ASSIGN, '*=', start_line, start_column)
                else: # *
                    self.advance()
                    return Token(TOKEN_MULTIPLY, '*', start_line, start_column)

            if self.current_char == '/':
                if self.peek() == '/':   
                    self.advance()       
                    if self.peek() == '=': 
                        self.advance()   
                        self.advance()   
                        return Token(TOKEN_INT_DIV_ASSIGN, '//=', start_line, start_column)
                    else: 
                        self.advance()   
                        return Token(TOKEN_INT_DIVIDE, '//', start_line, start_column)
                elif self.peek() == '=': 
                    self.advance(); self.advance()
                    return Token(TOKEN_DIV_ASSIGN, '/=', start_line, start_column)
                else: 
                    self.advance()
                    return Token(TOKEN_DIVIDE, '/', start_line, start_column)

            if self.current_char == '%':
                if self.peek() == '=': # %=
                    self.advance(); self.advance()
                    return Token(TOKEN_MOD_ASSIGN, '%=', start_line, start_column)
                else: # %
                    self.advance()
                    return Token(TOKEN_MODULO, '%', start_line, start_column)

            if self.current_char == '^':
                if self.peek() == '=': # ^=
                    self.advance(); self.advance()
                    return Token(TOKEN_POW_ASSIGN, '^=', start_line, start_column)
                else: # ^
                    self.advance()
                    return Token(TOKEN_POWER, '^', start_line, start_column)

            if self.current_char == '(':
                self.advance()
                return Token(TOKEN_LPAREN, '(', start_line, start_column)
            if self.current_char == ')':
                self.advance()
                return Token(TOKEN_RPAREN, ')', start_line, start_column)
            if self.current_char == ',':
                self.advance()
                return Token(TOKEN_COMMA, ',', start_line, start_column)
            
            # If char hasn't been handled by any rule above, it's unknown.
            unknown_char = self.current_char
            # self.advance() # Advance past the unknown character before erroring
            # Report error at the original position of the unknown character
            self.error(f"Unknown character: '{unknown_char}'", line=start_line, column=start_column)

        return Token(TOKEN_EOF, None, self.line, self.column) # Should be self.line, self.column at EOF

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TOKEN_EOF:
                break
        return tokens
