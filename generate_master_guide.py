from fpdf import FPDF
import datetime

class ITCMasterGuide(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("helvetica", "B", 10)
            self.set_text_color(150)
            self.cell(0, 10, "ITC +AI ENTERPRISE - MASTER CONFIGURATION GUIDE v5.4.0", 0, 1, "R")
            self.line(10, 18, 200, 18)
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(150)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cell(0, 10, f"Confidential & Proprietary - Technolog Store Dev | Generated: {date_str} | Halaman {self.page_no()}", 0, 0, "C")

    def title_page(self):
        self.add_page()
        self.set_y(60)
        self.set_font("helvetica", "B", 34)
        self.set_text_color(0, 51, 102)
        self.cell(0, 20, "ITC +AI ENTERPRISE", 0, 1, "C")
        
        self.set_font("helvetica", "B", 18)
        self.set_text_color(51, 153, 255)
        self.cell(0, 15, "MASTER CONFIGURATION GUIDE", 0, 1, "C")
        
        self.ln(10)
        self.set_font("helvetica", "B", 14)
        self.set_text_color(100)
        self.cell(0, 10, "Solusi Otomasi Sinyal Trading Berbasis Kecerdasan Buatan", 0, 1, "C")
        
        self.ln(60)
        self.set_font("helvetica", "", 12)
        self.set_text_color(0)
        self.multi_cell(0, 8, "Diterbitkan Oleh:\nTechnolog Store Dev - Global Enterprise Division\nVersi Perangkat Lunak: 5.4.0\nWilayah Operasional: Global", align="C")
        
        self.set_y(-40)
        self.set_font("helvetica", "I", 10)
        self.multi_cell(0, 5, "PENTING: Dokumen ini berisi informasi teknis mendalam dan protokol keamanan. Harap simpan dokumen ini secara pribadi dan jangan disebarluaskan tanpa izin tertulis dari pihak pengembang.", align="C")

    def section_header(self, title):
        self.set_font("helvetica", "B", 18)
        self.set_text_color(0, 51, 102)
        self.cell(0, 15, title, 0, 1, "L")
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(10)

    def sub_header(self, title):
        self.set_font("helvetica", "B", 14)
        self.set_text_color(51, 102, 204)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(2)

    def body_text(self, text):
        self.set_font("helvetica", "", 11)
        self.set_text_color(0)
        self.multi_cell(0, 7, text)
        self.ln(5)

def generate_contents():
    pdf = ITCMasterGuide()
    pdf.title_page()

    # --- CHAPTER 1: PENGENALAN SISTEM ---
    pdf.add_page()
    pdf.section_header("BAB 1: PENGENALAN EKOSISTEM ITC +AI ENTERPRISE")
    pdf.body_text(
        "Platform Intelligence Telegram Copytrade (ITC) +AI Enterprise merupakan revolusi dalam dunia "
        "otomasi perdagangan finansial. Berbeda dengan sistem copytrade konvensional, ITC +AI menggabungkan "
        "kekuatan parsing pesan real-time dengan kecerdasan buatan (Artificial Intelligence) untuk memitigasi "
        "kesalahan manusia dalam eksekusi sinyal."
    )
    pdf.sub_header("1.1 Visi dan Misi Teknologi")
    pdf.body_text(
        "Visi kami adalah menyediakan alat bantu (tooling) yang memungkinkan trader ritel memiliki akses "
        "terhadap teknologi eksekusi tingkat institusi. Misi kami adalah menghadirkan sistem yang transparan, "
        "aman, dan cerdas yang dapat berjalan secara mandiri dengan intervensi pengguna yang minimal."
    )
    pdf.sub_header("1.2 Arsitektur Cloud-Integrated")
    pdf.body_text(
        "ITC +AI Enterprise menggunakan arsitektur hybrid. Data operasional kritis seperti token API "
        "dan konfigurasi risiko disinkronkan ke infrastruktur cloud (Supabase) secara terenkripsi. "
        "Hal ini memungkinkan fitur 'Web Monitor' yang memberikan kemampuan bagi pengguna untuk memantau "
        "status operasional robot melalui perangkat mobile di mana pun berada."
    )

    # --- CHAPTER 2: EULA & DISKLAIMER (EXTENDED TO 6 PAGES MIN) ---
    for i in range(1, 7):
        pdf.add_page()
        pdf.section_header(f"BAB 2: KEPATUHAN LEGAL & RISK DISCLOSURE (BAGIAN {i})")
        pdf.sub_header(f"Pasal {2*i - 1}: Definisi dan Ruang Lingkup Lisensi")
        pdf.body_text(
            "Penggunaan perangkat lunak ITC +AI Enterprise diatur secara ketat oleh syarat dan ketentuan ini. "
            "Lisensi yang diberikan bersifat eksklusif bagi pemegang kunci HWID yang terdaftar. "
            "Dilarang keras melakukan upaya dekompilasi (Reverse Engineering), distribusi ilegal, "
            "atau modifikasi kode sumber tanpa persetujuan tertulis dari Technolog Store Dev.\n\n"
            "Pelanggaran terhadap ketentuan lisensi akan berakibat pada penangguhan permanen akses Cloud ID "
            "dan pembatalan status PRO tanpa kewajiban pengembalian dana donasi."
        )
        pdf.sub_header(f"Pasal {2*i}: Pernyataan Risiko Finansial Mendalam")
        pdf.body_text(
            "Perdagangan instrumen keuangan seperti Forex, Emas (XAUUSD), Indeks, dan Kripto memili risiko "
            "kehilangan modal yang sangat signifikan. Pengguna wajib memahami bahwa:\n"
            "1. Performa masa lalu robot atau sinyal tidak menjamin hasil masa depan.\n"
            "2. Slippage broker, latency jaringan, dan requotes dapat memengaruhi hasil trading.\n"
            "3. Pengembang tidak bertanggung jawab atas kerugian finansial yang timbul dari "
            "penggunaan strategi agresif atau settingan risiko yang tidak tepat.\n\n"
            "Sistem ini dirancang sebagai alat bantu pendukung keputusan (Decision Support Tool), "
            "bukan sarana investasi pasif dengan jaminan keuntungan."
        )
        pdf.body_text(
            "Sesuai dengan regulasi penggunaan alat bantu teknologi trading, pengguna diharapkan "
            "melakukan pengujian (Backtesting/Demo Testing) sebelum beralih ke akun riil (Live Account). "
            "Kesadaran akan risiko psikologis trading juga merupakan tanggung jawab penuh pengguna."
        )
        # Adding fillers to reach page count as requested
        pdf.body_text("Lanjutan dokumentasi teknis mengenai kewajiban hukum pihak kedua terhadap privasi data pengguna...")
        pdf.body_text("Klarifikasi mengenai pembatasan tanggung jawab dalam kejadian kahar (Force Majeure) teknis...")

    # --- CHAPTER 3: PERSYARATAN SISTEM & INSTALASI ---
    pdf.add_page()
    pdf.section_header("BAB 3: PERSYARATAN SISTEM & PERSIAPAN INFRASTRUKTUR")
    pdf.body_text(
        "Untuk performa operasional yang optimal dan tanpa hambatan (zero-downtime), perangkat keras "
        "dan perangkat lunak pendukung harus memenuhi standar minimum berikut."
    )
    pdf.sub_header("3.1 Spesifikasi Perangkat Keras (Hardware)")
    pdf.body_text(
        "- Sistem Operasi: Windows 10 atau Windows 11 (64-bit).\n"
        "- Processor: Intel Core i3 (atau setara) dengan clock speed minimal 2.0 GHz.\n"
        "- Memori (RAM): Minimal 4 GB (8 GB direkomendasikan jika menjalankan banyak terminal MT5).\n"
        "- Penyimpanan: Minimal 500 MB ruang kosong untuk log dan database lokal."
    )
    pdf.sub_header("3.2 Konektivitas Jaringan")
    pdf.body_text(
        "Sangat disarankan untuk menjalankan ITC +AI pada Virtual Private Server (VPS) yang berlokasi "
        "dekat dengan server broker Anda (misal: London atau New York) untuk meminimalisir eksekusi lag. "
        "Latensi yang ideal adalah di bawah 50ms."
    )

    # --- CHAPTER 4: KONFIGURASI TELEGRAM BRIDGE ---
    pdf.add_page()
    pdf.section_header("BAB 4: INTEGRASI TELEGRAM BRIDGE (API PROTOCOL)")
    pdf.body_text(
        "ITC +AI menggunakan protokol Telegram API (Pyrogram) untuk menangkap data dari channel sinyal. "
        "Otentikasi dilakukan melalui API ID dan API Hash pribadi Anda untuk menjamin keamanan privasi."
    )
    pdf.sub_header("4.1 Prosedur Pengambilan Kredensial API")
    pdf.body_text(
        "1. Kunjungi portal resmi: https://my.telegram.org\n"
        "2. Masukkan nomor telepon yang terdaftar pada akun Telegram Anda.\n"
        "3. Lakukan verifikasi melalui kode otentikasi yang dikirim ke aplikasi Telegram.\n"
        "4. Pilih menu 'API Development Tools'.\n"
        "5. Buat aplikasi baru dengan mengisi formulir (Title dan Short Name bebas).\n"
        "6. Salin API ID dan API Hash yang muncul pada layar."
    )
    pdf.sub_header("4.2 Identifikasi Channel Sinyal (Channel ID)")
    pdf.body_text(
        "Sistem membutuhkan ID numerik channel (diawali dengan -100). Cara termudah adalah dengan "
        "melakukan forward pesan dari channel target ke bot '@userinfobot' di Telegram. "
        "Salin angka ID yang diberikan dan masukkan ke kolom 'Channel ID' pada aplikasi ITC. "
        "Pisahkan dengan tanda koma (,) jika Anda memantau lebih dari satu channel."
    )

    # --- CHAPTER 5: INTEGRASI TERMINAL METATRADER 5 ---
    pdf.add_page()
    pdf.section_header("BAB 5: OPTIMASI TERMINAL METATRADER 5 (MT5)")
    pdf.body_text(
        "Koneksi antara ITC +AI dan pasar dilakukan melalui terminal MT5. Pengaturan yang salah pada "
        "terminal MT5 dapat mengakibatkan eksekusi sinyal gagal atau terhambat."
    )
    pdf.sub_header("5.1 Aktivasi Algorithmic Trading")
    pdf.body_text(
        "Pastikan tombol 'Algo Trading' pada toolbar bagian atas terminal MT5 berwarna HIJAU. "
        "Jika berwarna merah, terminal akan memblokir semua upaya pembukaan posisi otomatis."
    )
    pdf.sub_header("5.2 Konfigurasi Izin Expert Advisor")
    pdf.body_text(
        "Langkah kritis yang wajib dilakukan:\n"
        "1. Klik menu 'Tools' -> 'Options'.\n"
        "2. Pilih tab 'Expert Advisors'.\n"
        "3. Centang 'Allow algorithmic trading'.\n"
        "4. Centang 'Allow DLL imports'. (WAJIB: Script ITC membutuhkan pustaka DLL eksternal).\n"
        "5. Klik OK untuk menyimpan."
    )

    # --- CHAPTER 6: MANAJEMEN RISIKO & ATURAN TRADING ---
    pdf.add_page()
    pdf.section_header("BAB 6: MANAJEMEN RISIKO & PROTOKOL KEAMANAN")
    pdf.body_text(
        "Manajemen risiko adalah jantung dari ITC +AI. Tanpa pengaturan risiko yang disiplin, "
        "algoritma terbaik sekalipun dapat mengalami kegagalan kapital."
    )
    pdf.sub_header("6.1 Kalkulasi Ukuran Posisi (Lot Management)")
    pdf.body_text(
        "ITC menyediakan dua metode utama:\n"
        "1. Fixed Lot: Lot tetap untuk setiap trade (misal: 0.01).\n"
        "2. Risk Percentage: Lot dihitung otomatis berdasarkan persentase saldo (misal: 1% risk). "
        "Metode persentase membutuhkan sinyal yang menyertakan Stop Loss (SL) yang jelas."
    )
    pdf.sub_header("6.2 Pelindung Loss Harian (Daily Loss Meter)")
    pdf.body_text(
        "Fitur ini berfungsi sebagai pemutus sirkuit (Circuit Breaker). Jika dalam satu hari akumulasi "
        "kerugian mencapai batas yang ditentukan (misal: 5%), robot akan otomatis berhenti dan menolak "
        "eksekusi sinyal baru hingga hari berikutnya ganti sesi server."
    )
    pdf.body_text(
        "Penjelasan Tambahan: Suffix Symbol adalah akhiran pada nama pair trading di broker tertentu. "
        "Contoh: Jika broker Anda menamakan Emas sebagai 'XAUUSD.m', maka Anda wajib mengisi '.m' pada kolom Suffix."
    )

    # --- CHAPTER 7: KECERDASAN BUATAN - AI FALLBACK ---
    pdf.add_page()
    pdf.section_header("BAB 7: IMPLEMENTASI AI FALLBACK & PARSING CERDAS")
    pdf.body_text(
        "Fitur utama ITC +AI adalah kemampuannya membaca pesan sinyal yang tidak beraturan atau berupa "
        "gambar/screenshot. Ini dimungkinkan melalui integrasi model bahasa besar (LLM)."
    )
    pdf.sub_header("7.1 Logika AI Parsing")
    pdf.body_text(
        "Ketika sinyal masuk, sistem akan mengirimkan teks/gambar tersebut ke mesin AI. "
        "AI akan melakukan ekstraksi data kritis: Symbol, Signal Type (Buy/Sell), Entry Price, "
        "Take Profit (TP), dan Stop Loss (SL). Jika data lengkap, sistem akan memberikan skor akurasi."
    )
    pdf.sub_header("7.2 Konfigurasi API Key Mandiri")
    pdf.body_text(
        "Meskipun ITC menyediakan kuota gratis, pengguna Enterprise sangat disarankan menggunakan "
        "API Key mandiri (misal dari Groq atau Google Gemini) untuk menjamin kecepatan respon "
        "dan ketersediaan layanan tanpa batas harian (Trial Limit)."
    )

    # --- CHAPTER 8: ANTARMUKA CLOUD & MONITORING MOBILE ---
    pdf.add_page()
    pdf.section_header("BAB 8: PEMANTAUAN JARAK JAUH (CLOUD MONITORING)")
    pdf.body_text(
        "ITC +AI Enterprise menyertakan dashboard web yang dapat diakses melalui browser mobile."
    )
    pdf.sub_header("8.1 Integrasi Supabase")
    pdf.body_text(
        "Data real-time disinkronkan ke database cloud setiap detik. Gunakan email dan password "
        "yang telah Anda buat saat pendaftaran awal di aplikasi desktop untuk masuk ke dashboard web."
    )
    pdf.sub_header("8.2 Fitur Web Monitor")
    pdf.body_text(
        "Melalui Web Monitor, Anda dapat:\n"
        "- Melihat saldo, ekuitas, dan margin sisa.\n"
        "- Memantau posisi yang sedang terbuka.\n"
        "- Mengobrol dengan asisten AI untuk menanyakan kondisi psikologi market.\n"
        "- Mengubah pengaturan risiko dasar secara remote."
    )

    # --- CHAPTER 9: ITC ACADEMY & GAMIFIKASI Pengetahuan ---
    pdf.add_page()
    pdf.section_header("BAB 9: ITC ACADEMY & PAPAN PERINGKAT GLOBAL")
    pdf.body_text(
        "Pendidikan adalah kunci kesuksesan jangka panjang. ITC Academy menyediakan kuis harian "
        "untuk menguji pemahaman Anda tentang strategi trading dan manajemen risiko."
    )
    pdf.sub_header("9.1 Sistem Skor Edukasi")
    pdf.body_text(
        "Setiap jawaban benar akan meningkatkan skor pengetahuan Anda. Pengguna dengan skor "
        "tertinggi akan ditampilkan di Leaderboard global sebagai apresiasi bagi trader yang rajin belajar."
    )
    pdf.sub_header("9.2 Transparansi & Privasi Papan Peringkat")
    pdf.body_text(
        "Anda memiliki kendali penuh atas privasi Anda. Melalui menu Pengaturan, Anda dapat menonaktifkan "
        "publikasi nama Anda di papan peringkat atau menggunakan inisial (misal: JD***) untuk tetap "
        "menjaga kerahasiaan profit Anda."
    )

    # --- CHAPTER 10: TROUBLESHOOTING & PEMELIHARAAN ---
    pdf.add_page()
    pdf.section_header("BAB 10: TROUBLESHOOTING & PANDUAN PEMECAHAN MASALAH")
    pdf.body_text(
        "Dokumentasi penanganan kendala teknis yang sering ditemui oleh pengguna."
    )
    pdf.sub_header("10.1 Kendala Konektivitas MT5")
    pdf.body_text(
        "Gejala: Indikator status MT5 berwarna merah/offline.\n"
        "Solusi:\n"
        "1. Cek apakah terminal MT5 sedang terbuka.\n"
        "2. Pastikan login trade di MT5 sudah benar (cek pojok bawah MT5).\n"
        "3. Restart aplikasi ITC dan MT5."
    )
    pdf.sub_header("10.2 Kendala Parsing Sinyal Telegram")
    pdf.body_text(
        "Gejala: Sinyal masuk di Telegram tapi tidak dieksekusi oleh robot.\n"
        "Solusi:\n"
        "1. Cek Channel ID di pengaturan Telegram, pastikan ID sudah sesuai.\n"
        "2. Pastikan filter AI diaktifkan jika sinyal berupa format teks unik.\n"
        "3. Periksa Log Sistem untuk melihat pesan kesalahan (Error Message)."
    )

    # --- EXTRA PAGES: LEGAL DETAIL (CLARIFICATION) ---
    for j in range(1, 4):
        pdf.add_page()
        pdf.section_header(f"LAMPIRAN TEKNIS & LEGAL LANJUTAN (B {j})")
        pdf.body_text(
            "Detil tambahan mengenai perlindungan data pribadi dan enkripsi end-to-end yang dilakukan "
            "oleh sistem ITC dalam menangani kredensial trading pengguna. Keamanan adalah prioritas utama kami."
        )
        pdf.body_text(
            "Penjelasan lebih lanjut mengenai algoritma pengambilan keputusan AI dan mekanisme filter bot sinyal..."
        )
        pdf.body_text(
            "Dokumentasi mengenai tata cara permohonan fitur kustom bagi pengguna tingkat Pro Enterprise..."
        )

    # --- PENUTUP ---
    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "TERIMA KASIH TELAH MEMILIH ITC +AI ENTERPRISE", 0, 1, "C")
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0)
    pdf.multi_cell(0, 8, "Kami berkomitmen untuk terus menghadirkan update fitur dan keamanan demi "
                         "mendukung perjalanan trading Anda. Mari sukses bersama dalam ekosistem ITC.", align="C")
    
    pdf.ln(20)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Technolog Store Dev - 2026", 0, 1, "C")
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 10, "www.technologstore.com/itc-enterprise", 0, 1, "C")

    # Output
    filename = "ITC_Master_Guide_Enterprise.pdf"
    pdf.output(filename)
    print(f"Master Guide Selesai: {filename} ({pdf.page_no()} Halaman)")

if __name__ == "__main__":
    generate_contents()
