"""
This module analyzes the time complexity of Python code.
"""

import ast
import re

def analyze_loops(node):
    """
    Analyzes the loops in an AST node to estimate time complexity.
    
    Args:
        node (ast.AST): The AST node to analyze.
        
    Returns:
        str: A string representing the estimated time complexity.
    """
    loop_complexities = []
    max_depth = [1]  # Using a list to allow modification from inner function
    
    # Function to visit all nodes in the AST
    def visit_node(node, depth=1):
        if isinstance(node, ast.For) or isinstance(node, ast.While):
            # Update max depth if this is deeper than what we've seen
            if depth > max_depth[0]:
                max_depth[0] = depth
            
            # Check for nested loops
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth + 1)
            
            # Add complexity for this loop
            if is_logarithmic_pattern(node):
                loop_complexities.append("O(log n)")
            else:
                loop_complexities.append("O(n)")
        else:
            # Continue traversing non-loop nodes without increasing depth
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth)
                    
        # Visit all child nodes if not already visited as part of a loop
        if not isinstance(node, (ast.For, ast.While)):
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth)
    
    # Start traversing from the root node
    visit_node(node)
    
    # Determine final complexity
    if not loop_complexities:
        return "O(1)"  # No loops found
    
    # If we have nested loops, return O(n^depth)
    if max_depth[0] > 1:
        return f"O(n^{max_depth[0]})"
    
    # If we have logarithmic patterns, prioritize them
    if "O(log n)" in loop_complexities:
        return "O(log n)"
    
    # Otherwise return linear complexity
    return "O(n)"


def is_logarithmic_pattern(node):
    """
    Checks if a loop follows a logarithmic pattern (like divide-and-conquer).
    
    Args:
        node (ast.AST): The AST node to analyze.
        
    Returns:
        bool: True if the loop appears to have logarithmic complexity.
    """
    # Look for patterns like "i = i * 2" or "i = i // 2" that indicate logarithmic behavior
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Assign):
            if isinstance(child.value, ast.BinOp):
                if isinstance(child.value.op, (ast.Mult, ast.FloorDiv, ast.Div)):
                    # In Python 3.8+, ast.Num is deprecated in favor of ast.Constant
                    if (isinstance(child.value.right, ast.Constant) and child.value.right.value == 2) or \
                       (hasattr(ast, 'Num') and isinstance(child.value.right, ast.Num) and child.value.right.n == 2):
                        return True
    return False


def analyze_recursion(code_str):
    """
    Analyzes the recursive calls in the provided code string to estimate time complexity.
    
    Args:
        code_str (str): The Python code as a string.
        
    Returns:
        str: A string representing the estimated time complexity.
    """
    tree = ast.parse(code_str)
    recursive_functions = {}
    
    # Find all function definitions
    function_defs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    for func_def in function_defs:
        func_name = func_def.name
        calls_itself = False
        
        # Check if the function calls itself
        for node in ast.walk(func_def):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == func_name:
                    calls_itself = True
                    break
        
        if calls_itself:
            # Check for common recursive patterns
            if is_divide_and_conquer(func_def):
                recursive_functions[func_name] = "O(log n)"
            elif is_fibonacci_like(func_def):
                recursive_functions[func_name] = "O(2^n)"
            else:
                recursive_functions[func_name] = "O(n)"
    
    if not recursive_functions:
        return "O(1)"  # No recursion found
    
    # Return the worst case complexity
    complexities = list(recursive_functions.values())
    complexity_rank = {
        "O(1)": 1,
        "O(log n)": 2,
        "O(n)": 3,
        "O(n log n)": 4,
        "O(n^2)": 5,
        "O(2^n)": 6,
    }
    
    worst_complexity = max(complexities, key=lambda x: complexity_rank.get(x, 0))
    return worst_complexity


def is_divide_and_conquer(func_def):
    """
    Checks if a recursive function follows a divide-and-conquer pattern.
    
    Args:
        func_def (ast.FunctionDef): The function definition node.
        
    Returns:
        bool: True if the function appears to use divide-and-conquer.
    """
    # Look for patterns like recursive calls with divided input
    for node in ast.walk(func_def):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == func_def.name:
                for arg in node.args:
                    # Look for patterns like func(n//2) or func(n/2)
                    if isinstance(arg, ast.BinOp) and isinstance(arg.op, (ast.FloorDiv, ast.Div)):
                        if isinstance(arg.right, ast.Num) and arg.right.n == 2:
                            return True
    return False


def is_fibonacci_like(func_def):
    """
    Checks if a recursive function follows a Fibonacci-like pattern (multiple recursive calls).
    
    Args:
        func_def (ast.FunctionDef): The function definition node.
        
    Returns:
        bool: True if the function appears to be Fibonacci-like.
    """
    # Count recursive calls
    recursive_calls = 0
    for node in ast.walk(func_def):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == func_def.name:
                recursive_calls += 1
    
    # If there are multiple recursive calls, it's likely exponential
    return recursive_calls > 1


def estimate_time_complexity(code_str):
    """
    Estimates the time complexity of the provided Python code.
    
    Args:
        code_str (str): The Python code as a string.
        
    Returns:
        str: A string representing the estimated time complexity.
    """
    try:
        tree = ast.parse(code_str)
        
        # Analyze loops
        loop_complexity = analyze_loops(tree)
        
        # Analyze recursion
        recursion_complexity = analyze_recursion(code_str)
        
        # Combine complexities - take the worse of the two
        complexity_rank = {
            "O(1)": 1,
            "O(log n)": 2,
            "O(n)": 3,
            "O(n log n)": 4, 
            "O(n^2)": 5,
            "O(n^3)": 6,
            "O(n^4)": 7,
            "O(2^n)": 8,
            "O(n!)": 9
        }
        
        # Extract exponent from O(n^x) format if not in our map
        loop_rank = complexity_rank.get(loop_complexity, 0)
        recursion_rank = complexity_rank.get(recursion_complexity, 0)
        
        # Handle cases like O(n^k) where k is any number
        if loop_rank == 0 and "O(n^" in loop_complexity:
            try:
                # Extract the exponent value
                exponent = int(loop_complexity.split("^")[1].split(")")[0])
                loop_rank = 4 + exponent  # Position relative to n^2 (which is 5)
            except (ValueError, IndexError):
                loop_rank = 5  # Default to O(n^2) if parsing fails
                
        if recursion_rank == 0 and "O(n^" in recursion_complexity:
            try:
                # Extract the exponent value
                exponent = int(recursion_complexity.split("^")[1].split(")")[0])
                recursion_rank = 4 + exponent  # Position relative to n^2 (which is 5)
            except (ValueError, IndexError):
                recursion_rank = 5  # Default to O(n^2) if parsing fails
                
        if loop_rank >= recursion_rank:
            return loop_complexity
        else:
            return recursion_complexity
            
    except SyntaxError:
        return "Unknown (syntax error)"
    except Exception as e:
        return f"Unknown ({str(e)})"