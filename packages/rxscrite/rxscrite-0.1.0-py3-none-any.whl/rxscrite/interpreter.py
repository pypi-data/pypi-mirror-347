# rxscrite/interpreter.py

from .nodes import (
    NumberNode, UnaryOpNode, BinaryOpNode, VariableAssignNode,
    VariableAccessNode, FunctionCallNode, ProgramNode, IdentifierNode,
    StringNode, TruthNode, FalsityNode, EmptyNode, NoOpNode,
    CompoundAssignNode # Make sure this is imported
)
from .tokens import (
    TOKEN_PLUS, TOKEN_MINUS, TOKEN_MULTIPLY, TOKEN_DIVIDE, TOKEN_POWER,
    TOKEN_MODULO, TOKEN_INT_DIVIDE, # New arithmetic
    # Comparison tokens
    TOKEN_EE, TOKEN_NE, TOKEN_LT, TOKEN_GT, TOKEN_LTE, TOKEN_GTE,
    # Logical tokens
    TOKEN_LOGICAL_AND, TOKEN_LOGICAL_OR, TOKEN_LOGICAL_NOT,
    # Membership token (though full 'in' might need list support later)
    TOKEN_MEM_IN,
    # Compound assignment ops (used by CompoundAssignNode, op_token.type will be these)
    TOKEN_PLUS_ASSIGN, TOKEN_MINUS_ASSIGN, TOKEN_MUL_ASSIGN, TOKEN_DIV_ASSIGN,
    TOKEN_MOD_ASSIGN, TOKEN_POW_ASSIGN, TOKEN_INT_DIV_ASSIGN
)
from .errors import RxRuntimeError, RxNameError, RxTypeError, RxZeroDivisionError

