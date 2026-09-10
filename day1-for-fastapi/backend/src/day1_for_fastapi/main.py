from fastapi import FastAPI, HTTPException, Query
from day1_for_fastapi.services.main_service import chat as s_chat
from day1_for_fastapi.services.main_service import search as s_search
from day1_for_fastapi.services.models import SearchResponse, StructuredAnswer
from day1_for_fastapi.services.search_service import SearchError

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/chat", response_model=StructuredAnswer)
async def chat(message: str = Query(..., min_length=1)):
    return await s_chat(message)


@app.post("/search", response_model=SearchResponse)
async def search(message: str = Query(..., min_length=1)):
    try:
        return await s_search(message)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except SearchError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
