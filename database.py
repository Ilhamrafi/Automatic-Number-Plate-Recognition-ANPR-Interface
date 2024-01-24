#database.py
import mysql.connector

class KoneksiDB:
    def create_connection(self):
        # Ganti dengan informasi koneksi database MySQL Anda
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Informatika-20",
            database="deteksi_plat_nomor"
        )
        return db_connection

    def close_connection(self, connection):
        connection.close()

    def save_image_info(self, file_name, folder_name, image_data):
        if not file_name or not folder_name or not image_data:
            raise ValueError("Input tidak valid.")

        connection = self.create_connection()
        cursor = connection.cursor()

        insert_query = "INSERT INTO uploaded_images (file_name, folder_name, image_data) VALUES (%s, %s, %s)"
        values = (file_name, folder_name, image_data)

        cursor.execute(insert_query, values)

        connection.commit()

        cursor.close()
        self.close_connection(connection)

    def get_image_info(self, folder_name):
        if not folder_name:
            raise ValueError("Input tidak valid.")

        connection = self.create_connection()
        cursor = connection.cursor()

        query = "SELECT file_name FROM uploaded_images WHERE folder_name = %s"
        values = (folder_name,)

        cursor.execute(query, values)
        result = cursor.fetchall()

        cursor.close()
        self.close_connection(connection)

        return {"file_name": [item[0] for item in result]}

    def update_image_info(self, old_file_name, new_file_name):
        if not old_file_name or not new_file_name:
            raise ValueError("Input tidak valid.")

        connection = self.create_connection()
        cursor = connection.cursor()

        query = "UPDATE uploaded_images SET file_name = %s WHERE file_name = %s"
        values = (new_file_name, old_file_name)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        self.close_connection(connection)

    def delete_image_info(self, file_name):
        if not file_name:
            raise ValueError("Input tidak valid.")

        connection = self.create_connection()
        cursor = connection.cursor()

        query = "DELETE FROM uploaded_images WHERE file_name = %s"
        values = (file_name,)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        self.close_connection(connection)

    def get_all_image_data(self):
        connection = self.create_connection()
        cursor = connection.cursor()

        query = "SELECT file_name, folder_name, image_data FROM uploaded_images"
        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        self.close_connection(connection)

        return result

    def get_image_data_by_folder(self, folder_name):
        # Mendapatkan data gambar dari database berdasarkan folder yang dipilih
        query = "SELECT * FROM uploaded_images WHERE folder_name = %s"
        values = (folder_name,)

        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        self.close_connection(connection)

        return result
