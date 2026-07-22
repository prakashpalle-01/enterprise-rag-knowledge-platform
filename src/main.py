from fastapi import FastAPI

app = FastAPI(title="Enterprise RAG Knowledge Platform")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
