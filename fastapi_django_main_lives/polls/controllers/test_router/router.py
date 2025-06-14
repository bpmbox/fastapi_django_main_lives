from fastapi import APIRouter, Depends

router = APIRouter(prefix="/routerssample", tags=["choices"])

@router.get("/sample")
def test():
    return True