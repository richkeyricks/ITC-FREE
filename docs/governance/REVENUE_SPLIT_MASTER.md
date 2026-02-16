# 📜 REVENUE SPLIT MASTER — PANDUAN RESMI PEMBAGIAN UANG
# ═══════════════════════════════════════════════════════════════
# STATUS    : BERLAKU PERMANEN (Satu-satunya sumber kebenaran)
# VERSI     : 2.0.0
# TANGGAL   : 12 Februari 2026
# DIBUAT    : Hasil audit mendalam seluruh kode & dokumentasi
# ═══════════════════════════════════════════════════════════════

---

## ═══════════════════════════════════════
## BAGIAN 1: SIAPA SIAPA? (Semua Peran)
## ═══════════════════════════════════════

Ada **4 peran** dalam sistem ini. Setiap peran dijelaskan secara detail:

---

### PERAN 1: ADMIN / PLATFORM (Anda, Pemilik Aplikasi ITC)

- **Siapa**: Anda sendiri. Pemilik dan pengembang aplikasi ITC +AI.
- **Posisi**: Pemilik utama sistem. Semua uang dari customer MASUK DULU ke rekening Midtrans Anda.
- **Rekening**: Terhubung langsung ke Midtrans Production.
- **Tugasnya**:
  - Menerima semua pembayaran dari customer
  - Membayar komisi referrer secara MANUAL dari rekening pribadi (belum otomatis)
  - Membayar share seller secara MANUAL dari rekening pribadi (belum otomatis)
  - Mengelola sistem, approve payout request, dll

- **Apakah Admin bisa jadi Referrer?**
  - YA. Admin juga punya akun di sistem, jadi Admin bisa share link referral.
  - TAPI: Karena semua uang sudah masuk ke rekening Admin sendiri,
    maka komisi referral Admin = tidak perlu dibayar terpisah.
    Uangnya sudah di rekening Admin.
  - Kode saat ini MEMBOLEHKAN Admin punya referral code.
  - Self-referral dicegah oleh kode (tidak bisa pakai link sendiri).

- **Apakah Admin bisa jadi Seller?**
  - YA. Admin bisa publish strategy di marketplace seperti user lainnya.
  - TAPI: Karena semua uang sudah masuk ke Admin, maka Admin
    tidak perlu "membayar dirinya sendiri" 70%.
  - Dalam kode saat ini, TIDAK ADA pembeda antara strategy milik Admin
    dan strategy milik user biasa. Semuanya diperlakukan sama.
  - REKOMENDASI: Untuk strategy buatan Admin, tag sebagai
    "OFFICIAL" atau "ADMIN" dan skip revenue split (100% ke Admin).

---

### PERAN 2: SELLER (User Biasa yang Menjual Strategy di Marketplace)

- **Siapa**: User biasa yang BUKAN Admin. Dia membuat trading strategy
  dan menjualnya di marketplace.
- **Contoh**: "Budi" adalah trader Gold. Dia membuat strategy "Gold Scalper V1"
  dengan setting risk management dan filter signal khusus.
  Dia publish di marketplace seharga Rp 500.000.

- **Level/Tier apa yang bisa jadi Seller?**
  Berdasarkan kode saat ini (`verification_service.py` dan `marketplace_service.py`):

  **SYARAT PUBLISH STRATEGY KE MARKETPLACE:**
  1. Harus konek ke MT5 (MetaTrader 5 harus aktif)
  2. Harus punya minimal 5 trade dalam 14 hari terakhir (`MIN_TRADES = 5`)
  3. Harus punya minimum ROI 2% (`MIN_ROI = 2.0`)
  4. Harus punya minimum Win Rate 30% (`MIN_WINRATE = 30.0`)

  **CATATAN PENTING**: Dalam kode saat ini, TIDAK ADA pembatasan berdasarkan
  tier subscription (GOLD/PLATINUM/INSTITUTIONAL). Artinya bahkan user
  STANDARD (FREE) bisa publish strategy, SELAMA lulus verifikasi MT5.

  **TAPI** berdasarkan dokumentasi `03_QUANTUM_SIGNAL_MARKETPLACE.md`,
  SEHARUSNYA ada batasan:
  - STANDARD: 0 slot (tidak bisa publish)
  - GOLD PRO: 1 slot strategy
  - PLATINUM: 3 slot strategy
  - INSTITUTIONAL: 5 slot strategy

  **STATUS**: Batasan tier ini BELUM diimplementasikan di kode.

- **Bagaimana Seller dibayar?**
  Saat ini semua pembayaran masuk ke Midtrans Admin. Lalu:
  1. Admin melihat payout request dari seller di dashboard admin
  2. Admin MANUAL transfer dari rekeningnya ke rekening seller
  3. Belum ada auto-transfer

