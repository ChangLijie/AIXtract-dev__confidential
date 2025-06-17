import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union

from models import PageData, PageSize, ParserData
from readers.core import BaseReader


class XMLParser(BaseReader):
    """
    XMLParser class for parsing XML files.
    """

    def process(self, path: Union[Path, str], only_text: bool = True) -> ParserData:
        """
        Extracts and flattens all text content from `<text>` tags under each `<page>` in the XML file,
        including any nested tags like `<b>`, `<i>`, etc.

        Args:
            path (Union[Path, str]): Path to the XML file.
            only_text (bool): If True, only extract text content. Defaults to True.

        Returns:
            ParserData: A dict contain 'page size' and 'page data' for one page.

        Raises:
            FileNotFoundError:
                If the XML file does not exist.
            ValueError:
                - If the file extension is not supported.
                - If the XML root tag is missing or malformed.
            Exception:
                An error occurred while processing the file.
        """
        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise TypeError(f"Expected str or Path, but got {type(path).__name__}")
        if not path.exists():
            raise FileNotFoundError(f"The file {path} does not exist.")
        if not path.suffix.lower() == ".xml":
            raise ValueError(f"Expected an XML file, but got {path}")

        try:
            tree = ET.parse(path)
            root = tree.getroot()

            if root.tag != "pdf2xml":
                raise ValueError(f"Expected root tag <pdf2xml>, but got <{root.tag}>")

            pages_data = ParserData(pages={})

            for page in root.findall("page"):
                page_num = int(page.attrib["number"])
                page_size = PageSize(
                    top=float(page.attrib.get("top", 0)),
                    left=float(page.attrib.get("left", 0)),
                    height=float(page.attrib.get("height", 0)),
                    width=float(page.attrib.get("width", 0)),
                )

                page_texts = []
                if only_text:
                    for elem in page.findall("text"):
                        xml_str = ET.tostring(elem, encoding="unicode")
                        page_texts.append(xml_str)
                else:
                    for elem in page.iter():
                        xml_str = ET.tostring(elem, encoding="unicode")
                        page_texts.append(xml_str)

                pages_data.pages[page_num] = PageData(size=page_size, data=page_texts)
            return pages_data

        except Exception as e:
            raise Exception(f"An error occurred while processing the file: {e}") from e


if __name__ == "__main__":
    path = "/mnt/other/SmartDataTransform-dev__confidential/data/EMPU_3401_Datasheet/EMPU_3401_Datasheet.xml"
    xml_parser = XMLParser()

    xml_data = xml_parser.process(path=path)
    # print(len(xml_data.pages))
    # print(xml_data.pages)
    # print(xml_data.pages[1].size)
    # print(xml_data.pages[1].data[1])
