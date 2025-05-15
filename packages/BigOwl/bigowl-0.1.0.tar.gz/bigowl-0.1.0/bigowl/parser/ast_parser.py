"""
AST Parser module for BigOwl.
Parses Python code into an AST and provides methods for analysis.
"""

import ast
import asttokens
import builtins

class ASTParser:
    def __init__(self, code_str):
        """
        Initialize the AST parser with a code string.
        
        Args:
            code_str (str): The Python code to parse.
        """
        self.code_str = code_str
        try:
            self.tree = ast.parse(code_str)
            # Optional: Use asttokens for more precise token location information
            self.atok = asttokens.ASTTokens(code_str, parse=True)
        except SyntaxError as e:
            # Handle syntax errors gracefully
            self.tree = None
            self.syntax_error = e
        except Exception as e:
            self.tree = None
            self.error = e

    def analyze(self):
        """
        Analyze the AST for structures relevant to complexity analysis.
        
        Returns:
            dict: Analysis results including loops, recursion, data structures, etc.
        """
        if not hasattr(self, 'tree') or self.tree is None:
            if hasattr(self, 'syntax_error'):
                return {"error": f"Syntax error: {str(self.syntax_error)}"}
            return {"error": "Failed to parse code"}

        result = {
            "loops": self._find_loops(),
            "recursion": self._find_recursion(),
            "function_calls": self._find_function_calls(),
            "data_structures": self._find_data_structures(),
            "variable_assignments": self._find_variable_assignments(),
        }
        return result

    def _traverse(self, node):
        """
        Traverse the AST and build a structured representation.
        
        Args:
            node (ast.AST): The AST node to traverse.
            
        Returns:
            dict: A structured representation of the AST.
        """
        analysis_result = {
            "type": node.__class__.__name__,
        }
        
        # Add node-specific attributes
        if isinstance(node, ast.FunctionDef):
            analysis_result["name"] = node.name
            analysis_result["args"] = [arg.arg for arg in node.args.args]
            
        elif isinstance(node, ast.For):
            analysis_result["target"] = node.target.__class__.__name__
            analysis_result["iter"] = node.iter.__class__.__name__
            
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                analysis_result["func_name"] = node.func.id
                
        # Add child nodes
        children = {}
        for child in ast.iter_child_nodes(node):
            child_name = child.__class__.__name__
            if child_name not in children:
                children[child_name] = []
            children[child_name].append(self._traverse(child))
            
        if children:
            analysis_result["children"] = children
            
        return analysis_result

    def _find_loops(self):
        """
        Find all loops in the AST.
        
        Returns:
            list: Information about loops found in the code.
        """
        loops = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.For, ast.While)):
                loop_info = {
                    "type": node.__class__.__name__,
                    "line": getattr(node, 'lineno', -1),
                    "nested_level": self._get_nesting_level(node),
                }
                loops.append(loop_info)
                
        return loops

    def _get_nesting_level(self, node, level=0):
        """
        Calculate the nesting level of a node.
        
        Args:
            node (ast.AST): The AST node to analyze.
            level (int): The current nesting level.
            
        Returns:
            int: The nesting level of the node.
        """
        parent = getattr(node, 'parent', None)
        if parent is None:
            # Try to find the parent manually (simplified approach)
            for possible_parent in ast.walk(self.tree):
                for child in ast.iter_child_nodes(possible_parent):
                    if child == node:
                        parent = possible_parent
                        break
                if parent is not None:
                    break
        
        if parent is None:
            return level
        
        if isinstance(parent, (ast.For, ast.While)):
            level += 1
            
        return self._get_nesting_level(parent, level)

    def _find_recursion(self):
        """
        Find all recursive function calls in the AST.
        
        Returns:
            list: Information about recursive functions found in the code.
        """
        recursive_funcs = []
        
        # Find all function definitions
        function_defs = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                function_defs[node.name] = node
                
        # Check each function for recursive calls
        for func_name, func_node in function_defs.items():
            calls_itself = False
            
            for node in ast.walk(func_node):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id == func_name:
                        calls_itself = True
                        break
                        
            if calls_itself:
                recursive_funcs.append({
                    "name": func_name,
                    "line": func_node.lineno,
                })
                
        return recursive_funcs

    def _find_function_calls(self):
        """
        Find all function calls in the AST.
        
        Returns:
            list: Information about function calls found in the code.
        """
        function_calls = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = f"{node.func.value.__class__.__name__}.{node.func.attr}"
                
                # Check if it's a built-in function that might be expensive
                if func_name in dir(builtins) and func_name in ["sorted", "map", "filter"]:
                    function_calls.append({
                        "name": func_name,
                        "line": getattr(node, 'lineno', -1),
                        "is_builtin": True,
                    })
                else:
                    function_calls.append({
                        "name": func_name,
                        "line": getattr(node, 'lineno', -1),
                        "is_builtin": False,
                    })
                    
        return function_calls

    def _find_data_structures(self):
        """
        Find all data structure creations in the AST.
        
        Returns:
            list: Information about data structures found in the code.
        """
        data_structures = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.List, ast.Dict, ast.Set, ast.Tuple)):
                data_structures.append({
                    "type": node.__class__.__name__,
                    "line": getattr(node, 'lineno', -1),
                    "size": len(getattr(node, 'elts', [])) if hasattr(node, 'elts') else 0,
                })
            elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
                data_structures.append({
                    "type": node.__class__.__name__,
                    "line": getattr(node, 'lineno', -1),
                    "is_comprehension": True,
                })
                    
        return data_structures

    def _find_variable_assignments(self):
        """
        Find all variable assignments in the AST.
        
        Returns:
            list: Information about variable assignments found in the code.
        """
        assignments = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assignments.append({
                            "name": target.id,
                            "line": getattr(node, 'lineno', -1),
                            "value_type": node.value.__class__.__name__,
                        })
                    
        return assignments

    def get_analysis(self):
        """
        Public method to get the AST analysis.
        
        Returns:
            dict: Analysis results.
        """
        return self.analyze()


def parse_code(code_str):
    """
    Parse code string into an AST.
    
    Args:
        code_str (str): The Python code to parse.
        
    Returns:
        ast.AST: The AST of the parsed code.
    """
    try:
        return ast.parse(code_str)
    except SyntaxError as e:
        return {"error": f"Syntax error: {str(e)}"}
    except Exception as e:
        return {"error": f"Error parsing code: {str(e)}"}