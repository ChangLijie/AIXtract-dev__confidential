import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from readers import PDFParser

if __name__ == "__main__":
    path = "./data/EMPU_3401_Datasheet.pdf"
    pdf_parser = PDFParser()
    print(pdf_parser.process(path=path))
