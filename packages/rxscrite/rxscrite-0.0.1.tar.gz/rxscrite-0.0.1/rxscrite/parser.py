# rxscrite/parser.py

from .tokens import (
    TOKEN_INTEGER, TOKEN_FLOAT, TOKEN_PLUS, TOKEN_MINUS, TOKEN_MULTIPLY,
    TOKEN_DIVIDE, TOKEN_POWER, TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_EOF,
    TOKEN_IDENTIFIER, TOKEN_KEYWORD, TOKEN_ASSIGN, TOKEN_COMMA, TOKEN_NEWLINE,
    TOKEN_STRING
)
from .nodes import (
    NumberNode, BinaryOpNode, UnaryOpNode, VariableAssignNode,
    VariableAccessNode, FunctionCallNode, ProgramNode, IdentifierNode,
    StringNode, TruthNode, FalsityNode, EmptyNode
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
            self.current_token = self.tokens[-1] if self.tokens and self.tokens[-1].type == TOKEN_EOF else None
        return self.current_token

    def peek(self):
        if self.token_idx + 1 < len(self.tokens):
            return self.tokens[self.token_idx + 1]
        return None

    def error(self, expected_token_type=None, message=""):
        if not message:
            if expected_token_type and self.current_token:
                message = f"Expected {expected_token_type}, but got {self.current_token.type}"
            elif self.current_token:
                message = f"Unexpected token: {self.current_token}"
            else:
                message = "Unexpected end of file."
        
        line = self.current_token.line if self.current_token else (self.tokens[-1].line if self.tokens else None)
        column = self.current_token.column if self.current_token else (self.tokens[-1].column if self.tokens else None)
        raise RxParserError(message, line=line, column=column)

    def eat(self, token_type, token_value=None):
        if self.current_token is None:
            self.error(expected_token_type, f"Unexpected EOF. Expected {token_type}")
        
        if self.current_token.type == token_type:
            if token_value is not None and self.current_token.value != token_value:
                self.error(expected_token_type, f"Expected token value '{token_value}' but got '{self.current_token.value}'")
            eaten_token = self.current_token
            self.advance()
            return eaten_token
        else:
            self.error(expected_token_type)

    def program(self):
        prog_node = ProgramNode()
        while self.current_token and self.current_token.type == TOKEN_NEWLINE:
            self.eat(TOKEN_NEWLINE)

        while self.current_token and self.current_token.type != TOKEN_EOF:
            if self.current_token.type == TOKEN_NEWLINE:
                self.eat(TOKEN_NEWLINE)
                continue
            
            stmt = self.statement()
            if stmt:
                prog_node.statements.append(stmt)

            if self.current_token.type != TOKEN_EOF:
                if self.current_token.type == TOKEN_NEWLINE:
                    while self.current_token and self.current_token.type == TOKEN_NEWLINE:
                        self.eat(TOKEN_NEWLINE)
                else:
                    self.error(TOKEN_NEWLINE, "Expected newline or EOF after statement.")
            
            while self.current_token and self.current_token.type == TOKEN_NEWLINE:
                self.eat(TOKEN_NEWLINE)
        return prog_node

    def statement(self):
        if self.current_token.type == TOKEN_IDENTIFIER and self.peek() and self.peek().type == TOKEN_ASSIGN:
            return self.assignment_statement()
        else:
            return self.expression()

    def assignment_statement(self):
        var_name_token = self.eat(TOKEN_IDENTIFIER)
        self.eat(TOKEN_ASSIGN)
        value_node = self.expression()
        return VariableAssignNode(var_name_token, value_node)

    def atom(self):
        token = self.current_token

        if token.type == TOKEN_INTEGER:
            self.eat(TOKEN_INTEGER)
            return NumberNode(token)
        elif token.type == TOKEN_FLOAT:
            self.eat(TOKEN_FLOAT)
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
            elif keyword_val == 'display' or keyword_val == 'ask': # Added 'ask'
                self.eat(TOKEN_KEYWORD)
                return IdentifierNode(token) 
            else:
                self.error(message=f"Unexpected keyword '{keyword_val}' as an atom in an expression.")
        elif token.type == TOKEN_LPAREN:
            self.eat(TOKEN_LPAREN)
            node = self.expression()
            self.eat(TOKEN_RPAREN)
            return node
        
        self.error(message=f"Unexpected token in atom(): {token}")

    def call(self):
        node = self.atom()
        while self.current_token and self.current_token.type == TOKEN_LPAREN:
            if not isinstance(node, (IdentifierNode, VariableAccessNode)):
                 self.error(message="Expression is not callable.")

            self.eat(TOKEN_LPAREN)
            arg_nodes = []
            if self.current_token.type != TOKEN_RPAREN:
                arg_nodes.append(self.expression())
                while self.current_token.type == TOKEN_COMMA:
                    self.eat(TOKEN_COMMA)
                    arg_nodes.append(self.expression())
            self.eat(TOKEN_RPAREN)
            
            if isinstance(node, VariableAccessNode):
                func_name_node_for_call = IdentifierNode(node.var_name_token)
            elif isinstance(node, IdentifierNode):
                func_name_node_for_call = node
            else: 
                self.error(message="Internal parser error: Unexpected node type for function call.")
            node = FunctionCallNode(func_name_node_for_call, arg_nodes)
        return node

    def power(self):
        node = self.call()
        while self.current_token and self.current_token.type == TOKEN_POWER:
            op_token = self.eat(TOKEN_POWER)
            right_node = self.factor() 
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=right_node)
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

    def term(self):
        node = self.factor()
        while self.current_token and self.current_token.type in (TOKEN_MULTIPLY, TOKEN_DIVIDE):
            op_token = self.current_token
            if op_token.type == TOKEN_MULTIPLY:
                self.eat(TOKEN_MULTIPLY)
            elif op_token.type == TOKEN_DIVIDE:
                self.eat(TOKEN_DIVIDE)
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=self.factor())
        return node

    def arith_expression(self):
        node = self.term()
        while self.current_token and self.current_token.type in (TOKEN_PLUS, TOKEN_MINUS):
            op_token = self.current_token
            if op_token.type == TOKEN_PLUS:
                self.eat(TOKEN_PLUS)
            elif op_token.type == TOKEN_MINUS:
                self.eat(TOKEN_MINUS)
            node = BinaryOpNode(left_node=node, op_token=op_token, right_node=self.term())
        return node
        
    def comp_expression(self):
        return self.arith_expression()

    def expression(self):
        return self.comp_expression()

    def parse(self):
        if not self.tokens or (len(self.tokens) == 1 and self.tokens[0].type == TOKEN_EOF):
            return ProgramNode()
        ast = self.program()
        if self.current_token and self.current_token.type != TOKEN_EOF:
            self.error(TOKEN_EOF, f"Expected EOF but found {self.current_token.type}")
        return ast