---

### PERAN 3: REFERRER / AFFILIATE (User yang Menyebarkan Link)

- **Siapa**: User yang mengajak orang lain untuk mendaftar & membeli
  menggunakan link referral unik mereka.
- **Contoh**: "Andi" share link referral di grup Telegram.
  "Siti" klik link tersebut, daftar, lalu beli GOLD PRO.
  → Andi mendapat 10% komisi dari pembelian Siti.
- **Penting**: Referrer TIDAK menjual produk apapun. Dia hanya MENGAJAK.

- **Apakah Seller bisa juga jadi Referrer?**
  YA. Seorang user bisa punya DUA peran:
  - Dia menjual strategy (sebagai Seller) → dapat revenue dari penjualan
  - Dia mengajak teman (sebagai Referrer) → dapat komisi dari pembelian teman
  - KEDUA penghasilan ini DIHITUNG TERPISAH.

- **Level/Tier Referrer (Berdasarkan jumlah orang yang berhasil diajak):**

  TIER STARTER (0-9 referral)
  → Komisi: 10% dari setiap pembelian yang dilakukan orang yang diajak
  → Bonus naik tier: Tidak ada

  TIER GOLD MEMBER (10-49 referral)
  → Komisi: 15% dari setiap pembelian
  → Bonus naik tier: $50 (≈ Rp 800.000) — SEKALI saat naik ke tier ini

  TIER PLATINUM (50-99 referral)
  → Komisi: 20% dari setiap pembelian
  → Bonus naik tier: $250 (≈ Rp 4.000.000) — SEKALI saat naik ke tier ini

  TIER INSTITUTIONAL (100+ referral)
  → Komisi: 25% dari setiap pembelian
  → Bonus naik tier: $1.000 (≈ Rp 16.000.000) — SEKALI saat naik ke tier ini

  **CATATAN**: Tier referral ini berbeda dari tier subscription!
  - Tier SUBSCRIPTION (Gold Pro, Platinum, Institutional) = apa yang user BELI
  - Tier REFERRAL (Starter, Gold, Platinum, Institutional) = jumlah orang yang dia AJAK

  Seorang user bisa berlangganan STANDARD (Free) tapi punya tier
  referral INSTITUTIONAL jika dia berhasil mengajak 100+ orang.

- **STATUS DI KODE**:
  - Tier calculation → SUDAH ADA di `_calculate_tier()` (`affiliate_service.py` line 163-172)
  - TAPI komisi SELALU 10% flat (line 18: `COMMISSION_RATE = 0.10`)
  - `_calculate_tier()` menghitung tier tapi TIDAK dipakai di `payout_commission()`
  - Artinya: Tier hanya tampilan, belum mempengaruhi kalkulasi

---

### PERAN 4: CUSTOMER / BUYER (Pembeli)

- **Siapa**: User yang membayar uang untuk mendapatkan sesuatu.
- **Apa yang bisa dibeli?**
  1. Subscription (GOLD PRO / PLATINUM / INSTITUTIONAL)
  2. Strategy dari marketplace (buatan user lain atau Admin)
- **Uang kemana?**: 100% masuk ke rekening Midtrans Admin.
- **Referral**: Customer mungkin punya "upline" (orang yang mengajaknya).
  Jika ada, Admin WAJIB bayar komisi ke upline dari kantong Admin.

---

## ═══════════════════════════════════════════════
## BAGIAN 2: PRODUK APA SAJA YANG DIJUAL?
## ═══════════════════════════════════════════════

---

### PRODUK TIPE A: SUBSCRIPTION (Akses Platform)

**Dijual oleh**: Admin/Platform (ini produk Anda sendiri)
**Dibeli oleh**: Customer
**Uang masuk ke**: 100% ke Admin (via Midtrans)

Daftar harga berdasarkan `configs/pricing_config.py`:

**STANDARD (GRATIS)**
- Harga: Rp 0 (Gratis selamanya)
- Fitur: Terbatas (3 trade/hari, profit cap $10, AI chat terbatas)
- Tujuan: Entry point, supaya user merasakan "winning psychology" lalu upgrade

**GOLD PRO**
- Bulanan:  $29  / Rp     450.000
- Tahunan:  $279 / Rp   4.300.000
- Lifetime: $899 / Rp  13.900.000

**PLATINUM VIP**
- Bulanan:  $99    / Rp   1.500.000
- Tahunan:  $950   / Rp  14.700.000
- Lifetime: $2.499 / Rp  38.700.000

**INSTITUTIONAL**
- Bulanan:  $299   / Rp   4.600.000
- Tahunan:  $2.990 / Rp  46.300.000
- Lifetime: CONTRACT ONLY

