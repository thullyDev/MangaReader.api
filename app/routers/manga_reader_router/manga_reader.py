from typing import Any, Dict, List, Optional, Union
from bs4 import BeautifulSoup
from app.handlers.api_handler import ApiHandler
from app.resources.errors import CRASH
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

async def get_filter_mangas(*, params={}) -> Union[List[Dict[str, str]], int]:
    filter_data: Dict[str, Optional[str]] = {
        key: value
        for key, value in params.items()
        if value and key in { "type", "score", "rating_type", "sort", "genres", "language" }
    }

    response: Any = await api.get(endpoint="/filter", params=filter_data, html=True)
    
    if type(response) is int:
        return CRASH

    soup = get_soup(html=response)
    items: List = soup.select('.item.item-spc')
    data: List[Dict[str, str]] = []
    
    for item in items:
        genres = item.select(".fdi-item.fdi-cate>a")
        chapters = item.select(".chapter>a")[0].get("href").split("-")[-1]
        slug = item.select('.manga-poster')[0].get('href')
        image_data: Dict[str, str] = get_data_from_image(item)
        data.append({
            "chapters": chapters,
            "slug": slug,
            **image_data
        })

    return data

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
