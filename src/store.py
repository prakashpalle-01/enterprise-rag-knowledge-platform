from src.models import KnowledgeCreate, KnowledgeRecord, SearchMatch, SearchResponse


def _tokenize(text: str) -> set[str]:
    return {token.strip(".,:;!?()[]{}\"'`).lower() for token in text.split() if token.strip()}


def _chunk_text(text: str, max_words: int = 50) -> list[str]:
    words = text.split()
    return [" ".join(words[index : index + max_words]) for index in range(0, len(words), max_words)] or [text]


class KnowledgeStore:
    def __init__(self) -> None:
        self._items: dict[str, KnowledgeCreate] = {}

    def add_item(self, payload: KnowledgeCreate) -> KnowledgeRecord:
        self._items[payload.item_id] = payload
        return KnowledgeRecord(**payload.model_dump(), chunk_count=len(_chunk_text(payload.body)))

    def get_item(self, item_id: str) -> KnowledgeRecord | None:
        item = self._items.get(item_id)
        if item is None:
            return None
        return KnowledgeRecord(**item.model_dump(), chunk_count=len(_chunk_text(item.body)))

    def search(self, question: str, limit: int = 3) -> SearchResponse:
        question_terms = _tokenize(question)
        matches: list[SearchMatch] = []

        for item in self._items.values():
            for snippet in _chunk_text(item.body):
                snippet_terms = _tokenize(snippet)
                if not snippet_terms:
                    continue
                overlap = len(question_terms & snippet_terms)
                if overlap == 0:
                    continue
                score = round(overlap / max(len(question_terms), 1), 3)
                matches.append(SearchMatch(item_id=item.item_id, title=item.title, snippet=snippet, score=score))

        matches.sort(key=lambda item: item.score, reverse=True)
        matches = matches[:limit]
        answer = matches[0].snippet if matches else "No relevant knowledge item was found."
        return SearchResponse(question=question, answer=answer, matches=matches)