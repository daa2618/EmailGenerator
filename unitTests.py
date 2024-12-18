

import unittest
import re
from emailGenerator import _splitName, _getFormatListAndSeperator, _getSequencingWords, _getNewEmailFormat, generateEmailString # Assuming the file is saved as your_module.py

class TestEmailFunctions(unittest.TestCase):

    def test_splitName(self):
        self.assertEqual(_splitName("John Doe"), ("John", None, "Doe"))
        self.assertEqual(_splitName("John Michael Doe"), ("John", "Michael", "Doe"))
        self.assertEqual(_splitName("John"), ("John", None, None))
        self.assertEqual(_splitName(""), (None, None, None))
        self.assertEqual(_splitName("  John  Doe   "), ("John", None, "Doe")) # Handling extra spaces
        self.assertEqual(_splitName("  "), (None, None, None))
        self.assertEqual(_splitName("John Doe Smith  "), ("John", "Doe", "Smith"))

    def test_getFormatListAndSeperator(self):
        self.assertEqual(_getFormatListAndSeperator("[first]_[last]"), (["first", "last"], ["_"]))
        self.assertEqual(_getFormatListAndSeperator("[first].[last]"), (["first", "last"], ["."]))
        self.assertEqual(_getFormatListAndSeperator("[first][last]"), (["first", "last"], [""]))
        self.assertEqual(_getFormatListAndSeperator("[first]_[middle]_[last]"), (["first", "middle", "last"], ["_", "_"]))
        self.assertEqual(_getFormatListAndSeperator("prefix[first]suffix"), (["first"], ["suffix"]))
        self.assertEqual(_getFormatListAndSeperator("[first_initial]_[last]"), (["first_initial", "last"], ["_"]))
        self.assertEqual(_getFormatListAndSeperator(""), ([], []))
        self.assertEqual(_getFormatListAndSeperator("abc"), ([], []))
        self.assertEqual(_getFormatListAndSeperator("[first][last][middle]"), (['first', 'last', 'middle'], ['', '']))
        self.assertEqual(_getFormatListAndSeperator("[first]_[last]-"), (['first', 'last'], ['_', '-']))
        self.assertEqual(_getFormatListAndSeperator("-[first]_[last]"), (['first', 'last'], ['-', '_']))
    
    def test_getSequencingWords(self):
        self.assertEqual(_getSequencingWords(["first_two\b", "last_two\b"]), ["two", "two"])
        self.assertEqual(_getSequencingWords(["first_three\b", "last_two\b", "other"]), ["three", "two"])
        self.assertEqual(_getSequencingWords(["first_initial\b", "last_initial\b"]), ["initial", "initial"])
        self.assertEqual(_getSequencingWords([]), [])
        self.assertEqual(_getSequencingWords(["no_match"]), [])
        self.assertEqual(_getSequencingWords(["first_three\b", "middle_three\b", "last_one\b"]), ['three', 'three', 'one'])
        self.assertEqual(_getSequencingWords(["first_123\b", "last_abc\b"]), ["123", "abc"])

    def test_getNewEmailFormat(self):
        emailFormat = "[first_two][last]"
        self.assertEqual(_getNewEmailFormat("two", ['first_two', 'last'], emailFormat), ('first_two', '[first][last]'))
        self.assertEqual(_getNewEmailFormat("last", ["first", 'last'], emailFormat), ("last", '[first_two][last]'))
        
        emailFormat = "[first_initial]_[last]"
        self.assertEqual(_getNewEmailFormat("initial", ['first_initial', 'last'], emailFormat), ('first_initial', '[first]_[last]'))
       
        emailFormat = "[first][last_three]"
        self.assertEqual(_getNewEmailFormat("three", ['first', 'last_three'], emailFormat), ('last_three', '[first][last]'))

        emailFormat = "[first][middle][last]"
        self.assertEqual(_getNewEmailFormat("middle", ['first', 'middle', 'last'], emailFormat, ["first", "middle", "last"]), ('middle', '[first][middle][last]'))

        self.assertEqual(_getNewEmailFormat("invalid", ["first", "last"], emailFormat), (None, None))
        
        emailFormat = "[first][last]"
        self.assertEqual(_getNewEmailFormat("invalid", ["first", "last"], emailFormat), (None, None))
        
        emailFormat = "[first_two]_[last_one]"
        self.assertEqual(_getNewEmailFormat("two", ["first_two", "last_one"], emailFormat), ('first_two', '[first]_[last_one]'))
        self.assertEqual(_getNewEmailFormat("one", ["first_two", "last_one"], emailFormat), ('last_one', '[first_two]_[last]'))
        
        
        
        emailFormat = "[first][middle_three][last]"
        self.assertEqual(_getNewEmailFormat("three", ['first', 'middle_three','last'], emailFormat, ["middle"]), ('middle_three', '[first][middle][last]'))

    def test_generateEmailString(self):
        #Basic Cases
        self.assertEqual(generateEmailString("John Doe", "[first][last]", "example.com"), "johndoe@example.com")
        self.assertEqual(generateEmailString("John Doe", "[first]_[last]", "example.com"), "john_doe@example.com")
        self.assertEqual(generateEmailString("John Michael Doe", "[first].[last]", "example.com"), "john.doe@example.com")
        self.assertEqual(generateEmailString("John Doe", "[first_initial][last]", "example.com"), "jdoe@example.com")
        self.assertEqual(generateEmailString("John Doe", "[first][last_initial]", "example.com"), "johnd@example.com")
        self.assertEqual(generateEmailString("John Doe", "[first_three][last_three]", "example.com"), "johdoe@example.com")
        
        
        #Case Sensitivity
        self.assertEqual(generateEmailString("John Doe", "[FIRST][LAST]", "example.com"), "johndoe@example.com")
        self.assertEqual(generateEmailString("JOHN DOE", "[first][last]", "example.com"), "johndoe@example.com")
        
        
        #Middle Name
        self.assertEqual(generateEmailString("John Michael Doe", "[first][middle][last]", "example.com"), "johnmichaeldoe@example.com")
        self.assertEqual(generateEmailString("John Michael Doe", "[first_initial][middle_initial][last]", "example.com"), "jmd@example.com")
        self.assertEqual(generateEmailString("John Michael Doe", "[first_three][middle_three][last_three]", "example.com"), "johmicdoe@example.com")
        
        #Middle name error
        with self.assertRaises(NameError):
           generateEmailString("John Doe", "[first][middle][last]", "example.com")
        with self.assertRaises(NameError):
           generateEmailString("John Doe", "[first_initial][middle_initial][last]", "example.com") 

        
        # Edge Cases with no names
        self.assertIsNone(generateEmailString("", "[first][last]", "example.com"))
        self.assertIsNone(generateEmailString(" ", "[first][last]", "example.com"))
        
        # Edge Cases with domain format
        self.assertEqual(generateEmailString("John Doe", "[first][last]", "@example.com"), "johndoe@example.com")
        self.assertEqual(generateEmailString("John Doe", "[first][last]", "EXAMPLE.COM"), "johndoe@example.com")
        
        #Edge Case if middle name is formatted but no middle name is given
        with self.assertRaises(NameError):
            generateEmailString("John Doe", "[first][middle_three][last]", "example.com")
            
        #Edge cases with more than one separator
        self.assertEqual(generateEmailString("John Doe", "[first]-[last]", "example.com"), "john-doe@example.com")
        self.assertEqual(generateEmailString("John Doe", "[first]-[last]-", "example.com"), "john-doe-@example.com")
        self.assertEqual(generateEmailString("John Doe", "-[first]_[last]", "example.com"), "-john_doe@example.com")
        
        self.assertEqual(generateEmailString("John Doe", "[first][last][middle]", "example.com"), "johndoe@example.com")


        #Edge cases with different format variations.
        self.assertEqual(generateEmailString("John Doe", "[first_two][last]", "example.com"), "jodoe@example.com")
        self.assertEqual(generateEmailString("John Doe", "[first][last_one]", "example.com"), "john@example.com")
        self.assertEqual(generateEmailString("John Michael Doe", "[first_two][middle_two][last]", "example.com"), "jomidoe@example.com")
        self.assertEqual(generateEmailString("John Michael Doe", "[first][middle][last_one]", "example.com"), "johnmicha@example.com")

        
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
