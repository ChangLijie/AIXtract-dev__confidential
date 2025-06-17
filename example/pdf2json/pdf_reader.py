import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from readers import PDFParser

if __name__ == "__main__":
    path = "./data/EMPU_3401_Datasheet.pdf"
    pdf_parser = PDFParser()
    pdf_data = pdf_parser.process(path=path)

    # print(len(pdf_data.pages))
    # print(pdf_data.pages)
    # print(pdf_data.pages[1].size)
    # print(pdf_data.pages[1].data[1])