---

### PRODUK TIPE B: MARKETPLACE STRATEGY (Trading Preset)

**Dijual oleh**: Seller (user biasa) ATAU Admin
**Dibeli oleh**: Customer
**Harga**: Ditentukan oleh Seller sendiri (bebas)
**Uang masuk ke**: 100% masuk Midtrans Admin dulu → lalu Admin Split ke Seller
**Contoh**: Strategy "Gold Scalper V1" dijual Rp 500.000 oleh Budi

---

## ═══════════════════════════════════════════════════════════
## BAGIAN 3: ALUR PELACAKAN REFERRAL (TRACKING SYSTEM)
## ═══════════════════════════════════════════════════════════

Bagaimana sistem melacak siapa mengajak siapa? Berikut alurnya step by step:

---

### STEP 1: User Punya Kode Referral Unik

Setiap user yang login bisa generate kode referral 6 karakter.
Contoh: Andi punya kode "WXY123"
File kode: `affiliate_service.py` → `generate_my_code()`
Database: Disimpan di tabel `affiliate_codes` (user_id ↔ code)

### STEP 2: User Share Link Referral

Format link: `gravity.id/ref/WXY123` atau via protocol handler `itc://invite?code=WXY123`
Andi share link ini di media sosial, grup Telegram, dll.

### STEP 3: Orang Baru Klik Link & Daftar

Ketika Siti klik link Andi dan install/buka aplikasi:
1. Aplikasi membaca parameter `invite=WXY123`
   File: `protocol_handler.py` → membaca `params.get("invite")`
2. Saat first login, kode disimpan secara "stealth"
   File: `gui.py` line 401-404 → `bind_referral_stealth()`
3. Sistem memasangkan: Referrer=Andi ↔ Referee=Siti
   File: `affiliate_service.py` → `bind_referral(code)`
   Database: Insert ke tabel `affiliate_referrals`

### STEP 4: Proteksi

- **Self-Referral Dicegah**: Kode line 71-73: `if referrer_id == referee_id: return False`
- **Satu Upline Saja**: Database punya unique constraint pada `referee_id`
  → Jika Siti sudah punya referrer, dia tidak bisa ganti ke referrer lain
- **Lifetime Binding**: Sekali terhubung, ikatan referral PERMANEN
  Bahkan jika Siti ganti device, karena tracking berbasis user_id (bukan cookie/device)

### STEP 5: Saat Referral Membeli Sesuatu

Ketika Siti membeli GOLD PRO:
1. Payment berhasil via Midtrans
2. Sistem memanggil `payout_commission(order_id, purchase_amount, buyer_id)`
3. Fungsi ini mencari: "Siapa upline Siti?" → Andi
4. Hitung komisi: purchase_amount × COMMISSION_RATE
5. Insert ke tabel `affiliate_commissions`
6. Update wallet Andi: `balance_pending` bertambah
7. Setelah 3 hari (escrow) → pindah ke `balance_active` (BELUM DIIMPLEMENTASIKAN)

---

## ═══════════════════════════════════════════════════════════
## BAGIAN 4: SEMUA SKENARIO PEMBAGIAN UANG (DETAIL)
## ═══════════════════════════════════════════════════════════

---

### SKENARIO 1: Customer Beli Subscription (GOLD PRO Monthly Rp 450.000)
### Customer PUNYA Referrer

**Alur uang:**

```
SITI (Customer) bayar Rp 450.000
         │
         ▼
   ┌──────────┐
   │ MIDTRANS  │──→ 100% masuk ke rekening Admin
   └──────────┘
         │
    Admin terima Rp 450.000
         │
    Cek: Siti punya upline? ──→ YA (Andi)
         │
    Cek: Andi di tier referral berapa?
         │
         ├─── Andi = STARTER (0-9 orang diajak): Komisi 10%
         │    Komisi Andi = Rp 450.000 × 10% = Rp 45.000
         │    Admin bayar Andi = Rp 45.000
         │    SISA BERSIH ADMIN = Rp 450.000 - Rp 45.000 = Rp 405.000
         │
         ├─── Andi = GOLD (10-49 orang diajak): Komisi 15%
         │    Komisi Andi = Rp 450.000 × 15% = Rp 67.500
         │    Admin bayar Andi = Rp 67.500
         │    SISA BERSIH ADMIN = Rp 450.000 - Rp 67.500 = Rp 382.500
         │
         ├─── Andi = PLATINUM (50-99 orang diajak): Komisi 20%
         │    Komisi Andi = Rp 450.000 × 20% = Rp 90.000
         │    Admin bayar Andi = Rp 90.000
         │    SISA BERSIH ADMIN = Rp 450.000 - Rp 90.000 = Rp 360.000
         │
         └─── Andi = INSTITUTIONAL (100+ orang diajak): Komisi 25%
              Komisi Andi = Rp 450.000 × 25% = Rp 112.500
              Admin bayar Andi = Rp 112.500
              SISA BERSIH ADMIN = Rp 450.000 - Rp 112.500 = Rp 337.500
```

