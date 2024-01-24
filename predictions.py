#predictions.py
import cv2
import numpy as np
import torch
import easyocr
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class DeteksiObjek:
    def __init__(self):
        self.model = self.load_model()
        self.classes = self.model.names
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print("Menggunakan Perangkat: ", self.device)
        self.reader = easyocr.Reader(['en'], gpu=True)

    def load_model(self):
        model_path = "best.pt"
        model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path, force_reload=True)
        return model

    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxy[0][:, -1], results.xyxy[0][:, :-1]
        return labels, cord

    def class_to_label(self, x):
        return self.classes[int(x)]

    def plot_boxes(self, detections, frame):
        label_colors = {
            "plat": (0, 0, 255),  # Merah
        }

        for bounding_box in detections:
            x, y, width, height, confidence, class_idx = bounding_box

            # Hitung titik sudut relatif
            x1 = int(x)
            y1 = int(y)
            x2 = int(x + width)
            y2 = int(y + height)

            # Gambar kotak di atas gambar
            cv2.rectangle(frame, (x1, y1), (x2, y2), label_colors.get(self.class_to_label(class_idx), (0, 255, 0)), 2)

            # Tampilkan nama kelas dan kepercayaan dengan teks tebal
            label = f"{self.class_to_label(class_idx)}: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), thickness=5)

        return frame

    def crop_detected_regions(self, image, detections):
        crops = []
        for bbox in detections:
            x, y, width, height, _, _ = bbox
            x1, y1, x2, y2 = int(x), int(y), int(x + width), int(y + height)
            crop = image[y1:y2, x1:x2].copy()
            crops.append(crop)
        return crops

    def extract_text_from_image(self, image):
        # Terapkan blur pada citra sebelum OCR
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # Periksa jumlah saluran warna
        if len(blurred.shape) == 3 and blurred.shape[2] == 3:
            # Konversi citra ke hitam-putih
            gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        elif len(blurred.shape) == 2:
            gray = blurred
        else:
            # Jika tidak sesuai dengan kondisi di atas, tampilkan pesan kesalahan
            raise ValueError("Format citra tidak didukung.")

        # Terapkan metode OCR pada citra yang sudah di-blur tanpa di-threshold
        results = self.reader.readtext(gray)

        # Ambil teks dari hasil OCR EasyOCR
        text = ' '.join([result[1] for result in results])

        return text
    
    def filter_text(self, text):
        # Post-processing: Hanya simpan huruf dan angka
        filtered_text = re.sub(r'[^A-Za-z0-9]', '', text)
        return filtered_text

    def preprocess_image(self, image):
        # Konversi citra ke hitam-putih
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresholded

    def process_image(self, image_file):
        image_bytes = image_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        original_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Skor frame menggunakan model YOLOv5
        labels, cord = self.score_frame(original_frame)

        detections = []
        for i in range(len(labels)):
            detection = (
                cord[i, 0],
                cord[i, 1],
                cord[i, 2] - cord[i, 0],
                cord[i, 3] - cord[i, 1],
                cord[i, 4],
                labels[i]
            )
            detections.append(detection)

        # Gambar bounding box dan label pada frame
        frame_with_boxes = self.plot_boxes(detections, original_frame)

        # Crop bagian yang terdeteksi dari frame
        cropped_regions = self.crop_detected_regions(original_frame, detections)

        # Pra-pemrosesan: Konversi ke hitam-putih dan aplikasikan blur sebelum OCR
        preprocessed_crops = [self.preprocess_image(crop) for crop in cropped_regions]

        # Ekstraksi teks dari gambar
        extracted_texts = [self.extract_text_from_image(crop) for crop in preprocessed_crops]

        # Filter teks yang diekstraksi
        filtered_texts = [self.filter_text(text) for text in extracted_texts]

        return frame_with_boxes, preprocessed_crops,filtered_texts
