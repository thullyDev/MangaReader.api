from typing import Any, Dict, List, Optional, Union
from bs4 import BeautifulSoup
from app.handlers.api_handler import ApiHandler
from app.resources.errors import CRASH, NOT_FOUND
from pprint import pprint

api = ApiHandler("https://mangareader.to")

async def get_featured_mangas() -> Union[List[Dict[str, str]], int]:
    response: Any = await api.get(endpoint="/home", html=True)
    
    if type(response) is int:
        return CRASH

    soup = get_soup(html=response)
    items: List = soup.select('.deslide-item')
    data: List[Dict[str, str]] = []

    for item in items:
        slug = item.select('.deslide-cover')[0].get('href')
        description = item.select('.sc-detail > .scd-item.mb-3')[0].text
        image = item.select('.manga-poster-img')[0]
        image_url = image.get('src')
        title = image.get('alt')

        data.append({
            "title": title,
            "image_url": image_url,
            "description": description,
            "slug": slug,
        })

    return data

async def get_filter_mangas(*, endpoint="/filter", params={}) -> Union[Dict[str, Union[List, Dict]], int]:
    filter_data: Dict[str, Optional[str]] = {
        key: value
        for key, value in params.items()
        if value and key in { "type", "score", "rating_type", "sort", "genres", "language", "page" }
    }

    response: Any = await api.get(endpoint=endpoint, params=filter_data, html=True)
    
    if type(response) is int:
        return CRASH

    soup = get_soup(html=response)
    items: List = soup.select('.item.item-spc')
    last_page_link = soup.select('.page-link')[-1]
    pages = last_page_link.text 

    if pages == "»":
        href: Any = last_page_link.get("href")
        pages = href.split("=")[-1]

    page: str = params['page']
    data: List[Dict[str, Union[str, List]]] = []
    
    for item in items:
        genres_elems = item.select(".fdi-item.fdi-cate>a")
        genres: List[Dict[str, str]] = []
        for ele in genres_elems:
            genres.append({
                "name": ele.text,
                "slug": ele.get("href").split('/')[-1]
            })
        chapters = item.select(".chapter>a")[0].get("href").split("-")[-1]
        slug = item.select('.manga-poster')[0].get('href')
        image_data: Dict[str, str] = get_data_from_image(item)
        data.append({
            "chapters": chapters,
            "slug": slug,
            "genres": genres,
            **image_data
        })

    return {
        "mangas": data,
        "pagination": {
            "pages": pages,
            "page": page,
        }
    }


async def get_manga(manga_ID: str) -> Union[Dict[str, Any], int]:
    response: Any = await api.get(endpoint=f"/{manga_ID}", html=True)
    
    if type(response) is int:
        return NOT_FOUND

    soup = get_soup(html=response)
    title: str = soup.select('.manga-name')[0].text

    print("manga-name ==> ", title)

    return {}

def get_soup(html) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')

def get_data_from_image(item):
    image = item.select('.manga-poster-img')[0]
    image_url = image.get('src')
    title = image.get('alt')

    return {
        "title": title,
        "image_url": image_url,
    }
