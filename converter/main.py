import json
from typing import List, Union

from jinja2 import Template

from utils import chat


class Converter:
    def __init__(self, model: str, **kwargs):
        self.model = model
        self.url = kwargs.get("url", "http://127.0.0.1:6589/model_server/api/")
        self.prompt = kwargs.get(
            "prompt",
            """The following XML content was converted from a PDF using `pdf2xml`. Your task is to extract structured information from this XML based on the `<text>` tags, focusing on the actual text content and its positions (`top`, `left`).
            ### XML Content:
            ```xml
            {{xml_content}}
            ```
            Please convert the extracted information into a well-structured JSON format, organized by section headers and their corresponding key-value pairs. Do not include any attribute metadata in the JSON. Ensure that the JSON syntax is valid, with proper indentation, brackets, and quotation marks.
            Output only the JSON.""",
        )
        self.template = Template(self.prompt)

    def extract_json_blocks(self, text_blocks: List[str]) -> List[dict]:
        """
        Extracts JSON blocks from the given text blocks.
        Args:
            text_blocks (List[str]): List of text blocks to extract JSON from.
        Returns:
            List[dict]: List of extracted JSON objects.
        """
        parsed_results = []

        for block in text_blocks:
            try:
                cleaned = block.strip().strip("```").replace("json\n", "", 1).strip()

                parsed = json.loads(cleaned)

                parsed_results.append(parsed)
            except json.JSONDecodeError as e:
                print(f"[Warning] JSON decode failed: {e}")
                continue
        return parsed_results

    def __call__(
        self, datas: List, format: str = "text", **kwargs
    ) -> Union[List[str], List[dict]]:
        """
        Converts the given XML data to JSON format using a language model.
        Args:
            datas (List): List of XML data to convert.
            format (str): Format of the output. Can be "text" or "dict".
            **kwargs: Additional arguments for the conversion.
        Returns:
            Union[List[str], List[dict]]: Converted data in the specified format.
        """

        results = []
        for data in datas:
            rendered1 = self.template.render(xml_content=str(data))
            request_data = {
                "model": self.model,
                "messages": [{"role": "user", "content": rendered1}],
                "stream": False,
            }

            gen_text = ""

            for res in chat(request_data=request_data, ollama_url=self.url):
                if isinstance(res, str):
                    gen_text += res

            print(gen_text)
            results.append(gen_text)

        if format == "dict":
            return self.extract_json_blocks(results)
        return results
