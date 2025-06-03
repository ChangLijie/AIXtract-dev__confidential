import os
from pathlib import Path
from typing import Optional, Union

from readers.core import BaseReader
from readers.xmlparser import XMLParser
from utils import commandline_executor


class PDFParser(BaseReader):
    """
    PDFParser class for parsing PDF files.
    """

    def process(
        self, path: Union[Path, str], save_path: Optional[Union[Path, str]] = None
    ) -> dict:
        """
        Read data from the given PDF file and convert it to XML using pdftohtml.

        Args:
            path (Union[Path, str]): The path to the PDF file.
            save_path (Optional[Union[Path, str]]): Optional path to save the XML file.

        Returns:
            dict: A dict of pages, where each page is represented as a list of xml contents.

        Raises:
            TypeError:
                path with unexpected type.
            FileNotFoundError:
                If the PDF file does not exist.
            ValueError:
                The file extension error.
            Exception:
                An error occurred while processing the file.
        """

        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise TypeError(f"Expected str or Path, but got {type(path).__name__}")

        if save_path:
            if isinstance(save_path, str):
                save_path = Path(save_path)
            elif not isinstance(save_path, Path):
                raise TypeError(f"Expected str or Path, but got {type(path).__name__}")

        if not path.exists():
            raise FileNotFoundError(f"The file {path} does not exist.")
        if not path.suffix.lower() == ".pdf":
            raise ValueError(f"Expected an PDF file, but got {path}")
        try:
            if not save_path:
                filename_wo_ext = path.stem
                base_dir = path.parent
                save_folder = base_dir / filename_wo_ext
                os.makedirs(save_folder, exist_ok=True)
                save_path = save_folder / f"{filename_wo_ext}.xml"
            self.save_path = save_path
            command = f"pdftohtml -xml {path} {save_path}"

            commandline_executor.run(command)
            xml_parser = XMLParser()
            return xml_parser.process(save_path)

        except Exception as e:
            raise Exception(f"An error occurred while processing the file: {e}") from e


if __name__ == "__main__":
    path = (
        "/mnt/other/SmartDataTransform-dev__confidential/data/EMPU_3401_Datasheet.pdf"
    )
    xml_parser = PDFParser()

    print(xml_parser.process(path=path))
