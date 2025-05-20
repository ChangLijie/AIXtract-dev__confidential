import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, List, Union

from metrics.functions.core import BaseMetric


class Evaluator:
    def __init__(
        self,
        gt_data: Union[Path, List[str]],
        data: Union[Path, List[str]],
        metrics: BaseMetric,
        *args,
        **kwargs,
    ):
        self.gt_data = gt_data
        self.data = data
        self.metrics = metrics

    def _read_and_flatten_xml(
        self,
        xml_data: Union[Path, List[str], str] = None,
    ) -> List[str]:
        """
        Extracts and flattens all text content from <text> tags under <pdf2xml>,
        including nested tags like <b>, <i>, etc. Sorts by length descending.

        Args:
            xml_data (Union[Path, List[str], str]): Either path to XML file or list of XML lines.

        Returns:
            List[str]: Sorted flat list of all text content found within <text> tags.
        """
        if isinstance(xml_data, list):
            content = "<pdf2xml>\n" + "".join(xml_data) + "\n</pdf2xml>"
            root = ET.fromstring(content)
        else:
            if isinstance(xml_data, str):
                xml_data = Path(xml_data)
            tree = ET.parse(xml_data)
            root = tree.getroot()

            if root.tag != "pdf2xml":
                raise ValueError(f"Expected root tag <pdf2xml>, but got <{root.tag}>")

        fragments = [
            frag.strip()
            for elem in root.iter("text")
            for frag in elem.itertext()
            if frag.strip()
        ]

        return sorted(fragments, key=len, reverse=True)

    def _read_and_flatten_json(self, data: Union[str, List[dict]]) -> List[str]:
        """
        Reads a JSON file and flattens its contents into a list of strings.
        This function handles both string paths to JSON files and lists of dictionaries.

        Args:
            data (Union[str, List[dict]]): Path to the JSON file or a list of dictionaries.

        Returns:
            List[str]: A list of flattened strings from the JSON data.

        Raises:
            ValueError: If data is neither a string nor a list of dictionaries.
            FileNotFoundError: If the JSON file does not exist.
        """
        if isinstance(data, list):
            # If data is already a list of dictionaries, flatten it directly
            merged = {}
            for d in data:
                for k, v in d.items():
                    if k not in merged:
                        merged[k] = v
            data = merged
        else:
            # If data is a string, read the JSON file
            if not isinstance(data, str):
                raise ValueError("data must be a string or a list of dictionaries.")
            if not data.endswith(".json"):
                raise ValueError(f"Expected a JSON file, but got {data}")
            if not os.path.exists(data):
                raise FileNotFoundError(f"The file {data} does not exist.")
            with open(data, "r", encoding="utf-8") as f:
                data: dict = json.load(f)

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

    def __call__(self) -> float:
        """
        Evaluates the similarity between the ground truth data and the generated data.
        This function uses the specified metric to calculate the similarity score.
        Returns:
            float:  The similarity score between the ground truth and generated data.
        Raises:
            ValueError: If the metric is not found.
        """
        score = self.metrics.calculate(
            xml_list=self._read_and_flatten_xml(self.gt_data),
            json_list=self._read_and_flatten_json(self.data),
        )
        return score
