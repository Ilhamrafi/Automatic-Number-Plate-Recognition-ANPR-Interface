# utilities.py
import os
from PIL import Image
import pandas as pd
import requests
from streamlit import columns  # Import the 'columns' module from streamlit
from database import KoneksiDB

class Utilities:
    # Instance of KoneksiDB
    koneksi_db = KoneksiDB()

    @staticmethod
    def load_lottie_url(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    @staticmethod
    def display_images_from_folder(folder_name, image_files):
        columns.subheader(f"Citra dari Folder {folder_name}")

        col1, col2 = columns(2)
        image_width = 200

        folder_path = Utilities.koneksi_db.get_folder_path(folder_name)

        for i, (image_file,) in enumerate(image_files):
            image_path = os.path.join(folder_path, image_file)
            image = Image.open(image_path)
            image = image.resize((image_width, image_width))

            if i % 2 == 0:
                col1.image(image, use_column_width=True)
                col1.write(f"{image_file}")
            else:
                col2.image(image, use_column_width=True)
                col2.write(f"{image_file}")

    @staticmethod
    def get_folder_names(limit=None):
        folders = ['Train', 'Test', 'Valid', 'Data Baru (belum dilakukan labelling)']
        return folders[:limit] if limit is not None else folders

    @staticmethod
    def get_table_data(folder_path, valid_image_extensions):
        image_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file)) and any(file.lower().endswith(ext) for ext in valid_image_extensions)]
        table_data = {"Nama File": [file.split(".")[0] for file in image_files],
                      "Format": [file.split(".")[-1] for file in image_files]}
        return pd.DataFrame(table_data)
