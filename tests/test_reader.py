import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from readers import XMLParser


class TestXMLParser(unittest.TestCase):
    def setUp(self):
        pdf_path = "./data/EMPU_3401_Datasheet.pdf"
        self.parser = XMLParser(pdf_path)

    def test_get_data(self):
        # Test if the data is a list
        self.assertIsInstance(self.parser.data, list)
        # Test if the list is not empty
        self.assertGreater(len(self.parser.data), 0, "Parsed data should not be empty")
        # Test if the element is a string (XML fragment)
        self.assertTrue(all(isinstance(fragment, str) for fragment in self.parser.data))
        # Test if the XML fragments are not empty
        self.assertTrue(all(fragment.strip() for fragment in self.parser.data))


if __name__ == "__main__":
    unittest.main()
