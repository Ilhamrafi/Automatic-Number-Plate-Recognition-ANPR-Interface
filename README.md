# Automatic-Number-Plate-Recognition-ANPR-Interface
Aplikasi ANPR ini dikembangkan untuk mendeteksi dan mengenali plat kendaraan secara otomatis menggunakan model YOLOv5 untuk deteksi dan EasyOCR untuk pembacaan karakter. Berikut adalah penjelasan singkat tentang aplikasi:

## ANPR menggunakan YOLOv5 dan EasyOCR
ANPR (Automatic Number Plate Recognition) adalah aplikasi yang memanfaatkan teknologi deteksi objek YOLOv5 dan pembacaan karakter EasyOCR untuk mendeteksi dan mengenali plat kendaraan secara otomatis. Dengan menggunakan model YOLOv5, aplikasi ini mampu dengan akurat menentukan lokasi plat nomor pada gambar, sementara EasyOCR digunakan untuk membaca karakter-karakter pada plat nomor tersebut.
Aplikasi ini memiliki kemampuan untuk memproses dataset plat kendaraan melalui berbagai fitur, termasuk upload gambar, update, delete, dan eksplorasi dataset. Pada tahap training, aplikasi ini memanfaatkan Google Colab untuk melatih model YOLOv5, mengoptimalkan deteksi plat kendaraan pada berbagai kondisi gambar. Dengan menggunakan model yang telah di-training, halaman Prediction memberikan hasil prediksi plat kendaraan, termasuk visualisasi bounding box dan pembacaan karakter. Aplikasi ini memberikan solusi efektif untuk tugas deteksi dan pengenalan plat kendaraan dengan memanfaatkan teknologi terkini dalam bidang deteksi objek dan pengenalan karakter.

## Penggunaan
1. Install beberapa library dengan menjalankan perintah berikut:

   ```shell
   pip install opencv-python
   pip install numpy
   pip install torch
   pip install easyocr
   pip install streamlit
   pip install pandas
   pip install pillow
   pip install requests
   pip install streamlit-lottie
