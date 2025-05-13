# rxscrite/tokens.py

# Token types
TOKEN_EOF = 'EOF'

# Data types
TOKEN_INTEGER = 'INTEGER'
TOKEN_FLOAT = 'FLOAT'
TOKEN_STRING = 'STRING'
TOKEN_IDENTIFIER = 'IDENTIFIER'

# General Keywords (for control flow, definitions, etc., not operators)
TOKEN_KEYWORD = 'KEYWORD'

# Operators
TOKEN_PLUS = 'PLUS'            # +
TOKEN_MINUS = 'MINUS'           # -
TOKEN_MULTIPLY = 'MULTIPLY'        # *
TOKEN_DIVIDE = 'DIVIDE'           # /
TOKEN_POWER = 'POWER'           # ^
TOKEN_MODULO = 'MODULO'         # % (New)
TOKEN_INT_DIVIDE = 'INT_DIVIDE'   # // (New)

# Assignment
TOKEN_ASSIGN = 'ASSIGN'          # =
# Compound Assignment Operators (New)
TOKEN_PLUS_ASSIGN = 'PLUS_ASSIGN'     # +=
TOKEN_MINUS_ASSIGN = 'MINUS_ASSIGN'    # -=
TOKEN_MUL_ASSIGN = 'MUL_ASSIGN'       # *=
TOKEN_DIV_ASSIGN = 'DIV_ASSIGN'       # /=
TOKEN_MOD_ASSIGN = 'MOD_ASSIGN'       # %=
TOKEN_POW_ASSIGN = 'POW_ASSIGN'       # ^=
TOKEN_INT_DIV_ASSIGN = 'INT_DIV_ASSIGN' # //=

# Delimiters
TOKEN_LPAREN = 'LPAREN'        # (
TOKEN_RPAREN = 'RPAREN'        # )
TOKEN_COMMA = 'COMMA'           # ,
TOKEN_NEWLINE = 'NEWLINE'        # \n

# Comparison Operators (New - Python Style)
TOKEN_EE = 'EE'                # == (Equal Equal)
TOKEN_NE = 'NE'                # != (Not Equal)
TOKEN_LT = 'LT'                # <  (Less Than)
TOKEN_GT = 'GT'                # >  (Greater Than)
TOKEN_LTE = 'LTE'               # <= (Less Than or Equal)
TOKEN_GTE = 'GTE'               # >= (Greater Than or Equal)

# Logical Operators (New - Python Style Keywords, treated as distinct tokens)
TOKEN_LOGICAL_AND = 'LOGICAL_AND' # 'and'
TOKEN_LOGICAL_OR = 'LOGICAL_OR'  # 'or'
TOKEN_LOGICAL_NOT = 'LOGICAL_NOT' # 'not' (unary)

# Membership Operators (New - Python Style Keywords, treated as distinct tokens)
TOKEN_MEM_IN = 'MEM_IN'          # 'in'
TOKEN_MEM_NOT_IN = 'MEM_NOT_IN'  # 'not in' (will be lexed as two tokens: NOT then IN, or a single combined token)
                                 # For simplicity, let's aim for 'not in' as a distinct concept,
                                 # but lexing it might involve peeking.
                                 # For now, let's define distinct tokens for 'in' and 'not'.
                                 # The parser will handle 'not in' logic.

# Reserved Keywords (for language constructs, not operators anymore)
# We've removed: is_equal_to, greater_than, both, either, negate, inside etc.
# 'and', 'or', 'not', 'in' are now specific token types above.
RESERVED_KEYWORDS = {
    'display': TOKEN_KEYWORD,
    'ask': TOKEN_KEYWORD,
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
    'constructor': TOKEN_KEYWORD,
    'skip': TOKEN_KEYWORD,
    'exit_loop': TOKEN_KEYWORD,
    'next_item': TOKEN_KEYWORD,
    'use': TOKEN_KEYWORD,
    'from_module': TOKEN_KEYWORD,
    'alias': TOKEN_KEYWORD,
    'attempt': TOKEN_KEYWORD,
    'on_error': TOKEN_KEYWORD,
    'ensure': TOKEN_KEYWORD,
    'alert': TOKEN_KEYWORD,
    'verify': TOKEN_KEYWORD,
    'remove': TOKEN_KEYWORD,
    # Python's 'is' and 'is not' (identity) could be added later if needed
    # For now, 'in' is TOKEN_MEM_IN. 'not' is TOKEN_LOGICAL_NOT.
    # The parser will combine 'not' and 'in' if it sees them together for 'not in'.
}

# Special map for keyword-like operators, distinct from general identifiers
# This helps the lexer identify 'and', 'or', 'not', 'in' as specific operator tokens
# rather than TOKEN_IDENTIFIER or general TOKEN_KEYWORD.
KEYWORD_OPERATORS = {
    'and': TOKEN_LOGICAL_AND,
    'or': TOKEN_LOGICAL_OR,
    'not': TOKEN_LOGICAL_NOT,
    'in': TOKEN_MEM_IN,
}


class Token:
    def __init__(self, type, value=None, line=None, column=None):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)}" + \
               (f", line={self.line}, col={self.column}" if self.line is not None else "") + ")"

    def __repr__(self):
        return self.__str__()

    def matches(self, type_, value_):
        return self.type == type_ and self.value == value_
