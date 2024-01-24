# main.py
import streamlit as st
from PIL import Image
import pandas as pd
import io
import webbrowser
import hydralit_components as hc
from streamlit_lottie import st_lottie
from predictions import DeteksiObjek
from database import KoneksiDB
from utilities import Utilities

def setup_page_configuration():
    st.set_page_config(
        page_title='PLAT-VISION',
        page_icon="🎮",
        layout='wide',
        initial_sidebar_state='auto',
    )

def setup_navigation_bar():
    menu_data = [
        {'icon': "📇", 'label': "Upload Gambar"},
        {'icon': "💾", 'label': "Database"},
        {'icon': "️🖼️", 'label': "Dataset Plat Kendaraan"},
        {'icon': "🚀", 'label': "Training"},
        {'icon': "🔮", 'label': "Prediction"},
    ]

    over_theme = {
        'txc_inactive': '#FFFFFF',  # Ganti warna teks non-aktif (putih pada contoh ini)
        'txc_active': '#000000',    # Ganti warna teks aktif (biru pada contoh ini)
        'menu_background': '#2C3E50',  # Warna latar belakang menu
        'option_active': '#E74C3C',  # Warna opsi aktif (gunakan jika diperlukan)
        'font_family': 'Montserrat, sans-serif',  # Jenis huruf yang digunakan
    }

    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Home',
        hide_streamlit_markers=False,
        sticky_nav=True,
        sticky_mode='pinned',
    )

    return menu_id

# Buat instance dari DeteksiObjek dan KoneksiDB
deteksi_objek = DeteksiObjek()
koneksi_db = KoneksiDB()

import streamlit as st

def handle_home_menu():
    st.markdown(
        """
        <h1 style="text-align: center; color: #007BFF;">Selamat Datang di PLAT-VISION</h1>
        """,
        unsafe_allow_html=True
    )    

    st.info("Selamat datang di PLAT-VISION, solusi terdepan dalam pengenalan plat nomor kendaraan yang didukung oleh kecerdasan buatan. Aplikasi ini membawa kemudahan dalam mendeteksi dan mengidentifikasi plat nomor kendaraan secara cepat dan akurat. Dikembangkan untuk mendeteksi dan mengenali plat kendaraan secara otomatis, PLAT-VISION memanfaatkan model YOLOv5 untuk deteksi dan EasyOCR untuk pembacaan karakter, sehingga dapat dengan akurat menentukan lokasi plat nomor pada gambar dan membaca karakter-karakter pada plat nomor tersebut.")

    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #007BFF;'>Fitur-fitur yang ada di aplikasi ini : </h2>", unsafe_allow_html=True)

    col_logo, col_text = st.columns([2, 3])

    col_logo.image("./resources/classroom.png", width=100, use_column_width='always')

    with col_text:
        st.info("Aplikasi ini memiliki beberapa fitur utama yang memungkinkan pengguna untuk mengelola dan menganalisis data terkait plat kendaraan. Pertama adalah fitur Upload Citra Kendaraan memungkinkan pengguna dengan mudah mengunggah gambar kendaraan ke dalam aplikasi, memberikan fleksibilitas dalam menentukan folder penyimpanan dan menamai file. Dengan menampilkan preview gambar, fitur ini menyederhanakan proses pengelolaan dataset gambar kendaraan, memberikan pengguna kenyamanan dalam menyimpan dan mengelola informasi visual terkait kendaraan.")

    with col_text:
        st.info("Fitur Database Citra Kendaraan, di mana pengguna dapat memilih folder untuk melakukan update atau delete terhadap gambar. Informasi gambar yang ada dalam database ditampilkan dalam tabel, dan pengguna dapat memilih aksi yang diinginkan, baik itu update dengan memberikan nama file baru atau menghapus gambar.")


    with col_text:
        st.info("Fitur selanjutnya adalah Dataset Plat Kendaraan, yang memberikan gambaran tentang jumlah citra dalam setiap folder dataset seperti Train, Valid, Test, dan Data Baru yang belum dilakukan labelling. Pengguna dapat memilih folder dataset untuk melihat citra yang ada dalam bentuk tabel.")

    with col_text:
        st.info("Bagian Training Citra Kendaraan memungkinkan pengguna untuk memulai proses training dengan menekan tombol yang disediakan. Selama proses training, aplikasi menampilkan animasi lottie yang memberikan indikasi bahwa training sedang berlangsung. Pengguna juga diberikan link untuk beralih ke Google Colab guna memantau atau mengelola proses training lebih lanjut.")

    with col_text:
        st.info("Terakhir, terdapat fitur Prediksi Plat Nomor Kendaraan, di mana pengguna dapat mengunggah gambar untuk diprediksi. Setelah mengunggah gambar, pengguna dapat memulai proses prediksi dengan menekan tombol yang tersedia. Hasil prediksi, bersama dengan citra yang telah diproses sebelumnya, ditampilkan dengan rinci. Selain itu, aplikasi juga memberikan hasil pembacaan karakter pada plat nomor sebagai bagian dari output prediksi.")

