# rxscrite/nodes.py

class ASTNode:
    """Base class for all AST nodes."""
    def __init__(self, token=None): # Optional token for position tracking
        self.token = token
        # Safely access line and column, providing None if token or attributes are missing
        self.line = token.line if token and hasattr(token, 'line') else None
        self.column = token.column if token and hasattr(token, 'column') else None

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

# --- Literal and Identifier Nodes ---
class NumberNode(ASTNode):
    """Node representing a numeric literal (integer or float)."""
    def __init__(self, token):
        super().__init__(token)
        self.value = token.value # The actual number (int or float)

    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode(ASTNode):
    """Node representing a string literal."""
    def __init__(self, token):
        super().__init__(token)
        self.value = token.value # The actual string value

    def __repr__(self):
        return f"StringNode({repr(self.value)})"

class IdentifierNode(ASTNode):
    """Node representing an identifier (e.g., variable name, function name)."""
    def __init__(self, token):
        super().__init__(token)
        self.value = token.value # The name of the identifier

    def __repr__(self):
        return f"IdentifierNode({self.value})"

# --- Boolean and Null-equivalent Nodes ---
class TruthNode(ASTNode):
    """Node representing the 'Truth' keyword (boolean True)."""
    def __init__(self, token):
        super().__init__(token)
        self.value = True
    def __repr__(self):
        return f"TruthNode({self.value})"

class FalsityNode(ASTNode):
    """Node representing the 'Falsity' keyword (boolean False)."""
    def __init__(self, token):
        super().__init__(token)
        self.value = False
    def __repr__(self):
        return f"FalsityNode({self.value})"

class EmptyNode(ASTNode):
    """Node representing the 'Empty' keyword (similar to None)."""
    def __init__(self, token):
        super().__init__(token)
        self.value = None # Or a special EmptyType object if needed later
    def __repr__(self):
        return f"EmptyNode({self.value})"

# --- Operator Nodes ---
class UnaryOpNode(ASTNode):
    """Node representing a unary operation (e.g., -5, not True)."""
    def __init__(self, op_token, node):
        super().__init__(op_token) # op_token is like TOKEN_MINUS, TOKEN_LOGICAL_NOT
        self.op_token = op_token
        self.node = node # The node to operate on (e.g., NumberNode, ExpressionNode)

    def __repr__(self):
        return f"UnaryOpNode(op={self.op_token.type}, value={self.node})"

class BinaryOpNode(ASTNode):
    """Node representing a binary operation (e.g., a + b, x == y)."""
    def __init__(self, left_node, op_token, right_node):
        super().__init__(op_token) # op_token is like TOKEN_PLUS, TOKEN_EE
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f"BinaryOpNode(left={self.left_node}, op={self.op_token.type}, right={self.right_node})"

# --- Assignment Nodes ---
class VariableAssignNode(ASTNode):
    """Node representing a simple variable assignment (e.g., x = 10)."""
    def __init__(self, var_name_token, value_node): # var_name_token is an IDENTIFIER token
        super().__init__(var_name_token)
        self.var_name_token = var_name_token
        self.value_node = value_node # Node representing the value being assigned

    def __repr__(self):
        return f"VariableAssignNode(var_name='{self.var_name_token.value}', value={self.value_node})"

class CompoundAssignNode(ASTNode): # New Node
    """Node representing a compound variable assignment (e.g., x += 10)."""
    def __init__(self, var_name_token, op_token, value_node):
        super().__init__(var_name_token) # Position from variable name
        self.var_name_token = var_name_token # IDENTIFIER token for the variable
        self.op_token = op_token # The compound assignment token (e.g., TOKEN_PLUS_ASSIGN)
        self.value_node = value_node # Node representing the value on the right

    def __repr__(self):
        return f"CompoundAssignNode(var_name='{self.var_name_token.value}', op='{self.op_token.value}', value={self.value_node})"

