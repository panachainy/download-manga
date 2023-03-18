
import model
import json
# import os
from typing import List
import services.manga_a as manga_a

with open("config.json") as f:
    data = json.load(f)

imageConfigs = model.ImageConfig.formJson(data)

for obj in imageConfigs:
    print(obj.url, obj.alt, obj.folder)
    manga_a.downloadFromMangaA(obj.url, obj.alt, obj.folder)
