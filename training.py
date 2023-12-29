# training.py

import torch
import os
from roboflow import Roboflow
from IPython.display import Image, clear_output  # untuk menampilkan gambar

def run_training():
    # klon YOLOv5
    os.system("git clone https://github.com/ultralytics/yolov5")  # klon repo
    os.chdir("yolov5")
    os.system("pip install -qr requirements.txt")  # instal dependensi
    os.system("pip install -q roboflow")

    print(f"Setup selesai. Menggunakan torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")

    # atur lingkungan
    os.environ["DATASET_DIRECTORY"] = "/content/datasets"

    os.system("pip install roboflow")

    from roboflow import Roboflow
    rf = Roboflow(api_key="JOOy8ib1kct8yzsUUKjz")
    project = rf.workspace("ilhamrafi").project("deteksi-plat-nomor-kendaraan-ag6gj")
    dataset = project.version(1).download("yolov5")

    os.system(f"python train.py --img 416 --batch 32 --epochs 2 --data {dataset.location}/data.yaml --weights yolov5s.pt --cache")

if __name__ == "__main__":
    run_training()