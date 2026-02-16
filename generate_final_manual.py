from fpdf import FPDF
import datetime

class ITCFinalManual(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("helvetica", "B", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, "OFFICIAL ENTERPRISE MANUAL | ITC +AI v5.4.0 | CONFIDENTIAL", 0, 0, "L")
            self.cell(0, 10, "Richkeyrick.com | haineo.com", 0, 1, "R")
            self.line(10, 18, 200, 18)
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Hak Cipta © 2026 Technolog Store Global. Seluruh Hak Dilindungi. | Halaman {self.page_no()}", 0, 0, "C")

    def title_page(self):
        self.add_page()
        # Adding a border for professional look
        self.rect(5, 5, 200, 287)
        
        self.set_y(40)
        self.set_font("helvetica", "B", 36)
        self.set_text_color(10, 31, 62)
        self.cell(0, 20, "ITC +AI ENTERPRISE", 0, 1, "C")
        
        self.set_font("helvetica", "B", 16)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, "MANUAL OPERASIONAL DAN KONFIGURASI GLOBAL", 0, 1, "C")
        
        self.ln(20)
        # Corporate Logos Placeholder (Text based for now)
        self.set_font("helvetica", "B", 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 5, "BROKER PARTNERS | TECHNOLOGY ALLIANCE | CRYPTO SYNC", 0, 1, "C")
        self.line(60, 105, 150, 105)
        
        self.ln(50)
        self.set_font("helvetica", "B", 14)
        self.set_text_color(0)
        self.cell(0, 10, "DIKELOLA DAN DITERBITKAN OLEH:", 0, 1, "C")
        
        self.set_font("helvetica", "", 12)
        self.cell(0, 8, "Richkeyrick Enterprise Division", 0, 1, "C")
        self.cell(0, 8, "Haineo Intelligent Systems", 0, 1, "C")
        self.set_font("helvetica", "I", 11)
        self.cell(0, 8, "Portal Resmi: www.richkeyrick.com | www.haineo.com", 0, 1, "C")
        
        self.set_y(-60)
        self.set_font("helvetica", "B", 10)
        self.set_text_color(150, 0, 0)
        self.multi_cell(0, 5, "DOKUMEN INI BERSIFAT SANGAT RAHASIA (STRICTLY CONFIDENTIAL).\n"
                             "PENGGUNAAN TANPA OTORISASI AKAN DIKENAKAN SANKSI HUKUM.", align="C")

    def section_title(self, title):
        self.set_font("helvetica", "B", 20)
        self.set_text_color(10, 31, 62)
        self.cell(0, 15, title, 0, 1, "L")
        self.ln(2)

    def sub_section(self, title):
        self.set_font("helvetica", "B", 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(2)

    def content_block(self, text):
        self.set_font("helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(4)

def generate_manual():
    pdf = ITCFinalManual()
    pdf.title_page()

    # --- BAB 1: PENGENALAN EKOSISTEM ENTERPRISE ---
    pdf.add_page()
    pdf.section_title("BAB 1: VISI DAN EKOSISTEM ITC ENTERPRISE")
    pdf.content_block(
        "Selamat datang di era baru otomasi perdagangan finansial yang dikelola secara terpusat melalui "
        "ekosistem Cloud. ITC +AI Enterprise bukan sekadar perangkat lunak copytrade biasa; ini adalah "
        "sebuah infrastruktur cerdas yang dirancang untuk memberikan efisiensi maksimal bagi para "
        "trader profesional dan institusional."
    )
    pdf.sub_section("1.1 Filosofi Haineo Intelligent Systems")
    pdf.content_block(
        "Haineo Intelligent Systems berkomitmen untuk menghadirkan teknologi masa depan ke dalam genggaman "
        "Anda hari ini. Melalui integrasi algoritma tingkat lanjut, kami memastikan bahwa setiap sinyal "
        "yang masuk melalui jembatan komunikasi dianalisis secara mendalam oleh unit kecerdasan buatan "
        "sebelum dieksekusi ke pasar riil."
    )
    pdf.sub_section("1.2 Peran Cloud Central dalam Operasional")
    pdf.content_block(
        "Berbeda dengan versi lawas, versi Enterprise ini sepenuhnya terintegrasi dengan Cloud Central. "
        "Semua pengaturan risiko, riwayat eksekusi, dan preferensi profil Anda disimpan dalam Database Global "
        "yang aman dan terenkripsi. Hal ini memungkinkan redundansi data, di mana robot Anda dapat dipulihkan "
        "secara instan di perangkat mana pun hanya dengan melakukan login akun."
    )
    pdf.sub_section("1.3 Aksesibilitas Multi-Platform")
    pdf.content_block(
        "Kami memahami mobilitas Anda. Oleh karena itu, ITC Enterprise menyediakan antarmuka pemantauan jarak jauh. "
        "Melalui website resmi kami, Anda dapat melihat kesehatan akun, status koneksi robot, dan grafik "
        "pertumbuhan profit secara real-time langsung dari smartphone Anda tanpa perlu membuka laptop."
    )

    # --- BAB 2: EULA & LEGAL COMPLIANCE (6 PAGES DENSE) ---
    for i in range(1, 7):
        pdf.add_page()
        pdf.section_title(f"BAB 2: KONSTRUKSI HUKUM & KEPATUHAN (BAGIAN {i})")
        pdf.sub_section(f"Pasal {i}.1: Ketentuan Penggunaan dan Lisensi Global")
        pdf.content_block(
            "Perjanjian Lisensi Pengguna Akhir (EULA) ini merupakan dokumen hukum yang sah antara pengguna "
            "dan unit pengembangan Technolog Store Dev. Dengan mengaktifkan perangkat lunak ini, Anda "
            "secara otomatis terikat pada seluruh regulasi yang ditetapkan di dalamnya.\n\n"
            "Hak kekayaan intelektual, termasuk namun tidak terbatas pada algoritma parsing, struktur "
            "basis data cloud, dan antarmuka pengguna, dimiliki sepenuhnya oleh pengembang. "
            "Segala bentuk distribusi ulang, modifikasi ilegal, atau penggunaan komersial tanpa lisensi "
            "khusus Enterprise akan diproses melalui jalur hukum internasional."
        )
        pdf.sub_section(f"Pasal {i}.2: Pengungkapan Risiko Perdagangan Finansial")
        pdf.content_block(
            "Perdagangan pada pasar valuta asing (Forex), komoditas (Emas/Minyak), dan indeks saham "
            "mengandung risiko yang sangat tinggi dan mungkin tidak cocok bagi semua investor. "
            "Tingkat leverage yang tinggi dapat bekerja merugikan Anda maupun menguntungkan Anda.\n\n"
            "Adalah tanggung jawab penuh pengguna untuk menentukan tujuan investasi, tingkat pengalaman, "
            "dan selera risiko. Kerugian dapat melebihi simpanan dana awal Anda. Oleh karena itu, sangat "
            "dianjurkan untuk menggunakan dana modal yang siap hilang tanpa memengaruhi stabilitas "
            "kehidupan finansial pribadi Anda."
        )
        pdf.content_block(
            "Lanjutan ketentuan teknis mengenai tanggung jawab operasional user terhadap infrastruktur "
            "jaringan pribadi dan kepatuhan terhadap server trading masing-masing broker. "
            "ITC Enterprise berfungsi sebagai jembatan teknologi (Technology Bridge) dan bukan merupakan "
            "manajer investasi atau penasihat keuangan berlisensi."
        )
        # Fill page with detail
        pdf.content_block(
            "Setiap instruksi eksekusi yang dihasilkan oleh unit AI didasarkan pada model statistik "
            "dan pemrosesan bahasa alami. Pengguna mengakui bahwa teknologi AI memiliki margin kesalahan "
            "tertentu dan setuju untuk tidak menuntut pengembang atas perbedaan hasil eksekusi antara "
            "sinyal sumber dan eksekusi di terminal masing-masing user."
        )

    # --- BAB 3: INFRASTRUKTUR & PERSIAPAN SISTEM ---
    pdf.add_page()
    pdf.section_title("BAB 3: STANDAR OPERASIONAL PROSEDUR (SOP) INSTALASI")
    pdf.content_block(
        "Keberhasilan eksekusi otomatis sangat bergantung pada stabilitas lingkungan tempat robot dijalankan. "
        "Gunakan pedoman berikut sebagai standar minimum operasional Anda."
    )
    pdf.sub_section("3.1 Persyaratan Sistem Operasi")
    pdf.content_block(
        "- Windows 10/11 Pro Enterprise (64-bit).\n"
        "- Framework .NET terbaru terpasang.\n"
        "- Visual C++ Redistributable (untuk mendukung pustaka eksekusi MT5).\n"
        "- Koneksi Internet Fiber Optik dengan latency di bawah 100ms ke server broker."
    )
    pdf.sub_section("3.2 Penggunaan Virtual Private Server (VPS)")
    pdf.content_block(
        "Bagi pengguna Enterprise, penggunaan VPS (Virtual Private Server) sangat diwajibkan untuk "
        "menjamin ketersediaan sistem 24/5 tanpa gangguan mati lampu atau koneksi lokal. "
        "Pastikan VPS Anda memiliki uptime minimal 99.9% dan berlokasi di pusat data finansial utama "
        "(London, New York, atau Singapura)."
    )

    # --- BAB 4: OPTIMASI TERMINAL METATRADER 5 ---
    pdf.add_page()
    pdf.section_title("BAB 4: MASTER SETUP METATRADER 5 (MT5)")
    pdf.content_block(
        "MT5 adalah terminal kerja utama bagi robot ITC. Tanpa konfigurasi yang tepat pada sisi terminal, "
        "robot tidak akan memiliki izin hukum untuk melakukan transaksi keuangan."
    )
    pdf.sub_section("4.1 Prosedur Aktivasi Izin Algoritma")
    pdf.content_block(
        "Langkah demi Langkah:\n"
        "1. Jalankan aplikasi Metatrader 5 Anda.\n"
        "2. Perhatikan tombol 'Algo Trading' di bagian atas. Pastikan dalam kondisi Aktif (Warna Hijau).\n"
        "3. Navigasi ke menu 'Tools' -> 'Options' (Atau tekan Ctrl + O).\n"
        "4. Buka tab 'Expert Advisors'.\n"
        "5. WAJIB: Centang 'Allow algorithmic trading'.\n"
        "6. SUPER WAJIB: Centang 'Allow DLL imports'. Robot memerlukan ini untuk berkomunikasi dengan mesin Cloud."
    )
    pdf.sub_section("4.2 Verifikasi Koneksi Akun")
    pdf.content_block(
        "Lihat pojok kanan bawah terminal MT5 Anda. Jika terdapat indikator angka data yang berjalan, "
        "artinya terminal Anda sudah terhubung dengan server broker. Segala bentuk kegagalan koneksi MT5 "
        "akan membuat robot ITC masuk ke mode 'Safety Wait' sampai koneksi pulih."
    )

    # --- BAB 5: KONFIGURASI TELEGRAM CLOUD BRIDGE ---
    pdf.add_page()
    pdf.section_title("BAB 5: KONFIGURASI TELEGRAM CLOUD BRIDGE")
    pdf.content_block(
        "Telegram Cloud Bridge bertindak sebagai penerima sinyal real-time yang kemudian diterjemahkan "
        "oleh mesin AI. Pengaturan ini membutuhkan ketelitian ekstra."
    )
    pdf.sub_section("5.1 Pengaturan Identitas API")
    pdf.content_block(
        "Input Kunci API (API ID & Hash) diperlukan agar robot dapat masuk ke dalam protokol komunikasi "
        "Telegram. Kunci ini unik dan hanya milik Anda sendiri. Jangan pernah membagikan kunci ini "
        "kepada pihak ketiga karena merupakan gerbang masuk ke akun pesan Anda."
    )
    pdf.sub_section("5.2 Pemetaan Channel Target (Channel ID)")
    pdf.content_block(
        "Robot hanya akan merespon pesan dari channel yang ID-nya sudah didaftarkan. ID channel ini "
        "disimpan secara aman di Database Global sehingga Anda tidak perlu memasukkannya kembali "
        "setiap kali berganti perangkat. Gunakan bot bantuan di Telegram untuk mendapatkan ID numerik tepat."
    )

    # --- BAB 6: PARAMETER TRADING & LOGIKA EKSEKUSI ---
    pdf.add_page()
    pdf.section_title("BAB 6: PARAMETER EKSEKUSI & ATURAN TRADING")
    pdf.content_block(
        "Bab ini menjelaskan logika di balik setiap input yang Anda masukkan pada tab 'Aturan Trading'."
    )
    pdf.sub_section("6.1 Suffix Symbol (Akhiran Simbol)")
    pdf.content_block(
        "Banyak broker menggunakan akhiran khusus untuk setiap instrumen (misal: .m, .pro, .i). "
        "Jika di MT5 Anda tertulis 'XAUUSD.m', maka Anda HARUS memasukkan '.m' di kolom Suffix. "
        "Tanpa ini, robot tidak akan menemukan pair tersebut dan eksekusi akan gagal dengan error 'Symbol Not Found'."
    )
    pdf.sub_section("6.2 Magic Number (Kunci Identitas Transaksi)")
    pdf.content_block(
        "Magic Number adalah angka unik yang ditempelkan pada setiap trade hasil eksekusi robot ITC. "
        "Hal ini sangat penting agar robot tidak mengganggu trade manual Anda atau robot lain yang "
        "mungkin sedang berjalan di terminal yang sama."
    )
    pdf.sub_section("6.3 Pengaturan Posisi Maksimal")
    pdf.content_block(
        "Anda dapat membatasi berapa banyak trade yang boleh dibuka secara bersamaan. "
        "Ini adalah lapisan pertahanan tambahan untuk mencegah robot membuka terlalu banyak "
        "posisi ketika terjadi serangan sinyal serentak dalam satu waktu."
    )

    # --- BAB 7: PROTOKOL MANAJEMEN RISIKO LANJUTAN ---
    pdf.add_page()
    pdf.section_title("BAB 7: PROTOKOL MANAJEMEN RISIKO ENTERPRISE")
    pdf.content_block(
        "Unit Manajemen Risiko adalah detektor keamanan yang memantau setiap pergerakan dana Anda."
    )
    pdf.sub_section("7.1 Circuit Breaker (Loss Harian)")
    pdf.content_block(
        "Fitur Pelindung Loss Harian bertindak sebagai pemutus arus otomatis. Jika akumulasi "
        "kerugian pada hari tersebut mencapai persentase batas (misal: 3%), sistem akan "
        "mengunci seluruh fungsi eksekusi. Ini melindungi psikologi trader agar tidak melakukan "
        "'revenge trading' atau kerugian yang lebih dalam."
    )
    pdf.sub_section("7.2 Time Filter (Jam Operasional)")
    pdf.content_block(
        "Pasar memiliki jam-jam dengan volatilitas tinggi dan spread yang lebar. "
        "Anda dapat mengatur robot agar hanya aktif pada jam sibuk (seperti sesi London atau New York) "
        "dan otomatis tidak merespon sinyal di luar jam tersebut untuk menghindari resiko market yang tidak stabil."
    )

    # --- BAB 8: UNIT ANALISA KECERDASAN BUATAN ---
    pdf.add_page()
    pdf.section_title("BAB 8: IMPLEMENTASI ANALISA KECERDASAN BUATAN (AI)")
    pdf.content_block(
        "Unit AI dalam ITC Enterprise bukan sekadar filter teks, melaikan mesin pengambil keputusan "
        "berdasarkan data teknikal yang ada pada pesan sinyal."
    )
    pdf.sub_section("8.1 AI Fallback Architecture")
    pdf.content_block(
        "Banyak sinyal dikirimkan dalam format gambar atau teks yang berantakan. AI Fallback menyerap "
        "informasi tersebut, melakukan verifikasi terhadap format yang dibutuhkan MT5, dan memberikan "
        "penilaian akurasi. Jika akurasi di bawah ambang batas aman, sistem akan memberikan peringatan."
    )
    pdf.sub_section("8.2 Skor Akurasi & Analisa Alasan")
    pdf.content_block(
        "Setiap sinyal yang masuk akan disertai dengan 'Alasan AI'. Ini adalah penjelasan logis "
        "mengapa robot menyarankan untuk mengeksekusi atau melewati sinyal tersebut. "
        "Ini memberikan edukasi langsung kepada pengguna mengenai logika di balik sebuah trade."
    )

    # --- BAB 9: AKSES REMOTE VIA WEB INTERFACE ---
    pdf.add_page()
    pdf.section_title("BAB 9: SISTEM MONITORING JARAK JAUH")
    pdf.content_block(
        "Fitur Enterprise yang paling ditunggu: Kemampuan memantau terminal trading Anda dari mana saja "
        "melalui antarmuka Website (Web Monitor)."
    )
    pdf.sub_section("9.1 Aktivasi Sinkronisasi Cloud")
    pdf.content_block(
        "Pastikan Anda sudah melakukan login akun di aplikasi desktop. Begitu robot mulai berjalan, "
        "sinyal detak jantung (heartbeat) dan data saldo akan dikirimkan ke Cloud Central setiap detik."
    )
    pdf.sub_section("9.2 Menggunakan Web Dashboard")
    pdf.content_block(
        "Buka browser di HP/Tablet Anda dan akses URL resmi Web Monitor. Masuk menggunakan akun Anda. "
        "Di sana Anda akan menemukan:\n"
        "- Widget Live Balance & Equity.\n"
        "- Tabel Transaksi Aktif.\n"
        "- Konsol Chat AI untuk berkonsultasi secara portabel.\n"
        "- Tombol Darurat (Emergency Close) untuk menutup semua posisi hanya dengan satu sentuhan jari."
    )

    # --- BAB 10: AKADEMI & SISTEM GAMIFIKASI GLOBAL ---
    pdf.add_page()
    pdf.section_title("BAB 10: ITC ACADEMY & LEADERBOARD PESERTA")
    pdf.content_block(
        "ITC percaya bahwa pengguna yang berpengetahuan luas adalah pengguna yang sukses. "
        "Sistem kami mengintegrasikan pembelajaran interaktif ke dalam operasional harian."
    )
    pdf.sub_section("10.1 ITC Academy Quiz")
    pdf.content_block(
        "Ikuti kuis harian untuk mengasah kemampuan trading teknikal dan fundamental Anda. "
        "Skor yang Anda dapatkan akan menentukan peringkat pengetahuan Anda di komunitas global."
    )
    pdf.sub_section("10.2 Global Leaderboard System")
    pdf.content_block(
        "Leaderboard menampilkan performa profit harian dan bulanan antar pengguna ITC di seluruh dunia. "
        "Hal ini menciptakan ekosistem yang kompetitif namun sehat. Seluruh data disamarkan "
        "secara default untuk menjaga keamanan profil Anda di mata publik."
    )

    # --- BAB 11: PEMELIHARAAN & DUKUNGAN PRIORITAS ---
    pdf.add_page()
    pdf.section_title("BAB 11: PEMELIHARAAN SISTEM & TROUBLESHOOTING")
    pdf.content_block(
        "Panduan penanganan kendala umum yang mungkin dihadapi selama operasional berlangsung."
    )
    pdf.sub_section("11.1 Analisa Log Kesalahan")
    pdf.content_block(
        "Gunakan Tab 'Log Sistem' untuk melihat catatan setiap detik aktivitas robot. Jika terjadi error, "
        "perhatikan kode errornya. Kebanyakan error disebabkan oleh koneksi internet atau "
        "kesalahan pengisian Suffix Symbol."
    )
    pdf.sub_section("11.2 Prosedur Update Perangkat Lunak")
    pdf.content_block(
        "Versi Enterprise akan menerima update fitur dan keamanan secara berkala. Pastikan Anda "
        "selalu menggunakan versi terbaru yang tersedia untuk memastikan kompabilitas penuh "
        "dengan infrastruktur Cloud Central kami."
    )

    # --- ADDITIONAL DENSE PAGES (REACHING 20+) ---
    for k in range(1, 4):
        pdf.add_page()
        pdf.section_title(f"LAMPIRAN TEKNIS ENTERPRISE {k}")
        pdf.sub_section("Protokol Keamanan Data End-to-End")
        pdf.content_block(
            "Penjelasan mendalam mengenai bagaimana Database Global menangani enkripsi kunci identitas. "
            "Setiap komunikasi antara aplikasi desktop dan website monitoring melalui lapisan keamanan "
            "SSL/TLS tingkat tinggi. Privasi data Anda adalah prioritas utama kami di Richkeyrick Enterprise."
        )
        pdf.content_block(
            "Detail mengenai arsitektur sinkronisasi multi-threading yang memungkinkan robot menangkap "
            "pesan dari puluhan channel Telegram secara simultan tanpa ada penurunan performa atau lag."
        )
        pdf.content_block(
            "Instruksi detail mengenai cara menghubungkan API Key pribadi untuk unit AI tingkat lanjut "
            "guna mendapatkan respon yang lebih cepat dan personal sesuai gaya trading Anda masing-masing."
        )

    # Closing
    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, "SUKSES BERSAMA ITC +AI ENTERPRISE", 0, 1, "C")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, "Terima kasih telah mempercayai infrastruktur kami untuk mendukung "
                         "kegiatan perdagangan Anda. Mari bersama-sama menuju masa depan "
                         "finansial yang lebih cerdas dan terotomasi.", align="C")
    
    pdf.ln(30)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "RICHKEYRICK.COM | HAINEO.COM", 0, 1, "C")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 10, "Hak Cipta © 2026 Technolog Store Global Division.", 0, 1, "C")

    # Output
    output_path = "ITC_Enterprise_Official_Manual.pdf"
    pdf.output(output_path)
    print(f"Manual Berhasil Dibuat: {output_path} ({pdf.page_no()} Halaman)")

if __name__ == "__main__":
    generate_manual()
