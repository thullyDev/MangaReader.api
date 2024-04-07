from typing import Any, Dict, List, Union
from bs4 import BeautifulSoup
from app.handlers.api_handler import ApiHandler
from app.resources.errors import CRASH
from .blueprints import (
        features_blueprint,
    )

api = ApiHandler("https://mangareader.to")

async def get_featured_mangas() -> Union[List[Dict[str, str]], int]:
    response: Any = await api.get(endpoint="/home", html=True)
    
    if type(response) is int:
        return CRASH

    soup: BeautifulSoup = BeautifulSoup(response, 'html.parser')
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