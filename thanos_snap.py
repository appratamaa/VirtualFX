import cv2
import pyvirtualcam
import numpy as np
import time

# 1. Inisialisasi Kamera
cap = cv2.VideoCapture(1) # Ganti 0 jika menggunakan iPhone/continuity, ganti 1 untuk webcam Mac
time.sleep(1.5) # Berikan waktu 1,5 detik agar Auto-Exposure kamera M1 selesai beradaptasi

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30

# 2. Ambil Background Stabil (Buang 15 frame pertama untuk menghindari transisi kecerahan)
print("Sedang kalibrasi kamera... Harap menyingkir dari kamera selama 2 detik!")
for _ in range(15):
    cap.read()
time.sleep(2)
ret, bg_frame = cap.read()
if not ret:
    print("Gagal menangkap kamera!")
    exit()
bg_frame = cv2.flip(bg_frame, 1)

# 3. Buat Subtractor MOG2 dengan Fitur Deteksi Bayangan (detectShadows=True)
subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

# Latih subtractor dengan background yang stabil agar sistem paham mana area statis
for _ in range(30):
    subtractor.apply(bg_frame)

print("Kamera terkalibrasi! Silakan kembali duduk.")
print("Tekan 's' di jendela preview untuk menghilang.")
print("Tekan 'r' untuk mereset.")

is_snapping = False
dissolve_value = 1.0

# Buat kernel untuk proses memperhalus (morphology)
kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)) # Untuk menutup lubang di dalam tubuh
kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))    # Untuk membuang bintik kecil di luar tubuh

with pyvirtualcam.Camera(width, height, fps, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        
        # 4. Deteksi Gerakan & Tubuh
        fg_mask = subtractor.apply(frame, learningRate=0.001) # Tetapkan learningRate sangat kecil agar tidak merekam Anda sebagai background
        
        # 5. Hilangkan Bayangan (Di MOG2, bayangan ditandai dengan pixel bernilai 127, kita abaikan saja)
        _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        
        # 6. FILTER MORFOLOGI (PENTING: Agar potongan tidak compang-camping)
        # Menutup lubang/bolong-bolong di bagian dalam tubuh
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_close, iterations=2)
        # Menghapus bintik-bintik noise kecil di luar tubuh
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open, iterations=1)
        
        # Buat mask 3 dimensi (BGR)
        condition = (thresh > 0)[..., np.newaxis]
        condition = np.concatenate([condition, condition, condition], axis=-1)
        
        # 7. Penerapan Efek "Thanos Snap"
        if is_snapping:
            dissolve_value -= 0.015 
            if dissolve_value < 0: dissolve_value = 0
            
            # Efek Partikel/Debu Bergerak
            noise = np.random.rand(height, width, 1)
            dust_condition = noise < dissolve_value
            
            final_condition = condition & dust_condition
            output_image = np.where(final_condition, frame, bg_frame)
        else:
            output_image = np.where(condition, frame, bg_frame)
            
        output_image = output_image.astype(np.uint8)

        # 8. Tampilkan & Kirim Stream
        cv2.imshow("Preview Efek Menghilang (Sempurna)", output_image)
        cam.send(output_image)
        cam.sleep_until_next_frame()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            is_snapping = True 
        elif key == ord('r'):
            is_snapping = False
            dissolve_value = 1.0 
        elif key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()