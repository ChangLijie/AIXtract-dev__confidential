import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..."))
from models import ParserData
from readers import PDFParser


class TestXMLParser(unittest.TestCase):
    def setUp(self):
        self.pdf_path = "./data/EMPU_3401_Datasheet.pdf"
        self.pdf_parser = PDFParser()

    def test_get_data(self):
        pdf_data = self.pdf_parser.process(path=self.pdf_path)
        # Test if the data is a ParserData
        self.assertIsInstance(pdf_data, ParserData)
        # Test if the list is not empty
        self.assertEqual(len(pdf_data.pages), 3, "Parsed data should not be empty")


if __name__ == "__main__":
    unittest.main()
