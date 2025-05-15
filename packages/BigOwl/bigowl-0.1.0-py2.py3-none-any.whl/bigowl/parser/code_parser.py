"""
Code parser module for BigOwl.
Uses tokenize module for edge cases and finer analysis.
"""

import tokenize
import ast
import re
from io import BytesIO

def analyze_code(code_str):
    """
    Analyzes the provided code string for edge cases and finer details.
    
    Args:
        code_str (str): The Python code to analyze.
        
    Returns:
        dict: A dictionary containing analysis results.
    """
    analysis_results = {
        'line_count': 0,
        'function_count': 0,
        'class_count': 0,
        'import_count': 0,
        'comment_count': 0,
        'edge_cases': [],
        'potential_inefficiencies': []
    }
    
    try:
        # Tokenize the code string
        tokens = list(tokenize.tokenize(BytesIO(code_str.encode('utf-8')).readline))
        
        for token in tokens:
            if token.type == tokenize.NEWLINE:
                analysis_results['line_count'] += 1
            elif token.type == tokenize.NAME:
                if token.string == 'def':
                    analysis_results['function_count'] += 1
                elif token.string == 'class':
                    analysis_results['class_count'] += 1
                elif token.string == 'import':
                    analysis_results['import_count'] += 1
            elif token.type == tokenize.COMMENT:
                analysis_results['comment_count'] += 1
        
        # Check for potential inefficiencies
        analysis_results['potential_inefficiencies'] = identify_inefficiencies(code_str)
        
        # Check for commonly misused built-ins or patterns
        analysis_results['edge_cases'] = identify_edge_cases(code_str, tokens)
        
        return analysis_results
    except Exception as e:
        return {
            'error': str(e),
            'line_count': 0,
            'edge_cases': ['Error analyzing code']
        }


def extract_functions(tree):
    """
    Extract all function definitions from an AST.
    
    Args:
        tree (ast.AST or dict): The AST to analyze, or an error dict.
        
    Returns:
        dict: A dictionary mapping function names to their AST nodes.
    """
    functions = {}
    
    # Handle cases where tree might be a dict with error info
    if isinstance(tree, dict) and 'error' in tree:
        return functions
    
    # Handle case where tree is None
    if tree is None:
        return functions
    
    try:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = node
    except Exception as e:
        # If any errors occur, just return an empty dict
        print(f"Error extracting functions: {str(e)}")
        pass
        
    return functions


def identify_inefficiencies(code_str):
    """
    Identify potential inefficiencies in the code.
    
    Args:
        code_str (str): The Python code to analyze.
        
    Returns:
        list: A list of potential inefficiencies found.
    """
    inefficiencies = []
    
    # Check for repeated string concatenation in loops
    if re.search(r'for\s+.+\s+in\s+.+:.+\+=\s*[\'"]', code_str, re.MULTILINE):
        inefficiencies.append('String concatenation in loop detected - consider using join() or list comprehension')
    
    # Check for list appending in loops that could be a list comprehension
    if re.search(r'for\s+.+\s+in\s+.+:.+\.append\(', code_str, re.MULTILINE):
        inefficiencies.append('Multiple list.append() operations - consider using list comprehension')
    
    # Check for nested loops
    if len(re.findall(r'for\s+.+\s+in\s+.+:', code_str, re.MULTILINE)) > 1:
        # Check if they're nested (simplistic approach)
        if re.search(r'for\s+.+\s+in\s+.+:.*\n\s+for\s+.+\s+in\s+.+:', code_str, re.MULTILINE):
            inefficiencies.append('Nested loops detected - consider optimizing with sets or dictionaries')
    
    # Check for repeated lookups that could be cached
    if re.search(r'for\s+.+\s+in\s+.+:.*\[.+\].*\[.+\]', code_str, re.MULTILINE):
        inefficiencies.append('Repeated dictionary/list lookups - consider caching values in variables')
    
    # Check for recursive calls without memoization
    if re.search(r'def\s+(\w+)\(.+\):.*\1\(', code_str, re.DOTALL):
        if '@' not in code_str and 'memo' not in code_str and 'cache' not in code_str:
            inefficiencies.append('Recursive function without memoization - consider adding caching')
    
    return inefficiencies


def identify_edge_cases(code_str, tokens=None):
    """
    Identify potential edge cases or misused patterns in the code.
    
    Args:
        code_str (str): The Python code to analyze.
        tokens (list): List of tokens if already tokenized.
        
    Returns:
        list: A list of identified edge cases.
    """
    edge_cases = []
    
    # Check for usage of range with len which could be enumerate
    if re.search(r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(', code_str, re.MULTILINE):
        edge_cases.append('Using range(len()) - consider using enumerate() instead for more Pythonic and potentially more efficient code')
    
    # Check for empty list initialization followed by append in a loop
    if re.search(r'\w+\s*=\s*\[\]\s*(?:\n|.)*?for\s+.+\s+in\s+.+:.+\.append\(', code_str, re.DOTALL):
        edge_cases.append('Initializing empty list and using append in loop - consider using list comprehension for better performance')
    
    # Check for using lists where sets would be more efficient for lookup
    if re.search(r'if\s+.+\s+in\s+\[', code_str, re.MULTILINE):
        edge_cases.append('Using list for membership testing - consider using a set for O(1) lookups instead of O(n) list search')
    
    # Check for potential off-by-one errors in index ranges
    if re.search(r'for\s+\w+\s+in\s+range\s*\(.+,\s*.+\s*-\s*1\)', code_str, re.MULTILINE):
        edge_cases.append('Potential off-by-one error in range - double-check inclusive/exclusive bounds')
    
    # Check for unnecessary list creation when iterating
    if re.search(r'for\s+\w+\s+in\s+list\s*\(', code_str, re.MULTILINE):
        edge_cases.append('Unnecessary list creation in loop - consider using the iterable directly to save memory')
    
    # Check for potential infinite loops
    if re.search(r'while\s+[Tt]rue', code_str, re.MULTILINE):
        if not re.search(r'break', code_str, re.MULTILINE):
            edge_cases.append('Potential infinite loop detected - ensure there is a proper exit condition')
    
    # Check for sorting before min/max operations
    if re.search(r'sort\(\)|sorted\(', code_str, re.MULTILINE) and re.search(r'\[\s*0\s*\]|\[\s*-1\s*\]', code_str, re.MULTILINE):
        edge_cases.append('Sorting to find min/max values - consider using min()/max() functions directly for better performance - O(n) instead of O(n log n)')
    
    # Check for inefficient string formatting
    if re.search(r'\s*\+\s*str\(|\s*\+\s*"|\s*\+\s*\'', code_str, re.MULTILINE):
        edge_cases.append('Using + operator for string concatenation - consider using f-strings or str.format() for better readability and performance')
    
    # Check for manual index tracking that could use enumerate
    if re.search(r'\w+\s*=\s*0.*?\n.*?for\s+.+\s+in\s+.+:.*?\n.*?\w+\s*\+=\s*1', code_str, re.DOTALL):
        edge_cases.append('Manual index tracking in loop - consider using enumerate() for cleaner code')
    
    return edge_cases