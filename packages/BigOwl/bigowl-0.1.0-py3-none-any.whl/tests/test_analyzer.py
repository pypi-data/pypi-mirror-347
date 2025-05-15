import unittest
from bigowl import analyze

class TestAnalyzer(unittest.TestCase):

    def test_analyze_simple(self):
        code_str = "for i in range(10): pass"
        result = analyze(code_str)
        self.assertIn('Time Complexity', result)
        self.assertIn('Space Complexity', result)
        self.assertIn('Suggestions', result)

    def test_analyze_recursive(self):
        code_str = "def factorial(n): return 1 if n == 0 else n * factorial(n - 1)"
        result = analyze(code_str)
        self.assertIn('Time Complexity', result)
        self.assertIn('Space Complexity', result)
        self.assertIn('Suggestions', result)
        # Check that it detects recursion
        self.assertEqual(result['Time Complexity'], 'O(n)')

    def test_analyze_nested_loops(self):
        code_str = """
def nested_loops(n):
    result = []
    for i in range(n):
        for j in range(n):
            result.append(i * j)
    return result
"""
        result = analyze(code_str)
        self.assertIn('Time Complexity', result)
        self.assertEqual(result['Time Complexity'], 'O(n^2)')
        self.assertIn('Space Complexity', result)
        self.assertIn('Suggestions', result)
        # Check that it suggests optimizations for nested loops
        self.assertTrue(any('nested loops' in suggestion.lower() for suggestion in result['Suggestions']))

    def test_analyze_invalid_code(self):
        code_str = "this is not valid Python code"
        result = analyze(code_str)
        # Our implementation returns 'Unknown (syntax error)' directly instead of a separate Error key
        self.assertIn('Time Complexity', result)
        self.assertEqual(result['Time Complexity'], 'Unknown (syntax error)')

    def test_analyze_edge_case(self):
        code_str = "x = [1, 2, 3] * 1000"
        result = analyze(code_str)
        self.assertIn('Time Complexity', result)
        self.assertIn('Space Complexity', result)
        self.assertIn('Suggestions', result)

if __name__ == '__main__':
    unittest.main()