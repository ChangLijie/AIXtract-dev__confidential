import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, List, Union

from metrics.functions.core import BaseMetric


class Validate:
    def __init__(
        self,
        metrics: BaseMetric,
        *args,
        **kwargs,
    ):
        self.metrics = metrics

    def _read_and_flatten_xml(
        self,
        xml_data: Union[Path, dict, str] = None,
    ) -> List[str]:
        """
        Extracts and flattens all text content from <text> tags under <pdf2xml>,
        including nested tags like <b>, <i>, etc. Sorts by length descending.

        Args:
            xml_data (Union[Path, List[str], str]): Either path to XML file or list of XML lines.

        Returns:
            List[str]: Sorted flat list of all text content found within <text> tags.

        Exception:
            An error occurred while read and flatten xml data.
        """
        try:
            if isinstance(xml_data, list):
                content = "<pdf2xml>\n" + "".join(xml_data) + "\n</pdf2xml>"
                root = ET.fromstring(content)
            else:
                if isinstance(xml_data, str):
                    xml_data = Path(xml_data)
                tree = ET.parse(xml_data)
                root = tree.getroot()

                if root.tag != "pdf2xml":
                    raise ValueError(
                        f"Expected root tag <pdf2xml>, but got <{root.tag}>"
                    )

            fragments = [
                frag.strip()
                for elem in root.iter("text")
                for frag in elem.itertext()
                if frag.strip()
            ]

            return sorted(fragments, key=len, reverse=True)
        except Exception as e:
            raise Exception(f"An error occurred while read and flatten xml data: {e}")

    def _read_and_flatten_json(self, data: dict) -> List[str]:
        """
        Reads a JSON file and flattens its contents into a list of strings.
        This function handles both string paths to JSON files and lists of dictionaries.

        Args:
            data (Union[str, List[dict]]): Path to the JSON file or a list of dictionaries.

        Returns:
            List[str]: A list of flattened strings from the JSON data.

        Raise:
            Exception:
                An error occurred while read and flatten json data.
        """
        try:
            flattened_json = []

            def _flatten(value: Any) -> None:
                if isinstance(value, dict):
                    for inner_k, inner_v in value.items():
                        flattened_json.append(str(inner_k).strip())
                        _flatten(inner_v)
                elif isinstance(value, list):
                    for item in value:
                        if s := str(item):
                            flattened_json.append(s.strip())
                else:
                    if s := str(value):
                        flattened_json.append(s.strip())

            for k, v in data.items():
                flattened_json.append(str(k).strip())
                _flatten(v)

            return flattened_json
        except Exception as e:
            raise Exception(f"An error occurred while read and flatten json data: {e}")

    def process(
        self,
        gt_data: dict,
        data: dict,
    ) -> float:
        """
        Evaluates the similarity between the ground truth data and the generated data.
        This function uses the specified metric to calculate the similarity score.
        Returns:
            float:  The similarity score between the ground truth and generated data.
        Raises:
            ValueError:
                If the metric is not found.
            Exception:
                An error occurred while calculate score
        """
        try:
            scores = {}
            sum = 0.0

            for page, gt in gt_data.items():
                if data.get(page) is None:
                    raise ValueError(f"Page {page} not found in the generated data.")
                if len(data[page]) == 2:
                    merged = {**data[page][0], **data[page][1]}
                elif len(data[page]) == 1:
                    merged = data[page][1]
                else:
                    raise ValueError(
                        f"Invalid data format for page {page}. Expected 1 or 2 items, got {len(data[page])}."
                    )

                score = self.metrics.calculate(
                    xml_list=self._read_and_flatten_xml(gt),
                    json_list=self._read_and_flatten_json(merged),
                )
                scores.update({page: score})
                sum += score
            scores.update({"mean": sum / len(gt_data)})
            return scores
        except Exception as e:
            raise Exception(f"An error occurred while calculate score: {e}")
