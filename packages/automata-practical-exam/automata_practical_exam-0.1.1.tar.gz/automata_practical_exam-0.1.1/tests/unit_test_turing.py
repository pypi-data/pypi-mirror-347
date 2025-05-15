import unittest
from unittest.mock import patch
from automata_practical_exam.Turing_Machine.Turing_Machine import turing_machine_binary_numbers_divBy_3

class TestTuringMachineDivBy3(unittest.TestCase):
    # Test Accepted Cases
    def test_valid_binary_accepted(self):
        with patch('sys.stdout', new_callable=lambda: None):  
            self.assertEqual(turing_machine_binary_numbers_divBy_3("0"), "Accepted")
            self.assertEqual(turing_machine_binary_numbers_divBy_3("11"), "Accepted")
            self.assertEqual(turing_machine_binary_numbers_divBy_3("110"), "Accepted")
            self.assertEqual(turing_machine_binary_numbers_divBy_3("1001"), "Accepted")

    def test_empty_string(self):
        with patch('sys.stdout', new_callable=lambda: None): 
            self.assertEqual(turing_machine_binary_numbers_divBy_3(""), "Accepted")  

    # Test Rejected Cases
    def test_valid_binary_rejected(self):
        with patch('sys.stdout', new_callable=lambda: None):  
            self.assertEqual(turing_machine_binary_numbers_divBy_3("1"), "Rejected")
            self.assertEqual(turing_machine_binary_numbers_divBy_3("10"), "Rejected")
            self.assertEqual(turing_machine_binary_numbers_divBy_3("101"), "Rejected")
            self.assertEqual(turing_machine_binary_numbers_divBy_3("111"), "Rejected")

    def test_invalid_binary_input(self):
        with patch('sys.stdout', new_callable=lambda: None):  
            self.assertEqual(turing_machine_binary_numbers_divBy_3("abc"), "Rejected")
            self.assertEqual(turing_machine_binary_numbers_divBy_3("1012"), "Rejected")
            self.assertEqual(turing_machine_binary_numbers_divBy_3("10a0"), "Rejected")

if __name__ == '__main__':
    unittest.main()
