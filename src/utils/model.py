from typing import List
from pydantic import BaseModel
from pydantic import parse_obj_as
from pydantic.dataclasses import dataclass

class ImageConfig(BaseModel):
    url: str
    alt: str
    # TODO: remove
    folder: str

    def formJson(data):
        ImageDataList = List[ImageConfig]

        data_list = parse_obj_as(ImageDataList, data)
        return data_list

@dataclass
class TitleConfig():
    url: str
    folder: str
    chapter: str
