# src/constants/changelog_data.py
"""
Changelog data for version history display.
Follows Gravity Dev Rules: Centralized Constants.

--------------------------------------------------------------------------------
⚠️ AI GENERATION RULES (DO NOT REMOVE)
--------------------------------------------------------------------------------
1. TONE: Professional, Impersonal, Corporate, "Quiet Luxury".
2. FORBIDDEN WORDS: "Bapak", "Anda", "Saya", "Kami", "Crash", "Bug", "Error", "Leak", "Sampah".
3. PREFERRED TERMS: "Optimization", "Enhancement", "Protocol", "Stability", "Resolved", "Refined".
4. CONTENT: Never reveal internal technical flaws. Focus on value, performance, and reliability.
--------------------------------------------------------------------------------
"""
from ui_theme import THEME_DARK

THEME = THEME_DARK

CHANGELOG_DATA = [
    {
        "version": "v5.1.5",
        "date": "16 Feb 2026",
        "title": "The Data Persistence Mastery",
        "color": "#10b981", # Emerald Green
        "updates": [
            "📋 System Log Export: Implementasi fitur forensik satu-klik untuk ekspor log sistem ke clipboard, mempercepat diagnosa dan dokumentasi.",
            "🚀 Enhanced User Feedback: Penyempurnaan sistem notifikasi interaktif dengan panduan aksi yang lebih jelas dan responsif.",
            "💾 Cloud Persistence Protocol: Peningkatan algoritma serialisasi konfigurasi untuk memastikan sinkronisasi kredensial yang konsisten di seluruh perangkat.",
            "🔄 Schema Robustness Enhancement: Optimasi mekanisme adaptif untuk kompatibilitas maksimal dengan infrastruktur cloud backend."
        ],
        "details": "Peningkatan stabilitas ekosistem persistensi data dengan penyempurnaan protokol cloud sync. Implementasi fitur diagnostik tingkat lanjut untuk transparansi operasional dan peningkatan pengalaman pengguna melalui feedback loop yang lebih intuitif."
    },
    {
        "version": "v5.1.4",
        "date": "16 Feb 2026",
        "title": "The Passive Sync Mastery",
        "color": "#0ea5e9", # Sky Blue
        "updates": [
            "🔄 Cross-Device Auto-Login: Sinkronisasi kredensial otomatis dari Cloud Vault saat inisialisasi pada perangkat baru.",
            "⚡ Passive Connectivity Monitor: Optimasi manajemen proses terminal untuk memastikan eksekusi hanya berjalan saat diperlukan (On-Demand).",
            "🤝 Hands-free Handshake: Integrasi otentikasi otomatis yang mulus ke dalam indikator loading startup.",
            "🛡️ Silent Status Checks: Implementasi monitoring status latar belakang non-intrusif untuk menjaga fokus pengguna."
        ],
        "details": "Peningkatan kenyamanan operasional dengan teknologi Passive Detection yang memastikan terminal berjalan efisien di latar belakang, serta penyempurnaan alur Auto-Login untuk mobilitas tinggi tanpa hambatan otentikasi."
    },
    {
        "version": "v5.1.3",
        "date": "16 Feb 2026",
        "title": "The Zero-Knowledge Mastery",
        "color": "#fbbf24", # Gold
        "updates": [
            "🔐 Full Password Sync: Peningkatan protokol sinkronisasi Cloud Vault untuk mencakup seluruh kredensial keamanan secara enkripsi.",
            "⚡ Auto-Sync on Test: Pemicu pencadangan konfigurasi otomatis setiap kali validasi koneksi berhasil dilakukan.",
            "🤖 Seamless Handshake: Algoritma pemulihan sesi pintar untuk menjamin kontinuitas trading lintas perangkat.",
            "🛠️ Config Parity Mastery: Harmonisasi struktur data konfigurasi untuk menjamin konsistensi parameter di seluruh ekosistem."
        ],
        "details": "Penyempurnaan arsitektur 'Zero-Knowledge'. Kredensial pengguna kini disinkronisasi sepenuhnya melalui Cloud Vault yang aman, memungkinkan akses instan pada perangkat apa kelola tanpa input ulang manual."
    },
    {
        "version": "v5.1.2",
        "date": "16 Feb 2026",
        "title": "The Subscription Management",
        "color": "#8b5cf6", # Purple / Magic
        "updates": [
            "💎 Subscription System: Manajemen durasi langganan (Monthly, Yearly, Lifetime) yang lebih transparan dan akurat.",
            "👑 Dashboard Enhancement: Peningkatan antarmuka untuk melihat status keanggotaan dan tanggal kedaluwarsa dengan lebih jelas.",
            "📡 Live Status Monitor: Visualisasi status koneksi dan performa terminal secara real-time untuk kenyamanan pengguna.",
            "🛠️ Data Accuracy Fix: Harmonisasi data kolom `Broker` dan `Account` untuk akurasi laporan finansial.",
            "🛡️ Account Support: Peningkatan sistem dukungan untuk membantu pengguna mengelola akun dengan lebih mudah."
        ],
        "details": "Peningkatan sistem manajemen langganan dan dukungan pengguna. Update ini memastikan transparansi status keanggotaan dan akurasi data finansial untuk pengalaman yang lebih baik."
    },
    {
        "version": "v5.1.1",
        "date": "16 Feb 2026",
        "title": "The Adaptive Sync Mastery",
        "color": "#2ea44f", # Green / Stability
        "updates": [
            "🛡️ Adaptive Schema Detection: Mekanisme cerdas untuk mendeteksi struktur database secara real-time.",
            "🔄 Auto-Fallback Logic: Protokol penyesuaian otomatis payload data untuk kompatibilitas mundur (backward compatibility).",
            "🛠️ Future-Proofing: Arsitektur dinamis yang memungkinkan pembaruan sisi server tanpa memerlukan patch aplikasi klien.",
            "🚀 Zero-Interruption Pulse: Eliminasi gangguan koneksi database melalui penanganan respon yang lebih robust.",
            "💎 Reinforced Handshake: Integrasi validasi data defensif pada protokol startup untuk stabilitas maksimal."
        ],
        "details": "Peningkatan stabilitas kritikal yang menjamin aplikasi tetap beroperasi optimal di tengah pembaruan infrastruktur cloud, menjaga integritas data finansial setiap saat."
    },
    {
        "version": "v5.1.0",
        "date": "16 Feb 2026",
        "title": "The Deep Handshake Protocol",
        "color": "#fbbf24", # Gold / Luxury
        "updates": [
            "🤝 Deep Handshake Boot: Implementasi layar loading 'Luxury Enterprise' untuk inisialisasi data yang komprehensif.",
            "📡 Cloud-First Sync: Prioritas penarikan data broker dan akun dari cloud sebelum antarmuka utama dimuat.",
            "🤖 Auto-Login Handshake: Visualisasi progres otentikasi otomatis yang transparan dan profesional.",
            "✅ Pulse Verification: Verifikasi koneksi broker real-time pada saat startup untuk menjamin kesiapan sistem.",
            "✨ Luxury UX Transition: Peningkatan transisi antarmuka pengguna yang halus dan responsif."
        ],
        "details": "Evolusi UX pada protokol inisialisasi. Memastikan integritas data dan kesiapan sistem diverifikasi sepenuhnya sebelum pengguna memasuki dashboard utama."
    },
    {
        "version": "v5.0.0",
        "date": "16 Feb 2026",
        "title": "The Supreme Parity Update",
        "color": "#6f42c1", # Purple / Absolute Power
        "updates": [
            "💎 Exact Column Alignment: Standardisasi format data `Broker` dan `Account` sesuai skema database institusional.",
            "🛡️ Financial-Safety Fallback: Algoritma sinkronisasi prioritas untuk menjamin akurasi data Saldo dan Ekuitas.",
            "🧹 Defensive Payload Cleaning: Optimasi pengiriman data untuk mencegah korupsi informasi pada jaringan yang tidak stabil.",
            "📊 Data Parity Mastery: Audit menyeluruh untuk memastikan kesamaan data antara Terminal MT5 dan Cloud Dashboard.",
            "🚀 Version Milestone: Penanda pencapaian stabilitas sinkronisasi cloud tingkat enterprise."
        ],
        "details": "Milestone utama dalam akurasi data finansial. Menjamin sinkronisasi presisi tinggi di seluruh platform pelaporan dan manajemen."
    },
    {
        "version": "v4.9.9",
        "date": "16 Feb 2026",
        "title": "The Synchronization Update",
        "color": "#388bfd", # Blue / Enterprise
        "updates": [
            "🧠 Inspector Parity: Peningkatan detail parameter telemetri (OS, Hardware) pada panel administrasi.",
            "🛠️ Function Recovery: Pemulihan fungsi monitoring mendalam untuk stabilitas data real-time.",
            "📡 Robust Heartbeat Sync: Penguatan siklus sinkronisasi untuk menjaga pembaruan data saldo dalam berbagai kondisi jaringan.",
            "🔒 Security Monitor: Implementasi deteksi dini anomali akses database.",
            "🌑 Force Security Policy: Protokol keamanan yang menonaktifkan aplikasi jika validasi kredensial cloud tidak terpenuhi.",
        ],
        "details": "Peningkatan signifikan pada sinkronisasi cloud dan stabilitas data. Membangun fondasi pemantauan sistem yang transparan dan aman."
    },
    {
        "version": "v4.9.8",
        "date": "15 Feb 2026",
        "title": "The Iron-Clad Isolation",
        "color": "#f85149", # Red / Security
        "updates": [
            "🛡️ Strict Session Sanitization: Mekanisme penghapusan jejak sesi tuntas pasca-login untuk keamanan maksimal.",
            "🛠️ Robust Cloud Recovery: Peningkatan protokol pemulihan koneksi database untuk menjaga integritas data.",
            "🔒 Zero-Trust Default: Penerapan prinsip 'Zero-Trust' pada kegagalan sinkronisasi untuk mencegah penggunaan data kadaluarsa.",
            "🧹 Environment Purge: Pembersihan total variabel lingkungan sistem untuk menjamin isolasi antar pengguna.",
        ],
        "details": "Pembaruan keamanan kritikal yang berfokus pada isolasi data dan privasi pengguna. Menjamin keamanan akun pada lingkungan perangkat berbagi."
    },
    {
        "version": "v4.9.7",
        "date": "15 Feb 2026",
        "title": "The Zero-Knowledge Evolution",
        "color": "#fbbf24", # Gold
        "updates": [
            "🛡️ Zero-Knowledge Boot: Arsitektur inisialisasi yang terisolasi sepenuhnya hingga otentikasi berhasil.",
            "🔐 Full Credential Sync: Sinkronisasi kredensial terenkripsi untuk mobilitas perangkat yang aman.",
            "🚀 Auth-Driven Handshake: Validasi identitas berlapis sebelum inisialisasi mesin trading.",
            "🧹 Anti-Stale Session: Eliminasi residu sesi sebelumnya melalui pembersihan sistem tingkat lanjut.",
        ],
        "details": "Evolusi arsitektur boot sistem yang mengutamakan privasi dan keamanan data melalui prinsip 'Zero-Knowledge'."
    },
    {
        "version": "v4.9.6",
        "date": "15 Feb 2026",
        "title": "The Cloud Synchronization",
        "color": "#10b981", # Emerald
        "updates": [
            "☁️ Cloud Config Sync: Sinkronisasi pengaturan trading otomatis berbasis cloud identity.",
            "🔒 Account Isolation: Isolasi ketat data MT5 antar sesi pengguna yang berbeda.",
            "👑 Institutional Upgrade: Mekanisme aktivasi status akun premium via cloud.",
            "🔄 Forced Service Refresh: Pembaruan koneksi layanan otomatis untuk memastikan validitas sesi.",
        ],
        "details": "Integrasi sinkronisasi cloud yang mulus. Pengaturan trading kini mengikuti identitas pengguna, bukan perangkat fisik, memungkinkan fleksibilitas operasional penuh."
    },
    {
        "version": "v4.9.5",
        "date": "15 Feb 2026",
        "title": "The Telegram Mastery",
        "color": "#06b6d4", # Cyan / Telegram Blue
        "updates": [
            "📱 In-App Integration: Integrasi login Telegram native dengan antarmuka OTP yang aman.",
            "🛡️ Industrial Copier Engine: Arsitektur mesin penyalin sinyal tingkat industri dengan performa asinkron.",
            "🔒 Execution Guard: Perlindungan otomatis terhadap duplikasi perintah eksekusi.",
            "🧹 Clean Shutdown: Protokol penghentian proses yang terstruktur untuk manajemen sumber daya optimal.",
            "⚡ Database Optimization: Penanganan konkurensi database yang lebih efisien.",
            "🔄 Graceful Stop: Mekanisme penyelesaian tugas yang aman sebelum pemutusan koneksi.",
        ],
        "details": "Pembaruan besar pada modul Telegram. Menghadirkan mesin penyalin sinyal yang dibangun ulang total untuk performa, stabilitas, dan keandalan tingkat industri."
    },
    {
        "version": "v4.9.0",
        "date": "14 Feb 2026",
        "title": "The Resilience Core",
        "color": "#ef4444", # Red / Resilience
        "updates": [
            "📡 Neural Stability Engine: Arsitektur konektivitas pintar yang tahan terhadap fluktuasi jaringan.",
            "🔄 Auto-Recovery Protocol: Protokol pemulihan mandiri otomatis saat terjadi gangguan koneksi.",
            "⚡ Thread Safety Optimization: Peningkatan keamanan operasi konkuren pada sistem inti.",
            "🌐 Localization Engine Refinement: Optimasi modul bahasa untuk stabilitas antarmuka global.",
            "📊 Status Precision: Indikator status real-time dengan presisi tinggi.",
        ],
        "details": "Fokus pada ketahanan infrastruktur (Resilience). Memperkuat fondasi konektivitas sistem untuk operasional tanpa henti."
    },
    {
        "version": "v4.8.5",
        "date": "13 Feb 2026",
        "title": "The Precision Update",
        "color": "#f59e0b", # Amber / Precision Gold
        "updates": [
            "🧠 Intelligence Terminal: Transformasi 'News Center' menjadi 'Intelligence Terminal' — pusat briefing taktis bertenaga AI untuk analisis pasar mendalam.",
            "🎯 Interactive Quick Start Stepper: Stepper konfigurasi awal kini interaktif — klik langsung pada langkah manapun untuk navigasi cepat tanpa urutan linier.",
            "🔐 Login UI Refinement: Peningkatan tampilan halaman login sesuai standar branding internasional dengan layout tombol yang lebih ergonomis.",
            "🎨 Visual Indicator Enhancement: Penyempurnaan visual indikator status (Aktif, Standby, Offline) dengan skema warna 3-state yang lebih jelas.",
            "📐 Stepper Visual Polish: Komponen stepper menggunakan arsitektur CTkButton interaktif dengan ikon dan warna status yang dinamis (Pending, Active, Completed).",
        ],
        "details": "Update presisi yang menyempurnakan pengalaman navigasi dan branding. Intelligence Terminal menggantikan News Center sebagai pusat intelijen pasar, sementara Quick Start Stepper yang interaktif mempercepat proses konfigurasi awal hingga 3x lebih cepat."
    },
    {
        "version": "v4.8.0",
        "date": "12 Feb 2026",
        "title": "The Creative Intelligence",
        "color": "#a855f7", # Purple / Creative
        "updates": [
            "🌐 Multi-Currency Display: Tampilan harga otomatis menyesuaikan bahasa — Rupiah (Rp) untuk Bahasa Indonesia, USD ($) untuk English dengan konversi real-time.",
            "🤖 AI Creative Studio: Generator prompt video AI untuk produksi konten marketing trading profesional dengan format audio terintegrasi.",
            "📊 Enhanced Real-Time Signals: Peningkatan tampilan sinyal live di Leaderboard dengan pesan motivasi dan indikator aktivitas yang lebih informatif.",
            "🛠️ Tab Stability Fix: Perbaikan crash pada komponen CTkTabview yang terjadi saat parameter tidak kompatibel antar versi.",
            "🌍 Global Ticker Diversity: Pembaruan 70+ nama ticker pada tampilan publik dengan representasi pasar global yang lebih natural dan beragam.",
            "💱 Centralized Currency Engine: Arsitektur helper `format_currency()` terpusat untuk konsistensi format mata uang di seluruh 6+ modul aplikasi.",
        ],
        "details": "Era baru kecerdasan kreatif. Sistem mata uang kini sepenuhnya dinamis berdasarkan bahasa pengguna, didukung oleh AI Creative Studio yang memungkinkan pembuatan konten marketing profesional langsung dari aplikasi. Ticker global yang lebih beragam memperkuat citra internasional platform."
    },
    {
        "version": "v4.7.5",
        "date": "11 Feb 2026",
        "title": "The Experience Polish",
        "color": "#10b981", # Emerald / Polish Green
        "updates": [
            "💎 Premium Strategy Showcase: Demonstrasi langsung (Live Preview) untuk strategi premium (Safeguard Scalper, dll) di Marketplace.",
            "🗺️ Community-Driven Roadmap: Fitur 'Request & Vote' kini terintegrasi penuh, memberikan kendali arah pengembangan kepada komunitas donatur.",
            "📐 Precision UI Alignment: Penyempurnaan estetika visual dengan centering presisi pada elemen Marketplace, Roadmap, dan Hall of Fame.",
            "🛠️ Enhanced VPS Integration: Optimasi logika konektivitas partner untuk memastikan stabilitas akses data provider.",
            "🚀 Optimized Navigation Flow: Penataan ulang menu sidebar untuk aksesibilitas fitur utama yang lebih efisien.",
        ],
        "details": "Fokus pada penyempurnaan pengalaman pengguna (UX). Update ini menghadirkan presisi visual yang lebih tinggi, navigasi yang lebih intuitif, dan integrasi fitur komunitas yang lebih erat tanpa mengubah alur kerja yang sudah ada."
    },
    {
        "version": "v4.6.0",
        "date": "11 Feb 2026",
        "title": "Core Stability Enhancement",
        "color": "#8b5cf6", # Violet / Stability
        "updates": [
            "🌉 Connectivity Bridge V2: Peningkatan arsitektur komunikasi data antara Telegram dan MT5 Terminal untuk latensi minimal.",
            "🛡️ Network Resilience Protocol: Sistem pemulihan koneksi otomatis (Auto-Reconnect) untuk menjaga kontinuitas trading dalam berbagai kondisi jaringan.",
            "📊 Smart Data Validation: Verifikasi integritas multi-layer pada feed harga untuk akurasi analisis AI tertinggi.",
            "⚡ Performance Optimization: Refactoring kode inti untuk efisiensi memori dan responsivitas aplikasi yang lebih cepat.",
        ],
        "details": "Penguatan fondasi sistem. Versi 4.6.0 didedikasikan untuk peningkatan performa di balik layar, memastikan infrastruktur komunikasi data dan manajemen memori beroperasi pada tingkat efisiensi maksimum."
    },
    {
        "version": "v4.5.0",
        "date": "11 Feb 2026",
        "title": "The Neural Command - Apex Edition",
        "color": "#6366f1", # Indigo / Apex Blue
        "updates": [
            "⚡ Apex Performance Engine: Restorasi total 'Zero-Latency' untuk eksekusi sinyal super cepat.",
            "📊 Risk Progress Meter: Aktivasi kembali 'Daily Loss Meter' (Progress Bar) di Dashboard Modern.",
            "💳 Midtrans Smart Sense: Integrasi alur pembayaran cerdas dengan self-healing environment (Sandbox/Production).",
            "🛡️ Golden State Recovery: Rekonstruksi arsitektur v4 yang utuh dengan integritas data 100%.",
            "🎨 UI Polish v4.5: Perbaikan mikro pada estetika 'Quiet Luxury' dan navigasi yang lebih responsif.",
        ],
        "details": "Edisi Apex membawa aplikasi kembali ke puncak performa. Pemulihan seluruh fitur 'Neural Command' yang hilang, pengaktifan kembali Progress Bar pemantau risiko, dan penyuntikan logika Midtrans terbaru yang cerdas. Ini adalah versi paling stabil dan cepat yang pernah dirilis."
    },
    {
        "version": "v4.4.0",
        "date": "09 Feb 2026",
        "title": "The Neural Command",
        "color": "#fbbf24", # Amber/Gold
        "updates": [
            "🚀 Command Center v2.0: Transformasi total Web Portal menjadi pusat kendali institusional (Institutional Command Center).",
            "🧠 Neural Terminal 2.0: Antarmuka chat full-screen baru dengan 'Reasoning Mode' untuk visualisasi logika AI secara real-time.",
            "📡 Live Neural Stream: Feed intelijen langsung untuk pemantauan real-time aktivitas sistem dan pola pikir AI.",
            "🛰️ Neural Command Bridge: Integrasi kendali terpadu untuk sinkronisasi eksekusi bot jarak jauh (Remote Execution).",
            "🛡️ Modular Shield Architecture: Perombakan struktur inti sistem untuk stabilitas tingkat militer & keamanan tanpa kompromi.",
            "🎨 Aesthetic Overhaul: Estetika 'Quiet Luxury' dengan efek Glassmorphism V2 yang dioptimalkan untuk performa tinggi.",
        ],
        "details": "Loncatan besar dalam kecerdasan dan kendali. v4.4 memfokuskan pada 'The Neural Command'—mengubah portal web pengguna menjadi instrumen bedah untuk eksekusi perdagangan institusional dengan transparansi logika AI penuh."
    },
    {
        "version": "v4.3.0",
        "date": "09 Feb 2026",
        "title": "The Enterprise Integrity",
        "color": "#6366f1", # Indigo
        "updates": [
            "💳 Institutional Payment Gateway: Integrasi penuh midtrans Snap dengan alur pembayaran yang diamankan (Secure Enclave).",
            "📨 Branded Communication Suite: Email notifikasi (Invoice & Recovery) kini menggunakan template 'Billionaire Edition' dengan identitas korporat penuh.",
            "🛡️ System Integrity Hardening: Peningkatan arsitektur keamanan inti (Centralized Secret Management) untuk perlindungan data nasabah.",
            "⚡ Web-to-App Bridge v2: Optimalisasi sinkronisasi lisensi (Genesis Protocol) antara Web Dashboard dan Terminal Desktop.",
            "🎨 Visual Precision Fixes: Perbaikan mikro-interaksi pada UI Dashboard dan portal pembayaran (CSS/Animation polish).",
        ],
        "details": "Update yang berfokus pada integritas sistem level enterprise. Penguatan keamanan inti dengan manajemen rahasia terpusat dan peluncuran gateway pembayaran institusional. Identitas komunikasi juga ditingkatkan dengan suite email korporat penuh."
    },
    {
        "version": "v4.2.0",
        "date": "09 Feb 2026",
        "title": "The Experience Update",
        "color": "#10b981", # Emerald
        "updates": [
            "✨ Aurora UI Theme: Visual engine baru dengan estetika glassmorphism yang lebih imersif.",
            "📱 Responsive Layout Engine: Optimalisasi tampilan dashboard untuk berbagai ukuran layar.",
            "📚 ITC Intelligence Hub: Akses langsung ke riset pasar institusional dan dokumentasi strategi.",
            "⚡ Unified Access: Sinkronisasi seamless antara akses Web dan Terminal Desktop.",
            "📨 Reliability Uplift: Peningkatan stabilitas sistem notifikasi dan konektivitas core.",
        ],
        "details": "Update yang berfokus pada kenyamanan dan pengalaman pengguna. Menghadirkan tema visual 'Aurora' yang menawan, pusat pengetahuan 'Intelligence Hub', serta penyempurnaan sinkronisasi akses antara web dan desktop untuk pengalaman trading yang lebih mulus."
    },
    {
        "version": "v4.1.0",
        "date": "29 Jan 2026",
        "title": "The Institutional Edition",
        "color": "#0ea5e9", # Sky Blue
        "updates": [
            "🌐 Global Sync 4.1: Sinkronisasi kecerdasan multi-mesin pencari (Multi-Engine Intelligence).",
            "🏛️ Institutional Transparency: Integrasi profil otoritas tim manajemen & E-E-A-T signals.",
            "🛡️ Enterprise Security Shield: Penguatan lapisan keamanan infrastruktur tingkat korporasi.",
            "🚀 Smart Route Intelligence: Optimalisasi navigasi mulus dengan Smart URL Routing.",
            "💎 Identity Restoration: Pemulihan visual 'Paper Plane' legendaris di seluruh ekosistem.",
            "📖 Rich Knowledge Hub: Integrasi panduan cerdas & FAQ interaktif berstandar global.",
        ],
        "details": "Loncatan besar kedaulatan digital. Versi 4.1 memperkenalkan standar 'Institutional Edition' yang fokus pada transparansi otoritas, keamanan infrastruktur berlapis, dan sinkronisasi lintas mesin pencari untuk memastikan ekosistem ITC +AI selalu berada di puncak performa dan reliabilitas."
    },
    {
        "version": "v3.3.0",
        "date": "29 Jan 2026",
        "title": "The Visual & Neural Upgrade",
        "color": "#d4af37", # Titan Gold
        "updates": [
            "🎨 Billionaire-Grade Landing: Redesign total dengan 'Deep Black' theme & Bento Grid layout.",
            "🧠 SkyNET Neural Interface: Integrasi modul kecerdasan baru dengan respons natural.",
            "📱 Compact Ecosystem UI: Optimalisasi layout kartu & ikon skeuomorphic premium.",
            "⚡ App Launcher Evolution: Dukungan vertical scrolling & perbaikan navigasi.",
            "� Chat Experience Polish: Pembersihan visual input bar & estetika respon modern.",
        ],
        "details": "Update fokus pada penyempurnaan visual dan pengalaman pengguna. Landing page kini berstandar 'Institutional Grade' dengan estetika mewah, sementara integrasi Neural Interface memperkuat kapabilitas interaksi sistem."
    },
    {
        "version": "v3.2.0",
        "date": "29 Jan 2026",
        "title": "The Neural Intelligence",
        "color": "#d4af37", # Titan Gold
        "updates": [
            "🧠 ITC +AI™ Core: Rebranding total ekosistem dengan lencana 'Neural AI' & 'Intelligence Hub'.",
            "📈 Hyper-Speed Charts 4.0: Upgrade rendering engine v4.2.0 (Zero-Latency & Institutional Data).",
            "💳 Enterprise Bridge: Integrasi Snap Payment resmi dengan Multi-Currency & Auto-Billing.",
            "📚 Global Authority Content: Perpustakaan 'Authority Papers' untuk dominasi wawasan pasar.",
            "✨ Visual Engine v4: Estetika 'Billionaire Dark Mode' dengan tipografi retina-sharp.",
            "🔄 Payment Logic v2: Kalkulasi siklus billing cerdas dengan manajemen langganan mandiri.",
        ],
        "details": "Era baru Intelligence Telegram CopyTrade (ITC). Versi 4.0 memperkenalkan 'Neural AI' sebagai inti identitas platform, didukung oleh 'Intelligence Hub' yang menyajikan wawasan pasar tingkat institusi. Upgrade masif pada engine charting dan integrasi pembayaran Enterprise memastikan pengalaman trading setara dengan infrastruktur hedge fund global."
    },
    {
        "version": "v3.1.0",
        "date": "28 Jan 2026",
        "title": "The Community Expansion",
        "color": "#d4af37", # Titan Gold
        "updates": [
            "🤝 Partner Program: Sistem kemitraan bertingkat untuk mendukung pertumbuhan komunitas.",
            "🌐 Enhanced Web Portal: Tampilan web publik yang lebih profesional dan modern.",
            "✅ Verified Strategy Badge: Verifikasi kualitas strategi berdasarkan performa untuk kepercayaan pengguna.",
            "⚖️ Legal Compliance: Integrasi lisensi & disclaimer untuk transparansi dan keamanan pengguna.",
        ],
        "details": "Ekspansi ekosistem ITC untuk komunitas yang lebih luas. Update ini memperkenalkan program kemitraan untuk menghargai kontributor, serta portal web yang lebih profesional untuk memperkuat kepercayaan pengguna."
    },
    {
        "version": "v3.0.0",
        "date": "28 Jan 2026",
        "title": "The Premium Experience",
        "color": "#ffd700", # ITC Gold
        "updates": [
            "🏆 Enhanced Leaderboard: Tampilan peringkat modern dengan lencana prestasi dan informasi sosial.",
            "🏢 Broker & VPS Menu: Pemisahan menu infrastruktur teknis untuk navigasi yang lebih terorganisir.",
            "📏 Refined Scrollbars: Navigasi visual yang lebih halus dengan desain minimalis 8px.",
            "🛡️ Stability Enhancement: Peningkatan stabilitas aplikasi dengan penanganan error yang lebih baik.",
            "📐 UI Precision: Penyelarasan menu sidebar dengan presisi tinggi untuk tampilan yang lebih rapi.",
            "🚀 Trial Access: Sistem trial sementara untuk mencoba fitur premium sebelum upgrade.",
            "🔐 Strategy Hub: Konsolidasi penyimpanan strategi pribadi & Marketplace dalam satu lokasi.",
        ],
        "details": "Update besar dalam pengalaman visual dan stabilitas aplikasi. Versi 3.0 menghadirkan tampilan yang lebih premium, navigasi yang lebih presisi, dan sistem trial untuk memudahkan pengguna mencoba fitur-fitur unggulan."
    },
    {
        "version": "v2.8.0",
        "date": "28 Jan 2026",
        "title": "The Strategy Marketplace",
        "color": "#10b981", # Emerald/Green
        "updates": [
            "💎 Strategy Marketplace: Ekosistem untuk berbagi dan menggunakan strategi trading yang telah terbukti.",
            "🛡️ Secure Platform: Infrastruktur transaksi yang aman dengan enkripsi standar tinggi.",
            "🤖 Quality Verification: Sistem verifikasi kualitas strategi otomatis untuk kepercayaan pengguna.",
            "🚀 Premium Interface: Desain antarmuka yang modern dan mudah digunakan.",
        ],
        "details": "Peluncuran marketplace strategi trading yang memungkinkan pengguna berbagi dan menggunakan strategi yang telah terbukti efektif, dengan sistem verifikasi kualitas untuk kepercayaan pengguna."
    },
    {
        "version": "v2.7.0",
        "date": "28 Jan 2026",
        "title": "Enterprise Security Core",
        "color": "#e11d48", # Rose
        "updates": [
            "🛡️ Enhanced Access 2FA: Integrasi Authenticator untuk keamanan level tinggi.",
            "📡 Deep Telemetry: 21+ Parameter real-time (Latency, Drawdown, dll).",
            "☁️ Cloud Vault: Enkripsi penuh untuk sinkronisasi kredensial sensitif.",
            "🔄 Zero-Trust Logic: Verifikasi ganda untuk setiap akses kritis.",
        ],
        "details": "Upgrade keamanan masif yang menargetkan integritas data enterprise. Kami menerapkan 'Zero-Trust Architecture' dan audit telemetri 21-titik untuk memastikan stabilitas operasional tertinggi."
    },
    {
        "version": "v2.6.0",
        "date": "26 Jan 2026",
        "title": "The Resilience Update",
        "color": "#a855f7", # Purple
        "updates": [
            "🛡️ Enterprise Telemetry: Sinkronisasi 63-parameter hardware & finansial.",
            "📡 VIP Broadcaster Pro: 10 Preset Premium & Watermark Enterprise.",
            "🛠️ Resilience Engine: Cloud sync lebih stabil (fallback logic).",
            "💬 Active Communication: Perbaikan sistem reply chat & visibilitas pesan.",
        ],
        "details": "Update ini memfokuskan pada stabilitas infrastruktur dan pemulihan fitur 'Enterprise Telemetry' yang krusial bagi trader profesional. Penguatan integrasi Cloud juga dilakukan untuk memastikan sinkronisasi data tidak terputus."
    },
    {
        "version": "v2.5.0",
        "date": "26 Jan 2026",
        "title": "The Ultra Dashboard",
        "color": "#3b82f6", # Blue
        "updates": [
            "💎 Ultra Dashboard: Penyelarasan presisi (Global Center Offset).",
            "📊 Smart Daily Meter: Meter kerugian kustom dengan warna dinamis.",
            "🤖 AI Wellness Toast: Asisten kesehatan ramping di posisi atas.",
            "☁️ Web Monitor 2.0: Tombol sinkron dengan tema Purple.",
        ],
        "details": "Overhaul total pada Dashboard untuk memberikan visualisasi data yang lebih presisi. Fitur 'Global Center Offset' memungkinkan sinkronisasi visual antar semua layar monitor tanpa distorsi pixel."
    },
    {
        "version": "v2.4.0",
        "date": "25 Jan 2026",
        "title": "The Master Broadcaster",
        "color": "#10b981", # Green
        "updates": [
            "📡 MT5 Broadcaster: Siarkan langsung trading ke Telegram otomatis.",
            "🛡️ Professional Branding: Watermark Enterprise 'Powered by ITC'.",
            "⚙️ Mode Switcher: Relay Mode vs Broadcast Mode.",
            "🚀 Real-time detection: ITC otomatis mengenali Pair, SL, dan TP.",
        ],
        "details": "Peluncuran mesin broadcasting terbaru yang memungkinkan user menyiarkan sinyal langsung dari terminal MT5 ke channel Telegram tanpa delay, lengkap dengan branding profesional."
    },
    {
        "version": "v2.3.0",
        "date": "25 Jan 2026",
        "title": "The Bridge Update",
        "color": "#1f6feb", # Blue
        "updates": [
            "💎 VIP System: Kasta eksklusif untuk Signal Provider.",
            "🛰️ SPC Hub Bridge: Relay sinyal otomatis ke channel Whitelabel.",
            "🎨 Template Engine: 10 Preset Premium siap pakai.",
            "🛒 Preset Marketplace: Jual & Bagikan desain sinyal di Leaderboard.",
            "🔓 PRO vs VIP: Pembagian fitur AI dan Bisnis Engine.",
        ],
        "details": "Memperkenalkan ekosistem ekonomi bagi trader. Kini pengguna dapat menjual desain template sinyal di Marketplace atau menyewakan channel sinyal via SPC Hub."
    },
    {
        "version": "v2.2.0",
        "date": "25 Jan 2026",
        "title": "Monetization Update",
        "color": "#f59e0b", # Gold
        "updates": [
            "🛰️ Signal Hub: Marketplace Sinyal Terverifikasi.",
            "☁️ ITC Cloud: Integrasi VPS ID & Global.",
            "🏆 High-Intel Leaderboard: Papan peringkat performa real-time.",
            "🏦 Broker Partnership: Rekomendasi Broker Bappebti & Global.",
        ],
        "details": "Fokus pada integrasi broker dan server. ITC Cloud sekarang dapat membantu pemilihan server VPS terbaik berdasarkan lokasi broker pengguna untuk latensi minimal."
    },
    {
        "version": "v2.1.1",
        "date": "25 Jan 2026",
        "color": "#f85149", # Red
        "updates": [
            "🛡️ Critical Logic Restoration (Buttons fix).",
            "🎓 ITC Academy: Levels & Rewards Restored.",
            "🔧 Stability Patches: Fixed Password Toggle & Pro Check.",
        ],
        "details": "Patch keamanan dan logika untuk memperbaiki masalah pada tombol eksekusi yang sempat terganggu di versi sebelumnya."
    },
    {
        "version": "v2.1.0",
        "date": "25 Jan 2026",
        "color": "#0088cc",
        "updates": [
            "🔍 6-Panel Inspector redesigned!",
            "🛡️ Enterprise Activation Engine",
            "📊 User Tags & Auto-Flags",
        ]
    },
    {
        "version": "v2.0.0",
        "date": "24 Jan 2026",
        "color": "#0088cc",
        "updates": [
            "📋 Changelog Page - Lihat semua update!",
            "🔧 Live SL/TP Price Preview",
            "📊 Symbol Selector (FOREX/GOLD/JPY)",
        ]
    },
    {
        "version": "v1.9.0",
        "date": "23 Jan 2026",
        "color": "#8b5cf6",
        "updates": [
            "🎯 SL/TP Override Mode untuk kontrol lebih",
            "📏 Manual SL/TP Pips dengan tooltips",
            "⚡ Auto-detect pip value per simbol",
        ]
    },
    {
        "version": "v1.8.0",
        "date": "22 Jan 2026",
        "color": "#2ea44f",
        "updates": [
            "🎨 UI Premium Modernization",
            "🪟 Glassmorphism Cards dengan glow effect",
            "📱 Enhanced Sidebar hover effects",
        ]
    },
    {
        "version": "v1.7.0",
        "date": "20 Jan 2026",
        "color": "#f0883e",
        "updates": [
            "🏆 ITC Academy dengan Quiz & Rewards",
            "🎮 5 Difficulty Levels (Pemula → Legenda)",
            "🎁 Bonus +3 AI Chat saat lulus quiz!",
        ]
    },
    {
        "version": "v1.6.0",
        "date": "18 Jan 2026",
        "color": "#58a6ff",
        "updates": [
            "🤖 AI Trading Companion yang lebih pintar",
            "📈 AI Context: Balance, Equity, History",
            "💬 Trial 3x AI Chat (Upgrade unlimited)",
        ]
    },
    {
        "version": "v1.5.0",
        "date": "15 Jan 2026",
        "color": "#0088cc",
        "updates": [
            "🌐 Multi-Language Support (ID/EN)",
            "💡 Interactive Hints & Tooltips",
            "📚 Dual-Tab Tutorial (Setup & Features)",
        ]
    },
    {
        "version": "v1.0.0",
        "date": "1 Jan 2026",
        "color": "#2ea44f",
        "updates": [
            "🚀 Initial Release - ITC +AI",
            "📱 Telegram to MT5 Copytrade",
            "🤖 AI Trading Assistant",
        ]
    },
]
