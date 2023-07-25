# Impor pustaka yang dibutuhkan
import cv2
import os
import numpy as np

# Berikut adalah fungsi yang akan menyesuaikan kecerahan gambar
def adjust_brightness(image, brightness=1.0):
    # Ubah gambar ke ruang warna HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Skala kanal V (Value/Kecerahan)
    hsv[...,2] = cv2.convertScaleAbs(hsv[...,2], alpha=brightness)
    # Ubah kembali gambar ke ruang warna BGR
    bright_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bright_image

def capture_images():
    # Dapatkan nama pengguna
    name = input("Masukkan Nama Anda: ").lower()

    # Buat direktori untuk gambar jika tidak ada
    images_dir = 'images'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    path = os.path.join(images_dir, name)

    # Cek apakah direktori sudah ada
    if os.path.exists(path):
        print("Nama Sudah Digunakan")
        name = input("Masukkan Nama Anda Lagi: ").lower()
    else:
        os.makedirs(path)

    # Buka webcam
    cap = cv2.VideoCapture(0)

    # Inisialisasi hitungan gambar
    count = 0

    while True:
        # Tangkap frame-demi-frame
        ret, frame = cap.read()

        # Cek jika pembacaan frame berhasil
        if not ret:
            break

        # Sesuaikan kecerahan frame
        bright_frame = adjust_brightness(frame, brightness=1.5)  # Tingkatkan kecerahan sebesar 50%

        # Tampilkan frame hasil
        cv2.imshow('Tangkap Gambar', bright_frame)

        # Simpan gambar saat ini ke direktori
        img_name = os.path.join(path, f'{count}.jpg')
        cv2.imwrite(img_name, bright_frame)
        print(f'Membuat Gambar.........{img_name}')
        count += 1

        # Hentikan jika tombol 'q' ditekan atau kita sudah memiliki cukup gambar
        if cv2.waitKey(1) & 0xFF == ord('q') or count > 500:
            break

    # Ketika semuanya selesai, lepaskan tangkapan dan tutup jendela
    cap.release()
    cv2.destroyAllWindows()

# Panggil fungsi
capture_images()