**Perhitungan verifikasi (cek total):**
- Starter:      Rp 45.000 + Rp 405.000 = Rp 450.000 ✅
- Gold:         Rp 67.500 + Rp 382.500 = Rp 450.000 ✅
- Platinum:     Rp 90.000 + Rp 360.000 = Rp 450.000 ✅
- Institutional: Rp 112.500 + Rp 337.500 = Rp 450.000 ✅

**Kesimpulan**: Admin SELALU minimal dapat 75% dari subscription (worst case).

---

### SKENARIO 2: Customer Beli Subscription TANPA Referrer

```
SITI (Customer) bayar Rp 450.000
         │
         ▼
   ┌──────────┐
   │ MIDTRANS  │──→ 100% masuk ke rekening Admin
   └──────────┘
         │
    Admin terima Rp 450.000
         │
    Cek: Siti punya upline? ──→ TIDAK
         │
    Tidak ada komisi yang perlu dibayar.
    SISA BERSIH ADMIN = Rp 450.000 (100%)
```

---

### SKENARIO 3: Customer Beli Strategy MILIK USER BIASA (Marketplace)
### Customer PUNYA Referrer

**Situasi**:
- Budi (Seller, user biasa) jual "Gold Scalper V1" seharga Rp 500.000
- Siti (Customer) beli strategy Budi
- Siti diajak oleh Andi (Referrer, tier Starter 10%)

**Alur uang (Rekomendasi: 70% Seller / 30% Platform, komisi dari bagian Platform):**

```
SITI (Customer) bayar Rp 500.000
         │
         ▼
   ┌──────────┐
   │ MIDTRANS  │──→ 100% masuk ke rekening Admin
   └──────────┘
         │
    Admin terima Rp 500.000
         │
    Jenis produk = MARKETPLACE STRATEGY (bukan subscription)
         │
    STEP 1: Hitung bagian Seller (BUDI)
    Seller share = 70% × Rp 500.000 = Rp 350.000
    → Masuk ke wallet Budi (balance_pending)
    → Setelah 3 hari → pindah ke balance_active
    → Budi bisa request payout setelah terpenuhi syarat
         │
    STEP 2: Sisa untuk Platform (Admin)
    Platform pool = 30% × Rp 500.000 = Rp 150.000
         │
    STEP 3: Cek referrer
    Siti punya upline? → YA (Andi, tier Starter 10%)
    Komisi Andi = 10% × Rp 500.000 = Rp 50.000
    → Dipotong dari Platform Pool
         │
    STEP 4: Hitung sisa bersih Admin
    Admin net = Rp 150.000 - Rp 50.000 = Rp 100.000

    ═══════════════════════════════════════
    RINGKASAN:
    Seller (Budi)    = Rp 350.000 (70%)
    Referrer (Andi)  = Rp  50.000 (10%)
    Admin (Platform) = Rp 100.000 (20%)
    ─────────────────────────────────────
    TOTAL            = Rp 500.000 (100%) ✅
```

**Bagaimana jika Andi tier GOLD (15%)?**

```
    Seller (Budi)    = 70% × Rp 500.000 = Rp 350.000
    Referrer (Andi)  = 15% × Rp 500.000 = Rp  75.000
    Admin            = Rp 150.000 - Rp 75.000 = Rp  75.000
    ─────────────────────────────────────────────────────
    TOTAL = Rp 350.000 + Rp 75.000 + Rp 75.000 = Rp 500.000 ✅
```

**Bagaimana jika Andi tier PLATINUM (20%)?**

```
    Seller (Budi)    = 70% × Rp 500.000 = Rp 350.000
    Referrer (Andi)  = 20% × Rp 500.000 = Rp 100.000
    Admin            = Rp 150.000 - Rp 100.000 = Rp  50.000
    ─────────────────────────────────────────────────────
    TOTAL = Rp 350.000 + Rp 100.000 + Rp 50.000 = Rp 500.000 ✅
```

**Bagaimana jika Andi tier INSTITUTIONAL (25%)?**

