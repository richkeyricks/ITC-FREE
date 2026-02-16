import os
import sys
from fpdf import FPDF

# --- CONFIGURATION ---
ASSETS_DIR = r"c:\APLIKASI YANG DIBUAT\TELEGRAM MT5\assets"
OUTPUT_FILE = r"c:\APLIKASI YANG DIBUAT\TELEGRAM MT5\docs\ITC_Official_Tutorial.pdf"
VERSION = "4.9.5"

# --- CONTENT DATA ---
TUTORIAL_DATA = [
    {
        "title": "1. DOWNLOAD & INSTALASI / INSTALLATION",
        "intro_id": "Langkah pertama. Jangan khawatir, prosesnya mudah seperti menginstal aplikasi biasa.",
        "intro_en": "First step. Don't worry, it's as easy as installing any regular app.",
        "steps": [
            {
                "id": "Buka browser (Chrome/Edge) dan ketik alamat ini:",
                "en": "Open your browser (Chrome/Edge) and type this address:",
                "code": "www.Telegramcopytrading.com/download"
            },
            {
                "id": "Klik tombol biru bertuliskan [ DOWNLOAD FOR WINDOWS ].",
                "en": "Click the blue button labeled [ DOWNLOAD FOR WINDOWS ]."
            },
            {
                "id": "Tunggu download selesai. File bernama 'ITC_Setup.exe'. Klik 2x file tersebut.",
                "en": "Wait for download. File named 'ITC_Setup.exe'. Double click it."
            },
            {
                "id": "PENTING: Jika muncul pesan biru 'Windows protected your PC':\n   1. Klik tulisan kecil 'More info'.\n   2. Klik tombol 'Run anyway'.",
                "en": "IMPORTANT: If blue message 'Windows protected your PC' appears:\n   1. Click small text 'More info'.\n   2. Click button 'Run anyway'."
            },
            {
                "id": "Aplikasi akan terbuka secara otomatis.",
                "en": "The application will open automatically."
            }
        ]
    },
    {
        "title": "2. REGISTRASI / REGISTRATION",
        "intro_id": "Anda butuh akun agar settingan tidak hilang saat ganti komputer.",
        "intro_en": "You need an account so settings are not lost when switching PCs.",
        "steps": [
            {
                "id": "Di halaman awal aplikasi, klik tombol [ BUAT AKUN BARU ] atau [ SIGN UP ].",
                "en": "On app home screen, click button [ BUAT AKUN BARU ] or [ SIGN UP ]."
            },
            {
                "id": "Isi Nama Lengkap, Email, dan Password yang mudah diingat.",
                "en": "Fill Full Name, Email, and an easy-to-remember Password."
            },
            {
                "id": "Klik [ DAFTAR SEKARANG ].",
                "en": "Click [ SIGN UP NOW ]."
            },
            {
                "id": "JANGAN LOGIN DULU! Buka Email Anda (Gmail/Yahoo). Cari email dari 'ITC Admin'.\n   Klik link verifikasi di dalamnya.",
                "en": "DO NOT LOGIN YET! Open your Email (Gmail/Yahoo). Find email from 'ITC Admin'.\n   Click the verification link inside."
            },
            {
                "id": "Sekarang kembali ke aplikasi dan Login.",
                "en": "Now go back to app and Login."
            }
        ]
    },
    {
        "title": "3. KONEKSI TELEGRAM (CRITICAL STEP)",
        "intro_id": "Ini bagian paling penting. Baca pelan-pelan. Kita butuh 'Surat Jalan' (API) dari Telegram agar robot boleh membaca pesan.",
        "intro_en": "This is crucial. Read slowly. We need a 'Pass' (API) from Telegram so the robot is allowed to read messages.",
        "steps": [
            {
                "id": "Buka browser di HP atau PC, kunjungi: my.telegram.org",
                "en": "Open browser on Phone or PC, visit: my.telegram.org",
                "link": "https://my.telegram.org"
            },
            {
                "id": "Masukkan Nomor HP Telegram Anda (Wajib pakai kode negara, contoh: +62812345678). Klik Next.",
                "en": "Enter your Telegram Phone Number (Must use country code, e.g., +62812345678). Click Next."
            },
            {
                "id": "Telegram akan mengirim KODE RAHASIA ke APLIKASI Telegram Anda (Bukan SMS!). Cek chat dari 'Telegram Service'.",
                "en": "Telegram will send a SECRET CODE to your Telegram APP (Not SMS!). Check chat from 'Telegram Service'."
            },
            {
                "id": "Salin kode itu ke website tadi. Klik Sign In.",
                "en": "Copy that code to the website. Click Sign In."
            },
            {
                "id": "Di menu website, klik [ API development tools ].",
                "en": "On website menu, click [ API development tools ]."
            },
            {
                "id": "Isi formulir (asal saja tidak apa-apa):\n   - App title: ITCApp\n   - Shortname: itc123\n   - Platform: Desktop",
                "en": "Fill form (random is fine):\n   - App title: ITCApp\n   - Shortname: itc123\n   - Platform: Desktop"
            },
            {
                "id": "Klik [ Create application ].",
                "en": "Click [ Create application ]."
            },
            {
                "id": "Selamat! Anda akan melihat 'App api_id' (angka) dan 'App api_hash' (kode panjang).\n   JANGAN TUTUP HALAMAN INI.",
                "en": "Congrats! You will see 'App api_id' (numbers) and 'App api_hash' (long code).\n   DO NOT CLOSE THIS PAGE."
            },
            {
                "id": "Buka Aplikasi ITC. Masuk menu [ Telegram Config ].",
                "en": "Open ITC App. Go to menu [ Telegram Config ]."
            },
            {
                "id": "Copy 'api_id' dari website --> Paste ke kolom 'API ID' di aplikasi.",
                "en": "Copy 'api_id' from website --> Paste to 'API ID' field in app."
            },
            {
                "id": "Copy 'api_hash' dari website --> Paste ke kolom 'API Hash' di aplikasi.",
                "en": "Copy 'api_hash' from website --> Paste to 'API Hash' field in app."
            },
            {
                "id": "Masukkan Nomor HP Anda lagi di aplikasi. Klik [ UJI KONEKSI ].",
                "en": "Enter your Phone Number again in app. Click [ TEST CONNECTION ]."
            }
        ]
    },
    {
        "title": "4. SETTING MT5 & START",
        "intro_id": "Langkah terakhir. Menghubungkan robot ke akun trading.",
        "intro_en": "Final step. Connecting robot to trading account.",
        "steps": [
            {
                "id": "Buka MT5 Anda. Pastikan tombol 'Algo Trading' di bagian atas sudah ON (Warna Hijau/Play).",
                "en": "Open MT5. Check 'Algo Trading' button at top is ON (Green/Play color)."
            },
            {
                "id": "Masuk menu Tools -> Options -> Expert Advisors.\n   Centang [v] Allow DLL imports (Wajib!). Klik OK.",
                "en": "Go to Tools -> Options -> Expert Advisors.\n   Check [v] Allow DLL imports (Mandatory!). Click OK."
            },
            {
                "id": "Di Aplikasi ITC, masuk menu [ Akun MT5 ]. Isi Login ID & Password MT5 Anda.",
                "en": "In ITC App, go to [ MT5 Account ]. Fill your MT5 Login ID & Password."
            },
            {
                "id": "Klik [ UJI LOGIN ]. Jika sukses, klik Dashboard.",
                "en": "Click [ TEST LOGIN ]. If success, click Dashboard."
            },
            {
                "id": "Klik tombol besar [ MULAI COPIER ].",
                "en": "Click big button [ START COPIER ]."
            }
        ]
    }
]

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(10, 10, 10)

    def header(self):
        # Logo
        logo_path = os.path.join(ASSETS_DIR, "app_icon.png")
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 15)
        
        # Title
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(15, 23, 42)
        # Move right for title to avoid overlapping logo
        self.set_xy(30, 10)
        self.cell(0, 10, 'ITC +AI ENTERPRISE - OFFICIAL TUTORIAL', border=0, ln=1, align='L')
        
        # Line break
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} - ITC CopyTrade Official Guide {VERSION}', align='C')

    def add_section_title(self, title):
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(59, 130, 246)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(2)
        # Line separator
        self.set_draw_color(226, 232, 240)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def add_intro(self, text_id, text_en):
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(180, 6, text_id)
        
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.multi_cell(180, 6, text_en)
        self.ln(5)

    def add_step(self, num, step_data):
        # 1. Number
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(15, 23, 42)
        self.set_x(10)
        self.cell(10, 8, f"{num}.", ln=0)
        
        # 2. ID Text
        self.set_font('helvetica', '', 11)
        self.set_x(25)
        self.multi_cell(160, 6, step_data['id'])
        
        # 3. EN Text
        self.set_x(25)
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(80, 80, 80)
        self.multi_cell(160, 6, step_data['en'])
        
        # 4. Code / Link
        if 'code' in step_data:
            self.set_x(25)
            self.set_font('courier', 'B', 10)
            self.set_text_color(59, 130, 246)
            self.multi_cell(160, 6, step_data['code'])
            
        if 'link' in step_data:
            self.set_x(25)
            self.set_font('courier', 'B', 10)
            self.set_text_color(59, 130, 246)
            self.multi_cell(160, 6, step_data['link'])

        self.ln(4)

