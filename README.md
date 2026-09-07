# 🐍 Python Mini Projects

Kumpulan proyek Python yang saya buat untuk belajar dan mengembangkan
kemampuan dalam **Python, Computer Vision, Hand Tracking, Game
Development, GUI, dan Audio Processing**.

Proyek ini berisi beberapa eksperimen dan aplikasi sederhana yang dibuat
secara bertahap, mulai dari program dasar hingga proyek yang
memanfaatkan kamera dan interaksi berbasis gesture.

------------------------------------------------------------------------

## 📌 Daftar Proyek

  -----------------------------------------------------------------------
  Proyek                  Deskripsi               Teknologi
  ----------------------- ----------------------- -----------------------
  📷 **Filter**           Aplikasi kamera dengan  Python, OpenCV,
                          kontrol berbasis        MediaPipe
                          gerakan tangan untuk    
                          memilih dan menggunakan 
                          filter.                 

  🐦 **Flappy Bird**      Game bergaya Flappy     Python, Pygame
                          Bird yang dibuat ulang  
                          menggunakan Python.     

  🌫️ **Blur**             Eksperimen efek blur    Python, OpenCV
                          pada gambar/video       
                          menggunakan kamera.     

  🕐 **Clock**            Aplikasi jam digital    Python, Tkinter
                          sederhana.              

  🖐️ **Gesture**          Eksperimen pengenalan   Python, MediaPipe
                          gesture tangan          
                          menggunakan kamera.     

  ✋ **Hand Tracking**    Program untuk           Python, OpenCV,
                          mendeteksi dan melacak  MediaPipe
                          posisi tangan secara    
                          real-time.              

  🧮 **Kalkulator**       Kalkulator sederhana    Python
                          berbasis Python.        

  🎵 **Lirik**            Program yang berkaitan  Python
                          dengan                  
                          tampilan/pengelolaan    
                          lirik.                  

  🧩 **Puzzle**           Game puzzle sederhana.  Python

  🐍 **Snake**            Game Snake sederhana.   Python, Pygame

  🎙️ **Speech**           Eksperimen pengenalan   Python
                          suara/speech            
                          processing.             

  ⏱️ **Stopwatch**        Stopwatch digital       Python, Tkinter
                          dengan tombol Start,    
                          Stop, dan Reset.        

  ❌⭕ **Tic Tac Toe**    Game Tic Tac Toe        Python
                          sederhana.              
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# ⭐ Featured Project --- Filter Camera

**Filter** merupakan salah satu proyek yang memanfaatkan **Computer
Vision dan Hand Tracking** untuk membuat interaksi kamera menggunakan
gerakan tangan.

Aplikasi menggunakan kamera untuk mendeteksi tangan secara real-time.
Pengguna tidak perlu bergantung sepenuhnya pada mouse atau keyboard
karena beberapa fungsi dapat dikendalikan menggunakan gesture.

### 🖐️ Kontrol Gesture

-   ☝️ **Telunjuk + Jempol**\
    Digunakan sebagai gesture utama untuk berinteraksi dan memainkan
    aplikasi.

-   🤙 **Kelingking**\
    Digunakan untuk mengganti atau berpindah filter.

Dengan pendekatan ini, kamera tidak hanya berfungsi sebagai alat untuk
mengambil gambar, tetapi juga menjadi media interaksi antara pengguna
dan aplikasi.

### Teknologi

-   **Python**
-   **OpenCV** --- pemrosesan gambar dan kamera
-   **MediaPipe** --- deteksi serta tracking tangan secara real-time

------------------------------------------------------------------------

# 🐦 Featured Project --- Flappy Bird

Proyek **Flappy Bird** adalah implementasi game sederhana yang
terinspirasi dari game **Flappy Bird**.

> Catatan: Flappy Bird bukan game tahun 2000-an. Game aslinya dirilis
> pada **2013** dan menjadi sangat populer pada awal hingga pertengahan
> 2010-an.