```
    Seller (Budi)    = 70% × Rp 500.000 = Rp 350.000
    Referrer (Andi)  = 25% × Rp 500.000 = Rp 125.000
    Admin            = Rp 150.000 - Rp 125.000 = Rp  25.000
    ─────────────────────────────────────────────────────
    TOTAL = Rp 350.000 + Rp 125.000 + Rp 25.000 = Rp 500.000 ✅
    ⚠️ Margin Admin kecil, tapi TIDAK RUGI.
```

**Bagaimana jika TIDAK ADA Referrer?**

```
    Seller (Budi)    = 70% × Rp 500.000 = Rp 350.000
    Admin            = 30% × Rp 500.000 = Rp 150.000 (full)
    ─────────────────────────────────────────────────────
    TOTAL = Rp 350.000 + Rp 150.000 = Rp 500.000 ✅
```

---

### SKENARIO 4: Customer Beli Strategy MILIK ADMIN

**Situasi**:
- Admin (Anda) membuat strategy "Neural Gold Hunter" Rp 300.000
- Siti (Customer) beli strategy Anda
- Siti diajak oleh Andi (Referrer, tier Starter 10%)

**Alur uang:**

```
SITI (Customer) bayar Rp 300.000
         │
         ▼
   ┌──────────┐
   │ MIDTRANS  │──→ 100% masuk ke rekening Admin
   └──────────┘
         │
    Admin terima Rp 300.000
         │
    Jenis produk = MARKETPLACE STRATEGY
    TAPI: Seller = Admin sendiri
         │
    KARENA seller adalah Admin sendiri:
    → TIDAK PERLU split 70/30 (Admin tidak perlu bayar dirinya sendiri)
    → Strategy milik Admin = diperlakukan seperti SUBSCRIPTION
    → 100% milik Admin
         │
    STEP: Cek referrer
    Siti punya upline? → YA (Andi, tier Starter 10%)
    Komisi Andi = 10% × Rp 300.000 = Rp 30.000
         │
    SISA BERSIH ADMIN = Rp 300.000 - Rp 30.000 = Rp 270.000

    ═══════════════════════════════════════
    RINGKASAN:
    Admin            = Rp 270.000 (90%)
    Referrer (Andi)  = Rp  30.000 (10%)
    ─────────────────────────────────────
    TOTAL            = Rp 300.000 (100%) ✅
```

**Tanpa referrer:**

```
    Admin = Rp 300.000 (100%)
    TOTAL = Rp 300.000 ✅
```

---

### SKENARIO 5: Admin Menjalankan Referral Program Sendiri

**Situasi**: Admin share link referral sendiri. Orang yang diajak Admin beli sesuatu.

```
ADMIN share link referral → DANI mendaftar via link Admin
DANI beli GOLD PRO Monthly Rp 450.000
         │
         ▼
   ┌──────────┐
   │ MIDTRANS  │──→ 100% masuk ke rekening Admin
   └──────────┘
         │
    Admin terima Rp 450.000
         │
    Cek: Dani punya upline? → YA (Admin sendiri)
         │
    Komisi Admin = 10% × Rp 450.000 = Rp 45.000
    TAPI: komisi ini ke Admin sendiri!
    → Uangnya SUDAH di rekening Admin
    → Admin TIDAK PERLU bayar siapapun
    → Komisi ini otomatis "sudah dibayar" karena semua uang sudah di Admin

    SISA BERSIH ADMIN = Rp 450.000 (100%)
    Komisi formal (tercatat di database) = Rp 45.000 (ke wallet Admin)

    KESIMPULAN: Admin sebagai referrer = hanya formalitas pencatatan.
    Tidak ada uang keluar karena semua sudah di rekening Admin.
```

---

### SKENARIO 6: User Referrer Membagikan Strategy Milik Admin

**Situasi**:
- Admin publish strategy "Neural Gold Hunter" Rp 300.000
- Andi (Referrer tier Gold 15%) membagikan LINK strategy Admin ke temannya
- Siti beli strategy tersebut (Siti = downline Andi)

```
    Ini SAMA dengan Skenario 4 (Customer beli strategy Admin).
    Seller = Admin, jadi tidak ada split 70/30.

    Hitungan:
    Admin terima      = Rp 300.000
    Komisi Andi (15%) = Rp 300.000 × 15% = Rp 45.000
    SISA ADMIN        = Rp 300.000 - Rp 45.000 = Rp 255.000

    ═══════════════════════════════════════
    RINGKASAN:
    Admin            = Rp 255.000 (85%)
    Referrer (Andi)  = Rp  45.000 (15%)
    ─────────────────────────────────────
    TOTAL            = Rp 300.000 (100%) ✅
```

---

### SKENARIO 7: User Referrer Membagikan Strategy Milik User Lain

**Situasi**:
- Budi (Seller) publish strategy Rp 500.000
- Andi (Referrer tier Platinum 20%) bagikan link strategy Budi ke Siti
- Siti (Customer, downline Andi) beli strategy Budi

