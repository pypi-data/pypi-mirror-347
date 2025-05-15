"""
Helper functions for BigOwl.
"""

import ast
import re


def find_inefficiencies(code_str):
    """
    Identifies inefficiencies in the code and provides suggestions for improvement.
    
    Args:
        code_str (str): The Python code to analyze.
        
    Returns:
        list: A list of suggestions for code improvement.
    """
    suggestions = []
    
    # Check for common inefficient patterns
    
    # Check for nested loops that might be optimized
    if re.search(r'for\s+.+\s+in\s+.+:.*\n\s+for\s+.+\s+in\s+.+:', code_str, re.MULTILINE):
        suggestions.append("Nested loops detected – consider optimizing using hashing or sets to reduce time complexity from O(n²) to O(n).")
    
    # Check for list operations that could be replaced with more efficient data structures
    if re.search(r'if\s+.+\s+in\s+\[', code_str, re.MULTILINE):
        suggestions.append("List membership testing has O(n) complexity - consider using a set for O(1) lookups.")
    
    # Check for string concatenations in loops
    if re.search(r'for\s+.+\s+in\s+.+:.+\+=\s*[\'"]', code_str, re.MULTILINE):
        suggestions.append("String concatenation in a loop is inefficient with O(n²) complexity - use ''.join() for O(n) operations instead.")
    
    # Check for recursive functions without memoization
    if re.search(r'def\s+(\w+)\(.+\):.*\1\(', code_str, re.DOTALL):
        if 'memo' not in code_str and 'cache' not in code_str and '@functools.lru_cache' not in code_str:
            suggestions.append("Recursive function detected without memoization - consider using @functools.lru_cache or a memoization dict to improve exponential time complexity.")
    
    # Check for repeated dictionary lookups
    if re.search(r'for\s+.+\s+in\s+.+:.*\[[\'"].+[\'"]\].*\[[\'"].+[\'"]\]', code_str, re.MULTILINE):
        suggestions.append("Multiple dictionary lookups detected - consider storing lookup values in variables to reduce repeated O(1) operations.")
    
    # Check for range(len()) pattern
    if re.search(r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(', code_str, re.MULTILINE):
        suggestions.append("Using range(len(x)) detected - consider using enumerate() for cleaner and potentially more efficient code.")
    
    # Check for unnecessary list construction before iteration
    if re.search(r'for\s+\w+\s+in\s+list\s*\(', code_str, re.MULTILINE):
        suggestions.append("Unnecessary list construction before iteration detected - iterate over the original iterable directly to save O(n) space complexity.")
    
    # Check for sorting and then looking up specific values
    if 'sort(' in code_str and ('if' in code_str or 'while' in code_str):
        suggestions.append("You're sorting data (O(n log n)) - if you only need min/max values, consider using min()/max() functions (O(n)) instead.")
    
    # Check for slicing operations in loops
    if re.search(r'for\s+.+\s+in\s+.+:.*\[.*:.*\]', code_str, re.MULTILINE):
        suggestions.append("Repeated slicing operations in loops create additional copies of data with O(k) space complexity for each slice - consider pre-computing slices if possible.")
    
    # Check for list comprehensions that might be better as generator expressions
    list_comp_count = len(re.findall(r'\[\s*for\s+.+\s+in\s+.+\s*\]', code_str))
    if list_comp_count > 1:
        suggestions.append("Multiple list comprehensions detected - consider using generator expressions (parentheses instead of brackets) to save memory if you're only iterating over the results.")
        
    # Check for append operations in loops that could be list comprehensions
    if re.search(r'for\s+.+\s+in\s+.+:.*\.append\(', code_str, re.MULTILINE):
        suggestions.append("Building a list with append() in a loop - consider using a list comprehension for more concise and potentially faster code.")
    
    # Check for potential generator expressions
    if re.search(r'for\s+.+\s+in\s+.+:.+\.append\(', code_str, re.MULTILINE):
        suggestions.append("Try generator expressions if memory becomes a bottleneck.")
    
    return suggestions


def extract_patterns(code_str):
    """
    Extracts specific coding patterns from the code.
    
    Args:
        code_str (str): The Python code to analyze.
        
    Returns:
        dict: A dictionary of identified patterns.
    """
    patterns = {
        'has_loops': bool(re.search(r'for\s+.+\s+in\s+.+:', code_str, re.MULTILINE)),
        'has_recursion': bool(re.search(r'def\s+(\w+)\(.+\):.*\1\(', code_str, re.DOTALL)),
        'has_list_comprehension': bool(re.search(r'\[.+for\s+.+\s+in\s+.+\]', code_str, re.MULTILINE)),
        'has_try_except': bool(re.search(r'try:', code_str, re.MULTILINE)),
        'has_classes': bool(re.search(r'class\s+\w+', code_str, re.MULTILINE)),
        'has_function_calls': bool(re.search(r'\w+\(.+\)', code_str, re.MULTILINE)),
    }
    
    return patterns


def format_output(data):
    """
    Formats the output data for better readability.
    
    Args:
        data (dict): The analysis data to format.
        
    Returns:
        dict: A formatted version of the analysis data.
    """
    # Create a clean copy of the data
    formatted_data = {}
    
    # Format the time and space complexity
    if 'Time Complexity' in data:
        formatted_data['Time Complexity'] = data['Time Complexity']
    
    if 'Space Complexity' in data:
        formatted_data['Space Complexity'] = data['Space Complexity']
    
    # Format the suggestions
    if 'Suggestions' in data:
        formatted_data['Suggestions'] = data['Suggestions']
    
    return formatted_data


def format_suggestions(func_name, func_node):
    """
    Format suggestions specific to a function.
    
    Args:
        func_name (str): The name of the function.
        func_node (ast.FunctionDef): The AST node for the function.
        
    Returns:
        list: A list of formatted suggestions.
    """
    suggestions = []
    
    # Check for unused parameters
    param_names = set()
    used_names = set()
    
    # Get parameter names
    if isinstance(func_node, ast.FunctionDef):
        for arg in func_node.args.args:
            param_names.add(arg.arg)
        
        # Find used variables
        for node in ast.walk(func_node):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
        
        # Find unused parameters
        unused_params = param_names - used_names
        if unused_params:
            suggestions.append(f"Function '{func_name}' has unused parameters: {', '.join(unused_params)}")
    
    # Here you can add more function-specific suggestions
    
    return suggestions