def handle_upload_menu():
    st.markdown(
        """
        <h1 style="text-align: center; color: #007BFF;">Upload Citra Kendaraan</h1>
        """,
        unsafe_allow_html=True
    )    

    uploaded_images = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    selected_folder = st.selectbox("Pilih Folder", Utilities.get_folder_names())
    default_file_name = ""

    if uploaded_images:
        default_file_name = uploaded_images[0].name.split(".")[0]

    file_name = st.text_input("Nama File (tanpa ekstensi)", default_file_name)

    if uploaded_images:
        for uploaded_image in uploaded_images:
            st.image(uploaded_image, caption="Gambar yang Diunggah", width=500, use_column_width=False)

            if st.button("Simpan"):
                file_extension = uploaded_image.name.split(".")[-1]
                image_bytes = uploaded_image.read()
                koneksi_db.save_image_info(file_name, selected_folder, image_bytes)
                st.success(f"Gambar berhasil disimpan di folder {selected_folder} dengan nama {file_name}.{file_extension}")

def handle_database_menu():
    st.markdown(
        """
        <h1 style="text-align: center; color: #007BFF;">Database Citra Kendaraan</h1>
        """,
        unsafe_allow_html=True
    )    

    update_delete_folder = st.selectbox("Pilih Folder untuk Update dan Delete", Utilities.get_folder_names())
    valid_image_extensions = ['.jpg', '.jpeg', '.png']
    db_data = koneksi_db.get_image_info(update_delete_folder)

    if not db_data:
        st.warning("Tidak ada data gambar yang ditemukan.")
    else:
        st.table(pd.DataFrame(db_data).reset_index(drop=True))
        action = st.selectbox("Pilih Aksi", ["Update", "Delete"])

        if action == "Update":
            st.text("Form Update Gambar")
            selected_image_for_update = st.selectbox("Pilih Gambar untuk Update", db_data["file_name"])
            new_file_name = st.text_input("Nama File Baru (tanpa ekstensi)", selected_image_for_update)
            update_button = st.button("Update Gambar")

            if update_button:
                koneksi_db.update_image_info(selected_image_for_update, new_file_name)
                st.success(f"Gambar {selected_image_for_update} berhasil diupdate menjadi {new_file_name}.jpg")

        elif action == "Delete":
            st.text("Form Delete Gambar")
            selected_image_for_delete = st.selectbox("Pilih Gambar untuk Delete", db_data["file_name"])
            delete_button = st.button("Hapus Gambar")

            if delete_button:
                koneksi_db.delete_image_info(selected_image_for_delete)
                st.success(f"Gambar {selected_image_for_delete} berhasil dihapus.")