```
    Ini SAMA dengan Skenario 3.
    Seller = Budi (user biasa), jadi ada split 70/30.

    Hitungan:
    Seller (Budi)     = 70% × Rp 500.000 = Rp 350.000
    Platform Pool     = 30% × Rp 500.000 = Rp 150.000
    Komisi Andi (20%) = 20% × Rp 500.000 = Rp 100.000
    Admin net         = Rp 150.000 - Rp 100.000 = Rp 50.000

    ═══════════════════════════════════════
    RINGKASAN:
    Seller (Budi)      = Rp 350.000 (70%)
    Referrer (Andi)    = Rp 100.000 (20%)
    Admin (Platform)   = Rp  50.000 (10%)
    ─────────────────────────────────────
    TOTAL              = Rp 500.000 (100%) ✅
```

---

### SKENARIO 8: User Subscribe Via Link Referral User Tier Tertentu

**Situasi**: Andi (tier Platinum 20%) share link. Siti subscribe PLATINUM VIP Lifetime Rp 38.700.000.

```
    Ini SAMA dengan Skenario 1. Subscription = produk Admin.

    Hitungan:
    Admin terima      = Rp 38.700.000
    Komisi Andi (20%) = 20% × Rp 38.700.000 = Rp 7.740.000
    SISA ADMIN        = Rp 38.700.000 - Rp 7.740.000 = Rp 30.960.000

    ═══════════════════════════════════════
    RINGKASAN:
    Admin              = Rp 30.960.000 (80%)
    Referrer (Andi)    = Rp  7.740.000 (20%)
    ─────────────────────────────────────
    TOTAL              = Rp 38.700.000 (100%) ✅
```

---

## ═══════════════════════════════════════════════════════════
## BAGIAN 5: MEKANISME PAYOUT (Pencairan Uang)
## ═══════════════════════════════════════════════════════════

---

### Bagaimana User Dibayar?

Saat ini, SEMUA pembayaran ke user (seller/referrer) dilakukan MANUAL oleh Admin:

```
ALUR PAYOUT:

1. User mengumpulkan earning (dari referral komisi atau marketplace sales)
   → Masuk ke wallet: balance_pending (escrow)

2. Setelah 3 hari (T+3) → pindah ke balance_active
   (CATATAN: Escrow T+3 BELUM diimplementasikan di kode.
    Saat ini balance langsung ke pending dan tidak otomatis pindah.)

3. User melihat balance_active di dashboard
   → Jika sudah memenuhi minimum withdrawal → tombol PAYOUT muncul

4. User klik PAYOUT → muncul form input:
   → Masukkan jumlah withdrawal
   → Masukkan data rekening (bank_name, bank_number, account_holder)
   (CATATAN: Saat ini data bank masih MOCK/dummy di kode: BCA/123/User
    File: referral_view.py line 333. INI PERLU DIIMPLEMENTASIKAN.)

5. Request masuk ke tabel "payout_requests" dengan status "REQUESTED"
   → Admin buka dashboard admin
   → Admin lihat request
   → Admin transfer MANUAL dari rekening pribadinya ke rekening user
   → Admin update status jadi "PAID" (BELUM ADA UI untuk ini)

MINIMUM WITHDRAWAL:
   → IDR: Rp 100.000 (hardcoded di referral_view.py line 329)
   → USD: $7 (dari currency helper)
   → Docs lama bilang Rp 1.000.000 → INI PERLU DIPUTUSKAN
```

---

### Syarat-Syarat Sebelum Bisa Payout

Berdasarkan kode dan dokumentasi yang ada:

```
SYARAT PAYOUT REFERRER:
1. Harus punya balance_active > 0 (artinya sudah lolos escrow)
2. Jumlah withdrawal ≥ minimum (Rp 100.000 atau $7)
3. Harus input data rekening bank yang valid
4. Request masuk ke antrian, Admin approve manual

SYARAT PAYOUT SELLER:
1. Strategy harus terverifikasi (lulus Proof of Profit)
2. Harus ada penjualan yang berhasil (COMPLETED di marketplace_orders)
3. Balance_active harus ≥ minimum withdrawal
4. Input rekening bank
5. Admin approve manual

CATATAN: Banyak dari syarat ini BELUM diimplementasikan di kode:
- Escrow T+3 belum ada
- Form input rekening belum ada (masih mock)
- Admin approval UI belum ada
- Status tracking "REQUESTED" → "APPROVED" → "PAID" belum lengkap
```

---

## ═══════════════════════════════════════════════════════════
## BAGIAN 6: BATASAN AKSES PER TIER (Siapa Boleh Apa)
## ═══════════════════════════════════════════════════════════

