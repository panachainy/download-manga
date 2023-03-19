
import utils.model as model
import utils.scrapping as scrapping
import json
from typing import List
import services.manga_a as manga_a
from fpdf import FPDF
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
                folderPath = 'images/' + chapterLink.folder + '/'
                chapterPath = folderPath + chapterLink.chapter + '/'
                # manga_a.downloadFromMangaA(
                #     chapterLink.url, imageConfig.alt, folderPath)
                # Note: https://github.com/reingart/pyfpdf/blob/master/docs/reference/add_page.md
                pdf = FPDF('P', 'cm', 'A3')

                image_list = []

                for imageFile in os.listdir(chapterPath):
                    filePath = chapterPath + imageFile
                    # image = Image.open(chapterPath + imageFile)
                    # pdf.add_page()
                    # w, h = image.size

                    # print("wh", w, h)
                    # pdf.image(filePath, 0, 0, w/10, h/10)
                    image_list.append(Image.open(filePath).convert('RGB'))
                    # image_1 = Image.open(r'C:\Users\Ron\Desktop\Test\view_1.png')
                    # image_2 = Image.open(r'C:\Users\Ron\Desktop\Test\view_2.png')
                    # image_3 = Image.open(r'C:\Users\Ron\Desktop\Test\view_3.png')
                    # image_4 = Image.open(r'C:\Users\Ron\Desktop\Test\view_4.png')

                    # im_1 = image_1.convert('RGB')
                    # im_2 = image_2.convert('RGB')
                    # im_3 = image_3.convert('RGB')
                    # im_4 = image_4.convert('RGB')

                    # image_list = [im_2, im_3, im_4]

                s = folderPath + chapterLink.chapter + ".pdf"
                print('s=======', s)
                # pdf.output(s)
                image_list[0].save(s, save_all=True, append_images=image_list)

                # png = Image.open(object.logo.path)
                # png.load()  # required for png.split()

                # background = Image.new("RGB", png.size, (255, 255, 255))
                # background.paste(png, mask=png.split()[3])

                # from fpdf import FPDF
                # pdf = FPDF()
                # for image in imagelist:
                #     pdf.add_page()
                #     pdf.image(image)
                # pdf.output("yourfile.pdf", "F")

                exit(1)

# from fpdf import FPDF
# pdf = FPDF()
# for image in imagelist:
#     pdf.add_page()
#     pdf.image(image,x,y,w,h)
# pdf.output("yourfile.pdf", "F")
