# Aplikasi Pengolahan Citra Digital (PCD)

Aplikasi GUI untuk pengolahan citra digital berbasis Python, Tkinter, Pillow, dan Numpy.

## Struktur Folder

- pcd_app/
  - main.py
  - modules/
    - basic_ops.py
    - enhancement.py
    - noise.py
    - edge_detection.py
    - segmentation.py
    - about.py
  - assets/
    - sample_images/
    - icons/
      - undo.png
      - redo.png
- requirements.txt
- README.md

## Instalasi & Menjalankan Aplikasi

1. **Install Python**
   - Pastikan Python 3.8+ sudah terinstall di komputer Anda. Download di https://www.python.org/downloads/

2. **Install dependencies**
   Jalankan perintah berikut di terminal/cmd pada folder project:
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi**
   ```bash
   python pcd_app/main.py
   ```


1. **Buka Gambar**
   - Klik menu `File > Open Image` lalu pilih file gambar (jpg/png/bmp).

2. **Operasi Dasar**
   - Gunakan menu `Basic Ops`, `Enhancement`, `Noise`, `Edge Detection`, `Segmentation` untuk berbagai operasi citra.
   - Ikuti dialog/slider yang muncul untuk mengatur parameter operasi.

3. **Undo & Redo**
   - Gunakan tombol icon Undo/Redo di kiri atas (atau menu Edit) untuk membatalkan/mengulang perubahan gambar.
   - Shortcut: Ctrl+Z (Undo), Ctrl+Y (Redo).

4. **Simpan Gambar**
   - Klik `File > Save` untuk menyimpan perubahan ke file asli, atau `Save As` untuk menyimpan sebagai file baru.

5. **Tentang Aplikasi**
   - Klik menu `About` untuk info kelompok pengembang.

## Fitur Utama
## Cara Menggunakan (Panduan Pemula)

1. **Buka Gambar**
    - Klik menu `File > Open Image` lalu pilih file gambar (jpg/png/bmp).

2. **Operasi Dasar**
    - Gunakan menu `Basic Ops`, `Enhancement`, `Noise`, `Edge Detection`, `Segmentation` untuk berbagai operasi citra.
    - Ikuti dialog/slider yang muncul untuk mengatur parameter operasi.

3. **Undo & Redo**
    - Gunakan tombol icon Undo/Redo di kiri atas (atau menu Edit) untuk membatalkan/mengulang perubahan gambar.
    - Shortcut: Ctrl+Z (Undo), Ctrl+Y (Redo).

4. **Simpan Gambar**
    - Klik `File > Save` untuk menyimpan perubahan ke file asli, atau `Save As` untuk menyimpan sebagai file baru.

5. **Tentang Aplikasi**
    - Klik menu `About` untuk info kelompok pengembang.

## Catatan Penting
- Fitur preview sebelum apply TIDAK tersedia di versi ini.

## Fitur Utama
- Undo/Redo dengan icon dan shortcut
- Operasi dasar: Negative, Arithmetic, Boolean, Geometric
- Enhancement: Brightness, Contrast, Histogram, Smoothing, Sharpening
- Noise: Gaussian, Rayleigh, Erlang, Exponential, Uniform, Impulse
- Edge Detection: Sobel, Prewitt, Roberts, Laplacian, LoG, Canny, Compass
- Segmentation: Thresholding, Region Growing, Watershed

- UI mudah digunakan, cocok untuk pemula

---

Jika ada error saat menjalankan, pastikan semua dependensi sudah terinstall dan gunakan Python versi terbaru.
