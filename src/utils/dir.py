import os


def create_folder(folder_name: str) -> bool:
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder ${folder_name} created successfully! Start download..")
        return False
    return True
