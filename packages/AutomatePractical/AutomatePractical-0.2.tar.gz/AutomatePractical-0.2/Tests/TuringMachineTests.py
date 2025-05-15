import unittest#unittest module is used for unit testing in python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AutomataPractical import TuringMachine

class TuringMachineTests(unittest.TestCase):#we must inherit from the unittest.TastCase to can use assertion functions
    #each test function must start with test_
    def test_addition_simple_digits(self):
        tm = TuringMachine("1+1")
        expected="11"

        actual = tm.addition()

        self.assertEqual(actual, expected,f'Actual {actual} is expected to be {expected}')
        
    def test_addition_two_operands_is_zero(self):
        tm = TuringMachine("+")
        expected=""

        actual = tm.addition()

        self.assertEqual(actual, expected,f'Actual {actual} is expected to be {expected}')

    def test_addition_one_operand_is_zero(self):
        tm = TuringMachine("11111+")
        expected="11111"

        actual = tm.addition()    

        self.assertEqual(actual, expected,f'Actual {actual} is expected to be {expected}')

    def test_addition_invalid_input(self):
        tm = TuringMachine("2111-111")
        expected=""

        actual = tm.addition()
    

        self.assertEqual(actual, expected,f'Actual {actual} is expected to be {expected}')


    
    def test_addition_multiple_digits(self):
        tm = TuringMachine("11111111+11111")
        expected="1111111111111"
        
        actual = tm.addition()

        self.assertEqual(actual, expected,f'Actual {actual} is expected to be {expected}')

    def test_addition_empty_input(self):
        tm = TuringMachine("")
        expected = ""

        actual = tm.addition()

        self.assertEqual(actual, expected,f'Actual {actual} is expected to be {expected}')  # or raise an exception if you want

    def test_addition_only_one_number(self):
        tm = TuringMachine("111")
        expected="111"

        actual = tm.addition()
        
        self.assertNotEqual(actual, expected,f'Actual {actual} is expected to be {expected}')  # Should reject or stop early


if __name__ == "__main__":
    unittest.main()
    #test function discover all method in the file that is start with test_