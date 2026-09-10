from fastapi import FastAPI
from day1_for_fastapi.services.main_service import chat as s_chat

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/chat")
async def chat(message:str):
    result = await s_chat(message)
    return result