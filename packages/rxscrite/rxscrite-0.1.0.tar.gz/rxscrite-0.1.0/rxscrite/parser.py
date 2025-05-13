# rxscrite/parser.py

from .tokens import (
    TOKEN_INTEGER, TOKEN_FLOAT, TOKEN_PLUS, TOKEN_MINUS, TOKEN_MULTIPLY,
    TOKEN_DIVIDE, TOKEN_POWER, TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_EOF,
    TOKEN_IDENTIFIER, TOKEN_KEYWORD, TOKEN_ASSIGN, TOKEN_COMMA, TOKEN_NEWLINE,
    TOKEN_STRING,

    # New Operator Tokens
    TOKEN_EE, TOKEN_NE, TOKEN_LT, TOKEN_GT, TOKEN_LTE, TOKEN_GTE,
    TOKEN_LOGICAL_AND, TOKEN_LOGICAL_OR, TOKEN_LOGICAL_NOT, TOKEN_MEM_IN,
    
    TOKEN_MODULO, TOKEN_INT_DIVIDE,
    TOKEN_PLUS_ASSIGN, TOKEN_MINUS_ASSIGN, TOKEN_MUL_ASSIGN, TOKEN_DIV_ASSIGN,
    TOKEN_MOD_ASSIGN, TOKEN_POW_ASSIGN, TOKEN_INT_DIV_ASSIGN
)
from .nodes import (
    NumberNode, BinaryOpNode, UnaryOpNode, VariableAssignNode,
    VariableAccessNode, FunctionCallNode, ProgramNode, IdentifierNode,
    StringNode, TruthNode, FalsityNode, EmptyNode, NoOpNode,
    CompoundAssignNode 
)
from .errors import RxParserError

