from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from src.models import KnowledgeCreate, SearchRequest, SearchResponse
from src.store import KnowledgeStore

app = FastAPI(title="Enterprise RAG Knowledge Platform")
store = KnowledgeStore()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/knowledge")
def ingest_item(payload: KnowledgeCreate):
    return store.add_item(payload)


@app.get("/knowledge/{item_id}", responses={404: {"description": "Knowledge item not found"}})
def get_item(item_id: str):
    item = store.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Knowledge item not found")
    return item


@app.post("/search")
def search_items(payload: SearchRequest) -> SearchResponse:
    return store.search(payload.question)


@app.websocket("/ws/knowledge")
async def knowledge_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_json({"event": "indexed", "message": message})
    except WebSocketDisconnect:
        return
