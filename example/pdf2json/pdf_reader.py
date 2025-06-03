import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from readers import PDFParser

if __name__ == "__main__":
    path = "./data/EMPU_3401_Datasheet.pdf"
    xml_parser = PDFParser()
    print(xml_parser.process(path=path))
