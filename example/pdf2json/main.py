import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from converter import Transform
from evaluator import Validate
from metrics import SimilarityMetrics
from preprocessor import XMLPreProcessor
from readers import PDFParser

if __name__ == "__main__":
    import time

    start_t = time.time()  # Allow time for the model server to start
    # Example usage
    path = "./data/EMPU_3401_Datasheet.pdf"
    pdf_parser = PDFParser()
    xml_data = pdf_parser.process(path)

    start_p = time.time()
    xml_preprocessor = XMLPreProcessor()
    preprocessed_data = xml_preprocessor.process(xml_data)

    start_c = time.time()
    convert = Transform(
        model_name="llama3.2:1b", model_url="http://127.0.0.1:6589/model_server/"
    )

    converted_data = convert.process(data=preprocessed_data, format="dict")
    start_e = time.time()
    metric, settings = SimilarityMetrics.get("str_similarity")
    evaluator = Validate(
        metrics=metric,
    )
    # print(f"""\n gt:{xml_data} \n\n\n\n\n s_data:{converted_data}""")
    score = evaluator.process(
        gt_data=xml_data,
        data=converted_data,
    )
    print(f"Similarity score: {score}")

    print(f"""all : {time.time() - start_t}\n
            preprocess : {start_c - start_p}\n
            convert : {start_e - start_c}\n
            evaluate : {time.time() - start_e}\n""")
