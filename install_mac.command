#!/bin/bash
cd "$(dirname "$0")"
echo "=== Memulai Instalasi ZoomFX untuk macOS ==="

# 1. Cek Homebrew, jika belum ada instal otomatis
if ! command -v brew &> /dev/null; then
    echo "Menginstal Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 2. Instal Driver Audio & Kamera Virtual via Homebrew
echo "Menginstal driver BlackHole dan OBS Virtual Camera..."
brew install --cask blackhole-2ch obs-virtualcam

# 3. Buat Virtual Environment & Instal Library Python
echo "Menginstal dependensi Python..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install opencv-python pyvirtualcam numpy pyaudio rumps

echo "=== Instalasi Selesai! Silakan restart Mac Anda sebelum menjalankan ZoomFX. ==="
read -p "Tekan [Enter] untuk keluar..."