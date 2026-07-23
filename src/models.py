from pydantic import BaseModel, Field


class KnowledgeCreate(BaseModel):
    item_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class KnowledgeRecord(KnowledgeCreate):
    chunk_count: int


class SearchRequest(BaseModel):
    question: str = Field(min_length=1)


class SearchMatch(BaseModel):
    item_id: str
    title: str
    snippet: str
    score: float


class SearchResponse(BaseModel):
    question: str
    answer: str
    matches: list[SearchMatch]