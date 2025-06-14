# prompt: fastapi route 処理作成　引数は　calat wehth state x

from fastapi import APIRouter, HTTPException

#router = APIRouter()
router = APIRouter(prefix="/leaning", tags=["leaning"])
@router.get("/route/{calat}/{wehth}/{state}/{x}")
async def route(calat: float, wehth: float, state: str, x: int):
    # Validate input parameters
    if not (0.0 <= calat <= 90.0):
        raise HTTPException(status_code=400, detail="Invalid calat value.")
    if not (0.0 <= wehth <= 180.0):
        raise HTTPException(status_code=400, detail="Invalid wehth value.")
    if state not in ["AC", "AL", "AP", ..., "TO"]:
        raise HTTPException(status_code=400, detail="Invalid state value.")
    if not (0 <= x <= 100):
        raise HTTPException(status_code=400, detail="Invalid x value.")

    # Process the request and return a response
    # ...

    return {"result": "OK"}
