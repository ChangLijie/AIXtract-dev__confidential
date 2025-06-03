import json

from jinja2 import StrictUndefined, Template, UndefinedError

from GenAIServices import GenAIOperator, OllamaHandler


class Transform:
    def __init__(
        self,
        model_name: str,
        model_url: str = "http://127.0.0.1:6589/model_server/",
        **kwargs,
    ):
        self.model_name = model_name
        self.model_url = model_url

        self.gen_ai = OllamaHandler(url=self.model_url)

    def extract_json_blocks(self, text_blocks: str) -> dict:
        """
        Extracts JSON blocks from the given text blocks.

        Args:
            text_blocks (str): text blocks to extract JSON from.

        Returns:
            dict: dict of extracted JSON objects.

        Raises:
            Failed to parse JSON
        """

        try:
            parsed = json.loads(text_blocks)
            return parsed
        except json.JSONDecodeError as e:
            raise e

    def generate_json(
        self,
        gen_ai_service: GenAIOperator,
        request_data: dict,
        max_retries: int,
    ) -> str:
        """
        Generates a result with json type of the given data using a language model.

        Args:
            gen_ai_service (GenAIOperator): The language model service to use.
            request_data (dict): The request data for the language model.
            max_retries (int): Maximum number of retries for generating a valid JSON.

        Returns:
            str: The generated result in JSON format.

        Raises:
            ValueError:
                - Request data must be a dictionary.
                -
                - gen_ai_service must be an instance of GenAIOperator.
                - Request data must contain 'messages'.
            RuntimeError:
                Invalid JSON format after max_retries times.
            Exception:
                An error occurred while get summary.

        """
        if not isinstance(request_data, dict):
            raise ValueError("Request data must be a dictionary.")

        if not gen_ai_service:
            raise ValueError("gen_ai_service must be an instance of GenAIOperator.")

        if not request_data.get("messages"):
            raise ValueError("Request data must contain 'messages'.")

        if not request_data.get("model"):
            request_data["model"] = self.model_name

        if not request_data.get("stream"):
            request_data["stream"] = False

        if not request_data.get("ollama_url"):
            request_data["ollama_url"] = self.model_url

        try:
            copy_max_retries = max_retries
            while max_retries > 0:
                gen_text = ""
                for res in gen_ai_service.chat(request_data=request_data):
                    if isinstance(res, str):
                        gen_text += res
                cleaned = gen_text.strip().strip("```").replace("json\n", "", 1).strip()
                try:
                    json.loads(cleaned)
                    return json.loads(cleaned)
                except Exception:
                    max_retries -= 1
            raise RuntimeError(f"Invalid JSON format after {copy_max_retries} retries.")
        except Exception as e:
            raise e

    def process(
        self,
        data: dict,
        prompt: str = """The following XML content was converted from a PDF using `pdf2xml`. Your task is to extract structured information from this XML based on the `<text>` tags, focusing on the actual text content and its positions (`top`, `left`).
            ### XML Content:
            ```xml
            {{xml_content}}
            ```
            Please convert the extracted information into a well-structured JSON format, organized by section headers and their corresponding key-value pairs. Do not include any attribute metadata in the JSON. Ensure that the JSON syntax is valid, with proper indentation, brackets, and quotation marks.
            Output only the JSON.""",
        max_retries: int = 5,
        **kwargs,
    ) -> dict:
        """
        Processes the given data to extract structured information from XML content.
        This method iterates through the provided data, applies the template to each section of XML content, and generates a summary using the specified language model.
        It returns a dictionary containing the processed data, with each page's content summarized and structured.

        Args:
            data (dict): A dictionary where keys are page identifiers and values are containing upper and lower section data.
            prompt (str): The Jinja2 template string. It must include the variable `{{ xml_content }}` for rendering. Default: '"The following XML content was converted from a PDF using `pdf2xml`. Your task is to extract structured information from this XML based on the `<text>` tags, focusing on the actual text content and its positions (`top`, `left`).
            ### XML Content:
            ```xml
            {{xml_content}}
            ```
            Please convert the extracted information into a well-structured JSON format, organized by section headers and their corresponding key-value pairs. Do not include any attribute metadata in the JSON. Ensure that the JSON syntax is valid, with proper indentation, brackets, and quotation marks.
            Output only the JSON."'
            max_retries (int): Maximum number of retries for generating a valid JSON.
            kwargs (dict): Additional keyword arguments for processing.


        Returns:
            dict: A dictionary containing the processed data, where each key is a page identifier and the value is the structured summary of the XML content.
        Raises:
            ValueError:
                - max_retries must be a positive integer
                - Prompt missing required template variable.
            Exception:
                An error occurred while process data transform.
        """
        try:
            page_data = {}
            if not isinstance(max_retries, int) or max_retries <= 0:
                raise ValueError("max_retries must be a positive integer.")
            template = Template(prompt, undefined=StrictUndefined)
            for page in data:
                upper_data, lower_data = data[page]
                page_data[page] = {}
                for num, section_data in enumerate(
                    [data[page][upper_data], data[page][lower_data]]
                ):
                    try:
                        rendered1 = template.render(xml_content=str(section_data))
                    except UndefinedError as e:
                        raise ValueError(
                            f"Prompt missing required template variable: {e}"
                        )
                    request_data = {
                        "model": self.model_name,
                        "messages": [{"role": "user", "content": rendered1}],
                        "stream": False,
                    }
                    gen_text = self.generate_json(
                        gen_ai_service=self.gen_ai,
                        request_data=request_data,
                        max_retries=max_retries,
                    )
                    # print(gen_text, "\n*******************\n")
                    # if format == "dict":
                    #     gen_text = self.extract_json_blocks(gen_text)
                    page_data[page].update({num: gen_text})

            return page_data
        except Exception as e:
            raise Exception(
                f"An error occurred while process data transform: {e}"
            ) from e
