# 🌐 ITC +AI ENTERPRISE - Update & Distribution Guide

Sistem update ITC +AI dirancang agar Anda (Developer) memiliki kontrol penuh atas distribusi tanpa perlu mengirim file secara manual ke setiap user.

## 1. Bagaimana Sistem Bekerja?
Aplikasi ITC +AI melakukan **Cloud Version Handshake** setiap kali dijalankan:
1.  Aplikasi mengecek tabel `app_metadata` di Supabase.
2.  Jika kolom `version` di Cloud lebih tinggi dari versi lokal (saat ini v1.0.1), aplikasi akan memunculkan popup otomatis.
3.  User melihat daftar perubahan (Changelog) dan tombol download.

## 2. Cara Anda Meluncurkan Update (Admin)
Jika Anda selesai membuat fitur baru dan ingin semua user mendownload versi terbaru:
1.  **Build EXE**: Jalankan `build_exe.py` untuk mendapatkan file `.exe` baru.
2.  **Upload File**: Upload file `.exe` tersebut ke tempat penyimpanan Anda (Contoh: Google Drive, Dropbox, Mediafire, atau Website Anda).
3.  **Update Supabase**:
    - Buka **Supabase Dashboard** -> Tabel `app_metadata`.
    - Edit baris `ITC_ENTERPRISE`:
        - `version`: Ubah ke versi baru (Contoh: `1.0.2`).
        - `download_url`: Masukkan link download file baru Anda.
        - `changelog`: Tuliskan ringkasan fitur baru (aman & profesional).

## 3. Keamanan & Privasi
- **Zero Sensitive Data**: Update ini tidak menarik data pribadi user.
- **Manual Verification**: User tetap memegang kendali untuk mengklik tombol download, menghindari blokir dari Antivirus yang terlalu sensitif.

---
### 📈 Lokasi File di Cloud
Tabel: `app_metadata`
Link Portal: [Supabase Dashboard](https://supabase.com/dashboard/project/_/editor)
