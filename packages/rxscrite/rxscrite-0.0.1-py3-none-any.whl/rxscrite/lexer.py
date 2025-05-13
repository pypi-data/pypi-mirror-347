# rxscrite/lexer.py

from .tokens import (
    Token,
    TOKEN_INTEGER, TOKEN_FLOAT, TOKEN_PLUS, TOKEN_MINUS, TOKEN_MULTIPLY,
    TOKEN_DIVIDE, TOKEN_POWER, TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_EOF,
    TOKEN_IDENTIFIER, TOKEN_KEYWORD, RESERVED_KEYWORDS, TOKEN_ASSIGN,
    TOKEN_COMMA, TOKEN_NEWLINE, TOKEN_STRING # Added TOKEN_STRING
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
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
        
        self.column +=1

    def peek(self):
        """Look at the next character without consuming the current one."""
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        """Skips over whitespace characters."""
        while self.current_char is not None and self.current_char.isspace() and self.current_char != '\n':
            self.advance()

    def skip_comment(self):
        """Skips a single-line comment."""
        if self.current_char == '#':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        start_line = self.line
        start_column = self.column

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += '.'
            self.advance()
            if not (self.current_char and self.current_char.isdigit()):
                 self.error(f"Invalid character '{self.current_char if self.current_char else 'EOF'}' after '.' in number literal.")
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(TOKEN_FLOAT, float(result), start_line, start_column)
        else:
            return Token(TOKEN_INTEGER, int(result), start_line, start_column)

    def identifier(self):
        """Handle identifiers and reserved keywords."""
        result = ''
        start_line = self.line
        start_column = self.column

        if self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        else: 
            self.error(f"Identifier cannot start with '{self.current_char}'")
            # This path should ideally not be reached if get_next_token calls this appropriately.
            # However, if it is, returning an EOF or a special error token might be needed,
            # but raising an error is generally better.
            return Token(TOKEN_EOF, None, self.line, self.column) # Fallback, should be unreachable

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        token_type = RESERVED_KEYWORDS.get(result, TOKEN_IDENTIFIER)
        if token_type == TOKEN_KEYWORD:
            return Token(token_type, result, start_line, start_column)
        return Token(token_type, result, start_line, start_column)

    def string_literal(self):
        """Handles string literals (e.g., "hello"). Does not support escape sequences yet."""
        result = ''
        start_line = self.line
        start_column = self.column
        quote_char = self.current_char # Should be " (or ' if you add support)

        self.advance() # Consume the opening quote

        while self.current_char is not None and self.current_char != quote_char:
            # TODO: Add escape sequence handling here (e.g., \n, \t, \", \\)
            # For now, all characters are taken literally.
            result += self.current_char
            self.advance()

        if self.current_char is None: # Unterminated string
            self.error("Unterminated string literal (missing closing quote).")
        
        self.advance() # Consume the closing quote
        return Token(TOKEN_STRING, result, start_line, start_column)

    def error(self, message=""):
        """Raises a lexer error."""
        full_message = f"Lexical error"
        if message:
            full_message += f": {message}"
        else:
            full_message += f" on '{self.current_char}'"
        raise RxLexerError(full_message, line=self.line, column=self.column)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)"""
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
                if self.current_char is None:
                    break 
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            if self.current_char == '"': # Check for double-quoted strings
                return self.string_literal()
            
            # Add self.current_char == "'" for single-quoted strings if desired

            if self.current_char == '=':
                self.advance()
                return Token(TOKEN_ASSIGN, '=', start_line, start_column)

            if self.current_char == '+':
                self.advance()
                return Token(TOKEN_PLUS, '+', start_line, start_column)

            if self.current_char == '-':
                self.advance()
                return Token(TOKEN_MINUS, '-', start_line, start_column)

            if self.current_char == '*':
                self.advance()
                return Token(TOKEN_MULTIPLY, '*', start_line, start_column)

            if self.current_char == '/':
                self.advance()
                return Token(TOKEN_DIVIDE, '/', start_line, start_column)

            if self.current_char == '^':
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
            
            char_val = self.current_char
            self.advance() # Consume the char to prevent infinite loop if error isn't raised or re-raised
            self.error(f"Unknown character: '{char_val}'")

        return Token(TOKEN_EOF, None, self.line, self.column)

    def tokenize(self):
        """Returns a list of all tokens from the input text."""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TOKEN_EOF:
                break
        return tokens