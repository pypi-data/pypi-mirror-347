"""
This module analyzes the space complexity of Python code.
"""

import ast

def analyze_space_complexity(code_str):
    """
    Analyzes the given Python code string to estimate its space complexity.
    
    This function will track memory allocation by analyzing the data structures
    used in the code and their sizes. It will return an estimation of the space
    complexity in Big O notation.
    
    Parameters:
    code_str (str): The Python code as a string to analyze.
    
    Returns:
    str: A string representing the estimated space complexity (e.g., "O(n)", "O(1)").
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(code_str)
        
        # Analyze data structures and memory usage
        space_complexity = find_space_complexity(tree)
        
        return space_complexity
    except SyntaxError:
        return "Unknown (syntax error)"
    except Exception as e:
        return f"Unknown ({str(e)})"


def find_space_complexity(node):
    """
    Recursively analyzes the AST to find space complexity.
    
    Args:
        node (ast.AST): The AST node to analyze.
        
    Returns:
        str: A string representing the estimated space complexity.
    """
    complexities = ["O(1)"]  # Default complexity
    has_loop_without_storage = [False]  # Track if we found loops without storage
    has_n_squared_storage = [False]  # Track if we found O(n²) space usage
    
    # Helper function to visit nodes
    def visit_node(node):
        complexity = "O(1)"  # Default
        
        # Check for variables that are just incrementing or simple calculations in loops
        if isinstance(node, ast.For) or isinstance(node, ast.While):
            # Check if this loop only modifies primitive variables, not collections
            has_collection_modification = False
            for child in ast.walk(node):
                if isinstance(child, (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp)):
                    has_collection_modification = True
                    break
                    
            if not has_collection_modification:
                has_loop_without_storage[0] = True
                
        # Check for list comprehensions, which typically use O(n) space
        if isinstance(node, ast.ListComp):
            complexity = "O(n)"
        
        # Check for dictionary comprehensions
        elif isinstance(node, ast.DictComp):
            complexity = "O(n)"
        
        # Check for list/array creation
        elif isinstance(node, ast.List):
            complexity = "O(n)"
        
        # Check for dictionary creation
        elif isinstance(node, ast.Dict):
            complexity = "O(n)"
        
        # Check for recursive function calls (potential stack space)
        elif isinstance(node, ast.Call):
            # This is a simplification; actual recursive space analysis would be more complex
            if isinstance(node.func, ast.Name) and is_recursive_call(node):
                complexity = "O(n)"  # Assume linear stack space for recursion
        
        # Variable assignments with large data structures
        elif isinstance(node, ast.Assign):
            if has_large_data_structure(node.value):
                complexity = "O(n)"
        
        # Nested data structures (lists of lists, etc.)
        if has_nested_data_structure(node):
            complexity = "O(n^2)"
        
        complexities.append(complexity)
        
        # Visit all child nodes
        for child in ast.iter_child_nodes(node):
            visit_node(child)
    
    # Start traversing from the root node
    visit_node(node)
    
    # Return the worst-case complexity
    complexity_rank = {
        "O(1)": 1,
        "O(log n)": 2,
        "O(n)": 3,
        "O(n log n)": 4,
        "O(n^2)": 5,
        "O(n^3)": 6,
        "O(2^n)": 7,
        "O(n!)": 8
    }
    
    # If we have any O(n²) space usage patterns, prioritize those
    if has_n_squared_storage[0]:
        return "O(n^2)"
    
    # If we only have loops that don't store data, it's likely O(1) space
    if has_loop_without_storage[0] and all(c == "O(1)" for c in complexities):
        return "O(1)"
    
    # Special case for lists inside loops (common pattern for matrix creation)
    has_matrix_pattern = False
    for i, complexity in enumerate(complexities):
        if complexity == "O(n)" and i+1 < len(complexities) and complexities[i+1] == "O(n)":
            has_matrix_pattern = True
            break
    
    if has_matrix_pattern:
        return "O(n^2)"
        
    worst_complexity = max(complexities, key=lambda x: complexity_rank.get(x, 0))
    return worst_complexity


def is_recursive_call(node):
    """
    A simplified check if a call might be recursive.
    In a real implementation, this would need context about the enclosing function.
    
    Args:
        node (ast.Call): The function call to check.
        
    Returns:
        bool: True if the call might be recursive.
    """
    # Simplified check - in reality, we'd need to track function context
    return True


def has_large_data_structure(node):
    """
    Checks if a node represents a large data structure.
    
    Args:
        node (ast.AST): The AST node to check.
        
    Returns:
        bool: True if the node appears to create a large data structure.
    """
    return isinstance(node, (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp))


def has_nested_data_structure(node):
    """
    Checks if a node represents a nested data structure.
    
    Args:
        node (ast.AST): The AST node to check.
        
    Returns:
        bool: True if the node appears to create a nested data structure.
    """
    if isinstance(node, ast.List):
        # Check if any elements are lists
        return any(isinstance(elt, (ast.List, ast.ListComp)) for elt in node.elts)
    elif isinstance(node, ast.Dict):
        # Check if any values are dictionaries or lists
        return any(isinstance(v, (ast.Dict, ast.List)) for v in node.values)
    elif isinstance(node, ast.ListComp):
        return isinstance(node.elt, (ast.List, ast.Dict))
    
    return False