# --- Variable Access and Function Call ---
class VariableAccessNode(ASTNode):
    """Node representing access to a variable's value."""
    def __init__(self, var_name_token): # var_name_token is an IDENTIFIER token
        super().__init__(var_name_token)
        self.var_name_token = var_name_token

    def __repr__(self):
        return f"VariableAccessNode(var_name='{self.var_name_token.value}')"

class FunctionCallNode(ASTNode):
    """Node representing a function call."""
    def __init__(self, func_name_node, arg_nodes): # func_name_node is often an IdentifierNode
        # Try to get a representative token for line/col info, usually from the function name
        rep_token = None
        if isinstance(func_name_node, ASTNode) and func_name_node.token:
            rep_token = func_name_node.token
        super().__init__(rep_token)
        
        self.func_name_node = func_name_node # Node representing the function name (e.g., IdentifierNode)
        self.arg_nodes = arg_nodes # List of nodes representing arguments

    def __repr__(self):
        return f"FunctionCallNode(func_name={self.func_name_node}, args_count={len(self.arg_nodes)})"

# --- Program Structure and Control Flow (Placeholders / Basic) ---
class ProgramNode(ASTNode):
    """Node representing a whole program or a block of statements."""
    def __init__(self):
        super().__init__() # No specific token for the whole program
        self.statements = [] # List of statement nodes

    def __repr__(self):
        return f"ProgramNode(statements_count={len(self.statements)})"

class NoOpNode(ASTNode): # New Node
    """Node representing no operation, useful for empty parts or placeholders."""
    def __init__(self, token=None): # token is optional
        super().__init__(token)
    def __repr__(self):
        return "NoOpNode"

# --- Placeholder Nodes for Future Language Features ---
# These can be expanded upon when we implement these features.

class IfNode(ASTNode): # For 'check' statement
    """Node representing an if-elif-else conditional structure."""
    def __init__(self, conditions_and_blocks, else_block):
        # conditions_and_blocks is a list of tuples: (condition_node, block_node)
        # else_block is a block_node or None
        rep_token = None
        if conditions_and_blocks and conditions_and_blocks[0] and conditions_and_blocks[0][0]:
             if hasattr(conditions_and_blocks[0][0], 'token'):
                 rep_token = conditions_and_blocks[0][0].token
        super().__init__(rep_token)
        self.conditions_and_blocks = conditions_and_blocks
        self.else_block = else_block
    # __repr__ can be added for better debugging views

class ForLoopNode(ASTNode): # For 'loop' statement
    """Node representing a for-loop structure."""
    def __init__(self, var_name_token, iterable_node, body_node, else_node=None):
        super().__init__(var_name_token)
        self.var_name_token = var_name_token
        self.iterable_node = iterable_node
        self.body_node = body_node # This would typically be a ProgramNode (block of statements)
        self.else_node = else_node # Optional 'otherwise' block
    # __repr__ can be added

class WhileLoopNode(ASTNode): # For 'repeat_while' statement
    """Node representing a while-loop structure."""
    def __init__(self, condition_node, body_node, else_node=None):
        rep_token = condition_node.token if condition_node and hasattr(condition_node, 'token') else None
        super().__init__(rep_token)
        self.condition_node = condition_node
        self.body_node = body_node # This would typically be a ProgramNode
        self.else_node = else_node # Optional 'otherwise' block
    # __repr__ can be added

class FunctionDefNode(ASTNode): # For 'func' statement
    """Node representing a user-defined function."""
    def __init__(self, func_name_token, param_name_tokens, body_node, return_type_token=None):
        super().__init__(func_name_token)
        self.func_name_token = func_name_token
        self.param_name_tokens = param_name_tokens # List of IDENTIFIER tokens
        self.body_node = body_node # This would typically be a ProgramNode
        # self.return_type_token = return_type_token # For optional type hinting later
    # __repr__ can be added