class Interpreter:
    def __init__(self, filename="<stdin>"):
        self.filename = filename
        self.symbol_table = {} 
        self._setup_builtins()
        self.current_node_line = None # For error reporting context

    def _setup_builtins(self):
        self.symbol_table['display'] = BuiltInFunction('display', self._builtin_display)
        self.symbol_table['ask'] = BuiltInFunction('ask', self._builtin_ask)
        
        # These are Python values that TruthNode, FalsityNode, EmptyNode will produce.
        # They are not strictly needed in symbol_table if keywords always parse to specific nodes.
        self.symbol_table['Truth'] = True 
        self.symbol_table['Falsity'] = False
        self.symbol_table['Empty'] = None

    def _builtin_display(self, *args):
        output = " ".join(map(self._rx_str, args))
        print(output)
        return None 

    def _builtin_ask(self, *prompt_args):
        prompt_message = " ".join(map(self._rx_str, prompt_args)) if prompt_args else ""
        try:
            return input(prompt_message)
        except EOFError:
            return None # Represent EOF as Empty in RxScrite

    def _rx_str(self, value):
        if value is True: return "Truth"
        if value is False: return "Falsity"
        if value is None: return "Empty"
        return str(value)

    def visit(self, node):
        if node is None: # Should not happen with a proper AST, but safeguard
            return None
            
        if hasattr(node, 'line') and node.line is not None:
            self.current_node_line = node.line

        method_name = f'visit_{type(node).__name__}'
        visitor_method = getattr(self, method_name, self.generic_visit)
        # print(f"Visiting: {type(node).__name__} with {method_name} at line {self.current_node_line}") # Debug
        return visitor_method(node)

    def generic_visit(self, node):
        raise RxRuntimeError(f"No visit_{type(node).__name__} method defined", line=node.line, column=node.column)

    def visit_ProgramNode(self, node):
        result = None
        for statement_node in node.statements:
            result = self.visit(statement_node)
        return result # Value of last statement (mostly for REPL, scripts usually rely on display)

    def visit_NoOpNode(self, node):
        return None # No operation does nothing and returns nothing

    # --- Literal and Identifier Nodes ---
    def visit_NumberNode(self, node): return node.value
    def visit_StringNode(self, node): return node.value
    def visit_TruthNode(self, node): return True
    def visit_FalsityNode(self, node): return False
    def visit_EmptyNode(self, node): return None

    def visit_IdentifierNode(self, node): # Used for function names primarily now
        identifier_name = node.value
        if identifier_name in self.symbol_table:
            return self.symbol_table[identifier_name]
        raise RxNameError(f"Name '{identifier_name}' (from IdentifierNode) is not defined", line=node.line, column=node.column)

    def visit_VariableAccessNode(self, node):
        var_name = node.var_name_token.value
        if var_name in self.symbol_table:
            return self.symbol_table[var_name]
        raise RxNameError(f"Name '{var_name}' is not defined", line=node.line, column=node.column)

    # --- Assignment Nodes ---
    def visit_VariableAssignNode(self, node):
        var_name = node.var_name_token.value
        value = self.visit(node.value_node)
        self.symbol_table[var_name] = value
        return value # Assignment can be an expression in some languages

    def visit_CompoundAssignNode(self, node):
        var_name = node.var_name_token.value
        
        # Get current value of the variable
        if var_name not in self.symbol_table:
            raise RxNameError(f"Name '{var_name}' is not defined for compound assignment", line=node.var_name_token.line, column=node.var_name_token.column)
        current_value = self.symbol_table[var_name]
        
        # Get the value to apply from the right-hand side
        value_to_apply = self.visit(node.value_node)

        # Determine the base operation from the compound assignment token
        op_type = None
        if node.op_token.type == TOKEN_PLUS_ASSIGN: op_type = TOKEN_PLUS
        elif node.op_token.type == TOKEN_MINUS_ASSIGN: op_type = TOKEN_MINUS
        elif node.op_token.type == TOKEN_MUL_ASSIGN: op_type = TOKEN_MULTIPLY
        elif node.op_token.type == TOKEN_DIV_ASSIGN: op_type = TOKEN_DIVIDE
        elif node.op_token.type == TOKEN_MOD_ASSIGN: op_type = TOKEN_MODULO
        elif node.op_token.type == TOKEN_POW_ASSIGN: op_type = TOKEN_POWER
        elif node.op_token.type == TOKEN_INT_DIV_ASSIGN: op_type = TOKEN_INT_DIVIDE
        else:
            raise RxRuntimeError(f"Unknown compound assignment operator: {node.op_token.type}", line=node.op_token.line, column=node.op_token.column)

        # Perform the operation (reusing BinaryOpNode logic conceptually)
        # We need to handle types carefully here, similar to visit_BinaryOpNode
        if op_type == TOKEN_PLUS:
            if isinstance(current_value, (int, float)) and isinstance(value_to_apply, (int, float)):
                new_value = current_value + value_to_apply
            elif isinstance(current_value, str) or isinstance(value_to_apply, str): # String concatenation
                new_value = self._rx_str(current_value) + self._rx_str(value_to_apply)
            else:
                raise RxTypeError(f"Unsupported operand types for +: '{type(current_value).__name__}' and '{type(value_to_apply).__name__}'", line=node.op_token.line)
        elif isinstance(current_value, (int, float)) and isinstance(value_to_apply, (int, float)):
            if op_type == TOKEN_MINUS: new_value = current_value - value_to_apply
            elif op_type == TOKEN_MULTIPLY: new_value = current_value * value_to_apply
            elif op_type == TOKEN_DIVIDE:
                if value_to_apply == 0: raise RxZeroDivisionError("Division by zero", line=node.op_token.line)
                new_value = current_value / value_to_apply
            elif op_type == TOKEN_MODULO:
                if value_to_apply == 0: raise RxZeroDivisionError("Modulo by zero", line=node.op_token.line)
                new_value = current_value % value_to_apply
            elif op_type == TOKEN_POWER: new_value = current_value ** value_to_apply
            elif op_type == TOKEN_INT_DIVIDE:
                if value_to_apply == 0: raise RxZeroDivisionError("Integer division by zero", line=node.op_token.line)
                new_value = current_value // value_to_apply
            else: # Should not happen due to earlier check
                raise RxRuntimeError(f"Unhandled numeric operation for compound assignment: {op_type}", line=node.op_token.line)
        else:
            raise RxTypeError(f"Compound assignment operator '{node.op_token.value}' not supported for types '{type(current_value).__name__}' and '{type(value_to_apply).__name__}'", line=node.op_token.line)

        self.symbol_table[var_name] = new_value
        return new_value

    # --- Operator Nodes ---
    def visit_UnaryOpNode(self, node):
        operand_value = self.visit(node.node)

        if node.op_token.type == TOKEN_MINUS:
            if not isinstance(operand_value, (int, float)):
                raise RxTypeError(f"Unary '-' not supported for type {type(operand_value).__name__}", line=node.line)
            return -operand_value
        elif node.op_token.type == TOKEN_PLUS: # Unary plus
            if not isinstance(operand_value, (int, float)):
                raise RxTypeError(f"Unary '+' not supported for type {type(operand_value).__name__}", line=node.line)
            return +operand_value
        elif node.op_token.type == TOKEN_LOGICAL_NOT: # 'not' operator
            # In Python, 'not' works on any value (truthy/falsy).
            # We'll mimic this: 0, 0.0, "", Empty, Falsity are falsy. Others are truthy.
            if operand_value is False or operand_value is None or operand_value == 0 or operand_value == "":
                return True # not Falsy -> Truth
            else:
                return False # not Truthy -> Falsity
        
        raise RxRuntimeError(f"Unknown unary operator: {node.op_token.type}", line=node.line)

    def visit_BinaryOpNode(self, node):
        left_val = self.visit(node.left_node)
        
        # Short-circuiting for 'and' and 'or'
        if node.op_token.type == TOKEN_LOGICAL_AND:
            # If left_val is falsy, result is left_val, don't eval right_val
            is_left_falsy = left_val is False or left_val is None or left_val == 0 or left_val == ""
            if is_left_falsy:
                return left_val # Python's 'and' returns the first falsy value or the last value
            else:
                return self.visit(node.right_node) # Return result of right side

        if node.op_token.type == TOKEN_LOGICAL_OR:
            # If left_val is truthy, result is left_val, don't eval right_val
            is_left_truthy = not (left_val is False or left_val is None or left_val == 0 or left_val == "")
            if is_left_truthy:
                return left_val # Python's 'or' returns the first truthy value or the last value
            else:
                return self.visit(node.right_node) # Return result of right side

        # For other binary ops, evaluate right operand
        right_val = self.visit(node.right_node)
        op_type = node.op_token.type

        # Arithmetic and String Concatenation
        if op_type == TOKEN_PLUS:
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val + right_val
            elif isinstance(left_val, str) or isinstance(right_val, str): # String concatenation
                return self._rx_str(left_val) + self._rx_str(right_val)
            else:
                raise RxTypeError(f"Unsupported operand types for +: '{type(left_val).__name__}' and '{type(right_val).__name__}'", line=node.op_token.line)

        # Numeric Arithmetic Operations (excluding + which is handled above)
        if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
            if op_type == TOKEN_MINUS: return left_val - right_val
            elif op_type == TOKEN_MULTIPLY: return left_val * right_val
            elif op_type == TOKEN_DIVIDE:
                if right_val == 0: raise RxZeroDivisionError("Division by zero", line=node.op_token.line)
                return left_val / right_val
            elif op_type == TOKEN_POWER: return left_val ** right_val
            elif op_type == TOKEN_MODULO:
                if right_val == 0: raise RxZeroDivisionError("Modulo by zero", line=node.op_token.line)
                return left_val % right_val
            elif op_type == TOKEN_INT_DIVIDE:
                if right_val == 0: raise RxZeroDivisionError("Integer division by zero", line=node.op_token.line)
                return left_val // right_val
        
        # Comparison Operations (can work on various types, like Python)
        if op_type == TOKEN_EE: return left_val == right_val # Python's == handles type flexibility
        elif op_type == TOKEN_NE: return left_val != right_val # Python's !=
        # For <, <=, >, >=, Python raises TypeError if types are incompatible and not ordered.
        # We'll rely on Python's comparison behavior here.
        try:
            if op_type == TOKEN_LT: return left_val < right_val
            elif op_type == TOKEN_LTE: return left_val <= right_val
            elif op_type == TOKEN_GT: return left_val > right_val
            elif op_type == TOKEN_GTE: return left_val >= right_val
        except TypeError:
             raise RxTypeError(f"Comparison '{node.op_token.value}' not supported between instances of '{type(left_val).__name__}' and '{type(right_val).__name__}'", line=node.op_token.line)

        # Membership 'in' (rudimentary for now, assumes right_val is a string if left_val is char/string)
        # Full 'in' needs iterable support for lists, etc.
        if op_type == TOKEN_MEM_IN:
            if isinstance(right_val, str) and isinstance(left_val, str):
                return left_val in right_val
            # Add more sophisticated 'in' for lists/tuples/dicts when they are implemented
            raise RxTypeError(f"'in' operator not fully supported for types '{type(left_val).__name__}' and '{type(right_val).__name__}' yet.", line=node.op_token.line)

        # If we fall through, it's an unhandled binary op for the given types
        raise RxTypeError(f"Unsupported operand types for binary operator '{node.op_token.value}': '{type(left_val).__name__}' and '{type(right_val).__name__}'", line=node.op_token.line)


    def visit_FunctionCallNode(self, node):
        callable_obj = self.visit(node.func_name_node)

        if not isinstance(callable_obj, BuiltInFunction): # Later: add UserDefinedFunction
            func_name_str = node.func_name_node.value if hasattr(node.func_name_node, 'value') else 'unknown function'
            raise RxTypeError(f"'{func_name_str}' ({type(callable_obj).__name__}) is not a function", line=node.line)

        args = [self.visit(arg_node) for arg_node in node.arg_nodes]
        
        original_line = self.current_node_line
        if hasattr(node, 'line') and node.line is not None:
            self.current_node_line = node.line
        try:
            return callable_obj.execute(args, self)
        except RxError: raise
        except Exception as e:
            raise RxRuntimeError(f"Error during built-in function '{callable_obj.name}': {e}", line=self.current_node_line)
        finally:
            self.current_node_line = original_line

class BuiltInFunction:
    def __init__(self, name, python_callable=None):
        self.name = name
        self.python_callable = python_callable

    def execute(self, args, interpreter_instance): # interpreter_instance can be used for context
        if self.python_callable:
            try:
                return self.python_callable(*args)
            except TypeError as e: # Catch arity errors or other Python TypeErrors from the builtin
                # Try to provide a more RxScrite-like error message
                raise RxTypeError(f"Error calling built-in '{self.name}': {e}", line=interpreter_instance.current_node_line)
        else:
            raise NotImplementedError(f"Built-in function '{self.name}' is not implemented.")

    def __repr__(self):
        return f"<BuiltInFunction:{self.name}>"
