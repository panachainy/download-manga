
import utils.model as model
import json
from typing import List
import services.manga_a as manga_a


class downloadManga:
    def load(self):
        with open("config.json") as f:
            data = json.load(f)

        imageConfigs = model.ImageConfig.formJson(data)

        for obj in imageConfigs:
            print(obj.url, obj.alt, obj.folder)
            manga_a.downloadFromMangaA(obj.url, obj.alt, obj.folder)
