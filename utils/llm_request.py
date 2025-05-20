import json
import time
from typing import Generator

import httpx


def chat(request_data: dict, ollama_url: str) -> Generator[str, None, None]:
    """Generates a chat stream from the Ollama API.
    Args:
        request_data (dict): The request data to send to the API.
        ollama_url (str): The base URL of the Ollama API.
    Yields:
        str: The generated text from the API.
    Example:
        request_data = {
            "model": "llama3.2:1b",
            "messages": [{"role": "user", "content": "how r u?"}],
        }
        for res in chat(request_data=request_data, ollama_url="http://
    Raises:
        RuntimeError: If the response status code is not 200.
        json.JSONDecodeError: If the response cannot be decoded as JSON.
        BaseException: For any other exceptions that occur during the request.
    """

    try:
        with httpx.stream(
            "POST", url=ollama_url + "chat", json=request_data, timeout=None
        ) as response:
            response.encoding = "utf-8"
            if response.status_code != 200:
                raise RuntimeError(f"Unexpected error: {response.status_code}")
            else:
                if response.headers.get("Transfer-Encoding") == "chunked":
                    for chunk in response.iter_lines():
                        if chunk:
                            try:
                                yield json.loads(chunk)["message"]["content"]
                            except json.JSONDecodeError:
                                yield "Error: Failed to decode JSON response."
                else:
                    # If the response is not chunked, read the entire conten
                    content = response.read().decode("utf-8")
                    try:
                        data = json.loads(content)
                        yield data["message"]["content"]
                    except (json.JSONDecodeError, KeyError):
                        yield f"Error: Invalid full JSON response\n{content}"

    except BaseException as e:
        yield f"Error occurred: {str(e)}\n\n"


if __name__ == "__main__":
    ollama_url = "http://10.204.16.64:6589/model_server/api/"
    model_name = "llama3.2:1b"
    prompt = """how r u?
"""

    request_data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
    }
    start_time = time.time()
    gen_text = ""

    for res in chat(request_data=request_data, ollama_url=ollama_url):
        if isinstance(res, str):
            gen_text += res

    print(gen_text)

    print(f"\n time:{(time.time() - start_time)}")
