import unittest
from bigowl.complexity.time_complexity import estimate_time_complexity

class TestTimeComplexity(unittest.TestCase):

    def test_simple_loop(self):
        code = """
for i in range(10):
    print(i)
"""
        self.assertEqual(estimate_time_complexity(code), "O(n)")

    def test_nested_loops(self):
        code = """
for i in range(10):
    for j in range(5):
        print(i, j)
"""
        self.assertEqual(estimate_time_complexity(code), "O(n^2)")

    def test_recursive_function(self):
        code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
"""
        self.assertEqual(estimate_time_complexity(code), "O(n)")

    def test_fibonacci_recursive(self):
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""
        self.assertEqual(estimate_time_complexity(code), "O(2^n)")

    def test_logarithmic(self):
        code = """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
"""
        self.assertEqual(estimate_time_complexity(code), "O(log n)")

    def test_constant_time(self):
        code = """
print("Hello, World!")
"""
        self.assertEqual(estimate_time_complexity(code), "O(1)")

if __name__ == '__main__':
    unittest.main()