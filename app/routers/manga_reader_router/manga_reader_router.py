from fastapi import APIRouter, params
from fastapi.responses import JSONResponse
from ...handlers import ResponseHandler
from typing import Any, Dict, List, Union, Optional
from .manga_reader import (
     get_featured_mangas,
     get_filter_mangas
)

router: APIRouter = APIRouter(prefix="/manga")
response: ResponseHandler = ResponseHandler()

@router.get("/features")
async def features() -> JSONResponse:
     data: Union[List[Dict[str, str]], int] = await get_featured_mangas()
     return response.successful_response({"data": data })

@router.get("/filter")
async def filter(
     language: Optional[str] = None, 
     genres: Optional[str] = None, 
     sort: Optional[str] = None, 
     status: Optional[str] = None, 
     read_type: Optional[str] = None, 
     rating_type: Optional[str] = None
     ) -> JSONResponse:
     data: Union[List[Dict[str, str]], int] = await get_filter_mangas(params={
          "language": language,
          "genres": genres,
          "rating_type": rating_type,
          "sort": sort,
          "status": status,
          "type": read_type,

     })
     return response.successful_response({"data": data })