def handle_dataset_menu():
    st.markdown(
        """
        <h1 style="text-align: center; color: #007BFF;">Tampilan Dataset Citra Kendaraan</h1>
        """,
        unsafe_allow_html=True
    )    

    folder_names = {
        'Train': 'Train',
        'Valid': 'Valid',
        'Test': 'Test',
        'Data Baru (belum dilakukan labelling)': 'Data Baru (belum dilakukan labelling)'
    }

    image_counts = {}

    for folder_name in folder_names.values():
        query = "SELECT COUNT(*) FROM uploaded_images WHERE folder_name = %s"
        values = (folder_name,)

        connection = koneksi_db.create_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        koneksi_db.close_connection(connection)

        image_counts[folder_name] = result[0] if result else 0

    total_images = sum(image_counts.values())

    image_table = pd.DataFrame(list(image_counts.items()) + [('Total', total_images)], columns=['Folder', 'Jumlah Citra'])

    st.subheader("Jumlah Citra Kendaraan:")
    st.table(image_table.set_index('Folder', drop=True, inplace=False))

    selected_folder_for_images = st.selectbox("Pilih Folder untuk Menampilkan Citra", list(folder_names.values()))
    selected_image_data = koneksi_db.get_image_data_by_folder(selected_folder_for_images)

    if not selected_image_data:
        st.warning("Tidak ada data gambar yang ditemukan untuk folder yang dipilih.")
    else:
        st.subheader(f"Citra dari Data {selected_folder_for_images}")
        df = pd.DataFrame(selected_image_data, columns=['id', 'file_name', 'folder_name', 'image_data', 'upload_timestamp']).reset_index(drop=True)
        df = df.drop(['id', 'upload_timestamp'], axis=1)
        df['Gambar'] = [Image.open(io.BytesIO(img_data)) for img_data in df['image_data']]
        num_columns = 2
        num_rows_per_column = len(df) // num_columns
        columns = st.columns(num_columns)

        for i in range(num_columns):
            start_idx = i * num_rows_per_column
            end_idx = (i + 1) * num_rows_per_column
            captions = [f"{file_name} - {folder_name}" for file_name, folder_name in zip(df['file_name'][start_idx:end_idx], df['folder_name'][start_idx:end_idx])]
            columns[i].image(df['Gambar'][start_idx:end_idx].tolist(), caption=captions)

def handle_training_menu():
    st.markdown(
        """
        <h1 style="text-align: center; color: #007BFF;">Training Citra Kendaraan</h1>
        """,
        unsafe_allow_html=True
    )    
    train_button = st.button("Mulai Training")

    if train_button:
        animation_url = "https://lottie.host/32647c7a-3af2-46d9-bdd0-c651cd1e6f02/1vQLzP5Syi.json"
        lottie_data = Utilities.load_lottie_url(animation_url)

        if lottie_data is not None:
            st_lottie(lottie_data, speed=1, width=None, height=None)

        colab_url = "https://colab.research.google.com/drive/1MeXy5l5p0cwm-pM1bA-FmeXJUyfgz9id#scrollTo=kTvDNSILZoN9"
        webbrowser.open_new_tab(colab_url)

        st.success("Training telah dimulai di Colab. Silakan beralih ke halaman Google Colab.")

def handle_prediction_menu(deteksi_objek):
    st.markdown(
        """
        <h1 style="text-align: center; color: #007BFF;">Prediksi Plat Kendaraan</h1>
        """,
        unsafe_allow_html=True
    )    
    uploaded_image = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Gambar yang Diunggah", use_column_width=False)
        predict_button = st.button("Lakukan Prediksi")

        if predict_button:
            output_frame, cropped_regions, filtered_texts = deteksi_objek.process_image(uploaded_image)
            st.image(output_frame, caption="Hasil Prediksi", use_column_width=False)

            for i, cropped_region in enumerate(cropped_regions):
                st.image(cropped_region, caption=f"Citra Preprocessed #{i + 1}", use_column_width=False)
                st.subheader(f"Hasil OCR :")
                st.markdown(f"<p style='font-size:30px;'><b>{filtered_texts[i]}</b></p>", unsafe_allow_html=True)

def handle_menu_selection(menu_id, deteksi_objek):
    if menu_id == "Home":
        handle_home_menu()
    elif menu_id == "Upload Gambar":
        handle_upload_menu()
    elif menu_id == "Database":
        handle_database_menu()
    elif menu_id == "Dataset Plat Kendaraan":
        handle_dataset_menu()
    elif menu_id == "Training":
        handle_training_menu()
    elif menu_id == "Prediction":
        handle_prediction_menu(deteksi_objek)

def main():
    setup_page_configuration()
    menu_id = setup_navigation_bar()
    handle_menu_selection(menu_id, deteksi_objek)

if __name__ == "__main__":
    main()
