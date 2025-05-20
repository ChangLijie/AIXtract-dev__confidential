import os
import xml.etree.ElementTree as ET
from typing import List, Optional

from readers.core import BaseReader
from utils import run_shell_command


class XMLParser(BaseReader):
    """
    XMLParser class for parsing XML files.
    """

    def _get_data(self, path: str, only_text: bool = True) -> List[str]:
        """
        Extracts and flattens all text content from `<text>` tags under `<pdf2xml>` in the XML file,
        including any nested tags like `<b>`, `<i>`, etc. Then, sorts them by length in descending order.

        Args:
            path (str): Path to the XML file.
            only_text (bool): If True, only extract text content. Defaults to True.

        Returns:
            List[str]: List of all text content found within `<text>` tags.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        if not path.endswith(".xml"):
            raise ValueError(f"Expected an XML file, but got {path}")

        tree = ET.parse(path)
        root = tree.getroot()

        if root.tag != "pdf2xml":
            raise ValueError(f"Expected root tag <pdf2xml>, but got <{root.tag}>")

        fragments = []
        if only_text:
            for elem in root.iter("text"):
                xml_str = ET.tostring(elem, encoding="unicode")
                fragments.append(xml_str)
        else:
            for elem in root.iter():
                xml_str = ET.tostring(elem, encoding="unicode")
                fragments.append(xml_str)
        return fragments

    def _read(self, path: str, save_path: Optional[str] = None) -> List[str]:
        """
        Read data from the given PDF file and convert it to XML using pdftohtml.

        Args:
            path (str): The path to the PDF file.
            save_path (Optional[str]): Optional path to save the XML file.

        Returns:
            List[str]: List of all text content found within `<text>` tags.
        Raises:
            FileNotFoundError: If the PDF file does not exist.
            Exception: If the command fails.
        """

        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        try:
            if not save_path:
                filename_wo_ext = os.path.splitext(os.path.basename(path))[0]
                base_dir = os.path.dirname(path)
                save_folder = os.path.join(base_dir, filename_wo_ext)
                os.makedirs(save_folder, exist_ok=True)
                save_path = os.path.join(save_folder, filename_wo_ext + ".xml")
            self.save_path = save_path
            command = f"pdftohtml -xml {path} {save_path}"

            run_shell_command(command)
            return self._get_data(save_path)

        except Exception as e:
            raise Exception(f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    path = (
        "/mnt/other/SmartDataTransform-dev__confidential/data/EMPU_3401_Datasheet.pdf"
    )
    xml_parser = XMLParser(path=path)

    print(xml_parser.row_data)
