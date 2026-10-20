<p align="center">
  <h1 align="center">VIRTUAL FX (ZoomFX)</h1>
  <p align="center">
    <b>Aplikasi macOS Menu Bar Pintar untuk Efek Visual Thanos (Room Dust Disintegration), Pengubah Suara Chipmunk, & Simulasi Lag Ekstrem.</b>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-macOS-lightgrey?style=for-the-badge&logo=apple" alt="macOS">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-red?style=for-the-badge&logo=opencv" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<br/>

## ⯁ Tentang Proyek

**VirtualFX** adalah aplikasi ringan berbasis *macOS Menu Bar* murni yang berjalan di latar belakang tanpa ikon mengganggu di *Dock*. Dirancang khusus untuk memberikan sentuhan sinematik dan interaktif saat melakukan panggilan video (Zoom, Google Meet, Microsoft Teams, dll.) melalui kamera dan mikrofon virtual.

---

## ⯁ Fitur Unggulan

*   **► Thanos Room Disintegration & Reverse:** Menghancurkan seluruh ruangan beserta tubuh Anda menjadi partikel debu yang tertiup angin secara sinematik, serta dapat direkonstruksi balik secara halus saat di-*reset*.
*   **► Chipmunk Voice Changer:** Mengubah suara Anda menjadi nada tinggi yang imut dan khas menggunakan resampling interpolasi NumPy berlatensi rendah.
*   **► Extreme Lag Simulator:** Mensimulasikan jeda dan pembekuan video (*freeze*) serta pemutusan audio (*stutter/silence*) secara acak untuk keperluan uji jaringan atau hiburan.
*   **► Interactive macOS Integration:** Dilengkapi *popup* selamat datang kustom dan integrasi langsung ke profil profesional pengembang.

---

## ⯁ Prasyarat Sistem & Driver

Agar aplikasi ini dapat mengalirkan video dan audio virtual ke platform *meeting*, pastikan Mac Anda telah terpasang *driver* pendukung berikut:

1.  **OBS Virtual Camera** (untuk *output* video virtual).
2.  **BlackHole 2ch** (untuk *routing* audio virtual).

---

## ⯁ Panduan Instalasi (Bagi Pengguna yang baru Clone)

> **Catatan Penting:** Folder `venv`, `build`, dan `dist` sengaja tidak disertakan di dalam repository untuk menjaga ukuran tetap ringan. Anda dapat membuatnya secara otomatis melalui langkah-langkah di bawah ini.

**1. Clone Repositori ini:**
```bash
git clone https://github.com/UsernameAnda/VirtualFX.git
cd VirtualFX
```

**2. Jalankan Skrip Installer Otomatis:**
Cukup klik dua kali pada file `install_mac.command` yang ada di dalam folder, atau jalankan melalui Terminal:
```bash
chmod +x install_mac.command
./install_mac.command
```
*Skrip ini akan secara otomatis membuat `venv`, menginstal seluruh pustaka Python yang dibutuhkan, serta mengunduh driver pendukung.*

**3. Wajib Restart Mac Anda:**
Restart MacBook Anda agar driver audio BlackHole terbaca sempurna oleh sistem macOS.

**4. Jalankan Aplikasi:**
Buka file aplikasi `VirtualFX.app` di dalam folder `dist`. Ikon teks **ZoomFX** akan muncul di bagian Status Bar atas layar Mac Anda.

---

## ⯁ Panduan untuk Developer (Menjalankan dari Source Code)

Jika Anda ingin memodifikasi kode sumber (`app.py`) secara manual, ikuti langkah berikut di Terminal:

```bash
# 1. Buat dan aktifkan virtual environment mandiri
python3 -m venv venv
source venv/bin/activate

# 2. Instal dependensi pustaka
pip install opencv-python pyvirtualcam numpy pyaudio rumps

# 3. Jalankan aplikasi
python app.py
```

---

## ⯁ Cara Memaketkan Menjadi .app Mandiri (PyInstaller)

Untuk merakit ulang kode sumber menjadi aplikasi `.app` mandiri dengan PyInstaller, gunakan perintah berikut:

```bash
pyinstaller ZoomFX.spec
codesign --force --deep --sign - dist/VirtualFX.app
```

---

## ⯁ Developer & Kontributor

Dibuat dengan penuh dedikasi oleh **Andre Putra Pratama**.
Jangan lupa untuk terhubung dan memberikan dukungan pada profil LinkedIn pengembang!

## ⯁ Lisensi

Distribusi di bawah lisensi **MIT**. Bebas digunakan, dimodifikasi, dan dibagikan.