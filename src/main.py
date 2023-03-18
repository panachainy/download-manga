import dir
import image
import scrapping

import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')
alt = os.getenv('ALT')
folder = os.getenv('FOLDER')

if not url:
    print('URL environment variable is not set')
    exit(1)
elif not alt:
    print('ALT environment variable is not set')
    exit(1)
elif not folder:
    print('FOLDER environment variable is not set')
    exit(1)

fileFormat = '{:03d}'

listLink = scrapping.get_image_link_from(url, alt)
folderPath = 'images/' + folder + '/'
dir.create_folder(folderPath)

page = 1
for link in listLink:
    full_path = image.get_full_path(folderPath, fileFormat.format(page))
    print('full_path', full_path)
    image.download_image_v2(link, full_path)
    page = page + 1
