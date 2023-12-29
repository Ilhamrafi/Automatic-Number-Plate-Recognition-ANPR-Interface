# main.py
from streamlit_option_menu import option_menu
import streamlit as st
import os
from PIL import Image
import pandas as pd
import webbrowser
import requests
from streamlit_lottie import st_lottie
from predictions import DeteksiObjek

# Buat instance dari DeteksiObjek
deteksi_objek = DeteksiObjek()

# Fungsi untuk mengambil data animasi dari URL
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Fungsi untuk mendapatkan path folder berdasarkan pilihan pengguna
def get_folder_path(selected_folder):
    base_folder = "C:/Users/ASUS/OneDrive/Dokumen/Informatika Semester 7/Pengembangan Aplikasi AI/Deteksi_PlatNomorKendaraan/dataset nomor kendaraan"  # Ganti dengan path folder utama
    return os.path.join(base_folder, selected_folder)

# Fungsi untuk mendapatkan nama-nama folder
def get_folder_names():
    return ['K1', 'K2', 'K3', 'K4']

# Fungsi untuk mendapatkan data nama file dan format dalam tabel
def get_table_data(folder_path, valid_image_extensions):
    image_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file)) and any(file.lower().endswith(ext) for ext in valid_image_extensions)]
    table_data = {"Nama File": [file.split(".")[0] for file in image_files],
                  "Format": [file.split(".")[-1] for file in image_files]}
    return pd.DataFrame(table_data)

# Fungsi untuk mendapatkan data nama file dan format dalam tabel
def get_table_data(folder_path, valid_image_extensions):
    image_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file)) and any(file.lower().endswith(ext) for ext in valid_image_extensions)]
    table_data = {"Nama File": [file.split(".")[0] for file in image_files],
                  "Format": [file.split(".")[-1] for file in image_files]}
    return pd.DataFrame(table_data)

# Opsi di sidebar
with st.sidebar:
    selected = option_menu(
        "Menu",
        ['Upload Gambar', 'Update dan Delete', 'Dataset Plat Kendaraan',  'Training', 'Prediction' ],
        icons=['cloud-upload', 'database-fill-check', 'images',  'gear', 'kanban' ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "padding-top": "0px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
        }
    )

# Konten utama berdasarkan opsi yang dipilih
if selected == "Upload Gambar":
    st.title("Upload Gambar Citra Kendaraan")
    uploaded_image = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

    # Pilihan folder
    selected_folder = st.selectbox("Pilih Folder", get_folder_names())

    # Input untuk nama file
    default_file_name = uploaded_image.name.split(".")[0] if uploaded_image else ""
    file_name = st.text_input("Nama File (tanpa ekstensi)", default_file_name)

    if uploaded_image:
        st.image(uploaded_image, caption="Gambar yang Diunggah", use_column_width=True)

        # Simpan gambar ke folder yang dipilih
        if st.button("Simpan"):
            folder_path = get_folder_path(selected_folder)
            file_extension = uploaded_image.name.split(".")[-1]
            file_path = os.path.join(folder_path, f"{file_name}.{file_extension}")
            with open(file_path, "wb") as f:
                f.write(uploaded_image.read())
            st.success(f"Gambar berhasil disimpan di folder {selected_folder} dengan nama {file_name}.{file_extension}")

