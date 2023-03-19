
import utils.model as model
import utils.scrapping as scrapping
import json
from typing import List
import services.manga_a as manga_a
import os
from PIL import Image
import utils.dir as dir
from natsort import natsorted, ns
from pypdf import PdfMerger


class commands:
    # def load(self):
    #     with open("config.json") as f:
    #         data = json.load(f)

    #     imageConfigs = model.ImageConfig.formJson(data)

    #     for imageConfig in imageConfigs:
    #         manga_a.downloadFromMangaA(
    #             imageConfig.url, imageConfig.alt, imageConfig.folder)

    def download(self, chapter: str = "", skipDownload: bool = False):
        """_summary_

        Args:
            chapter (str): _description_
            download (bool): _description_
        """

        with open("config.json") as f:
            data = json.load(f)
        imageConfigs = model.ImageConfig.formJson(data)

        if skipDownload == False:
            print('Start download images..')
            for imageConfig in imageConfigs:
                chapterLinks = scrapping.get_chapter_link_from(imageConfig.url)
                for chapterLink in chapterLinks:
                    if chapter:
                        if chapterLink.chapter != chapter:
                            continue

                    folderPath = 'pdfs/' + chapterLink.folder + '/'
                    chapterPath = folderPath + chapterLink.chapter + '/'
                    manga_a.downloadFromMangaA(
                        chapterLink.url, chapterPath)
        else:
            print('Skip download')

        print('Start convert images to pdfs..')

        for imageConfig in imageConfigs:
            chapterLinks = scrapping.get_chapter_link_from(imageConfig.url)
            for chapterLink in chapterLinks:
                folderPath = 'pdfs/' + chapterLink.folder + '/'
                chapterPath = folderPath + chapterLink.chapter + '/'

                if chapter:
                    if chapterLink.chapter != chapter:
                        continue

                image_list = []

                imageFiles = natsorted(os.listdir(chapterPath), alg=ns.PATH)

                for imageFile in imageFiles:
                    filePath = chapterPath + imageFile

                    image_list.append(Image.open(filePath).convert('RGB'))

                if not image_list:
                    print('[SKIP] not have image_list in',
                          chapterLink.folder + chapterLink.chapter)
                    continue

                pdfFolder = folderPath + "/newPDF/" + chapterLink.folder
                dir.create_folder(pdfFolder)
                pdfPath = pdfFolder + "/" + chapterLink.chapter + ".pdf"

                firstImage = image_list[0]
                del image_list[0]

                firstImage.save(pdfPath, save_all=True,
                                append_images=image_list)
                print('Saved:', pdfPath)
        print('Done all processes')

    def convertImagesToPDF(self):
        # TODO:
        """_summary_
        convert all manga under `pdfs` to .pdf in each chapter
        """

        return

    def mergePDF(self):
        """_summary_
        Merge PDF follow folder under ./pdfs
        """

        rootPDFs: str = 'pdfs'
        files = natsorted(os.listdir(rootPDFs), alg=ns.PATH)

        for dir in files:
            filePath = os.path.join(rootPDFs, dir)
            if os.path.isdir(filePath):
                newPDfDirPath = os.path.join(filePath, 'newPDF')
                pdfs = natsorted(os.listdir(newPDfDirPath), alg=ns.PATH)

                merger = PdfMerger()
                for pdf in pdfs:
                    pdfPath = os.path.join(newPDfDirPath, pdf)
                    merger.append(pdfPath)

                mergedPDFPath = os.path.join('readypdf', dir + '.pdf')
                merger.write(mergedPDFPath)
                merger.close()
