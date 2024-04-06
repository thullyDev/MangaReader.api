from ..handlers import ApiHandler 
from ..resources import BAD_REQUEST
from bs4 import BeautifulSoup

"""
this is old code i reuse, and the code is kinda bad, but it does the job,
if needed feel free to refactor and optimize it
"""

class Scraper:
    def __init__(self, BASE) -> None:
        self.api = ApiHandler(BASE)

    async def get_data(self, blueprint, endpoint="", params={}):
        html = await self.api.get(endpoint, params=params, html=True)

        if html == BAD_REQUEST: return BAD_REQUEST
        
        data = {}
        soup = BeautifulSoup(html, 'html.parser')
        for key, value in blueprint.items():
            data[key] = self.process(soup=soup, blueprint=value)

        return data

    def extract(self, element, config):
        data = {}
        for key, value in config.items():
            data[key] = {}
            selector = value.get("selector")
            return_type = value.get("return_type")
            selected_elements = element.select(selector)

            if return_type == "list": data = []

            for select_element in selected_elements:
                for attr_key, attr_value in value.get("attributes").items():
                    if return_type != "list": 
                        if attr_value == "text_content": 
                            data[key][attr_key] = select_element.text.strip()
                            continue

                        if attr_value == "html": 
                            data[key][attr_key] = str(select_element)
                            continue

                        data[key][attr_key] = select_element.get(attr_value) 
                        continue

                    if attr_value == "text_content": 
                        data.append(select_element.text)
                        continue

                    if attr_value == "html": 
                        data.append(str(select_element))
                        continue

                    data.append(select_element.get(attr_value)) 

        return data

    # processes each parent select, and passes to the children to the extract function
    def process(self, soup, blueprint):
        parent_selector = blueprint.get("parent_selector")
        single_select = blueprint.get("single_select")

        data = {}
        if single_select:
            elements = soup.select(parent_selector)
            attribute = blueprint.get("attribute")
            key = blueprint.get("key")

            for element in elements:
                if attribute == "html": data[key] = str(element); continue
                
                value = element.get(attribute).strip() if attribute != "text_content" else element.text.replace("\n", " ").strip()
                data[key] = value
            
            return data

        elements = soup.select(parent_selector)

        data = [self.extract(element, blueprint["children"]) for element in elements]

        return data