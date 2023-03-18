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


listLink = scrapping.get_image_link_from(url, alt)

dir.create_folder('images/' + folder)

full_path = image.get_full_path('images/', 'file_name')
image.download_image_v2(listLink[0], full_path)
