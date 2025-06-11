import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..."))
from models import ParserData
from readers import XMLParser


class TestXMLParser(unittest.TestCase):
    def setUp(self):
        self.xml_path = "./data/EMPU_3401_Datasheet/EMPU_3401_Datasheet.xml"
        self.xml_parser = XMLParser()

    def test_get_data(self):
        xml_data = self.xml_parser.process(path=self.xml_path)
        # Test if the data is a ParserData
        self.assertIsInstance(xml_data, ParserData)
        # Test if the list is not empty
        self.assertEqual(len(xml_data.pages), 3, "Parsed data should not be empty")


if __name__ == "__main__":
    unittest.main()