Versi pada repository ini dibuat sebagai proyek pembelajaran untuk
memahami konsep dasar game development menggunakan Python.

### Konsep yang Dipelajari

-   Game loop
-   Pergerakan objek
-   Collision detection
-   Score system
-   Pengaturan kecepatan
-   Input pemain
-   Rendering menggunakan Pygame

------------------------------------------------------------------------

# 🛠️ Teknologi yang Digunakan

Project ini terutama menggunakan:

-   **Python 3.10 -- 3.12**
-   **OpenCV**
-   **MediaPipe**
-   **Pygame**
-   **PyOpenGL**
-   **NumPy**
-   **Tkinter**

> **Catatan:** Yang dimaksud pada README lama dengan "Python 10--12"
> adalah **Python 3.10--3.12**. Python 10--12 bukan versi Python yang
> digunakan pada project ini.

------------------------------------------------------------------------

# 🚀 Instalasi

## 1. Clone Repository

``` bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
```

Ganti `USERNAME/REPOSITORY` dengan alamat repository kamu.

------------------------------------------------------------------------

## 2. Buat Virtual Environment

Windows:

``` powershell
python -m venv .venv
```

Aktifkan virtual environment:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Jika PowerShell menolak menjalankan script, gunakan:

``` powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Kemudian aktifkan kembali:

``` powershell
.\.venv\Scripts\Activate.ps1
```

------------------------------------------------------------------------

## 3. Install Library

Jalankan:

``` powershell
python -m pip install numpy opencv-python mediapipe pygame PyOpenGL
```

> Tkinter biasanya sudah tersedia pada instalasi Python untuk Windows.
> Jika tidak tersedia, pastikan Python yang digunakan merupakan
> instalasi resmi yang menyertakan Tk/Tcl.

------------------------------------------------------------------------

# ▶️ Menjalankan Project

Setelah virtual environment aktif dan library telah terpasang, jalankan
file Python sesuai proyek yang ingin dicoba.

Contoh:

``` powershell
python filter.py
```

atau:

``` powershell
python flappyBird/flappyBird.py
```

Untuk stopwatch:

``` powershell
python stopwatch.py
```

Nama file dapat disesuaikan dengan struktur repository.

------------------------------------------------------------------------

# 📁 Struktur Repository

``` text
Python-Projects/
│
├── filter/
│
├── flappyBird/
│   └── pipeTop.png
│
├── README.md
│
├── blur.py
├── clock.py
├── gesture.py
├── hand.py
├── hbd.py
├── kalkulator.py
├── lirik.py
├── note.txt
├── puzzle.py
├── snake.py
├── speech.py
├── stopwatch.py
└── tictactoe.py
```

------------------------------------------------------------------------

# 🎯 Tujuan Project

Repository ini dibuat sebagai **portofolio dan dokumentasi proses
belajar Python**.

Melalui proyek-proyek ini, saya mempelajari berbagai konsep, seperti:

-   Dasar-dasar pemrograman Python
-   Pemrograman berorientasi objek dan struktur program
-   GUI sederhana
-   Game development
-   Computer Vision
-   Hand Tracking
-   Gesture Recognition
-   Pemrosesan gambar
-   Pemrosesan suara
-   Penggunaan library pihak ketiga
-   Pengelolaan project menggunakan Git dan GitHub

------------------------------------------------------------------------

# 📈 Progress

Project ini akan terus dikembangkan dengan menambahkan fitur,
meningkatkan tampilan, memperbaiki performa, serta membuat proyek-proyek
Python yang lebih kompleks.

Jika menemukan bug atau memiliki saran pengembangan, masukan sangat
terbuka.

------------------------------------------------------------------------

## 👨‍💻 Author

**Rafa Ahmad Zakaria**

> Python • Computer Vision • Game Development • Software Development

------------------------------------------------------------------------

## 📄 License

Project ini dibuat untuk tujuan **pembelajaran dan portofolio pribadi**.
