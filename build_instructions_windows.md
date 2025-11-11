# Build Aplikasi PCD Tugas Besar Menjadi EXE (Windows)

Panduan ini untuk mengubah aplikasi Python Anda menjadi file .exe yang bisa di-download dan dijalankan tanpa Python.

## 1. Install PyInstaller

Buka terminal/cmd di folder project, lalu jalankan:
```bash
pip install pyinstaller
```

## 2. Build EXE

Jalankan perintah berikut dari root project:
```bash
pyinstaller --onefile --noconsole --add-data "pcd_app/assets;pcd_app/assets" pcd_app/main.py --name=PCD_TugasBesar
```
Penjelasan:
- `--onefile`: hasilkan 1 file exe
- `--noconsole`: tidak muncul jendela console
- `--add-data`: agar folder assets ikut dibundle
- `--name`: nama file exe

## 3. Hasil Build

- File exe akan ada di folder `dist/` dengan nama `PCD_TugasBesar.exe`
- Copy seluruh folder `dist/` ke komputer lain, aplikasi bisa dijalankan tanpa install Python.

## 4. Tips
- Pastikan semua gambar/icon ada di `pcd_app/assets`.
- Jika ada error import, tambahkan hidden-import di perintah pyinstaller.
- Untuk distribusi, bisa compress folder dist ke .zip sebelum upload/share.

---

Jika ingin installer (setup.exe), gunakan Inno Setup atau NSIS setelah build .exe.
## Catatan
- Fitur preview sebelum apply tidak tersedia di aplikasi ini. Semua operasi langsung diterapkan ke gambar utama.
