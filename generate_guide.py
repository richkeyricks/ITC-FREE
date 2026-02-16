from fpdf import FPDF

class ITC_Guide(FPDF):
    def header(self):
        # Header - only show on sub-pages if titles are long
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Halaman {self.page_no()} - Sahabat ITC +AI Enterprise", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("helvetica", "B", 16)
        self.set_fill_color(230, 230, 250)  # Lavender light
        self.cell(0, 10, title, 0, 1, "L", True)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("helvetica", "", 12)
        self.multi_cell(0, 7, body)
        self.ln()

def create_pdf():
    pdf = ITC_Guide()
    pdf.add_page()
    
    # --- HALAMAN JUDUL ---
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(0, 51, 102) # Dark Blue
    pdf.cell(0, 40, "BUKU PANDUAN SAHABAT ITC +AI", 0, 1, "C")
    
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Panduan Super Mudah & Super Detail - Versi Anak SD", 0, 1, "C")
    
    pdf.ln(20)
    pdf.set_font("helvetica", "I", 12)
    pdf.multi_cell(0, 10, "Halo Sahabat! Buku ini akan menemanimu berkenalan dengan Robot ITC +AI. \nBacalah pelan-pelan ya, supaya kita bisa dapet untung bareng-bareng!", align="C")
    
    pdf.ln(20)
    
    # --- BAGIAN 1: EULA (JANJI SAHABAT) ---
    pdf.chapter_title("1. JANJI SAHABAT ITC (Aturan Main)")
    eula_elif = (
        "Sebelum kita mulai, yuk kita buat janji dulu! Seperti main lari-larian, kita harus tahu aturan mainnya:\n\n"
        "1. Robot Ini Teman Bantu: Robot ini hanya membantu kamu. Dia bukan tukang sihir yang bisa merubah daun jadi emas. Kamu tetap yang pegang kendali.\n\n"
        "2. Hati-Hati Uang Bisa Hilang: Main trading itu seperti main sepeda, kadang bisa jatuh (rugi). Jangan pakai uang jajan sekolah ya, pakai uang yang memang 'boleh' hilang.\n\n"
        "3. Kamu Penentunya: Semua tombol yang kamu tekan adalah tanggung jawabmu. Robot cuma jalankan perintahmu saja.\n\n"
        "4. Menjaga Rahasia: Password dan kunci akunmu jangan dikasih ke siapa-siapa ya. Cuma kamu dan robotmu yang boleh tahu!\n\n"
        "5. Bukan Janji Pasti Kaya: Kita berusaha bareng, tapi robot tidak menjanjikan pasti untung terus. Kadang market lagi galak, jadi kita harus sabar.\n\n"
        "DENGAN MEMAKAI ROBOT INI, BERARTI KAMU SUDAH SETUJU DAN PAHAM JANJI DI ATAS!"
    )
    pdf.chapter_body(eula_elif)

    # --- BAGIAN 2: TUTORIAL KONEKSI (CARA MENYALAKAN ROBOT) ---
    pdf.add_page()
    pdf.chapter_title("2. CARA MENYALAKAN ROBOTMU (Tutorial Dari Nol)")
    tutorial_elif = (
        "Ikuti langkah-langkah ini ya, jangan ada yang dilewatkan!\n\n"
        "LANGKAH A: Siapkan Kandang Robot (Laptop & Internet)\n"
        "- Pakai Laptop Windows ya. Pastikan Internetnya kencang, supaya robot tidak ngantuk.\n\n"
        "LANGKAH B: Pasang Mesin Kerja (MT5)\n"
        "- Download MT5 dari websitemu. Pasang dan buka aplikasinya. \n"
        "- INGAT: MT5 harus selalu terbuka di laptopmu kalau mau robot kerja!\n\n"
        "LANGKAH C: Kasih Ijin Robot (Paling Penting!)\n"
        "- Di MT5, klik tombol 'Algo Trading' sampai warnanya HIJAU.\n"
        "- Buka menu Tools -> Options -> Expert Advisors.\n"
        "- Centang (Klik) kotak: Allow Algorithmic Trading dan Allow DLL Imports.\n\n"
        "LANGKAH D: Hubungkan ke Telegram\n"
        "- Ambil Kunci (API ID & Hash) dari my.telegram.org.\n"
        "- Masukkan nomor rumah (Channel ID) ke aplikasi ITC.\n\n"
        "LANGKAH E: Klik MULAI!\n"
        "- Masuk ke Dashboard, klik tombol besar 'MULAI COPIER'.\n"
        "- Selesai! Robot sekarang sudah siap jaga pintu buat kamu."
    )
    pdf.chapter_body(tutorial_elif)

    # --- BAGIAN 3: KENALAN SAMA FITUR (APA SAJA YANG BISA DILAKUKAN?) ---
    pdf.add_page()
    pdf.chapter_title("3. KENALAN SAMA FITUR HEBAT (Cara Mainnya)")
    features_elif = (
        "Robotmu punya banyak jurus rahasia lho:\n\n"
        "A. SAKLAR LAMPU (DASHBOARD)\n"
        "- Tombol Mulai/Berhenti itu seperti saklar lampu. Klik untuk kasih tugas ke robot.\n\n"
        "B. BENSIN MOBIL (METER RUGI)\n"
        "- Kalau bar bensinnya penuh ke kanan, robot akan istirahat buat jagain uangmu.\n\n"
        "C. ASISTEN PINTAR (CHAT AI)\n"
        "- Kamu bisa ngobrol sama robot! Tanya apa saja, nanti asisten AI yang jawab.\n\n"
        "D. TEROPONG AJAIB (ANALISA SINYAL)\n"
        "- Robot bisa gambar grafik otomatis! Dia kasih tahu kamu sinyalnya bagus atau tidak.\n\n"
        "E. SATPAM PENJAGA (MANAJEMEN RISIKO)\n"
        "- Kamu bisa suruh robot: 'Jangan habiskan uang lebih dari 5% ya!'. Nanti satpam ini akan jaga uangmu.\n\n"
        "F. SEKOLAH TRADING (AKADEMI)\n"
        "- Ada kuis seru! Sambil nunggu robot kerja, kamu bisa belajar biar makin pintar.\n\n"
        "G. PAPAN JUARA (LEADERBOARD)\n"
        "- Kalau kamu pintar dan profit, namamu akan muncul di papan juara dunia!"
    )
    pdf.chapter_body(features_elif)

    # --- PENUTUP ---
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Selamat Berteman Dengan Robot ITC +AI!", 0, 1, "C")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 10, "Technolog Store Dev - 2026", 0, 1, "C")

    # Save
    pdf.output("ITC_Guide_Lengkap.pdf")
    print("PDF Berhasil Dibuat: ITC_Guide_Lengkap.pdf")

if __name__ == "__main__":
    create_pdf()
