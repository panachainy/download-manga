
import utils.model as model
import utils.scrapping as scrapping
import json
from typing import List
import services.manga_a as manga_a
import os
from PIL import Image


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
                folderPath = 'pdfs/' + chapterLink.folder + '/'
                chapterPath = folderPath + chapterLink.chapter + '/'
                manga_a.downloadFromMangaA(
                    chapterLink.url, imageConfig.alt, chapterPath)
                image_list = []

                for imageFile in os.listdir(chapterPath):
                    filePath = chapterPath + imageFile

                    image_list.append(Image.open(filePath).convert('RGB'))

                pdfPath = folderPath + chapterLink.chapter + ".pdf"

                firstImage = image_list[0]
                del image_list[0]

                firstImage.save(pdfPath, save_all=True,
                                   append_images=image_list)
                print('Saved:', pdfPath)