class Parser:
    def __init__(self, tokens, filename="<stdin>"):
        self.tokens = tokens
        self.filename = filename
        self.token_idx = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            last_tok = self.tokens[-1] if self.tokens else None
            line = last_tok.line if last_tok else (self.current_token.line if self.current_token else 1)
            col = last_tok.column if last_tok else (self.current_token.column if self.current_token else 1)
            self.current_token = Token(TOKEN_EOF, None, line=line, column=col)
        # print(f"Advanced to: {self.current_token}") # General advance debug
        return self.current_token
    
    def _current_line_col(self): # Helper for error reporting if current_token is None
        if self.current_token and self.current_token.type != TOKEN_EOF:
            return self.current_token.line, self.current_token.column
        # Try to get from previous token if at EOF or current_token is None
        if self.token_idx > 0 and self.token_idx -1 < len(self.tokens) :
             prev_token = self.tokens[self.token_idx-1]
             return prev_token.line, prev_token.column
        return 1,1 # Fallback

    def peek(self):
        if self.token_idx + 1 < len(self.tokens):
            return self.tokens[self.token_idx + 1]
        l,c = self._current_line_col()
        return Token(TOKEN_EOF, None, line=l, column=c) 

    def error(self, expected_token_type=None, message=""):
        line, column = self._current_line_col()
        if self.current_token and self.current_token.type != TOKEN_EOF : # Prefer current token's pos if valid
            line = self.current_token.line
            column = self.current_token.column

        if not message:
            if expected_token_type and self.current_token:
                message = f"Expected {expected_token_type}, but got {self.current_token.type} ('{self.current_token.value}')"
            elif self.current_token:
                message = f"Unexpected token: {self.current_token}"
            else:
                message = "Unexpected end of file (or token is None)."
        
        raise RxParserError(message, line=line, column=column)

    def eat(self, token_type, token_value=None):
        if self.current_token is None or self.current_token.type == TOKEN_EOF:
            l,c = self._current_line_col()
            raise RxParserError(f"Unexpected EOF. Expected {token_type}", line=l, column=c)
        
        if self.current_token.type == token_type:
            if token_value is not None and self.current_token.value != token_value:
                self.error(expected_token_type, f"Expected token value '{token_value}' but got '{self.current_token.value}'")
            eaten_token = self.current_token
            self.advance()
            return eaten_token
        else:
            self.error(expected_token_type, f"Expected token type {token_type} but got {self.current_token.type} ('{self.current_token.value}')")


    def program(self):
        prog_node = ProgramNode()
        while self.current_token and self.current_token.type == TOKEN_NEWLINE:
            self.eat(TOKEN_NEWLINE)

        while self.current_token and self.current_token.type != TOKEN_EOF:
            if self.current_token.type == TOKEN_NEWLINE: 
                self.eat(TOKEN_NEWLINE)
                continue
            
            # print(f"Program loop: current token before statement(): {self.current_token}") # Debug
            stmt = self.statement()
            # print(f"Program loop: current token after statement(): {self.current_token}") # Debug
            
            if stmt and not isinstance(stmt, NoOpNode):
                prog_node.statements.append(stmt)

            if self.current_token.type != TOKEN_EOF:
                if self.current_token.type == TOKEN_NEWLINE:
                    while self.current_token and self.current_token.type == TOKEN_NEWLINE:
                        self.eat(TOKEN_NEWLINE)
                else:
                    # print(f"ERROR Point in program(): current_token is {self.current_token}") # Debug
                    self.error(TOKEN_NEWLINE, "Expected newline or EOF after statement.")
            
            while self.current_token and self.current_token.type == TOKEN_NEWLINE: # Consume any further blank lines
                self.eat(TOKEN_NEWLINE)
        return prog_node

    def statement(self):
        if self.current_token.type == TOKEN_IDENTIFIER:
            peeked_token = self.peek()
            if peeked_token.type in (TOKEN_ASSIGN, TOKEN_PLUS_ASSIGN, TOKEN_MINUS_ASSIGN,
                                     TOKEN_MUL_ASSIGN, TOKEN_DIV_ASSIGN, TOKEN_MOD_ASSIGN,
                                     TOKEN_POW_ASSIGN, TOKEN_INT_DIV_ASSIGN):
                return self.assignment_statement()
        
        return self.expression()


    def assignment_statement(self):
        var_name_token = self.eat(TOKEN_IDENTIFIER)
        assign_op_token = self.current_token
        
        if assign_op_token.type == TOKEN_ASSIGN:
            self.eat(TOKEN_ASSIGN)
            value_node = self.expression()
            return VariableAssignNode(var_name_token, value_node)
        elif assign_op_token.type in (TOKEN_PLUS_ASSIGN, TOKEN_MINUS_ASSIGN, TOKEN_MUL_ASSIGN, 
                                      TOKEN_DIV_ASSIGN, TOKEN_MOD_ASSIGN, TOKEN_POW_ASSIGN,
                                      TOKEN_INT_DIV_ASSIGN):
            self.eat(assign_op_token.type)
            value_node = self.expression()
            return CompoundAssignNode(var_name_token, assign_op_token, value_node)
        else:
            self.error(message=f"Expected assignment operator (=, +=, etc.) but got {assign_op_token.type}")
            return NoOpNode() 

    def expression(self):
        return self.logical_or_expression()

    def logical_or_expression(self):
        node = self.logical_and_expression()
        while self.current_token.type == TOKEN_LOGICAL_OR:
            op_token = self.eat(TOKEN_LOGICAL_OR)
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=self.logical_and_expression())
        return node

    def logical_and_expression(self):
        node = self.not_expression() # Changed from comparison_expression
        while self.current_token.type == TOKEN_LOGICAL_AND:
            op_token = self.eat(TOKEN_LOGICAL_AND)
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=self.not_expression())
        return node

    def not_expression(self):
        if self.current_token.type == TOKEN_LOGICAL_NOT:
            op_token = self.eat(TOKEN_LOGICAL_NOT)
            node = UnaryOpNode(op_token, self.not_expression()) 
            return node
        else:
            return self.comparison_expression()

    def comparison_expression(self):
        node = self.membership_expression()
        while self.current_token.type in (TOKEN_EE, TOKEN_NE, TOKEN_LT, TOKEN_GT, TOKEN_LTE, TOKEN_GTE):
            op_token = self.current_token
            self.eat(op_token.type)
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=self.membership_expression())
        return node

    def membership_expression(self):
        node = self.arith_expression()
        # Handle 'in' and 'not in'
        # 'not in' is parsed as: not (expr in expr) due to not_expression precedence
        if self.current_token.type == TOKEN_MEM_IN:
            op_token = self.eat(TOKEN_MEM_IN)
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=self.arith_expression())
        return node

    def arith_expression(self):
        node = self.term()
        while self.current_token.type in (TOKEN_PLUS, TOKEN_MINUS):
            op_token = self.current_token
            self.eat(op_token.type)
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (TOKEN_MULTIPLY, TOKEN_DIVIDE, TOKEN_INT_DIVIDE, TOKEN_MODULO):
            op_token = self.current_token
            self.eat(op_token.type)
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == TOKEN_PLUS:
            op_token = self.eat(TOKEN_PLUS)
            return UnaryOpNode(op_token, self.factor())
        elif token.type == TOKEN_MINUS:
            op_token = self.eat(TOKEN_MINUS)
            return UnaryOpNode(op_token, self.factor())
        return self.power()

    def power(self):
        node = self.call() 
        while self.current_token.type == TOKEN_POWER:
            op_token = self.eat(TOKEN_POWER)
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=self.factor())
        return node

    def call(self):
        node = self.atom()
        while self.current_token.type == TOKEN_LPAREN:
            if not isinstance(node, (IdentifierNode, VariableAccessNode)): # Check if atom is callable
                 self.error(message=f"'{node}' is not callable.")

            self.eat(TOKEN_LPAREN)
            arg_nodes = []
            if self.current_token.type != TOKEN_RPAREN:
                arg_nodes.append(self.expression())
                while self.current_token.type == TOKEN_COMMA:
                    self.eat(TOKEN_COMMA)
                    arg_nodes.append(self.expression())
            self.eat(TOKEN_RPAREN)
            
            func_name_node_for_call = node
            if isinstance(node, VariableAccessNode): # Convert VarAccess to Identifier for func name
                func_name_node_for_call = IdentifierNode(node.var_name_token)
            
            node = FunctionCallNode(func_name_node_for_call, arg_nodes)
        return node

    def atom(self):
        token = self.current_token

        if token.type == TOKEN_INTEGER:
            self.eat(TOKEN_INTEGER)
            # ---- DEBUG PRINT ----
            # print(f"DEBUG (atom - INTEGER): Ate {token}, current_token is now {self.current_token}")
            # ---- END DEBUG PRINT ----
            return NumberNode(token)
        elif token.type == TOKEN_FLOAT:
            self.eat(TOKEN_FLOAT)
            # print(f"DEBUG (atom - FLOAT): Ate {token}, current_token is now {self.current_token}")
            return NumberNode(token)
        elif token.type == TOKEN_STRING:
            self.eat(TOKEN_STRING)
            return StringNode(token)
        elif token.type == TOKEN_IDENTIFIER:
            self.eat(TOKEN_IDENTIFIER)
            return VariableAccessNode(token)
        elif token.type == TOKEN_KEYWORD:
            keyword_val = token.value
            if keyword_val == 'Truth':
                self.eat(TOKEN_KEYWORD)
                return TruthNode(token)
            elif keyword_val == 'Falsity':
                self.eat(TOKEN_KEYWORD)
                return FalsityNode(token)
            elif keyword_val == 'Empty':
                self.eat(TOKEN_KEYWORD)
                return EmptyNode(token)
            elif keyword_val in ('display', 'ask'):
                self.eat(TOKEN_KEYWORD)
                return IdentifierNode(token)
            else:
                self.error(message=f"Unexpected keyword '{keyword_val}' as an atom.")
        elif token.type == TOKEN_LPAREN:
            self.eat(TOKEN_LPAREN)
            node = self.expression()
            self.eat(TOKEN_RPAREN)
            return node
        
        self.error(message=f"Unexpected token in atom(): {token}")
        return NoOpNode() 

    def parse(self):
        # print("Starting parse...") # Debug
        # for t in self.tokens: print(t) # Debug: Print all tokens parser received
        if not self.tokens or (len(self.tokens) == 1 and self.tokens[0].type == TOKEN_EOF):
            # print("Parser: Empty or EOF-only tokens, returning empty ProgramNode.") # Debug
            return ProgramNode()
            
        ast = self.program()
        # print(f"Parse complete. Final current_token: {self.current_token}") # Debug
        if self.current_token and self.current_token.type != TOKEN_EOF:
            self.error(TOKEN_EOF, f"Expected EOF but found {self.current_token.type} ('{self.current_token.value}') after parsing.")
        return ast

