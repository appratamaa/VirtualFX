import cv2
import pyvirtualcam
import numpy as np
import time
import random
import pyaudio
import threading
import rumps
import subprocess
import webbrowser

# --- STATE GLOBAL ---
GLOBAL_STATE = {
    "lag_active": False,
    "snap_active": False,
    "voice_active": False
}

# --- FUNGSI POPUP & LINKEDIN ---
def show_welcome_popup():
    """Menampilkan popup sambutan saat aplikasi pertama kali berjalan di macOS"""
    script = (
        'display dialog "Terima kasih telah menggunakan VirtualFX!\\n\\n'
        'Suka dengan aplikasi ini? Yuk, dukung dan terhubung dengan developer-nya di LinkedIn." '
        'buttons {"Tutup", "Kunjungi LinkedIn"} '
        'default button "Kunjungi LinkedIn" '
        'with title "VirtualFX" with icon note'
    )
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if "Kunjungi LinkedIn" in result.stdout:
            webbrowser.open("https://www.linkedin.com/in/andreputrap/")
    except Exception:
        pass

# --- ENGINE AUDIO (CHIPMUNK & EXTREME AUDIO LAG) ---
def run_virtual_audio():
    p = pyaudio.PyAudio()
    input_idx = None
    output_idx = None
    
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        name = info['name']
        if info['maxInputChannels'] > 0 and ('Microphone' in name or 'MacBook' in name or 'Built-in' in name):
            if input_idx is None:
                input_idx = i
        if 'BlackHole 2ch' in name:
            output_idx = i

    if input_idx is None:
        input_idx = 0
    if output_idx is None:
        return

    CHUNK = 1024
    RATE = 44100
    
    try:
        stream_in = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, input_device_index=input_idx, frames_per_buffer=CHUNK)
        stream_out = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, output_device_index=output_idx, frames_per_buffer=CHUNK)
        
        lag_counter = 0
        
        while True:
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # 1. EFEK CHIPMUNK
            if GLOBAL_STATE["voice_active"]:
                original_len = len(audio_data)
                factor = 1.5
                x_old = np.arange(original_len)
                x_new = np.linspace(0, original_len, int(original_len / factor))
                resampled = np.interp(x_new, x_old, audio_data).astype(np.int16)
                
                if len(resampled) < original_len:
                    audio_data = np.pad(resampled, (0, original_len - len(resampled)), 'constant')
                else:
                    audio_data = resampled[:original_len]

            # 2. EFEK AUDIO LAG EXTREME
            if GLOBAL_STATE["lag_active"]:
                if lag_counter > 0:
                    audio_data = np.zeros(CHUNK, dtype=np.int16) 
                    lag_counter -= 1
                elif random.random() < 0.55: 
                    lag_counter = random.randint(3, 8) 
                    audio_data = np.zeros(CHUNK, dtype=np.int16)

            stream_out.write(audio_data.tobytes())
    except Exception as e:
        pass

