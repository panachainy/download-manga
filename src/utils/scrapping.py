import requests
from bs4 import BeautifulSoup
import utils.model as model
from typing import List
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

def get_chapter_link_from(url: str) -> List[model.TitleConfig]:
    # print('[======]', requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS)
    # requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'DES-CBC3-SHA'

    # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # print('[======]', requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS)

    # print("==after set DEFAULT_CIPHERS==")
    response = requests.get(url)
    # print("==res==")

    soup = BeautifulSoup(response.text, 'html.parser')
    objs = soup.find_all('div', {"class": "eph-num"})
    title = soup.find('h1', {"class": "entry-title"})

    if not title:
        exit(1)

    # remove first object
    del objs[0]

    titleConfigs: List[model.TitleConfig] = []
    for x in objs:
        titleConfigs.append(model.TitleConfig(
            x.a['href'], title.text, x.span.text))

    return titleConfigs


def get_image_link_from(url: str, alt: str) -> list[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img', alt=True)

    altLinks: list[str] = []

    for image in images:  # we find all img alt names
        # if alt name matchs with your numbers
        if image['alt'].__contains__(alt):
            altLinks.append(image.get('src'))  # adding into list

    return altLinks
