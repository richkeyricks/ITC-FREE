# 🚀 Panduan Upload (Deploy) File Midtrans

Berikut adalah panduan lengkap cara meng-upload (deploy) ketiga file baru tersebut agar aktif dan bekerja.

## 1. Upload ke Supabase (Edge Functions)

Kita perlu meng-upload 2 fungsi ke server Supabase.
Pastikan Anda sudah login Supabase di terminal (`npx supabase login`).

### A. Deploy `payment-gateway`
File: `supabase/functions/payment-gateway/index.ts`

Jalankan perintah ini di terminal VS Code:
```bash
npx supabase functions deploy payment-gateway --no-verify-jwt
```
> **Catatan:** Fungsi ini wajib di-deploy agar aplikasi bisa membuat Token Transaksi Midtrans dengan aman.

### B. Deploy `payment-webhook` (Dari file `midtrans_webhook.ts`)
File sumber: `src/edge_functions/midtrans_webhook.ts`
Target fungsi: `payment-webhook`

Karena file sumbernya ada di folder `src`, kita perlu menyalinnya dulu ke folder fungsi Supabase, lalu deploy.

Jalankan perintah ini berurutan:
```bash
# 1. Copy file baru ke folder fungsi target (Menimpa file lama)
copy "src\edge_functions\midtrans_webhook.ts" "supabase\functions\payment-webhook\index.ts"

# 2. Deploy fungsi ke Supabase
npx supabase functions deploy payment-webhook --no-verify-jwt
```

---

## 2. Upload ke Vercel (Frontend API)

File: `vercel_deploy/api/pay.js`
Folder project: `vercel_deploy`

Kita perlu meng-update deployment Vercel Anda.

### Cara Deploy:
Jalankan perintah ini di terminal:

```bash
# 1. Masuk ke folder Vercel
cd vercel_deploy

# 2. Upload ke Vercel (Production)
vercel --prod
```

> **Penting:**
> Jika diminta konfirmasi (Y/N) atau memilih project, tekan `Enter` (Yes) atau pilih project `ITC-Copytrade-Website` yang sudah ada.

---

## ✅ Checklist Verifikasi
Setelah selesai deploy, pastikan:

1.  Buka Dashboard Supabase → Edge Functions.
    *   Pastikan `payment-gateway` dan `payment-webhook` statusnya **Active** (baru saja di-update).
    *   Pastikan ada **Secrets** `MIDTRANS_SERVER_KEY` di Supabase.

2.  Buka Website Anda.
    *   Coba klik tombol **Upgrade/Buy**.
    *   Pastikan Pop-up Midtrans muncul (artinya `pay.js` dan `payment-gateway` bekerja).

3.  Coba Bayar (Mode Sandbox/Test).
    *   Lihat apakah status di database berubah jadi `SUCCESS` (artinya `payment-webhook` bekerja).
