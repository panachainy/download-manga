
import utils.model as model
import utils.scrapping as scrapping
import json
from typing import List
import services.manga_a as manga_a
import os
from PIL import Image
import utils.dir as dirLib
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

        print('Start download images..')
        for imageConfig in imageConfigs:
            chapterLinks = scrapping.get_chapter_link_from(imageConfig.url)
            for chapterLink in chapterLinks:
                if chapter:
                    if chapterLink.chapter != chapter:
                        continue

                folderPath = 'pdfs/' + chapterLink.folder + '/'
                chapterPath = folderPath + chapterLink.chapter + '/'
                try:
                    manga_a.downloadFromMangaA(
                        chapterLink.url, chapterPath)
                    print(f"=== {chapterPath} downloaded ===")
                except Exception as e:
                    print(imageConfig.folder, chapterLink.chapter,
                          'error in:', chapterLink.url, "detail", e)
                    
                    for imageFile in os.listdir(chapterPath):
                        os.remove(os.path.join(chapterPath, imageFile))
                    
                    os.removedirs(chapterPath)

                    continue

        print("=== downloaded ===")

    def makePDFs(self):
        # TODO:
        """_summary_
        convert all manga under `pdfs` to .pdf in each chapter
        """

        rootPDFs: str = 'pdfs'
        files = natsorted(os.listdir(rootPDFs), alg=ns.PATH)
        for dir in files:
            titleDirPath = os.path.join(rootPDFs, dir)
            if os.path.isdir(titleDirPath):
                chapterDirs = natsorted(
                    os.listdir(titleDirPath), alg=ns.PATH)
                for chapterDir in chapterDirs:
                    if chapterDir == 'newPDF':
                        continue

                    chapterDirPath = os.path.join(titleDirPath, chapterDir)

                    image_list = []
                    imageFiles = natsorted(
                        os.listdir(chapterDirPath), alg=ns.PATH)
                    for imageFile in imageFiles:
                        filePath = os.path.join(chapterDirPath, imageFile)
                        image_list.append(Image.open(filePath).convert('RGB'))

                    pdfFolder = os.path.join(titleDirPath, "newPDF")

                    dirLib.create_folder(pdfFolder)

                    pdfPath = os.path.join(pdfFolder, chapterDir + ".pdf")
                    # print('image_list', image_list)
                    # print('pdfPath', pdfPath)
                    firstImage = image_list[0]
                    del image_list[0]
                    firstImage.save(pdfPath, save_all=True,
                                    append_images=image_list)
                    print('Saved:', pdfPath)

    def mergePDFs(self):
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

                def remove_extension(fileName: str):
                    return os.path.splitext(fileName)[0]

                destinationDir = os.path.join('readypdf')

                dirLib.create_folder(destinationDir)
                mergedPDFPath = os.path.join(
                    destinationDir,  f"{dir} {remove_extension(pdfs[0])}-{remove_extension(pdfs[-1])}.pdf")
                merger.write(mergedPDFPath)
                merger.close()
