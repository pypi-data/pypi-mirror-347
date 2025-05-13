# rxscrite/interpreter.py

from .nodes import (
    NumberNode, UnaryOpNode, BinaryOpNode, VariableAssignNode,
    VariableAccessNode, FunctionCallNode, ProgramNode, IdentifierNode,
    StringNode, TruthNode, FalsityNode, EmptyNode
)
from .tokens import (
    TOKEN_PLUS, TOKEN_MINUS, TOKEN_MULTIPLY, TOKEN_DIVIDE, TOKEN_POWER
)
from .errors import RxRuntimeError, RxNameError, RxTypeError, RxZeroDivisionError

class Interpreter:
    def __init__(self, filename="<stdin>"):
        self.filename = filename
        self.symbol_table = {} 
        self._setup_builtins()
        self.current_node_line = None # For better error reporting in builtins

    def _setup_builtins(self):
        self.symbol_table['display'] = BuiltInFunction('display', self._builtin_display)
        self.symbol_table['ask'] = BuiltInFunction('ask', self._builtin_ask) # Added ask
        
        self.symbol_table['Truth'] = True
        self.symbol_table['Falsity'] = False
        self.symbol_table['Empty'] = None

    def _builtin_display(self, *args):
        output = " ".join(map(self._rx_str, args))
        print(output)
        return None

    def _builtin_ask(self, *prompt_args): # New builtin function
        prompt_message = ""
        if prompt_args:
            # Convert all prompt arguments to their RxScrite string form and join
            prompt_message = " ".join(map(self._rx_str, prompt_args))
        try:
            return input(prompt_message)
        except EOFError: # Handle cases where input stream might be closed (e.g. piping)
            return "Empty" # Or raise an RxScrite specific error

    def _rx_str(self, value):
        if value is True:
            return "Truth"
        if value is False:
            return "Falsity"
        if value is None:
            return "Empty"
        return str(value)

    def visit(self, node):
        # Store line number of current node for potential use in runtime errors from builtins
        if hasattr(node, 'line') and node.line is not None:
            self.current_node_line = node.line

        method_name = f'visit_{type(node).__name__}'
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    def generic_visit(self, node):
        raise RxRuntimeError(f"No visit_{type(node).__name__} method defined", line=node.line, column=node.column)

    def visit_ProgramNode(self, node):
        result = None
        for statement_node in node.statements:
            result = self.visit(statement_node)
        return result

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_TruthNode(self, node):
        return True

    def visit_FalsityNode(self, node):
        return False

    def visit_EmptyNode(self, node):
        return None

    def visit_UnaryOpNode(self, node):
        operand_value = self.visit(node.node)
        if not isinstance(operand_value, (int, float)):
            raise RxTypeError(f"Unary operator '{node.op_token.value}' not supported for type {type(operand_value).__name__}", line=node.line, column=node.column)
        if node.op_token.type == TOKEN_MINUS:
            return -operand_value
        elif node.op_token.type == TOKEN_PLUS:
            return +operand_value
        raise RxRuntimeError(f"Unknown unary operator: {node.op_token.type}", line=node.line, column=node.column)

    def visit_BinaryOpNode(self, node):
        left_val = self.visit(node.left_node)
        right_val = self.visit(node.right_node)

        # Handle string concatenation with '+'
        if node.op_token.type == TOKEN_PLUS:
            if isinstance(left_val, str) or isinstance(right_val, str):
                return self._rx_str(left_val) + self._rx_str(right_val)

        # Arithmetic operations for numbers
        if not (isinstance(left_val, (int, float)) and isinstance(right_val, (int, float))):
            err_msg = (f"Unsupported operand types for {node.op_token.value}: "
                       f"'{type(left_val).__name__}' and '{type(right_val).__name__}'")
            raise RxTypeError(err_msg, line=node.op_token.line, column=node.op_token.column)

        op_type = node.op_token.type
        try:
            if op_type == TOKEN_PLUS: # Should be numbers here due to above string check
                return left_val + right_val
            elif op_type == TOKEN_MINUS:
                return left_val - right_val
            elif op_type == TOKEN_MULTIPLY:
                return left_val * right_val
            elif op_type == TOKEN_DIVIDE:
                if right_val == 0:
                    raise RxZeroDivisionError("Division by zero", line=node.op_token.line, column=node.op_token.column)
                return left_val / right_val
            elif op_type == TOKEN_POWER:
                return left_val ** right_val
        except TypeError: # Should generally be caught by type checks above
            err_msg = (f"Problem with operand types for {node.op_token.value}: "
                       f"'{type(left_val).__name__}' and '{type(right_val).__name__}'")
            raise RxTypeError(err_msg, line=node.op_token.line, column=node.op_token.column)
        
        raise RxRuntimeError(f"Unknown binary operator: {op_type}", line=node.op_token.line, column=node.op_token.column)


    def visit_VariableAssignNode(self, node):
        var_name = node.var_name_token.value
        value = self.visit(node.value_node)
        self.symbol_table[var_name] = value
        return value

    def visit_VariableAccessNode(self, node):
        var_name = node.var_name_token.value
        # Keywords like Truth, Falsity, Empty are not accessed via VariableAccessNode
        # They are parsed into TruthNode, FalsityNode, EmptyNode directly.
        if var_name in self.symbol_table:
            return self.symbol_table[var_name]
        raise RxNameError(f"Name '{var_name}' is not defined", line=node.line, column=node.column)

    def visit_IdentifierNode(self, node):
        identifier_name = node.value
        # This node is used by FunctionCallNode for the function's name.
        # It could be a built-in like 'display' or 'ask', or a user-defined function later.
        # It can also be used by atom() for keywords like Truth, Falsity, Empty if they are directly used
        # in a way that results in an IdentifierNode (though parser now makes specific nodes for them).
        
        # For built-in functions/constants identified by keywords by the parser:
        if identifier_name in self.symbol_table:
            return self.symbol_table[identifier_name] # Returns BuiltInFunction or True/False/None
            
        raise RxNameError(f"Name '{identifier_name}' (from IdentifierNode) is not defined", line=node.line, column=node.column)


    def visit_FunctionCallNode(self, node):
        callable_obj = self.visit(node.func_name_node)

        if not isinstance(callable_obj, BuiltInFunction): # Later: add UserDefinedFunction
            func_name_str = node.func_name_node.value if hasattr(node.func_name_node, 'value') else 'unknown function'
            raise RxTypeError(f"'{func_name_str}' ({type(callable_obj).__name__}) is not a function", line=node.line, column=node.column)

        args = [self.visit(arg_node) for arg_node in node.arg_nodes]
        
        # Store current node's line for potential use in BuiltInFunction error reporting
        original_line = self.current_node_line
        if hasattr(node, 'line') and node.line is not None: # FunctionCallNode itself
            self.current_node_line = node.line

        try:
            return callable_obj.execute(args, self)
        except RxError: # Re-raise RxScrite errors directly
            raise
        except Exception as e: # Wrap other Python exceptions from builtins
            raise RxRuntimeError(f"Error during built-in function '{callable_obj.name}': {e}", line=self.current_node_line)
        finally:
            self.current_node_line = original_line


class BuiltInFunction:
    def __init__(self, name, python_callable=None):
        self.name = name
        self.python_callable = python_callable

    def execute(self, args, interpreter_instance):
        if self.python_callable:
            # The python_callable (e.g., _builtin_ask) will be called.
            # It can raise Python errors or RxErrors.
            return self.python_callable(*args)
        else:
            raise NotImplementedError(f"Built-in function '{self.name}' is not implemented.")

    def __repr__(self):
        return f"<BuiltInFunction:{self.name}>"