import math
import threading
import tkinter as tk
from tkinter import messagebox
import re

import speech_recognition as sr



BG_COLOR = "#0F1419"  
CARD_COLOR = "#1A2332" 
TEXT_BG = "#111820"
TEXT_FG = "#FFFFFF"  
MUTED_TEXT = "#8B94A6"  

PRIMARY = "#7C3AED"
PRIMARY_HOVER = "#9968F4"  
LISTENING_COLOR = "#FF4757"  
SUCCESS_COLOR = "#2ED573"  
WARNING_COLOR = "#FFB643"  
DANGER_COLOR = "#FF6B6B"  
DANGER_HOVER = "#FF8787"

WAVE_COLOR = (255, 71, 87)  
BG_RGB = (15, 20, 25)

CANVAS_SIZE = 240
CENTER = CANVAS_SIZE // 2
BASE_RADIUS = 46
MAX_RADIUS = 108
RING_COUNT = 4



AUTO_CORRECT_DICT = {
    "paiton": "python",
    "pyhton": "python",
    "piton": "python",
    "jawa": "java",
    "javas": "javascript",
    "javas krip": "javascript",
    "javascript krip": "javascript",
    "c plus plus": "C++",
    "c sharp": "C#",
    "node js": "Node.js",
    "type script": "typescript",
    "selenim": "selenium",
    "data base": "database",
    "api": "API",
    "html": "HTML",
    "css": "CSS",
    "js": "JS",
    "sql": "SQL",
    "xml": "XML",
    "json": "JSON",
    "rest": "REST",
    "git hab": "GitHub",
    "github": "GitHub",
    "version control": "version control",
    "framework": "framework",
    "library": "library",
    "plugin": "plugin",
    "debug": "debug",
    "refaktor": "refactor",
    "refactor": "refactor",
    "optimasi": "optimization",
    "optimize": "optimize",
    "deploy": "deploy",
    "server": "server",
    "client": "client",
    "database": "database",
    "algoritma": "algorithm",
    "algoritm": "algorithm",
    
    "kodenya": "kodenya",
    "aku ingin": "saya ingin",
    "saya mau": "saya ingin",
    "mohon": "mohon",
    "tolong": "tolong",
    
    "klik klik": "klik",
    "ok ok": "oke",
    "baik baik": "baik",
    
}


class SpeechToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceNote — Speech to Text")
        self.root.geometry("760x700")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(680, 620)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.10
        self.recognizer.dynamic_energy_ratio = 1.25
        self.recognizer.energy_threshold = 180
        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.4
        self.recognizer.phrase_threshold = 0.15

        self.is_listening = False
        self.stop_listening_func = None
        self.wave_progress = [i / RING_COUNT for i in range(RING_COUNT)]
        self.animation_job = None

        self._build_ui()

    def _build_ui(self):
        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=24, pady=20)

        header = tk.Frame(container, bg=BG_COLOR)
        header.pack(fill="x", pady=(0, 16))

        tk.Label(
            header,
            text="VoiceNote",
            font=("Segoe UI", 28, "bold"),
            fg=TEXT_FG,
            bg=BG_COLOR,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Ubah suara menjadi teks dengan koreksi otomatis",
            font=("Segoe UI", 10),
            fg=MUTED_TEXT,
            bg=BG_COLOR,
        ).pack(anchor="w", pady=(6, 0))

        # Microphone card dengan border yang lebih subtle
        mic_card = tk.Frame(
            container,
            bg=CARD_COLOR,
            highlightthickness=1,
            highlightbackground="#2D3E52",
        )
        mic_card.pack(fill="x", pady=(0, 16))

        mic_inner = tk.Frame(mic_card, bg=CARD_COLOR)
        mic_inner.pack(pady=20)

        self.canvas = tk.Canvas(
            mic_inner,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            bg=CARD_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.wave_ids = []
        for _ in range(RING_COUNT):
            ring = self.canvas.create_oval(
                CENTER - BASE_RADIUS,
                CENTER - BASE_RADIUS,
                CENTER + BASE_RADIUS,
                CENTER + BASE_RADIUS,
                outline=CARD_COLOR,
                width=3,
            )
            self.wave_ids.append(ring)

        # Outer glow circle dengan warna yang lebih harmonis
        self.mic_shadow = self.canvas.create_oval(
            CENTER - BASE_RADIUS - 8,
            CENTER - BASE_RADIUS - 8,
            CENTER + BASE_RADIUS + 8,
            CENTER + BASE_RADIUS + 8,
            fill="#2A1F3D",
            outline="",
        )

        self.mic_circle = self.canvas.create_oval(
            CENTER - BASE_RADIUS,
            CENTER - BASE_RADIUS,
            CENTER + BASE_RADIUS,
            CENTER + BASE_RADIUS,
            fill=PRIMARY,
            outline="",
        )

        self.mic_text = self.canvas.create_text(
            CENTER,
            CENTER,
            text="🎤",
            font=("Segoe UI Emoji", 36),
        )

        for item in (self.mic_shadow, self.mic_circle, self.mic_text):
            self.canvas.tag_bind(item, "<Button-1>", lambda e: self.toggle_listening())

        self.canvas.config(cursor="hand2")

        self.status_label = tk.Label(
            mic_inner,
            text="Siap mendengarkan",
            font=("Segoe UI", 12, "bold"),
            fg=SUCCESS_COLOR,
            bg=CARD_COLOR,
        )
        self.status_label.pack(pady=(4, 0))

        self.helper_label = tk.Label(
            mic_inner,
            text="Klik mikrofon untuk mulai atau berhenti",
            font=("Segoe UI", 9),
            fg=MUTED_TEXT,
            bg=CARD_COLOR,
        )
        self.helper_label.pack(pady=(6, 0))

        # Sensitivity control dengan styling yang lebih baik
        sensitivity_card = tk.Frame(container, bg=CARD_COLOR)
        sensitivity_card.pack(fill="x", pady=(0, 16))

        sensitivity_inner = tk.Frame(sensitivity_card, bg=CARD_COLOR)
        sensitivity_inner.pack(fill="x", padx=16, pady=12)

        tk.Label(
            sensitivity_inner,
            text="Sensitivitas Mikrofon",
            font=("Segoe UI", 10, "bold"),
            fg=TEXT_FG,
            bg=CARD_COLOR,
        ).pack(side="left")

        self.sensitivity_value = tk.Label(
            sensitivity_inner,
            text="Sedang",
            font=("Segoe UI", 9, "bold"),
            fg=PRIMARY_HOVER,
            bg=CARD_COLOR,
        )
        self.sensitivity_value.pack(side="right")

        self.sensitivity = tk.Scale(
            sensitivity_card,
            from_=1,
            to=5,
            orient="horizontal",
            showvalue=False,
            resolution=1,
            command=self._change_sensitivity,
            bg=CARD_COLOR,
            fg=TEXT_FG,
            troughcolor="#253349",
            activebackground=PRIMARY_HOVER,
            highlightthickness=0,
            bd=0,
            length=300,
        )
        self.sensitivity.set(3)
        self.sensitivity.pack(fill="x", padx=14, pady=(0, 10))

        # Transcript header dengan action button
        transcript_header = tk.Frame(container, bg=BG_COLOR)
        transcript_header.pack(fill="x", pady=(0, 10))

        tk.Label(
            transcript_header,
            text="Hasil Transkripsi",
            font=("Segoe UI", 12, "bold"),
            fg=TEXT_FG,
            bg=BG_COLOR,
        ).pack(side="left")

        button_frame = tk.Frame(transcript_header, bg=BG_COLOR)
        button_frame.pack(side="right")

        self.clear_btn = tk.Button(
            button_frame,
            text="Hapus teks",
            command=self.clear_text,
            font=("Segoe UI", 9, "bold"),
            bg=DANGER_COLOR,
            fg="white",
            activebackground=DANGER_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
        )
        self.clear_btn.pack(side="right")
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg=DANGER_HOVER))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg=DANGER_COLOR))

        self.copy_btn = tk.Button(
            button_frame,
            text="Salin",
            command=self.copy_text,
            font=("Segoe UI", 9, "bold"),
            bg=PRIMARY,
            fg="white",
            activebackground=PRIMARY_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
        )
        self.copy_btn.pack(side="right", padx=(0, 8))
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg=PRIMARY_HOVER))
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg=PRIMARY))

        # Transcript card
        text_card = tk.Frame(
            container,
            bg=TEXT_BG,
            highlightthickness=1,
            highlightbackground="#2D3E52",
        )
        text_card.pack(fill="both", expand=True)

        self.text_area = tk.Text(
            text_card,
            wrap="word",
            font=("Segoe UI", 11),
            bg=TEXT_BG,
            fg=TEXT_FG,
            insertbackground=PRIMARY,
            selectbackground=PRIMARY,
            selectforeground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=14,
            spacing1=3,
            spacing3=5,
        )
        self.text_area.pack(fill="both", expand=True, side="left")

        scrollbar = tk.Scrollbar(
            text_card,
            command=self.text_area.yview,
            relief="flat",
            bd=0,
            bg=CARD_COLOR,
        )
        scrollbar.pack(side="right", fill="y", padx=(0, 2))
        self.text_area.config(yscrollcommand=scrollbar.set)

        footer_frame = tk.Frame(container, bg=BG_COLOR)
        footer_frame.pack(fill="x", pady=(10, 0))

        tk.Label(
            footer_frame,
            text="🌐 Bahasa: Indonesia",
            font=("Segoe UI", 9),
            fg=MUTED_TEXT,
            bg=BG_COLOR,
        ).pack(side="left")

        tk.Label(
            footer_frame,
            text="✓ Auto-correct aktif",
            font=("Segoe UI", 9),
            fg=SUCCESS_COLOR,
            bg=BG_COLOR,
        ).pack(side="right")

    @staticmethod
    def _blend(rgb_from, rgb_to, t):
        r = int(rgb_from[0] + (rgb_to[0] - rgb_from[0]) * t)
        g = int(rgb_from[1] + (rgb_to[1] - rgb_from[1]) * t)
        b = int(rgb_from[2] + (rgb_to[2] - rgb_from[2]) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _animate_waves(self):
        if not self.is_listening:
            for ring in self.wave_ids:
                self.canvas.itemconfig(ring, outline=CARD_COLOR)
            self.canvas.itemconfig(self.mic_circle, fill=PRIMARY)
            self.canvas.itemconfig(self.mic_shadow, fill="#2A1F3D")
            return

        self.canvas.itemconfig(self.mic_circle, fill=LISTENING_COLOR)
        self.canvas.itemconfig(self.mic_shadow, fill="#4A1A28")

        for i, ring in enumerate(self.wave_ids):
            progress = self.wave_progress[i]
            radius = BASE_RADIUS + progress * (MAX_RADIUS - BASE_RADIUS)
            color = self._blend(WAVE_COLOR, BG_RGB, progress)

            self.canvas.coords(
                ring,
                CENTER - radius,
                CENTER - radius,
                CENTER + radius,
                CENTER + radius,
            )
            self.canvas.itemconfig(ring, outline=color)

            self.wave_progress[i] += 0.018
            if self.wave_progress[i] > 1:
                self.wave_progress[i] = 0

        self.animation_job = self.root.after(30, self._animate_waves)

    def _change_sensitivity(self, value):
        level = int(float(value))

        labels = {
            1: ("Rendah", 1.60),
            2: ("Agak rendah", 1.40),
            3: ("Sedang", 1.25),
            4: ("Sensitif", 1.10),
            5: ("Sangat sensitif", 0.95),
        }

        label, ratio = labels[level]
        self.sensitivity_value.config(text=label)
        self.recognizer.dynamic_energy_ratio = ratio

        if level >= 4:
            self.recognizer.energy_threshold = min(
                self.recognizer.energy_threshold, 220
            )
        elif level == 3:
            self.recognizer.energy_threshold = min(
                self.recognizer.energy_threshold, 300
            )

    def toggle_listening(self):
        if self.is_listening:
            self._stop_listening()
        else:
            self._start_listening()

    def _start_listening(self):
        self.is_listening = True
        self.status_label.config(
            text="Sedang mendengarkan...",
            fg=WARNING_COLOR,
        )
        self.helper_label.config(text="Silakan berbicara dengan jelas")
        self.wave_progress = [i / RING_COUNT for i in range(RING_COUNT)]
        self._animate_waves()

        def begin():
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1.2)
                    self.recognizer.energy_threshold = max(
                        120, min(self.recognizer.energy_threshold, 450)
                    )

                self.stop_listening_func = self.recognizer.listen_in_background(
                    self.microphone,
                    self._on_phrase,
                    phrase_time_limit=12,
                )

            except Exception as e:
                self._show_error(str(e))
                self.is_listening = False
                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text="Mikrofon tidak tersedia",
                        fg=DANGER_COLOR,
                    ),
                )

        threading.Thread(target=begin, daemon=True).start()

    def _stop_listening(self):
        self.is_listening = False

        if self.stop_listening_func:
            self.stop_listening_func(wait_for_stop=False)
            self.stop_listening_func = None

        self.status_label.config(
            text="Perekaman dihentikan",
            fg=SUCCESS_COLOR,
        )
        self.helper_label.config(text="Klik mikrofon untuk mulai lagi")

    def _auto_correct(self, text):
        """
        Menerapkan auto-correct pada teks yang dikenali.
        Mendukung matching case-insensitive dan word boundaries.
        """
        if not text.strip():
            return text

        corrected = text
        words = corrected.split()
        corrected_words = []

        for word in words:
            # Cek apakah kata lengkap cocok dengan kamus
            word_lower = word.lower()
            
            # Coba exact match dulu (case-insensitive)
            if word_lower in AUTO_CORRECT_DICT:
                corrected_words.append(AUTO_CORRECT_DICT[word_lower])
            else:
                # Coba partial/fuzzy matching untuk kesalahan huruf
                found = False
                for key, value in AUTO_CORRECT_DICT.items():
                    # Jika panjang berbeda banyak, lewatkan
                    if abs(len(word_lower) - len(key)) > 2:
                        continue
                    
                    # Simple similarity check
                    if self._string_similarity(word_lower, key) > 0.75:
                        corrected_words.append(value)
                        found = True
                        break
                
                if not found:
                    corrected_words.append(word)

        return " ".join(corrected_words)

    @staticmethod
    def _string_similarity(s1, s2):
        """
        Menghitung similarity antara dua string menggunakan
        Levenshtein distance approximation.
        """
        if len(s1) == 0 or len(s2) == 0:
            return 0.0
        
        matches = sum(1 for a, b in zip(s1, s2) if a == b)
        return matches / max(len(s1), len(s2))

    def _on_phrase(self, recognizer, audio):
        try:
            text = recognizer.recognize_google(audio, language="id-ID")
            if text.strip():
                # Terapkan auto-correct sebelum menambahkan teks
                corrected_text = self._auto_correct(text)
                self._append_text(corrected_text)

        except sr.UnknownValueError:
            # Suara tidak dikenali, biarkan saja
            pass

        except sr.RequestError as e:
            self._show_error(
                f"Gagal terhubung ke layanan pengenalan suara:\n{e}"
            )

    def _append_text(self, text):
        def do_append():
            current = self.text_area.get("1.0", "end-1c").strip()

            if current:
                self.text_area.insert("end", " " + text)
            else:
                self.text_area.insert("end", text)

            self.text_area.see("end")

        self.root.after(0, do_append)

    def copy_text(self):
        """Menyalin teks ke clipboard."""
        content = self.text_area.get("1.0", "end-1c").strip()
        
        if not content:
            messagebox.showinfo("Info", "Tidak ada teks untuk disalin")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Sukses", "Teks berhasil disalin ke clipboard")

    def _show_error(self, message):
        self.root.after(
            0,
            lambda: messagebox.showerror("Error", message),
        )

    def clear_text(self):
        content = self.text_area.get("1.0", "end-1c").strip()

        if not content:
            return

        if messagebox.askyesno(
            "Hapus teks",
            "Hapus seluruh hasil transkripsi di layar?",
        ):
            self.text_area.delete("1.0", "end")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()