elif selected == "Update dan Delete":
    st.title("Update dan Delete Citra Kendaraan")

    # Tampilkan daftar gambar yang dapat diupdate atau dihapus
    update_delete_folder = st.selectbox("Pilih Folder untuk Update dan Delete", get_folder_names())

    folder_path_for_update_delete = get_folder_path(update_delete_folder)
    
    # Menyertakan valid_image_extensions untuk mendapatkan daftar file gambar
    valid_image_extensions = ['.jpg', '.jpeg', '.png']
    all_image_files = [file for file in os.listdir(folder_path_for_update_delete) if os.path.isfile(os.path.join(folder_path_for_update_delete, file)) and any(file.lower().endswith(ext) for ext in valid_image_extensions)]

    # Pilihan gambar untuk update atau delete
    page_number = st.number_input("Pilih Halaman", min_value=1, max_value=(len(all_image_files) // 10) + 1, value=1, step=1)

    start_index = (page_number - 1) * 10
    end_index = min(page_number * 10, len(all_image_files))

    table_data = {"Nama File": [file.split(".")[0] for file in all_image_files[start_index:end_index]],
                  "Format": [file.split(".")[-1] for file in all_image_files[start_index:end_index]]}

    # Tampilkan data nama file dan format dalam tabel dengan indeks dimulai dari 1
    st.table(pd.DataFrame(table_data).reset_index(drop=True))

    # Pilihan aksi: Update atau Delete
    action = st.selectbox("Pilih Aksi", ["Update", "Delete"])

    if action == "Update":
        st.text("Form Update Gambar")
        # Tambahkan form atau fungsi update di sini

        # Pilih gambar untuk diupdate
        selected_image_for_update = st.selectbox("Pilih Gambar untuk Update", table_data["Nama File"])

        # Form untuk mengupdate nama file
        new_file_name = st.text_input("Nama File Baru (tanpa ekstensi)", selected_image_for_update)

        # Tampilkan tombol update
        update_button = st.button("Update Gambar")

        if update_button:
            # Lakukan pembaruan nama file
            old_file_path = os.path.join(folder_path_for_update_delete, f"{selected_image_for_update}.jpg")
            new_file_path = os.path.join(folder_path_for_update_delete, f"{new_file_name}.jpg")

            os.rename(old_file_path, new_file_path)
            st.success(f"Gambar {selected_image_for_update} berhasil diupdate menjadi {new_file_name}.jpg")

    elif action == "Delete":
        # Pilihan gambar untuk update atau delete
        selected_image_for_update_delete = st.selectbox("Pilih Gambar untuk Update atau Delete", table_data["Nama File"])

        # Tampilkan tombol delete
        delete_button = st.button("Hapus Gambar Terpilih")

        if delete_button:
            # Hapus gambar jika tombol di tekan
            os.remove(os.path.join(folder_path_for_update_delete, selected_image_for_update_delete + ".jpg"))
            st.success(f"Gambar {selected_image_for_update_delete} berhasil dihapus.")

elif selected == "Dataset Plat Kendaraan":
    st.title("Dataset Plat Kendaraan")

    # Ambil jumlah data pada masing-masing folder
    folder_paths = {
        'Train': 'C:/Users/ASUS/OneDrive/Dokumen/Informatika Semester 7/Pengembangan Aplikasi AI/Deteksi_PlatNomorKendaraan/Deteksi Plat Nomor Kendaraan.v2i.voc/train',
        'Valid': 'C:/Users/ASUS/OneDrive/Dokumen/Informatika Semester 7/Pengembangan Aplikasi AI/Deteksi_PlatNomorKendaraan/Deteksi Plat Nomor Kendaraan.v2i.voc/valid',
        'Test': 'C:/Users/ASUS/OneDrive/Dokumen/Informatika Semester 7/Pengembangan Aplikasi AI/Deteksi_PlatNomorKendaraan/Deteksi Plat Nomor Kendaraan.v2i.voc/test'
    }
    image_counts = {}

    # Memilih file dengan ekstensi tertentu (misalnya: jpg, jpeg, png)
    valid_image_extensions = ['.jpg', '.jpeg', '.png']

    for folder, path in folder_paths.items():
        image_counts[folder] = len([file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and any(file.lower().endswith(ext) for ext in valid_image_extensions)])

    # Hitung total citra dari semua folder
    total_images = sum(image_counts.values())

    # Buat DataFrame untuk menampilkan dalam tabel
    image_table = pd.DataFrame(list(image_counts.items()) + [('Total', total_images)], columns=['Folder', 'Jumlah Citra'])

    # Tampilkan dalam bentuk tabel tanpa index
    st.subheader("Jumlah Citra Kendaraan:")
    st.table(image_table.set_index('Folder', drop=True, inplace=False))

    # Selectbox untuk memilih folder
    selected_folder_for_images = st.selectbox("Pilih Folder untuk Menampilkan Citra", list(folder_paths.keys()))

    # Tampilkan citra dari folder yang dipilih
    st.subheader(f"Citra dari Folder {selected_folder_for_images}")

    # Maksimal 8 citra yang ditampilkan
    folder_path_for_images = folder_paths[selected_folder_for_images]
    image_files = [file for file in os.listdir(folder_path_for_images) if os.path.isfile(os.path.join(folder_path_for_images, file)) and any(file.lower().endswith(ext) for ext in valid_image_extensions)]

    # Membagi layar menjadi dua kolom
    col1, col2 = st.columns(2)

    image_width = 200  # Tentukan lebar citra yang diinginkan

    for i, image_file in enumerate(image_files[:10]):
        image_path = os.path.join(folder_path_for_images, image_file)
        image = Image.open(image_path)

        # Mengatur ukuran citra
        image = image.resize((image_width, image_width))

        # Memasukkan citra ke dalam kolom
        if i % 2 == 0:
            col1.image(image, use_column_width=True)
            col1.write(f"{image_file}")
        else:
            col2.image(image, use_column_width=True)
            col2.write(f"{image_file}")

elif selected == "Training":
    st.title("Training Citra Kendaraan")
    train_button = st.button("Mulai Training")

    if train_button:

        animation_url = "https://lottie.host/32647c7a-3af2-46d9-bdd0-c651cd1e6f02/1vQLzP5Syi.json"
        lottie_data = load_lottie_url(animation_url)

        if lottie_data is not None:
            st_lottie(lottie_data, speed=1, width=None, height=None)

        # Panggil fungsi pelatihan dari training.py
        colab_url = "https://colab.research.google.com/drive/1MeXy5l5p0cwm-pM1bA-FmeXJUyfgz9id#scrollTo=kTvDNSILZoN9"
        webbrowser.open_new_tab(colab_url)

        st.success("Training telah dimulai di Colab. Silakan beralih ke halaman Google Colab.")

elif selected == "Prediction":
    st.title("Prediksi Plat Nomor Kendaraan")
    uploaded_image = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Gambar yang Diunggah", use_column_width=True)
        predict_button = st.button("Lakukan Prediksi")

        if predict_button:
            # Perform prediction
            output_frame, cropped_regions, filtered_texts = deteksi_objek.process_image(uploaded_image)
            st.image(output_frame, caption="Hasil Prediksi", use_column_width=True)

            for i, cropped_region in enumerate(cropped_regions):
                st.image(cropped_region, caption=f"Citra Preprocessed #{i + 1}", use_column_width=True)

                # Terapkan OCR pada bagian yang terdeteksi
                text_result = filtered_texts[i]  # Change to use filtered text
                st.text(f"Hasil OCR #{i + 1}: {text_result}")

                array_result = list(text_result)
                st.write(f"Array hasil OCR #{i+1}: {array_result}")