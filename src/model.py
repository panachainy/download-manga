from typing import List
from pydantic import BaseModel
from pydantic import parse_obj_as


class ImageData(BaseModel):
    url: str
    alt: str
    folder: str

    def formJson(data):
        ImageDataList = List[ImageData]

        data_list = parse_obj_as(ImageDataList, data)
        return data_list