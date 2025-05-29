import os
import xml.etree.ElementTree as ET

from readers.core import BaseReader


class XMLParser(BaseReader):
    """
    XMLParser class for parsing XML files.
    """

    def process(self, path: str, only_text: bool = True) -> dict:
        """
        Extracts and flattens all text content from `<text>` tags under each `<page>` in the XML file,
        including any nested tags like `<b>`, `<i>`, etc.

        Args:
            path (str): Path to the XML file.
            only_text (bool): If True, only extract text content. Defaults to True.

        Returns:
            dict: A dict where each element is a list of `<text>` contents for one page.

        Raises:
            FileNotFoundError:
                If the XML file does not exist.
            ValueError:
                - If the file extension is not supported.
                - If the XML root tag is missing or malformed.
            Exception:
                An error occurred while processing the file.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        if not path.endswith(".xml"):
            raise ValueError(f"Expected an XML file, but got {path}")
        try:
            tree = ET.parse(path)
            root = tree.getroot()

            if root.tag != "pdf2xml":
                raise ValueError(f"Expected root tag <pdf2xml>, but got <{root.tag}>")

            pages_data = {}

            for page in root.findall("page"):
                page_texts = []
                if only_text:
                    for elem in page.findall("text"):
                        xml_str = ET.tostring(elem, encoding="unicode")
                        page_texts.append(xml_str)
                else:
                    for elem in page.iter():
                        xml_str = ET.tostring(elem, encoding="unicode")
                        page_texts.append(xml_str)
                pages_data.update({page.attrib["number"]: page_texts})
            return pages_data

        except Exception as e:
            raise Exception(f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    path = "/mnt/other/SmartDataTransform-dev__confidential/data/EMPU_3401_Datasheet/EMPU_3401_Datasheet.xml"
    xml_parser = XMLParser()

    print(xml_parser.process(path=path))
