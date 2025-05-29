import os
from typing import Optional

from readers.core import BaseReader
from readers.xmlparser import XMLParser
from utils import commandline_executor


class PDFParser(BaseReader):
    """
    PDFParser class for parsing PDF files.
    """

    def process(self, path: str, save_path: Optional[str] = None) -> dict:
        """
        Read data from the given PDF file and convert it to XML using pdftohtml.

        Args:
            path (str): The path to the PDF file.
            save_path (Optional[str]): Optional path to save the XML file.

        Returns:
            dict: A dict of pages, where each page is represented as a list of xml contents.

        Raises:
            FileNotFoundError:
                If the PDF file does not exist.
            ValueError:
                The file extension error.
            Exception:
                An error occurred while processing the file.
        """

        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        if not path.endswith(".pdf"):
            raise ValueError(f"Expected an PDF file, but got {path}")
        try:
            if not save_path:
                filename_wo_ext = os.path.splitext(os.path.basename(path))[0]
                base_dir = os.path.dirname(path)
                save_folder = os.path.join(base_dir, filename_wo_ext)
                os.makedirs(save_folder, exist_ok=True)
                save_path = os.path.join(save_folder, filename_wo_ext + ".xml")
            self.save_path = save_path
            command = f"pdftohtml -xml {path} {save_path}"

            commandline_executor.run(command)
            xml_parser = XMLParser()
            return xml_parser.process(save_path)

        except Exception as e:
            raise Exception(f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    path = (
        "/mnt/other/SmartDataTransform-dev__confidential/data/EMPU_3401_Datasheet.pdf"
    )
    xml_parser = PDFParser()

    print(xml_parser.process(path=path))