def create_pdf():
    try:
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # Cover Content
        pdf.ln(40)
        pdf.set_font('helvetica', 'B', 30)
        pdf.set_text_color(15, 23, 42)
        pdf.multi_cell(0, 15, "PANDUAN LENGKAP\nCOPY TRADING", align='C')
        pdf.ln(10)
        
        pdf.set_font('helvetica', '', 16)
        pdf.set_text_color(100)
        pdf.multi_cell(0, 10, "Complete Installation & Step-by-Step Guide\nFor Beginners", align='C')
        
        # Banner Image
        banner_path = os.path.join(ASSETS_DIR, "itc_enterprise_banner_v2_1769130181986.png")
        if os.path.exists(banner_path):
            img_width = 150
            x_pos = (210 - img_width) / 2
            pdf.image(banner_path, x=x_pos, y=pdf.get_y() + 10, w=img_width)
            pdf.ln(80)
        else:
             pdf.ln(20)
        
        pdf.ln(10)
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 10, f"VERSI APLIKASI: {VERSION}", align='C', ln=1)
        
        pdf.add_page()

        # Content Loop
        for section in TUTORIAL_DATA:
            pdf.add_section_title(section['title'])
            pdf.add_intro(section['intro_id'], section['intro_en'])
            
            for i, step in enumerate(section['steps']):
                pdf.add_step(i + 1, step)
            
            pdf.ln(10)

        pdf.output(OUTPUT_FILE)
        print(f"SUCCESS: PDF created at {OUTPUT_FILE}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ERROR: {e}")
