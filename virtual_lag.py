import cv2
import pyvirtualcam
import time
import random
import threading
import pyaudio

# ================= PENGATURAN EFEK =================
IS_LAG_ACTIVE = True
# Peluang lag ditingkatkan (40% frame akan nyangkut)
LAG_PROBABILITY = 0.40 
# Durasi freeze sangat lama (1 hingga 4 detik)
MIN_FREEZE = 1.0
MAX_FREEZE = 4.0
# ===================================================

def process_audio():
    p = pyaudio.PyAudio()
    
    # Mencari indeks mikrofon bawaan dan output BlackHole
    input_idx = None
    output_idx = None
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if 'MacBook' in info['name'] or 'Built-in Microph' in info['name']:
            input_idx = info['index']
        if 'BlackHole 2ch' in info['name']:
            output_idx = info['index']
    
    if output_idx is None:
        print("Peringatan: BlackHole tidak terdeteksi. Suara tidak akan diproses.")
        return

    CHUNK = 1024
    RATE = 44100

    try:
        stream_in = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, 
                           input=True, input_device_index=input_idx, frames_per_buffer=CHUNK)
        stream_out = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, 
                            output=True, output_device_index=output_idx, frames_per_buffer=CHUNK)
        
        print("Audio Virtual (BlackHole) aktif. Suara akan ikut nge-lag!")
        
        while True:
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            
            # Logika Audio Lag: Jika sedang nge-lag, suara akan putus-putus/kosong (silence)
            if IS_LAG_ACTIVE and random.random() < 0.30: # 30% peluang suara hilang per sekian milidetik
                data = b'\x00' * len(data) # Ubah suara menjadi sunyi (stutter effect)
                
            stream_out.write(data)
            
    except Exception as e:
        print(f"Error Audio: {e}")

def process_video():
    cap = cv2.VideoCapture(1) # Gunakan 1 untuk Webcam Mac, atau 0
    time.sleep(1)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 30

    print(f"Memulai Virtual Camera {width}x{height}...")

    with pyvirtualcam.Camera(width, height, fps, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
        last_frame = None
        freeze_timer = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # MENCEGAH MIRROR: Balikkan gambar secara horizontal
            frame = cv2.flip(frame, 1)

            if IS_LAG_ACTIVE:
                if freeze_timer <= 0:
                    if random.random() < LAG_PROBABILITY: 
                        freeze_timer = random.uniform(MIN_FREEZE, MAX_FREEZE) 
                        last_frame = frame 
                
                if freeze_timer > 0:
                    freeze_timer -= (1.0 / fps)
                    frame = last_frame
            
            cv2.imshow("Preview Efek Lag Parah", frame)
            cam.send(frame)
            cam.sleep_until_next_frame()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# Jalankan Audio dan Video secara bersamaan
if __name__ == "__main__":
    audio_thread = threading.Thread(target=process_audio, daemon=True)
    audio_thread.start()
    process_video()