---

### Berdasarkan Dokumentasi & Kode:

```
STANDARD (FREE):
├── Copy Trade: 3 trade per hari (limit_manager.py)
├── Profit Cap: $10 USD per hari
├── AI Chat: Terbatas
├── Marketplace: Bisa BELI strategy
├── Publish Strategy: SEHARUSNYA 0 slot (docs), TAPI kode saat ini TIDAK membatasi
├── Referral: BISA (siapa saja bisa share link referral)
└── Signal Broadcast: TIDAK bisa

GOLD PRO:
├── Copy Trade: Unlimited
├── Profit Cap: Unlimited
├── AI Chat: Extended
├── Marketplace: Bisa BELI dan JUAL strategy
├── Publish Strategy: SEHARUSNYA 1 slot (docs)
├── Referral: BISA
└── Signal Broadcast: SEHARUSNYA 1 slot (docs, belum implementasi)

PLATINUM VIP:
├── Copy Trade: Unlimited
├── Profit Cap: Unlimited
├── AI Chat: Unlimited
├── Marketplace: Bisa BELI dan JUAL strategy
├── Publish Strategy: SEHARUSNYA 3 slot (docs)
├── Referral: BISA
├── Signal Broadcast: SEHARUSNYA 3 slot (docs, belum implementasi)
└── Priority Payout: Lebih cepat diproses

INSTITUTIONAL:
├── Copy Trade: Unlimited
├── Profit Cap: Unlimited
├── AI Chat: Unlimited
├── Marketplace: Bisa BELI dan JUAL strategy
├── Publish Strategy: SEHARUSNYA 5 slot (docs)
├── Referral: BISA
├── Signal Broadcast: SEHARUSNYA 5 slot (docs, belum implementasi)
├── Priority Payout: Tercepat
└── Dedicated Support
```

---

## ═══════════════════════════════════════════════════════════
## BAGIAN 7: APA SAJA YANG SUDAH ADA vs BELUM DI KODE
## ═══════════════════════════════════════════════════════════

---

### SUDAH ADA (WORKING):

```
✅ Semua pembayaran masuk ke Midtrans Admin
✅ Referral code generation (generate_my_code)
✅ Referral binding (bind_referral)
✅ Self-referral prevention
✅ One upline only (database unique constraint)
✅ Stealth referral via protocol handler
✅ Tier calculation based on referral count (_calculate_tier)
✅ Commission recording ke tabel affiliate_commissions
✅ Wallet balance tracking (balance_pending, total_earned)
✅ Payout request creation ke tabel payout_requests
✅ Strategy verification via MT5 history
✅ Strategy publish ke marketplace_presets
✅ Strategy purchase via Midtrans
✅ Minimum withdrawal check (Rp 100.000)
```

### BELUM ADA (PERLU IMPLEMENTASI):

```
❌ Tier-based commission rates (15%/20%/25%) — selalu flat 10%
❌ Marketplace revenue split (seller 70% / admin 30%)
❌ Escrow T+3 days (pending → active otomatis)
❌ Tier bonus saat naik tier ($50/$250/$1000)
❌ Form input rekening bank (saat ini masih mock data)
❌ Admin payout approval UI
❌ Batasan publish per tier subscription (0/1/3/5 slot)
❌ Signal broadcast tier limits
❌ Listing fee ($1 per signal)
❌ Usage fee ($0.10 per copy trade)
❌ Auto-transfer Friday
❌ Admin strategy tagging (mark sebagai OFFICIAL)
❌ Revenue split skip untuk strategy Admin
```

---

## ═══════════════════════════════════════════════════════════
## BAGIAN 8: RUMUS FINAL (Rangkuman Matematika)
## ═══════════════════════════════════════════════════════════

---

### RUMUS SUBSCRIPTION (Produk Admin):

```
Revenue Admin = Harga - Komisi Referrer
Komisi Referrer = Harga × Rate Tier Referrer

Dimana Rate Tier Referrer:
  Tanpa Referrer  = 0%     → Admin dapat 100%
  Starter         = 10%    → Admin dapat 90%
  Gold            = 15%    → Admin dapat 85%
  Platinum        = 20%    → Admin dapat 80%
  Institutional   = 25%    → Admin dapat 75%

ADMIN MINIMUM MENDAPAT 75% dari setiap subscription.
```

### RUMUS MARKETPLACE (Produk Seller/User Biasa):

