import urllib.request


def get_full_path(file_path: str, file_name: str):
    return file_path + file_name + '.jpg'


def download_image_v1(url: str, file_path: str):
    urllib.request.urlretrieve(url, file_path)


def download_image_v2(url: str, file_path: str):
    headers = {'User-Agent': 'Mozilla/5.0'}

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response, open(file_path, 'wb') as outfile:
        outfile.write(response.read())
