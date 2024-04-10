from fastapi import APIRouter, params
from fastapi.responses import JSONResponse

from app.resources.errors import CRASH, NOT_FOUND
from ...handlers import ResponseHandler
from typing import Any, Dict, List, Union, Optional
from .manga_reader import (
     get_featured_mangas,
     get_filter_mangas,
     get_manga,
     get_panels
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
     rating_type: Optional[str] = None,
     page: Optional[str] = "1"
     ) -> JSONResponse:
     data: Union[Dict[str, Union[List, Dict]], int] = await get_filter_mangas(params={
          "language": language,
          "genres": genres,
          "rating_type": rating_type,
          "sort": sort,
          "status": status,
          "type": read_type,
          "page": page,
     })

     if data == CRASH:
          return response.crash_response()

     return response.successful_response({"data": data })

@router.get("/genre/{genre_ID}")
async def genre(genre_ID, page: Optional[str] = "1") -> JSONResponse:
     data: Union[Dict[str, Union[List, Dict]], int] = await get_filter_mangas(endpoint=f"/genre/{genre_ID}", params={ "page": page })

     if data == CRASH:
          return response.crash_response()

     return response.successful_response({"data": data })

@router.get("/type/{type_ID}")
async def get_type(type_ID, page: Optional[str] = "1") -> JSONResponse:
     data: Union[Dict[str, Union[List, Dict]], int] = await get_filter_mangas(endpoint=f"/type/{type_ID}", params={ "page": page })

     if data == CRASH:
          return response.crash_response()

     return response.successful_response({"data": data })

@router.get("/read/{manga_ID}/{lang}/{chapter_ID}")
async def read(manga_ID: str, chapter_ID: str, lang: str) -> JSONResponse:
     data: Union[Dict[str, str], int] = await get_panels(manga_ID=manga_ID, chapter_ID=chapter_ID, lang=lang)

     if data == NOT_FOUND:
          return response.not_found_response()

     return response.successful_response({"data": data })

@router.get("/{manga_ID}")
async def manga(manga_ID: str) -> JSONResponse:
     data: Union[Dict[str, str], int] = await get_manga(manga_ID=manga_ID)

     if data == NOT_FOUND:
          return response.not_found_response()

     return response.successful_response({"data": data })


