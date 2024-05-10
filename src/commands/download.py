
from bs4 import BeautifulSoup
import numpy as np
import requests
from utils.deprecated import deprecated
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
import utils.image as imageLib


class commands:
    def load_config(self):
        with open("config.json") as f:
            data = json.load(f)
        imageConfigs = model.ImageConfig.formJson(data)
        for imageConfig in imageConfigs:
            chapterLinks = scrapping.get_chapter_link_from(imageConfig.url)

            folderPath = 'configs/' + chapterLinks[0].folder + "/"
            configPath = folderPath + 'config.json'
            dirLib.create_folder(folderPath)

            for chapterLink in chapterLinks:
                chapterPath = folderPath + chapterLink.chapter + '.json'
                fileFormat = '{:03d}'

                response = requests.get(chapterLink.url)
                soup = BeautifulSoup(response.text, 'html.parser')

                readArea = soup.find('div', id="readerarea")
                images = readArea.find_all("img")  # type: ignore

                links: list[str] = []
                for image in images:
                    links.append(image.get('src'))

                configs = []
                page = 1
                for link in links:
                    full_path = imageLib.get_full_path(
                        'pdfs/' + chapterLink.folder + '/' + chapterLink.chapter + "/", fileFormat.format(page))

                    configs.append({"full_path": full_path, "url": link})
                    page = page + 1

                # write to file in json format
                with open(chapterPath, 'a') as f:
                    json.dump(configs, f, indent=4)

    @deprecated
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
        chapterPdfPath: str = 'chapterPDFs'
        files = natsorted(os.listdir(rootPDFs), alg=ns.PATH)
        for dir in files:
            title_name = dir
            titleDirPath = os.path.join(rootPDFs, title_name)
            if os.path.isdir(titleDirPath):
                chapterDirs = natsorted(
                    os.listdir(titleDirPath), alg=ns.PATH
                )
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

                    chapterTitlePdfPath = os.path.join(
                        chapterPdfPath, title_name)

                    dirLib.create_folder(chapterTitlePdfPath)

                    pdfPath = os.path.join(
                        chapterTitlePdfPath, title_name + '_' + chapterDir + ".pdf")
                    # print('image_list', image_list)
                    # print('pdfPath', pdfPath)
                    firstImage = image_list[0]
                    del image_list[0]
                    firstImage.save(pdfPath, save_all=True,
                                    append_images=image_list)
                    print('Saved:', pdfPath)

    def mergePDFs(self):
        """_summary_
        Merge PDF follow folder under ./pdfs, in every 20 chapters
        """

        rootPDFs: str = 'chapterPDFs'
        dirs = natsorted(os.listdir(rootPDFs), alg=ns.PATH)

        for dir in dirs:
            titleDirPath = os.path.join(rootPDFs, dir)
            if os.path.isdir(titleDirPath):
                pdfsAll = natsorted(os.listdir(titleDirPath), alg=ns.PATH)

                # pdfsAllWithFullPath = []

                # for p in pdfsAll:
                #     pdfsAllWithFullPath.append(os.path.join(titleDirPath, p))

                # print(pdfsAllWithFullPath)
                pdfsSets = self.split_array(pdfsAll, 20)
                print(pdfsSets)

                for pdfs in pdfsSets:
                    self.mergePdf(pdfs, titleDirPath)  # type: ignore

                # merger = PdfMerger()
                # for pdf in pdfs:
                #     pdfPath = os.path.join(titleDirPath, pdf)
                #     merger.append(pdfPath)

                # def remove_extension(fileName: str):
                #     return os.path.splitext(fileName)[0]

                # destinationDir = os.path.join('readypdf')

                # dirLib.create_folder(destinationDir)
                # mergedPDFPath = os.path.join(
                #     destinationDir,  f"{dir} {remove_extension(pdfs[0])}-{remove_extension(pdfs[-1])}.pdf")
                # merger.write(mergedPDFPath)
                # merger.close()

    def mergePdf(self, pdfs: List[str], titleDirPath: str):
        merger = PdfMerger()
        for pdf in pdfs:
            p = os.path.join(titleDirPath, pdf)
            merger.append(p)

        destinationDir = os.path.join('readypdf')
        mergedPDFPath = os.path.join(
            destinationDir,  f"{self.remove_extension(pdfs[0])}-{self.remove_extension(pdfs[-1])}.pdf")

        merger.write(mergedPDFPath)
        merger.close()
        print(f"Merge PDF to {mergedPDFPath}")

    def remove_extension(self, fileName: str):
        return os.path.splitext(fileName)[0]

    def split_array(self, arr, size):
        return np.array_split(arr, (len(arr) + size - 1) // size)
