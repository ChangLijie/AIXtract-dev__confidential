from difflib import SequenceMatcher
from typing import List

from metrics.functions.core import BaseMetric


class StrSimilarity(BaseMetric):
    def calculate(xml_list: List[str], json_list: List[str]) -> float:
        """Calculates the average similarity between two lists of strings.

        Args:
            xml_list (List[str]): A list of strings extracted from XML content.
            json_list (List[str]): A list of strings extracted from JSON content.

        Returns:
            float: The average similarity score between the XML and JSON strings, rounded to two decimals.
        """
        xml_json_scores = []

        print("(XML string, JSON string, Similarity)")

        for xml_str in xml_list:
            each_json_score = []
            print_json_str = ""

            # Calculate similarity scores between the XML string and all JSON strings
            for idx, json_str in enumerate(json_list):
                if xml_str in json_str:
                    each_json_score.append(
                        (1.0, -1)
                    )  # assign the similarity score as 1 directly
                    print_json_str = json_list[idx]
                    json_list[idx] = json_str.replace(
                        xml_str, "", 1
                    ).strip()  # remove the matched substring
                    break
                else:
                    each_json_score.append(
                        (
                            round(SequenceMatcher(None, xml_str, json_str).ratio(), 2),
                            idx,
                        )
                    )  # use `difflib.SequenceMatcher` for approximate matching

            # Find out the maximum similarity score
            max_score_val = max(each_json_score, key=lambda x: x[0])[0]
            max_score_idx = max(each_json_score, key=lambda x: x[0])[1]
            xml_json_scores.append(max_score_val)
            print(
                f"({xml_str}, {json_list[max_score_idx] if max_score_idx >= 0 else print_json_str}, {xml_json_scores[-1]})"
            )

        return round(sum(xml_json_scores) / len(xml_json_scores), 2)
