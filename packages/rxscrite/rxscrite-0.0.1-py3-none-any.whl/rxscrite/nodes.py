# rxscrite/nodes.py

class ASTNode:
    """Base class for all AST nodes."""
    def __init__(self, token=None): # Optional token for position tracking
        self.token = token
        self.line = token.line if token and hasattr(token, 'line') else None
        self.column = token.column if token and hasattr(token, 'column') else None

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

# For expressions
class NumberNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.value = token.value # The actual number (int or float)

    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode(ASTNode): # We'll use this later
    def __init__(self, token):
        super().__init__(token)
        self.value = token.value

    def __repr__(self):
        return f"StringNode({repr(self.value)})"

class IdentifierNode(ASTNode): # For variable names, function names
    def __init__(self, token):
        super().__init__(token)
        self.value = token.value # The name of the identifier

    def __repr__(self):
        return f"IdentifierNode({self.value})"

class UnaryOpNode(ASTNode):
    def __init__(self, op_token, node):
        super().__init__(op_token) # op_token is like TOKEN_MINUS for negation
        self.op_token = op_token
        self.node = node # The node to operate on (e.g., NumberNode)

    def __repr__(self):
        return f"UnaryOpNode({self.op_token}, {self.node})"

class BinaryOpNode(ASTNode):
    def __init__(self, left_node, op_token, right_node):
        super().__init__(op_token)
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f"BinaryOpNode({self.left_node}, {self.op_token}, {self.right_node})"

class VariableAssignNode(ASTNode):
    def __init__(self, var_name_token, value_node): # var_name_token is an IDENTIFIER token
        super().__init__(var_name_token)
        self.var_name_token = var_name_token
        self.value_node = value_node # Node representing the value being assigned

    def __repr__(self):
        return f"VariableAssignNode({self.var_name_token.value} = {self.value_node})"

class VariableAccessNode(ASTNode):
    def __init__(self, var_name_token): # var_name_token is an IDENTIFIER token
        super().__init__(var_name_token)
        self.var_name_token = var_name_token

    def __repr__(self):
        return f"VariableAccessNode({self.var_name_token.value})"

class FunctionCallNode(ASTNode):
    def __init__(self, func_name_node, arg_nodes): # func_name_node is often an IdentifierNode
        super().__init__(func_name_node.token if isinstance(func_name_node, ASTNode) else None)
        self.func_name_node = func_name_node
        self.arg_nodes = arg_nodes # List of nodes representing arguments

    def __repr__(self):
        return f"FunctionCallNode({self.func_name_node}, args={self.arg_nodes})"

class ProgramNode(ASTNode):
    """Represents a whole program or a block of statements."""
    def __init__(self):
        super().__init__() # No specific token for the whole program
        self.statements = [] # List of statement nodes

    def __repr__(self):
        return f"ProgramNode(statements_count={len(self.statements)})"

# --- Placeholder Nodes for Future Features ---
class IfNode(ASTNode): # 'check' statement
    def __init__(self, conditions_and_blocks, else_block):
        # conditions_and_blocks is a list of tuples: (condition_node, block_node)
        # else_block is a block_node or None
        # Attempt to get a representative token for line/col info
        rep_token = None
        if conditions_and_blocks and conditions_and_blocks[0] and conditions_and_blocks[0][0]:
             rep_token = conditions_and_blocks[0][0].token # Token from the first condition
        super().__init__(rep_token)
        self.conditions_and_blocks = conditions_and_blocks
        self.else_block = else_block

class ForLoopNode(ASTNode): # 'loop' statement
    def __init__(self, var_name_token, iterable_node, body_node, else_node):
        super().__init__(var_name_token)
        self.var_name_token = var_name_token
        self.iterable_node = iterable_node
        self.body_node = body_node
        self.else_node = else_node # Optional 'otherwise' block

class WhileLoopNode(ASTNode): # 'repeat_while' statement
    def __init__(self, condition_node, body_node, else_node):
        super().__init__(condition_node.token if condition_node else None) # Token from condition
        self.condition_node = condition_node
        self.body_node = body_node
        self.else_node = else_node # Optional 'otherwise' block

class FunctionDefNode(ASTNode): # 'func' statement
    def __init__(self, func_name_token, param_name_tokens, body_node, return_type_token=None):
        super().__init__(func_name_token)
        self.func_name_token = func_name_token
        self.param_name_tokens = param_name_tokens # List of IDENTIFIER tokens
        self.body_node = body_node
        # self.return_type_token = return_type_token # For optional type hinting later

# Boolean / Value Nodes
class TruthNode(ASTNode): # Represents the 'Truth' keyword
    def __init__(self, token):
        super().__init__(token)
        self.value = True
    def __repr__(self):
        return f"TruthNode({self.value})"

class FalsityNode(ASTNode): # Represents the 'Falsity' keyword
    def __init__(self, token):
        super().__init__(token)
        self.value = False
    def __repr__(self):
        return f"FalsityNode({self.value})"

class EmptyNode(ASTNode): # Represents the 'Empty' keyword
    def __init__(self, token):
        super().__init__(token)
        self.value = None # Or a special EmptyType object
    def __repr__(self):
        return f"EmptyNode({self.value})"

# You will add many more node types here as the language grows, e.g.:
# ListNode, DictNode, ReturnNode, ClassDefNode, ImportNode, etc.