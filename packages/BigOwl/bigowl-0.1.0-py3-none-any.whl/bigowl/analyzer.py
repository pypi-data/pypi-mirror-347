"""
Analyzer module for BigOwl library.
This is the main module that handles code analysis.
"""

import ast
from .parser.ast_parser import ASTParser
from .parser.code_parser import analyze_code as analyze_code_structure, identify_edge_cases
from .complexity.time_complexity import estimate_time_complexity
from .complexity.space_complexity import analyze_space_complexity
from .utils.helpers import format_output, find_inefficiencies

def analyze(code_str):
    """
    Analyzes the given Python code string for time and space complexity.

    Parameters:
    code_str (str): The Python code to analyze.

    Returns:
    dict: A dictionary containing time and space complexity estimates and suggestions.
    """
    try:
        # Parse the code using our AST parser
        parser = ASTParser(code_str)
        ast_analysis = parser.get_analysis()
        
        # Get code structure analysis
        code_structure = analyze_code_structure(code_str)
        
        # Estimate time complexity
        time_complexity = estimate_time_complexity(code_str)
        
        # Estimate space complexity
        space_complexity = analyze_space_complexity(code_str)
        
        # Find inefficiencies and edge cases
        inefficiencies = find_inefficiencies(code_str)
        edge_cases = identify_edge_cases(code_str)
        
        # Combine all suggestions and remove duplicates
        # We'll use a dictionary with suggestion text as key to remove duplicates
        # while preserving order of suggestions
        unique_suggestions = {}
        for suggestion in inefficiencies + edge_cases:
            # Use lowercase version as key to catch near-duplicates with different case
            key = suggestion.lower()
            unique_suggestions[key] = suggestion
            
        all_suggestions = list(unique_suggestions.values())
        
        # If no suggestions were found, add a message saying code looks fine
        if not all_suggestions:
            all_suggestions = ["No suggestion, Code looks fine."]
        
        # Format the results
        results = {
            'Time Complexity': time_complexity,
            'Space Complexity': space_complexity,
            'Suggestions': all_suggestions
        }
        
        return results
    except SyntaxError as e:
        return {
            'Error': f"Syntax error: {str(e)}",
            'Time Complexity': 'Unknown',
            'Space Complexity': 'Unknown',
            'Suggestions': ['Code analysis failed due to syntax errors. Please check your code syntax.']
        }
    except Exception as e:
        return {
            'Error': f"Analysis error: {str(e)}",
            'Time Complexity': 'Unknown',
            'Space Complexity': 'Unknown',
            'Suggestions': ['Code analysis failed. Please check if the code is valid Python.']
        }