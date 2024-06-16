import unittest
from typing import NamedTuple
from unittest.mock import patch

from myproject import fibonacci


class TestCase(NamedTuple):
    n: int
    expectedResult: int
    expectedRecursiveCalls: int


generalTestCases: list[TestCase] = [
    TestCase(n=0, expectedResult=0, expectedRecursiveCalls=1),
    TestCase(n=1, expectedResult=1, expectedRecursiveCalls=1),
    TestCase(n=2, expectedResult=1, expectedRecursiveCalls=3),   # 3  = 1 + 1 + 1
    TestCase(n=3, expectedResult=2, expectedRecursiveCalls=5),   # 5  = 1 + 3 + 1
    TestCase(n=4, expectedResult=3, expectedRecursiveCalls=9),   # 9  = 1 + 5 + 3
    TestCase(n=5, expectedResult=5, expectedRecursiveCalls=15),  # 15 = 1 + 9 + 5
]


class Fibo_Test(unittest.TestCase):

    def test_callWithValidInput_0(self):
        result = fibonacci.fibo(0)
        self.assertEqual(result, 0)

    def test_callWithValidInput_6(self):
        result = fibonacci.fibo(6)
        self.assertEqual(result, 8)

    def test_callWithInvalidInput_negative(self):
        with self.assertRaises(AssertionError):
            fibonacci.fibo(-1)

    def test_callWithValidInputsResultsAndComplexity(self):

        for testCase in generalTestCases:
            with self.subTest(testCase.n):

                # Arrange
                originalFibo = fibonacci.fibo
                with patch('myproject.fibonacci.fibo') as mockedFibo:

                    mockedFibo.side_effect = originalFibo

                    # Act
                    result = fibonacci.fibo(testCase.n)

                    # Assert
                    self.assertEqual(testCase.expectedResult, result)
                    self.assertEqual(testCase.expectedRecursiveCalls, mockedFibo.call_count)


class FiboAsync_Test(unittest.IsolatedAsyncioTestCase):

    async def test_callWithValidInput_0(self):
        result = await fibonacci.fibo_async(0)
        self.assertEqual(result, 0)

    async def test_callWithValidInput_6(self):
        result = await fibonacci.fibo_async(6)
        self.assertEqual(result, 8)

    async def test_callWithInvalidInput_negative(self):
        with self.assertRaises(AssertionError):
            await fibonacci.fibo_async(-1)

    async def test_callWithValidInputsResultsAndComplexity(self):

        for testCase in generalTestCases:
            with self.subTest(testCase.n):

                # Arrange
                originalFibo = fibonacci.fibo_async
                with patch('myproject.fibonacci.fibo_async') as mockedFibo:
                    mockedFibo.side_effect = originalFibo

                    # Act
                    result = await fibonacci.fibo_async(testCase.n)

                    # Assert
                    self.assertEqual(testCase.expectedResult, result)
                    # Testing for implementation detail is not a great idea.
                    # Just wanted to play with mocks on recursive calls
                    self.assertEqual(testCase.expectedRecursiveCalls, mockedFibo.call_count)
