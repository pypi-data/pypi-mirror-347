# rxscrite/tokens.py

# Token types
# EOF (End Of File) token is used to indicate that
# there is no more input left for lexical analysis
TOKEN_EOF = 'EOF'

# Data types
TOKEN_INTEGER = 'INTEGER'        # e.g., 10, 234
TOKEN_FLOAT = 'FLOAT'          # e.g., 3.14, 0.5
TOKEN_STRING = 'STRING'        # e.g., "hello", 'world'
TOKEN_IDENTIFIER = 'IDENTIFIER'    # e.g., my_variable, my_function

# Keywords
TOKEN_KEYWORD = 'KEYWORD'        # e.g., display, check, loop (used for all keywords)

# Operators
TOKEN_PLUS = 'PLUS'            # +
TOKEN_MINUS = 'MINUS'           # -
TOKEN_MULTIPLY = 'MULTIPLY'        # *
TOKEN_DIVIDE = 'DIVIDE'           # /
TOKEN_POWER = 'POWER'           # ^

# Assignment
TOKEN_ASSIGN = 'ASSIGN'          # =

# Delimiters
TOKEN_LPAREN = 'LPAREN'        # (
TOKEN_RPAREN = 'RPAREN'        # )
TOKEN_COMMA = 'COMMA'           # , (for function arguments, list items etc.)
TOKEN_NEWLINE = 'NEWLINE'        # \n (important for statement separation)

# This dictionary maps keyword strings to their token type (TOKEN_KEYWORD)
# The lexer will use this to identify keywords.
RESERVED_KEYWORDS = {
    'display': TOKEN_KEYWORD,
    'Truth': TOKEN_KEYWORD,
    'Falsity': TOKEN_KEYWORD,
    'Empty': TOKEN_KEYWORD,
    'check': TOKEN_KEYWORD,
    'otherwise': TOKEN_KEYWORD,
    'orcheck': TOKEN_KEYWORD,
    'loop': TOKEN_KEYWORD,
    'repeat_while': TOKEN_KEYWORD,
    'func': TOKEN_KEYWORD,
    'blueprint': TOKEN_KEYWORD,
    'giveback': TOKEN_KEYWORD,
    'constructor': TOKEN_KEYWORD, # For classes
    'both': TOKEN_KEYWORD,    # Logical and
    'either': TOKEN_KEYWORD,  # Logical or
    'negate': TOKEN_KEYWORD,  # Logical not (can also be an operator depending on grammar)
    'inside': TOKEN_KEYWORD,  # Membership 'in'
    'skip': TOKEN_KEYWORD,    # pass
    'exit_loop': TOKEN_KEYWORD, # break
    'next_item': TOKEN_KEYWORD, # continue
    'use': TOKEN_KEYWORD,       # import
    'from_module': TOKEN_KEYWORD, # from
    'alias': TOKEN_KEYWORD,     # as
    'attempt': TOKEN_KEYWORD,   # try
    'on_error': TOKEN_KEYWORD,  # except
    'ensure': TOKEN_KEYWORD,    # finally
    'alert': TOKEN_KEYWORD,     # raise
    'verify': TOKEN_KEYWORD,    # assert
    'remove': TOKEN_KEYWORD,    # del
}


class Token:
    def __init__(self, type, value=None, line=None, column=None):
        self.type = type    # token type: INTEGER, PLUS, IDENTIFIER, etc.
        self.value = value  # token value: 10, "+", "my_var"
        self.line = line    # line number where token appears
        self.column = column # column number where token appears

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 10)
            Token(PLUS, '+')
            Token(IDENTIFIER, 'foo')
        """
        return f"Token({self.type}, {repr(self.value)}" + \
               (f", line={self.line}, col={self.column}" if self.line is not None else "") + ")"

    def __repr__(self):
        return self.__str__()

    def matches(self, type_, value_):
        """Checks if the token matches a given type and value."""
        return self.type == type_ and self.value == value_