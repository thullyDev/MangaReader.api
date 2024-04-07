from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ...handlers import ResponseHandler
from typing import Any, Dict, List, Union
from .manga_reader import get_featured_mangas

router: APIRouter = APIRouter(prefix="/manga")
response: ResponseHandler = ResponseHandler()

@router.get("/features")
async def features() -> JSONResponse:
     data: Union[List[Dict[str, str]], int] = await get_featured_mangas()
     return response.successful_response({"data": data })

