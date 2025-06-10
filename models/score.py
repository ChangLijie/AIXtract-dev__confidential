from typing import Dict, Union

from pydantic import BaseModel


class Scores(BaseModel):
    pages: Dict[Union[int, str], float]
