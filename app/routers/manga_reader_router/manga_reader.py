from typing import Any, Dict, List, Optional, Union
from bs4 import BeautifulSoup
from app.handlers.api_handler import ApiHandler
from app.resources.errors import CRASH, NOT_FOUND
from pprint import pprint
import json

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

    if pages in [ "»", "‹" ]:
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
    image_data = get_data_from_image(soup)
    alt_name: str = soup.select('.manga-name-or')[0].text
    description: str = soup.select('.description')[0].text.strip()
    types = get_data_from_ticks(soup.select(".item.item-title:first-child > a")) 
    magazines = get_data_from_ticks(soup.select(".item.item-title:nth-child(4) > a")) 
    authors = get_data_from_ticks(soup.select(".item.item-title:nth-child(3) > a")) 
    genres = get_data_from_ticks(soup.select(".genres > a")) 
    status = get_data_from_ticks(soup.select(".item.item-title:nth-child(2) > span.name"), is_dynamic=False) 
    published = get_data_from_ticks(soup.select(".item.item-title:nth-child(5) > span.name"), is_dynamic=False) 
    score = get_data_from_ticks(soup.select(".item.item-title:nth-child(6) > span.name"), is_dynamic=False) 
    views = get_data_from_ticks(soup.select(".item.item-title:nth-child(7) > span.name"), is_dynamic=False) 

    characters: list[Dict] = []
    for item in soup.select(".cl-item"):
        image_url = item.select(".character-thumb img")[0].get("src")
        name = item.select(".character-thumb img")[0].get("alt")
        role = item.select(".sub")[0].text

        characters.append({
            "image_url": image_url,
            "name": name,
            "role": role,
        })

    chapters: list[Dict] = []
    for item in soup.select(".chapter-item > a"):
        slug = item.get("href")
        title = item.get("title")

        chapters.append({
            "slug": slug,
            "title": title,
        })


    return {
        "manga": {
            **image_data,
            "alt_name": alt_name,
            "description": description,
            "genres": genres,
            "types": types,
            "magazines": magazines,
            "authors": authors,
            "status": status,
            "published": published,
            "score": score,
            "views": views,
            "characters": characters,
            "chapters": chapters,
        }
    }

async def get_panels(chapter_ID: str) -> Union[Dict[str, List], int]:
    ID: str = chapter_ID.replace("chapter-", "")
    response: Any = await api.get(endpoint=f"/ajax/image/list/chap/{ID}", params={
            "mode": "horizontal",
            "quality": "high",
        }, html=True)

    if type(response) is int:
        return NOT_FOUND

    response = json.loads(response)
    soup = get_soup(html=response.get("html"))
    images_elements = soup.select(".ds-image.shuffled")  
    panels: List[str] = []  
    for image_ele in images_elements:
        image_url = image_ele.get("data-url")
        panels.append(image_url)

    return {
        "panels": panels,
    }

def get_soup(html) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')

def get_data_from_image(item) -> Dict[str, str]:
    image = item.select('.manga-poster-img')[0]
    image_url = image.get('src')
    title = image.get('alt')

    return {
        "title": title,
        "image_url": image_url,
    }

def get_data_from_ticks(items, is_dynamic: bool =True) -> Optional[List[Dict[str, str]]]:
    if not items:
        return None

    if not is_dynamic:
        return items[0].text

    data: List[Dict[str, str]] = []
    for item in items:
        slug = item.get("href").split("/")[-1]
        name = item.text

        data.append({
            "name": name,
            "slug": slug,
        })

    return data