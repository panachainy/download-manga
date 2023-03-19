import utils.dir as dir
import utils.image as imageLib
import utils.scrapping as scrapping
import requests
from bs4 import BeautifulSoup
import utils.model as model
from typing import List


def downloadFromMangaA(url: str, folderPath: str):
    fileFormat = '{:03d}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    readArea = soup.find('div', id="readerarea")
    images = readArea.find_all("img")  # type: ignore

    links: list[str] = []
    for image in images:
        links.append(image.get('src'))

    dir.create_folder(folderPath)

    page = 1
    for link in links:
        full_path = imageLib.get_full_path(
            folderPath, fileFormat.format(page))
        imageLib.download_image_v2(link, full_path)
        page = page + 1
