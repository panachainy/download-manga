import requests
from bs4 import BeautifulSoup


def get_image_link_from(url: str, alt: str) -> list[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img', alt=True)

    altLinks: list[str] = []

    for x in soup.find_all('img', alt=True):  # we find all img alt names
        if x['alt'].__contains__(alt):  # if alt name matchs with your numbers
            altLinks.append(x.get('src'))  # adding into list

    return altLinks
