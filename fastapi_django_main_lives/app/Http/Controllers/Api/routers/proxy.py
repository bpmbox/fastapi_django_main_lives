from fastapi import APIRouter, Request, HTTPException, Response
import httpx

LARAVEL_URL = "http://localhost:8000"
router = APIRouter(prefix="/laravel", tags=["laravel"])

# GET
@router.get("/route/{path:path}")
async def proxy_get(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)
        try:
            proxied = await client.get(f"{LARAVEL_URL}/{path}", headers=headers)
            return Response(
                content=proxied.content,
                status_code=proxied.status_code,
                headers=dict(proxied.headers),
                media_type=proxied.headers.get("content-type")
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request proxy failed: {str(e)}")

# POST
@router.post("/route/{path:path}")
async def proxy_post(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        req_data = await request.body()
        headers = dict(request.headers)
        try:
            proxied = await client.post(f"{LARAVEL_URL}/{path}", headers=headers, content=req_data)
            return Response(
                content=proxied.content,
                status_code=proxied.status_code,
                headers=dict(proxied.headers),
                media_type=proxied.headers.get("content-type")
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request proxy failed: {str(e)}")

# PUT
@router.put("/route/{path:path}")
async def proxy_put(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        req_data = await request.body()
        headers = dict(request.headers)
        try:
            proxied = await client.put(f"{LARAVEL_URL}/{path}", headers=headers, content=req_data)
            return Response(
                content=proxied.content,
                status_code=proxied.status_code,
                headers=dict(proxied.headers),
                media_type=proxied.headers.get("content-type")
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request proxy failed: {str(e)}")

# DELETE
@router.delete("/route/{path:path}")
async def proxy_delete(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)
        try:
            proxied = await client.delete(f"{LARAVEL_URL}/{path}", headers=headers)
            return Response(
                content=proxied.content,
                status_code=proxied.status_code,
                headers=dict(proxied.headers),
                media_type=proxied.headers.get("content-type")
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request proxy failed: {str(e)}")