# --- ENGINE VIDEO (FULL ROOM THANOS DUST & EXTREME VIDEO LAG) ---
def run_virtual_camera():
    cap = cv2.VideoCapture(1)
    time.sleep(1.5)
    width, height = int(cap.get(3)), int(cap.get(4))
    
    freeze_timer = 0
    last_frame = None
    
    was_snap = False
    frozen_frame = None
    dust_canvas = None
    dissolve_val = 0.0

    with pyvirtualcam.Camera(width, height, 30, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
        while True:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)

            # 1. EFEK LAG VIDEO EXTREME
            if GLOBAL_STATE["lag_active"]:
                if freeze_timer <= 0:
                    if random.random() < 0.70: 
                        freeze_timer = random.uniform(2.0, 6.0) 
                        last_frame = frame
                if freeze_timer > 0:
                    freeze_timer -= (1.0 / 30)
                    if last_frame is not None:
                        frame = last_frame
            else: 
                freeze_timer = 0

            # 2. EFEK THANOS SELURUH RUANGAN & REVERSE
            if GLOBAL_STATE["snap_active"]:
                if not was_snap:
                    was_snap = True
                    frozen_frame = frame.copy()
                    dissolve_val = 0.0
                    dust_canvas = np.zeros_like(frame)
                
                dissolve_val += 0.012 
                if dissolve_val > 1.2: dissolve_val = 1.2
                
                noise = np.random.rand(height, width)
                intact_mask = (noise > dissolve_val)
                just_dusted = (noise > (dissolve_val - 0.03)) & (noise <= dissolve_val)
                
                M_wind = np.float32([[1, 0, 8], [0, 1, -5]])
                dust_canvas = cv2.warpAffine(dust_canvas, M_wind, (width, height))
                
                new_dust = np.zeros_like(frame)
                new_dust[just_dusted] = frozen_frame[just_dusted]
                dust_canvas = cv2.add(dust_canvas, new_dust)
                
                out_img = np.zeros_like(frame)
                out_img[intact_mask] = frozen_frame[intact_mask]
                out_img = cv2.add(out_img, dust_canvas)
                
            else:
                if was_snap:
                    dissolve_val -= 0.025
                    if dissolve_val <= 0.0:
                        was_snap = False
                        dissolve_val = 0.0
                        out_img = frame
                    else:
                        M_reverse = np.float32([[1, 0, -8], [0, 1, 5]])
                        dust_canvas = cv2.warpAffine(dust_canvas, M_reverse, (width, height))
                        
                        noise = np.random.rand(height, width)
                        intact_mask = (noise > dissolve_val)
                        
                        out_img = np.zeros_like(frame)
                        out_img[intact_mask] = frozen_frame[intact_mask]
                        out_img = cv2.add(out_img, dust_canvas)
                else:
                    out_img = frame

            cam.send(out_img.astype(np.uint8))
            cam.sleep_until_next_frame()

# --- ANTARMUKA MENU BAR MAC ---
class ZoomFXApp(rumps.App):
    def __init__(self):
        super().__init__("ZoomFX") 
        
        self.menu = [
            rumps.MenuItem("Status: Siap Digunakan"),
            None,
            rumps.MenuItem("Efek Sinyal Lag (Video & Audio)", callback=self.toggle_lag),
            rumps.MenuItem("Efek Thanos Ruangan Menghilang", callback=self.toggle_snap),
            rumps.MenuItem("Efek Suara Chipmunk (Tupai)", callback=self.toggle_voice),
            None,
            rumps.MenuItem("Kunjungi LinkedIn Developer", callback=self.open_linkedin),
            rumps.MenuItem("Tutup VirtualFX", callback=self.quit_app)
        ]

    def toggle_lag(self, sender):
        GLOBAL_STATE["lag_active"] = not GLOBAL_STATE["lag_active"]
        sender.state = 1 if GLOBAL_STATE["lag_active"] else 0

    def toggle_snap(self, sender):
        GLOBAL_STATE["snap_active"] = not GLOBAL_STATE["snap_active"]
        sender.state = 1 if GLOBAL_STATE["snap_active"] else 0

    def toggle_voice(self, sender):
        GLOBAL_STATE["voice_active"] = not GLOBAL_STATE["voice_active"]
        sender.state = 1 if GLOBAL_STATE["voice_active"] else 0

    def open_linkedin(self, sender):
        webbrowser.open("https://www.linkedin.com/in/andreputrap/")

    def quit_app(self, sender):
        rumps.quit_application()

if __name__ == '__main__':
    # Munculkan popup sambutan di awal dalam thread terpisah agar tidak memblokir UI
    threading.Thread(target=show_welcome_popup, daemon=True).start()
    
    # Jalankan engine audio dan video
    threading.Thread(target=run_virtual_audio, daemon=True).start()
    threading.Thread(target=run_virtual_camera, daemon=True).start()
    
    ZoomFXApp().run()