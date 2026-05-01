from pydantic import BaseModel
from typing import Optional, List

class SearchResponse(BaseModel):
    query: str
    results: List[dict]
    pagination: dict

class SearchSuggestionResponse(BaseModel):
    query: str
    suggestions: List[str]
