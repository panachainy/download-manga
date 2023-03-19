
import utils.model as model
import utils.scrapping as scrapping
import json
from typing import List
import services.manga_a as manga_a
import os
from PIL import Image
import utils.dir as dir
from natsort import natsorted, ns


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

        print('Start download images..')

        for imageConfig in imageConfigs:
            chapterLinks = scrapping.get_chapter_link_from(imageConfig.url)
            for chapterLink in chapterLinks:
                folderPath = 'pdfs/' + chapterLink.folder + '/'
                chapterPath = folderPath + chapterLink.chapter + '/'
                manga_a.downloadFromMangaA(
                    chapterLink.url, imageConfig.alt, chapterPath)

        print('Start convert images to pdfs..')

        for imageConfig in imageConfigs:
            chapterLinks = scrapping.get_chapter_link_from(imageConfig.url)
            for chapterLink in chapterLinks:
                folderPath = 'pdfs/' + chapterLink.folder + '/'
                chapterPath = folderPath + chapterLink.chapter + '/'

                image_list = []

                imageFiles = natsorted(os.listdir(chapterPath), alg=ns.PATH)

                for imageFile in imageFiles:
                    filePath = chapterPath + imageFile
                    print('filePath', filePath)

                    image_list.append(Image.open(filePath).convert('RGB'))

                pdfFolder = folderPath + "/newPDF/" + chapterLink.folder
                dir.create_folder(pdfFolder)
                pdfPath = pdfFolder + "/" + chapterLink.chapter + ".pdf"

                firstImage = image_list[0]
                del image_list[0]

                firstImage.save(pdfPath, save_all=True,
                                append_images=image_list)
                print('Saved:', pdfPath)
