
import utils.model as model
import utils.scrapping as scrapping
import json
from typing import List
import services.manga_a as manga_a


class downloadManga:
    def load(self):
        with open("config.json") as f:
            data = json.load(f)

        imageConfigs = model.ImageConfig.formJson(data)

        for imageConfig in imageConfigs:
            manga_a.downloadFromMangaA(
                imageConfig.url, imageConfig.alt, imageConfig.folder)

    def t(self):
        with open("config.json") as f:
            data = json.load(f)
        imageConfigs = model.ImageConfig.formJson(data)

        for imageConfig in imageConfigs:
            chapterLinks = scrapping.get_chapter_link_from(imageConfig.url)
            for chapterLink in chapterLinks:
                folderPath = 'images/' + chapterLink.folder + '/' + chapterLink.chapter + '/'
                # print('folderPath',folderPath)
                # print(chapterLink.url, imageConfig.alt, folderPath)
                manga_a.downloadFromMangaA(chapterLink.url, imageConfig.alt, folderPath)
