from fastapi import APIRouter, Request, HTTPException, Response
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx


router = APIRouter(prefix="/hasura", tags=["hasura"])
# --------------------
# Hasuraクライアント定義
# --------------------
class HasuraClient:
    def __init__(self, url: str, admin_secret: str):
        self.url = url
        self.headers = {
            "x-hasura-admin-secret": admin_secret,
            "Content-Type": "application/json"
        }

    async def execute(self, query: str, variables: dict):
        async with httpx.AsyncClient() as client:
            res = await client.post(
                self.url,
                json={"query": query, "variables": variables},
                headers=self.headers
            )
            res.raise_for_status()
            return res.json()["data"]

    async def insert_chat(self, item: dict):
        query = """
        mutation InsertChat($object: chat_history_insert_input!) {
          insert_chat_history_one(object: $object) {
            id
            ownerid
            messages
            status
            soundRecord
            isread
            status_created
          }
        }
        """
        return (await self.execute(query, {"object": item}))["insert_chat_history_one"]

    async def get_chat(self, id: int):
        query = """
        query GetChat($id: Int!) {
          chat_history_by_pk(id: $id) {
            id
            ownerid
            messages
            status
            soundRecord
            isread
            status_created
          }
        }
        """
        return (await self.execute(query, {"id": id}))["chat_history_by_pk"]

    async def update_chat(self, id: int, changes: dict):
        query = """
        mutation UpdateChat($id: Int!, $changes: chat_history_set_input!) {
          update_chat_history_by_pk(pk_columns: {id: $id}, _set: $changes) {
            id
            messages
            status
            isread
          }
        }
        """
        return (await self.execute(query, {"id": id, "changes": changes}))["update_chat_history_by_pk"]

    async def delete_chat(self, id: int):
        query = """
        mutation DeleteChat($id: Int!) {
          delete_chat_history_by_pk(id: $id) {
            id
          }
        }
        """
        return (await self.execute(query, {"id": id}))["delete_chat_history_by_pk"]

# --------------------
# FastAPI アプリ定義
# --------------------
app = FastAPI()

# Hasura設定（自分の環境に置き換えてください）
HASURA_URL = "https://your-hasura-instance/v1/graphql"
HASURA_ADMIN_SECRET = "your-admin-secret"
client = HasuraClient(HASURA_URL, HASURA_ADMIN_SECRET)

# --------------------
# Pydanticモデル
# --------------------
class ChatHistoryCreate(BaseModel):
    ownerid: str
    messages: str
    status: str
    soundRecord: str

class ChatHistoryUpdate(BaseModel):
    messages: str | None = None
    status: str | None = None
    isread: bool | None = None

# --------------------
# ルート
# --------------------
@router.post("/chat_history")
async def create_chat(item: ChatHistoryCreate):
    try:
        return await client.insert_chat(item.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat_history/{id}")
async def get_chat(id: int):
    try:
        return await client.get_chat(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/chat_history/{id}")
async def update_chat(id: int, item: ChatHistoryUpdate):
    try:
        return await client.update_chat(id, {k: v for k, v in item.dict().items() if v is not None})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat_history/{id}")
async def delete_chat(id: int):
    try:
        deleted = await client.delete_chat(id)
        return {"deleted_id": deleted["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
