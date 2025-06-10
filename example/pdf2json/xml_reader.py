import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from readers import XMLParser

if __name__ == "__main__":
    path = "./data/EMPU_3401_Datasheet/EMPU_3401_Datasheet.xml"
    xml_parser = XMLParser()

    xml_data = xml_parser.process(path=path)
    # print(len(xml_data.pages))
    # print(xml_data.pages)
    # print(xml_data.pages[1].size)
    # print(xml_data.pages[1].data[1])
