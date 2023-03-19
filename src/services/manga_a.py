import utils.dir as dir
import utils.image as image
import utils.scrapping as scrapping

def downloadFromMangaA(url: str, alt: str, folderPath: str):
    fileFormat = '{:03d}'

    listLink = scrapping.get_image_link_from(url, alt)
    dir.create_folder(folderPath)

    page = 1
    for link in listLink:
        full_path = image.get_full_path(folderPath, fileFormat.format(page))
        # print('full_path', full_path)
        image.download_image_v2(link, full_path)
        page = page + 1
