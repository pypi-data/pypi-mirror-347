# rxscrite/errors.py

class RxError(Exception):
    """Base class for all RxScrite errors."""
    def __init__(self, message, line=None, column=None, details=""):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.details = details # For more context if needed

    def __str__(self):
        loc = ""
        if self.line is not None:
            loc = f" (Line {self.line}"
            if self.column is not None:
                loc += f", Column {self.column}"
            loc += ")"
        return f"{self.__class__.__name__}{loc}: {self.message}" + (f"\nDetails: {self.details}" if self.details else "")

class RxLexerError(RxError):
    """Error during lexical analysis."""
    pass

class RxParserError(RxError):
    """Error during parsing (syntax error)."""
    pass

class RxSemanticError(RxError):
    """Error during semantic analysis (e.g., type mismatch, undefined variable)."""
    pass # We'll use this more when the interpreter/checker is more advanced

class RxRuntimeError(RxError):
    """Error during program execution (interpreter)."""
    pass

# Specific runtime errors (can be expanded from our plan like ValueProblem, TypeProblem)
class RxNameError(RxRuntimeError):
    """Raised when a name (variable, function) is not found."""
    pass

class RxTypeError(RxRuntimeError):
    """Raised when an operation or function is applied to an object of inappropriate type."""
    pass

class RxZeroDivisionError(RxRuntimeError):
    """Raised when division or modulo by zero takes place for integers or floats."""
    pass

# Example of a more specific planned error
class RxValueProblem(RxRuntimeError): # Corresponds to Python's ValueError
    """Raised when a built-in operation or function receives an argument that has the
    right type but an inappropriate value."""
    pass

# You can add more specific error types here as needed, for example:
# class RxImportProblem(RxRuntimeError): pass
# class RxIndexProblem(RxRuntimeError): pass