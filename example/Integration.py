import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from converter import Converter
from evaluator import Evaluator
from metrics import Metrics
from preprocessor import XmlPreProcessor
from readers import XMLParser

if __name__ == "__main__":
    # Example usage
    path = (
        "/mnt/other/SmartDataTransform-dev__confidential/data/EMPU_3401_Datasheet.pdf"
    )
    xml_parser = XMLParser(path=path)
    xml_data = xml_parser.data
    # print(xml_data)

    xml_preprocessor = XmlPreProcessor(data=xml_data)
    preprocessed_data_a, preprocessed_data_b = xml_preprocessor.process()

    # for line in preprocessed_data_a:
    #     print(line)
    # print(f"\n{'-' * 50}\n")
    # for line in preprocessed_data_b:
    #     print(line)

    convert = Converter(
        model="llama3.2:1b", url="http://127.0.0.1:6589/model_server/api/"
    )

    summary_data = convert(
        datas=[preprocessed_data_a, preprocessed_data_b], format="dict"
    )

    # print((summary_data))

    # for line in summary_data:
    #     if isinstance(line, str):
    #         print(line)
    #     else:
    #         for key, value in line.items():
    #             print(f"{key}: {value}")

    metric, settings = Metrics.get("str_similarity")
    evaluator = Evaluator(
        gt_data=preprocessed_data_a + preprocessed_data_b,
        data=summary_data,
        metrics=metric,
    )
    score = evaluator()
    print(f"Similarity score: {score}")
