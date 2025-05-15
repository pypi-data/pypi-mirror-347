import unittest
from unittest.mock import patch
from automata_practical_exam.DFA_task.dfa import accepts_all_strings_substring_101  

class TestDFASubstring101(unittest.TestCase):
    #Test Accepted Cases
    def test_accept_cases(self):
        with patch('sys.stdout', new_callable=lambda: None):  
            self.assertEqual(accepts_all_strings_substring_101("101"), "Accepted")
            self.assertEqual(accepts_all_strings_substring_101("1101"), "Accepted")
            self.assertEqual(accepts_all_strings_substring_101("000101000"), "Accepted")
            self.assertEqual(accepts_all_strings_substring_101("101101"), "Accepted")
            self.assertEqual(accepts_all_strings_substring_101("1110101"), "Accepted")

    #Test Rejected Cases
    def test_reject_cases(self):
        with patch('sys.stdout', new_callable=lambda: None):  
            self.assertEqual(accepts_all_strings_substring_101(""), "Rejected")
            self.assertEqual(accepts_all_strings_substring_101("0"), "Rejected")
            self.assertEqual(accepts_all_strings_substring_101("11"), "Rejected")
            self.assertEqual(accepts_all_strings_substring_101("100"), "Rejected")
            self.assertEqual(accepts_all_strings_substring_101("111111"), "Rejected")

    def test_invalid_input(self):
        with patch('sys.stdout', new_callable=lambda: None):  
            self.assertEqual(accepts_all_strings_substring_101("10a1"), "Rejected")
            self.assertEqual(accepts_all_strings_substring_101("abc"), "Rejected")
            self.assertEqual(accepts_all_strings_substring_101("1012"), "Rejected")
            self.assertEqual(accepts_all_strings_substring_101("1 0 1"), "Rejected")

if __name__ == '__main__':
    unittest.main()