```
Seller Share   = Harga × 70%    (SELALU TETAP)
Platform Pool  = Harga × 30%
Komisi Referrer = Harga × Rate Tier Referrer (dari Platform Pool)
Admin Net      = Platform Pool - Komisi Referrer

Dimana:
  Tanpa Referrer  → Admin = 30%, Seller = 70%
  Starter (10%)   → Admin = 20%, Seller = 70%, Referrer = 10%
  Gold (15%)      → Admin = 15%, Seller = 70%, Referrer = 15%
  Platinum (20%)  → Admin = 10%, Seller = 70%, Referrer = 20%
  Institutional (25%) → Admin = 5%, Seller = 70%, Referrer = 25%

ADMIN MINIMUM MENDAPAT 5% dari setiap penjualan marketplace.
SELLER SELALU MENDAPAT 70%.
```

### RUMUS MARKETPLACE (Produk Admin Sendiri):

```
Revenue Admin = Harga - Komisi Referrer
(Sama dengan rumus subscription karena seller = admin)

ADMIN MINIMUM MENDAPAT 75% dari setiap penjualan strategy Admin.
```

---

## ═══════════════════════════════════════════════════════════
## BAGIAN 9: KEPUTUSAN YANG MASIH PERLU DIAMBIL
## ═══════════════════════════════════════════════════════════

Berikut hal-hal yang BELUM final dan membutuhkan keputusan Anda:

---

### Keputusan 1: Platform Fee = Berapa?

Opsi A: 30% (berdasarkan docs arsitektur) → Seller dapat 70%
Opsi B: 20% (berdasarkan teks UI saat ini) → Seller dapat 80%

REKOMENDASI: 30%. Alasan:
- Marketplace serupa (Apple App Store, Gumroad) ambil 30%
- Docs arsitektur sudah menetapkan 30%
- Jika ada referrer tier tinggi, Admin masih untung (minimal 5%)
- Jika 20%, Admin bisa RUGI jika referrer tier tinggi (20% - 25% = -5%)

### Keputusan 2: Minimum Withdrawal = Berapa?

Opsi A: Rp 100.000 (kode saat ini)
Opsi B: Rp 1.000.000 (docs arsitektur)

REKOMENDASI: Rp 100.000 untuk referrer, Rp 1.000.000 untuk seller.

### Keputusan 3: Bonus Naik Tier = Implementasi atau Tampilan?

Opsi A: Implementasi nyata → benar-benar credit wallet saat naik tier
Opsi B: Tampilan motivasi saja → tidak ada bayaran nyata

REKOMENDASI: Tergantung budget. Bonus besar ($1000) bisa jadi beban.

### Keputusan 4: Batasan Publish Per Tier = Terapkan?

Opsi A: Semua user boleh publish (kode saat ini)
Opsi B: Hanya Gold+ boleh publish (sesuai docs)

REKOMENDASI: Opsi B. Ini mendorong user upgrade dari STANDARD.

---

## ═══════════════════════════════════════════════════════════
## BAGIAN 10: REFERENSI FILE KODE
## ═══════════════════════════════════════════════════════════

```
LOGIC LAYER (Otak Kalkulasi):
├── src/modules/logic/affiliate_service.py    → Referral & komisi
├── src/modules/logic/merchant_service.py     → Wallet & payout
├── src/modules/logic/marketplace_service.py  → Pembelian strategy
├── src/modules/logic/payment_service.py      → Bridge ke Midtrans
├── src/modules/logic/verification_service.py → Verifikasi strategy

UI LAYER (Tampilan):
├── src/modules/ui/referral_view.py           → Halaman referral
├── src/modules/ui/merchant_dashboard_view.py → Dashboard merchant
├── src/modules/ui/marketplace_view.py        → Halaman marketplace
├── src/modules/ui/publisher_dialog.py        → Dialog publish strategy
├── src/modules/ui/subscription_view.py       → Halaman subscription

CONFIG:
├── src/configs/pricing_config.py             → Harga subscription
├── src/utils/currency.py                     → Format mata uang

DATABASE:
├── Tabel: affiliate_codes                    → Kode referral per user
├── Tabel: affiliate_referrals                → Ikatan referrer-referee
├── Tabel: affiliate_commissions              → Log komisi
├── Tabel: user_wallets                       → Saldo wallet
├── Tabel: payout_requests                    → Request pencairan
├── Tabel: marketplace_presets                → Strategy di marketplace
├── Tabel: marketplace_orders                 → Pembelian strategy
```

---

> **DOKUMEN INI ADALAH SATU-SATUNYA SUMBER KEBENARAN.**
> Semua dokumentasi lama yang bertentangan dianggap KADALUARSA.
> Setelah keputusan di Bagian 9 dijawab, dokumen ini akan diupdate menjadi FINAL
> dan akan menjadi dasar implementasi kode.
>
> — Terakhir diaudit: 12 Februari 2026, Versi 2.0.0
