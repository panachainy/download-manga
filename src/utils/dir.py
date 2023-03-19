import os


def create_folder(folder_name: str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder ${folder_name} created successfully!")
    # else:
        # print("Folder already exists.")
