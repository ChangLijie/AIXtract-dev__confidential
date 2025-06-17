from typing import Dict

from pydantic import BaseModel


class PageGenerate(BaseModel):
    data: Dict[int, Dict]


class TransformData(BaseModel):
    pages: Dict[int, PageGenerate]
