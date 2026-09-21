"""
Tools module for Day 1 Assessment.
Contains:
1. Private institutional data (COURSE_FEES).
2. Safe Python tool implementations (get_course_fee, calculator).
3. JSON schema tool definitions for Groq/OpenAI tool calling.
"""

import ast
import operator

# ==============================================================================
# PRIVATE DATA (Institutional Course Fees)
# This dictionary represents confidential institutional data that is NOT part
# of any public LLM training set.
# ==============================================================================
COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}


# ==============================================================================
# TOOL 1: get_course_fee
# ==============================================================================
def get_course_fee(course_code: str) -> str:
    """
    Retrieves the fee for a given course code from private institutional data.
    
    Args:
        course_code: The course code (e.g., 'CS101', 'AI202', 'DS303').
        
    Returns:
        The fee as a formatted string or integer, or an error message if not found.
    """
    if not isinstance(course_code, str):
        return f"Error: Invalid course code format: {course_code}"
    
    clean_code = course_code.strip().upper()
    if clean_code in COURSE_FEES:
        return str(COURSE_FEES[clean_code])
    else:
        available_courses = ", ".join(COURSE_FEES.keys())
        return f"Error: Course '{clean_code}' not found. Available courses: {available_courses}"


# ==============================================================================
# TOOL 2: calculator (SAFE AST EVALUATION - NO EVAL())
# ==============================================================================
# Supported binary operators mapped to safe Python operator functions
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_ast_node(node):
    """
    Recursively and safely evaluates an AST node containing only basic arithmetic.
    Strictly forbids function calls, variable lookups, imports, or arbitrary code.
    """
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body)
    
    # Python 3.8+ numeric constant
    elif isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
        
    # Python < 3.8 compatibility
    elif hasattr(ast, 'Num') and isinstance(node, ast.Num):
        return node.n
        
    # Binary operations (e.g., a + b, a * b)
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left_val = _eval_ast_node(node.left)
        right_val = _eval_ast_node(node.right)
        
        # Guard against division by zero
        if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right_val == 0:
            raise ZeroDivisionError("Division by zero in arithmetic expression.")
            
        return SAFE_OPERATORS[op_type](left_val, right_val)
        
    # Unary operations (e.g., -a, +a)
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand_val = _eval_ast_node(node.operand)
        return SAFE_OPERATORS[op_type](operand_val)
        
    else:
        raise ValueError(f"Disallowed expression element: {type(node).__name__}")


def calculator(expression: str) -> str:
    """
    Safely evaluates an arithmetic expression string using AST parsing.
    Strictly prohibits eval() to guarantee zero risk of arbitrary code execution.
    
    Args:
        expression: A mathematical expression string, e.g. '(12000 + 18000) * 0.9'.
        
    Returns:
        The evaluated numeric result as a string, or a clear error message.
    """
    if not isinstance(expression, str):
        return "Error: Expression must be a string."
        
    # Clean expression: remove commas and common currency symbols if model passed them
    cleaned_expr = expression.replace(",", "").replace("Rs.", "").replace("Rs", "").replace("₹", "").strip()
    
    try:
        parsed_tree = ast.parse(cleaned_expr, mode='eval')
        result = _eval_ast_node(parsed_tree)
        # Format as integer if whole number, else float
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except (SyntaxError, ValueError, ZeroDivisionError) as err:
        return f"Calculation Error: {err}"
    except Exception as err:
        return f"Calculation Error: Unable to evaluate '{expression}' ({err})"


# ==============================================================================
# TOOL REGISTRY & DISPATCHER
# ==============================================================================
TOOL_FUNCTIONS = {
    "get_course_fee": get_course_fee,
    "calculator": calculator,
}


def execute_tool(tool_name: str, arguments: dict) -> str:
    """
    Dispatches tool execution by name with validated dictionary arguments.
    """
    if tool_name not in TOOL_FUNCTIONS:
        return f"Error: Unknown tool '{tool_name}'."
    
    func = TOOL_FUNCTIONS[tool_name]
    try:
        return func(**arguments)
    except TypeError as err:
        return f"Error invoking tool '{tool_name}' with args {arguments}: {err}"


# ==============================================================================
# TOOL SCHEMAS FOR GROQ / OPENAI FUNCTION CALLING
# ==============================================================================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Look up the official private fee for a course code (e.g. 'CS101', 'AI202', 'DS303') from the private college fee database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "The exact course code to look up, e.g., 'CS101', 'AI202', or 'DS303'."
                    }
                },
                "required": ["course_code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Safely calculate the result of an arithmetic expression (e.g. addition, subtraction, multiplication, division, discount/scholarship percentages).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression string to compute, e.g. '(12000 + 18000) * 0.9' or '15000 - 12000'."
                    }
                },
                "required": ["expression"],
            },
        },
    },
]
