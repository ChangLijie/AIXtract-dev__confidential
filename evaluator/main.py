import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, List, Union

from metrics.functions.core import BaseMetric
from models import PageData, PageGenerate, Scores


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
            raise e

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
            raise e

    def get_mean_score(self, scores: Scores) -> float:
        """
        Get the mean score.

        Args:
            scores (Scores): A dict that contain similarity score from each page.

        Returns:
            float: mean score.

        Raises
            Exception:
                An error occurred while calculate mean.
        """
        try:
            sum_score = 0
            valid_page = 0
            for page, score in scores.pages.items():
                if not isinstance(score, float):
                    continue
                sum_score += score
                valid_page += 1
            return sum_score / valid_page
        except Exception as e:
            return e

    def process(
        self,
        gt_data: PageData,
        data: PageGenerate,
    ) -> Scores:
        """
        Evaluates the similarity between the ground truth data and the generated data.
        This function uses the specified metric to calculate the similarity score.

        Args:
            gt_data (PageData): Ground truth. (from Parser.)
            data (PageGenerate): Validate data. (from Transform.)

        Returns:
            Scores:  The similarity score between the ground truth and generated data.

        Raises:
            ValueError:
                If the metric is not found.
            Exception:
                An error occurred while calculate score
        """
        try:
            scores = Scores(pages={})
            sum = 0.0

            def deep_merge(a: dict, b: dict) -> dict:
                result = a.copy()
                if not isinstance(b, dict):
                    return result
                for key, val in b.items():
                    if (
                        key in result
                        and isinstance(result[key], dict)
                        and isinstance(val, dict)
                    ):
                        result[key] = deep_merge(result[key], val)
                    else:
                        result[key] = val
                return result

            for page_num, page in gt_data.pages.items():
                merged = {}
                for section_id, section_data in data.pages[page_num].data.items():
                    merged = deep_merge(merged, section_data)

                score = self.metrics.calculate(
                    xml_list=self._read_and_flatten_xml(page.data),
                    json_list=self._read_and_flatten_json(merged),
                )

                scores.pages[page_num] = score
                sum += score
            mean = self.get_mean_score(scores)
            scores.pages["mean"] = mean
            return scores
        except Exception as e:
            raise Exception(f"An error occurred while calculate score: {e}") from e
