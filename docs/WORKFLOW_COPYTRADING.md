# 📡 ITC +AI — Dokumentasi Workflow CopyTrading

> **Versi Dokumen:** v4.9.5
> **Terakhir Diperbarui:** 15 Februari 2026
> **Bahasa:** Indonesia

---

## 1. Arsitektur Umum Sistem

Diagram berikut menunjukkan arsitektur tingkat tinggi dari seluruh sistem ITC CopyTrading.

### 📋 Visual: Alur Data Sistem

```
┌─────────────────────┐
│  📱 TELEGRAM CHANNEL │  (Sumber Sinyal Trading)
│  (Signal Provider)   │
└─────────┬───────────┘
          │ Pesan Masuk
          ▼
┌─────────────────────────────────────────────────────┐
│  🖥️  ITC +AI DESKTOP APPLICATION                    │
│                                                     │
│  ┌──────────────┐    ┌──────────────┐               │
│  │  Pyrogram    │───▶│ Regex Parser │──── Berhasil ─▶│
│  │  Client      │    │ (Tahap 1)    │               │
│  │  (Listener)  │    └──────┬───────┘               │
│  └──────────────┘           │ Gagal                 │
│                             ▼                       │
│                    ┌──────────────┐                  │
│                    │  AI Parser   │──── Berhasil ─┐  │
│                    │  (Tahap 2)   │               │  │
│                    └──────────────┘               │  │
│                                                   ▼  │
│                    ┌──────────────────────────────┐  │
│                    │  🛡️ GUARD SYSTEM              │  │
│                    │  • Filter Waktu              │  │
│                    │  • Equity Guard              │  │
│                    │  • Tier Limit                │  │
│                    └──────────┬───────────────────┘  │
│                               │ Lolos                │
│                               ▼                      │
│                    ┌──────────────┐                  │
│                    │  MT5 Service │─── Order ──┐     │
│                    │  (Executor)  │            │     │
│                    └──────────────┘            │     │
│                                               │     │
│  ┌──────────────┐                             │     │
│  │ Monitor Loop │◀── Posisi Terbuka ──────────┤     │
│  │ (Background) │                             │     │
│  └──────┬───────┘                             │     │
│         │ Trade Baru (VIP)                    │     │
│         ▼                                     │     │
│  ┌──────────────┐                             │     │
│  │ Broadcaster  │                             │     │
│  │ (VIP Only)   │                             │     │
│  └──────┬───────┘                             │     │
└─────────┼─────────────────────────────────────┼─────┘
          │                                     │
          ▼                                     ▼
┌──────────────────┐              ┌──────────────────┐
│ ☁️ Telegram Bot   │              │ 📊 MetaTrader 5   │
│ (Notifikasi)     │              │ (Terminal)        │
└──────────────────┘              └──────────────────┘
          │
          ▼
┌──────────────────┐
│ ☁️ Supabase       │
│ (Database Cloud) │
└──────────────────┘
```

### 🔗 Diagram Mermaid (untuk renderer)

```mermaid
graph TB
    subgraph "📱 Sumber Sinyal"
        TG["Telegram Channel<br/>(Signal Provider)"]
    end

    subgraph "🖥️ ITC +AI Desktop App"
        PYR["Pyrogram Client<br/>(Listener)"]
        REGEX["Regex Parser"]
        AI["AI Parser<br/>(Fallback)"]
        GUARD["Guard System<br/>(Time + Equity + Limit)"]
        MT5S["MT5 Service<br/>(Executor)"]
        MON["Monitor Loop<br/>(Background)"]
        BC["Broadcaster<br/>(VIP Only)"]
    end

    subgraph "📊 MetaTrader 5"
        MT5["MT5 Terminal"]
    end

    subgraph "☁️ Cloud Services"
        SB["Supabase<br/>(Database)"]
        TG_BOT["Telegram Bot<br/>(Notifikasi)"]
    end

    TG -->|"Pesan Masuk"| PYR
    PYR -->|"Teks Sinyal"| REGEX
    REGEX -->|"Gagal"| AI
    REGEX -->|"Berhasil"| GUARD
    AI -->|"Berhasil"| GUARD
    GUARD -->|"Lolos"| MT5S
    MT5S -->|"Order Request"| MT5
    MT5 -->|"Posisi Terbuka"| MON
    MON -->|"Deteksi Trade Baru"| BC
    BC -->|"Kirim Sinyal"| TG_BOT
    MT5S -->|"Log Trade"| SB
    MT5S -->|"Notifikasi"| TG_BOT

    style TG fill:#0088cc,color:#fff
    style MT5 fill:#2962ff,color:#fff
    style SB fill:#3ecf8e,color:#fff
    style PYR fill:#6366f1,color:#fff
    style GUARD fill:#ef4444,color:#fff
    style MT5S fill:#f59e0b,color:#000
```

---

## 2. Alur Utama: Telegram → MT5 CopyTrading

Ini adalah alur inti dari proses copy sinyal dari Telegram ke eksekusi di MetaTrader 5.

### 📋 Visual: Langkah-Langkah Utama

| Step | Aksi | Kondisi | Hasil |
|------|------|---------|-------|
| 1 | 🚀 User klik **START COPIER** | — | Mulai proses |
| 2 | Validasi Input | API ID & Hash kosong? | ❌ → Error: Missing Config |
| 3 | Cek Thread Guard | Thread copier sudah aktif? | ❌ → ⚠️ Already Running |
| 4 | Set Flag | `copier_running = True` | Tombol berubah → **STOP COPIER** |
| 5 | Mulai 2 Thread | `monitor_trades()` + `run_telegram()` | Background threads aktif |
| 6 | Buat Event Loop | `asyncio.new_event_loop()` | Loop baru untuk async |
| 7 | Hapus Client Lama | `index.app = None` | Bersihkan referensi lama |
| 8 | Buat Client Baru | `create_telegram_client()` | ❌ Gagal → Error log |
| 9 | Connect & Start | `await client.start()` | ✅ Telegram terhubung |
| 10 | 📡 **Loop Mendengarkan** | `while copier_running` → sleep 1 detik | Terus mendengarkan sinyal |
| 11 | User klik **STOP** | `copier_running = False` | Keluar dari loop |
| 12 | 🧹 Clean Shutdown | `await client.stop()` | Client terputus bersih |
| 13 | Reset | Flag & tombol direset | Kembali ke kondisi awal |

```
Alur Singkat:

  START COPIER ──▶ Validasi ──▶ Guard Thread ──▶ Set Flag
                                                    │
                         ┌──────────────────────────┘
                         ▼
              ┌─── monitor_trades() (Background)
              │
              └─── run_telegram()
                      │
                      ▼
              Buat Client ──▶ Connect ──▶ 📡 LISTENING LOOP
                                              │         ▲
                                              │ sleep 1s│
                                              └─────────┘
                                              │
                                         STOP COPIER
                                              │
                                              ▼
                                     🧹 Clean Shutdown
```

### 🔗 Diagram Mermaid (untuk renderer)

```mermaid
flowchart TD
    START(["🚀 User Klik START COPIER"]) --> VALIDATE{"Validasi Input<br/>API ID, API Hash?"}
    VALIDATE -->|"❌ Kosong"| ERR_INPUT["Log Error: Missing Config"]
    VALIDATE -->|"✅ Lengkap"| GUARD_THREAD{"Thread Copier<br/>Sudah Aktif?"}

    GUARD_THREAD -->|"Ya (Aktif)"| ERR_DOUBLE["⚠️ Copier Already Running"]
    GUARD_THREAD -->|"Tidak"| SET_FLAG["Set copier_running = True<br/>Ubah Tombol → STOP COPIER"]

    SET_FLAG --> START_MONITOR["🔁 Mulai monitor_trades()<br/>(Background Thread)"]
    SET_FLAG --> START_TG["📡 Mulai run_telegram()<br/>(Background Thread)"]

    START_TG --> NEW_LOOP["Buat Event Loop Baru<br/>(asyncio.new_event_loop)"]
    NEW_LOOP --> CLEAR_OLD["Hapus Referensi Client Lama<br/>(index.app = None)"]
    CLEAR_OLD --> CREATE_CLIENT["Buat Client Pyrogram Baru<br/>(create_telegram_client)"]

    CREATE_CLIENT -->|"❌ Gagal"| ERR_CLIENT["Log Error: Client Gagal"]
    CREATE_CLIENT -->|"✅ Berhasil"| AWAIT_START["await client.start()"]

    AWAIT_START --> SET_ACTIVE["Set is_telegram_active = True"]
    SET_ACTIVE --> LISTEN_LOOP["🔄 Loop Mendengarkan<br/>(while copier_running)"]

    LISTEN_LOOP -->|"copier_running = True"| SLEEP["await asyncio.sleep(1)"]
    SLEEP --> LISTEN_LOOP

    LISTEN_LOOP -->|"copier_running = False<br/>(User klik STOP)"| SHUTDOWN["🧹 Clean Shutdown"]
    SHUTDOWN --> DISCONNECT["await client.stop()"]
    DISCONNECT --> RESET["Reset Flag & Tombol<br/>copier_running = False"]

    style START fill:#10b981,color:#fff
    style ERR_INPUT fill:#f85149,color:#fff
    style ERR_DOUBLE fill:#d29922,color:#000
    style ERR_CLIENT fill:#f85149,color:#fff
    style LISTEN_LOOP fill:#6366f1,color:#fff
    style SHUTDOWN fill:#ef4444,color:#fff
```

---

## 3. Alur Parsing Sinyal (Regex + AI Fallback)

Ketika pesan masuk dari Telegram, sistem menggunakan dua tahap parsing untuk mengekstrak sinyal trading.

### 📋 Visual: Proses Parsing

| Tahap | Proses | Detail |
|-------|--------|--------|
| 0 | 📨 Pesan masuk dari channel | Teks mentah dari Telegram |
| 1 | Cek teks kosong | Jika kosong → **Skip** |
| 2 | Cek duplikasi (MD5 Cache) | Jika sudah pernah → **Skip** |
| 3 | **🔍 REGEX PARSER** | Parsing cepat menggunakan pattern |
| 3a | ↳ Deteksi Simbol | Pattern: `[A-Z0-9.]{3,}` (contoh: XAUUSD, EURUSD) |
| 3b | ↳ Deteksi Tipe | Kata kunci: BUY, SELL, LONG, SHORT, BULLISH, BEARISH |
| 3c | ↳ Deteksi Entry | Pattern: ENTRY/CMP/PRICE/AT/@ diikuti angka |
| 3d | ↳ Deteksi SL | Pattern: SL/STOPLOSS/STOP diikuti angka |
| 3e | ↳ Deteksi TP | Pattern: TP/TP1/TAKEPROFIT diikuti angka |
| 4 | Cek kelengkapan | Harus ada: Symbol + Type + Entry + SL + TP |
| 5 | **🧠 AI PARSER** (jika regex gagal) | Kirim prompt ke AI Waterfall |
| 5a | ↳ Coba Groq API | Provider utama |
| 5b | ↳ Coba Cloudflare | Fallback pertama |
| 5c | ↳ Coba OpenRouter | Fallback kedua |
| 6 | Parse JSON response AI | Ekstrak {symbol, type, entry, tp, sl} |
| 7 | Kirim ke GUI / Eksekusi langsung | Tergantung ada callback atau tidak |

```
Alur Singkat:

  📨 Pesan ──▶ Teks Kosong? ──▶ Duplikat? ──▶ REGEX PARSER
                                                    │
                                         ┌──────────┴──────────┐
                                     Berhasil              Gagal
                                         │                     │
                                         ▼                     ▼
                                   Signal Object         🧠 AI PARSER
                                   {symbol, type,      Groq → CF → OR
                                    entry, tp, sl}          │
                                         │            Berhasil/Gagal
                                         │                 │
                                         ▼                 ▼
                                    GUI Callback      Signal / Skip
```

### 🔗 Diagram Mermaid (untuk renderer)

```mermaid
flowchart TD
    MSG(["📨 Pesan Masuk<br/>dari Telegram Channel"]) --> CHECK_TEXT{"Teks Kosong?"}
    CHECK_TEXT -->|"Ya"| SKIP["⏭️ Skip (Abaikan)"]
    CHECK_TEXT -->|"Tidak"| DEDUP{"Cek Duplikasi<br/>(MD5 Hash Cache)"}

    DEDUP -->|"Sudah Pernah"| SKIP
    DEDUP -->|"Baru"| CACHE_ADD["Tambah ke Signal Cache"]

    CACHE_ADD --> REGEX["🔍 TAHAP 1: Regex Parser"]

    subgraph "Regex Parser"
        REGEX --> DETECT_SYMBOL["Deteksi Simbol<br/>(Pattern: 3+ huruf kapital)"]
        DETECT_SYMBOL --> DETECT_TYPE["Deteksi Tipe<br/>(BUY/SELL/LONG/SHORT)"]
        DETECT_TYPE --> DETECT_ENTRY["Deteksi Entry Price<br/>(ENTRY/CMP/PRICE/AT/@)"]
        DETECT_ENTRY --> DETECT_SL["Deteksi Stop Loss<br/>(SL/STOPLOSS/STOP)"]
        DETECT_SL --> DETECT_TP["Deteksi Take Profit<br/>(TP/TP1/TAKEPROFIT)"]
    end

    DETECT_TP --> REGEX_OK{"Semua Data<br/>Terdeteksi?"}
    REGEX_OK -->|"✅ Ya"| SIGNAL_OUT["📊 Signal Object:<br/>{symbol, type, entry, tp, sl}"]

    REGEX_OK -->|"❌ Tidak Lengkap"| AI_CHECK{"API Key AI<br/>Tersedia?"}
    AI_CHECK -->|"Tidak"| NO_SIGNAL["❌ Bukan Sinyal Trading"]
    AI_CHECK -->|"Ya"| AI_PARSE["🧠 TAHAP 2: AI Parser"]

    subgraph "AI Parser (Waterfall)"
        AI_PARSE --> AI_PROMPT["Kirim Prompt ke AI:<br/>'Extract signal as JSON'"]
        AI_PROMPT --> AI_GROQ["Coba Groq API"]
        AI_GROQ -->|"Gagal"| AI_CF["Coba Cloudflare"]
        AI_CF -->|"Gagal"| AI_OR["Coba OpenRouter"]
        AI_GROQ -->|"Berhasil"| AI_JSON["Parse JSON Response"]
        AI_CF -->|"Berhasil"| AI_JSON
        AI_OR -->|"Berhasil"| AI_JSON
    end

    AI_JSON -->|"✅ Valid"| SIGNAL_OUT
    AI_JSON -->|"❌ Invalid"| NO_SIGNAL

    SIGNAL_OUT --> CALLBACK{"Signal Callback<br/>Terdaftar?"}
    CALLBACK -->|"Ya (GUI)"| TO_GUI["Kirim ke GUI<br/>(on_signal_detected)"]
    CALLBACK -->|"Tidak"| DIRECT_EXEC["Eksekusi Langsung<br/>(execute_trade)"]

    style MSG fill:#0088cc,color:#fff
    style REGEX fill:#a855f7,color:#fff
    style AI_PARSE fill:#06b6d4,color:#fff
    style SIGNAL_OUT fill:#10b981,color:#fff
    style NO_SIGNAL fill:#f85149,color:#fff
```

---

## 4. Alur Eksekusi Trade di MT5

Setelah sinyal berhasil di-parse, sistem menjalankan serangkaian pemeriksaan keamanan sebelum mengirim order ke MetaTrader 5.

### 📋 Visual: Langkah Eksekusi Trade

| Step | Proses | Lolos ✅ | Ditolak ❌ |
|------|--------|---------|-----------|
| 1 | ⏰ **Filter Waktu** | Dalam jam trading | Di luar jam → Blokir |
| 2 | 💰 **Equity Guard** | Drawdown < batas | Drawdown ≥ limit → Blokir |
| 3 | 🎫 **Tier Limit** | Kuota tersedia | Standard: max 5/hari → Blokir |
| 4 | 🔌 **Init MT5** | Login berhasil | Gagal → Retry 1x → Blokir |
| 5 | 🔍 **Cek Simbol** | Symbol + Suffix ada | Tidak ditemukan → Blokir |
| 6 | 📐 **Hitung Lot** | Fixed/Dynamic | — |
| 7 | 📝 **Bangun Order** | Action, Price, SL, TP, Magic | — |
| 8 | 📤 **Kirim Order** | `TRADE_RETCODE_DONE` | Error → Log gagal |
| 9 | ✅ **Pasca-Eksekusi** | Log CSV + Supabase + Notif | — |

```
Alur Guard (3 Lapisan):

  📊 Signal ──▶ ⏰ Jam OK? ──▶ 💰 Equity OK? ──▶ 🎫 Kuota OK?
                   │                │                   │
                   ❌               ❌                  ❌
              "Di Luar Jam"   "Loss Limit"        "Kuota Habis"

  Jika semua ✅ lolos:

  🔌 Init MT5 ──▶ 🔍 Cek Simbol ──▶ 📐 Hitung Lot ──▶ 📤 Order
                                                           │
                                                  ┌────────┴────────┐
                                               Berhasil           Gagal
                                                  │                 │
                                            ┌─────┴─────┐     Log Error
                                            │           │
                                         📝 CSV    ☁️ Supabase
                                                        │
                                                   📨 Notif TG
```

### 📐 Detail Kalkulasi Lot

| Mode | Rumus | Keterangan |
|------|-------|------------|
| **Fixed Lot** | `FIXED_LOT` dari config | Langsung digunakan |
| **Dynamic** | `Risk = Balance × (Risk% / 100)` | Hitung uang yang siap dirisikokan |
| | `SL Points = │Entry - SL│ / Point` | Hitung jarak SL dalam poin |
| | `Lot = Risk / (SL Points × 0.1)` | Minimum: 0.01, pembulatan 2 desimal |

### 🔗 Diagram Mermaid (untuk renderer)

```mermaid
flowchart TD
    SIG(["📊 Signal Diterima"]) --> TIME_CHECK{"⏰ Filter Waktu<br/>Dalam Jam Trading?"}
    TIME_CHECK -->|"❌ Di Luar Jam"| BLOCK_TIME["🚫 Ditolak:<br/>Di Luar Jam Trading"]
    TIME_CHECK -->|"✅ Dalam Jam"| EQUITY_CHECK{"💰 Equity Guard<br/>Drawdown < Batas?"}

    EQUITY_CHECK -->|"❌ Melebihi Batas"| BLOCK_EQUITY["🚫 Ditolak:<br/>Daily Loss Limit Tercapai"]
    EQUITY_CHECK -->|"✅ Aman"| TIER_CHECK{"🎫 Cek Limit Tier<br/>Trade Harian < Kuota?"}

    TIER_CHECK -->|"❌ Kuota Habis"| BLOCK_TIER["🚫 Ditolak:<br/>Batas Trade Harian Tercapai<br/>(Saran: Upgrade Tier)"]
    TIER_CHECK -->|"✅ Masih Tersedia"| MT5_INIT{"🔌 Inisialisasi MT5<br/>Login + Password + Server"}

    MT5_INIT -->|"❌ Gagal"| MT5_RETRY["🔄 Reconnect (1 detik)"]
    MT5_RETRY -->|"❌ Masih Gagal"| BLOCK_MT5["🚫 MT5 Tidak Tersedia"]
    MT5_RETRY -->|"✅ Berhasil"| SYMBOL_CHECK
    MT5_INIT -->|"✅ Berhasil"| SYMBOL_CHECK{"🔍 Cek Simbol<br/>+ Suffix Broker"}

    SYMBOL_CHECK -->|"❌ Tidak Ditemukan"| BLOCK_SYMBOL["🚫 Simbol Tidak Tersedia<br/>di Broker"]
    SYMBOL_CHECK -->|"✅ Ditemukan"| LOT_CALC["📐 Kalkulasi Lot"]

    subgraph "Kalkulasi Lot"
        LOT_CALC --> LOT_TYPE{"Fixed Lot<br/>Diatur?"}
        LOT_TYPE -->|"Ya"| USE_FIXED["Gunakan Fixed Lot<br/>(dari konfigurasi)"]
        LOT_TYPE -->|"Tidak"| CALC_RISK["Hitung Dinamis:<br/>Risk = Balance × Risk%<br/>Lot = Risk ÷ (SL Points × 0.1)<br/>Min: 0.01"]
    end

    USE_FIXED --> BUILD_ORDER
    CALC_RISK --> BUILD_ORDER["📝 Bangun Order Request"]

    subgraph "Order Request"
        BUILD_ORDER --> SET_ACTION["Action: DEAL (Market)"]
        SET_ACTION --> SET_PRICE["Price: ASK (Buy) / BID (Sell)"]
        SET_PRICE --> SET_SLTP["SL & TP dari Sinyal"]
        SET_SLTP --> SET_MAGIC["Magic Number: ITC Identifier"]
        SET_MAGIC --> SET_FILL["Filling Mode:<br/>IOC → FOK → RETURN"]
    end

    SET_FILL --> SEND_ORDER["📤 Kirim Order ke MT5"]
    SEND_ORDER --> RESULT{"Hasil Order?"}

    RESULT -->|"❌ Error"| LOG_ERR["Log Error: {comment}"]
    RESULT -->|"✅ EXECUTED"| SUCCESS["✅ Trade Berhasil!"]

    SUCCESS --> LOG_TRADE["📝 Log ke CSV"]
    SUCCESS --> PUSH_DB["☁️ Push ke Supabase"]
    SUCCESS --> NOTIFY["📨 Notifikasi Telegram"]

    style SIG fill:#0088cc,color:#fff
    style BLOCK_TIME fill:#f85149,color:#fff
    style BLOCK_EQUITY fill:#f85149,color:#fff
    style BLOCK_TIER fill:#d29922,color:#000
    style BLOCK_MT5 fill:#f85149,color:#fff
    style BLOCK_SYMBOL fill:#f85149,color:#fff
    style SUCCESS fill:#10b981,color:#fff
```

---

## 5. Alur Autentikasi Telegram (In-App OTP Login)

Proses login Telegram langsung dari dalam aplikasi tanpa konfigurasi manual.

### 📋 Visual: 7 Langkah Autentikasi

| Step | Proses | Kemungkinan Hasil |
|------|--------|-------------------|
| 0 | 🔐 User klik **Test Connection** | Jika sudah berjalan → ⚠️ |
| 1 | 🔌 **Connect** ke Telegram Server | ✅ Terhubung / ❌ Timeout / ❌ API Invalid |
| 2 | 🔍 **Cek Session Lama** (`get_me()`) | ✅ Session valid → Login otomatis! |
| | | ❌ Expired → Hapus session, buat ulang |
| 3 | 📱 **Ambil Nomor HP** | Dari UI / popup / env fallback |
| | | Format: `0812...` → `+62812...` (otomatis) |
| 4 | 📨 **Kirim OTP** (`send_code`) | ✅ Kode dikirim ke HP |
| | | ❌ API Invalid → Error |
| 5 | 🔢 **Input OTP** (popup di aplikasi) | User ketik kode dari Telegram |
| 6 | 🔐 **Sign In** | ✅ Berhasil → Session tersimpan |
| | | ❌ Kode salah / kedaluwarsa |
| | | 🔒 **2FA diperlukan** → lanjut Step 7 |
| 7 | 🔒 **2FA Password** (jika aktif) | ✅ Password benar → Login berhasil |
| | | ❌ Password salah |

```
Alur Singkat:

  🔐 Test ──▶ 🔌 Connect ──▶ 🔍 Session Valid?
                                    │
                          ┌─────────┴─────────┐
                         ✅ Ya              ❌ Tidak
                          │                    │
                    Login Otomatis!      📱 Input Phone
                                               │
                                         📨 Kirim OTP
                                               │
                                         🔢 Input OTP
                                               │
                                    ┌──────────┴──────────┐
                                 ✅ OK              🔒 Perlu 2FA
                                    │                     │
                              Login Berhasil!       Input Password
                                                          │
                                                    Login 2FA!
```

### 🔗 Diagram Mermaid (untuk renderer)

```mermaid
flowchart TD
    TEST(["🔐 User Klik Test Connection"]) --> GUARD{"Sudah Dalam<br/>Proses Test?"}
    GUARD -->|"Ya"| WARN["⚠️ Test Sedang Berjalan"]
    GUARD -->|"Tidak"| SET_TEST["Set _tg_testing = True"]

    SET_TEST --> READ_UI["Baca Nilai dari UI:<br/>API ID, API Hash, Phone"]
    READ_UI --> CREATE["Buat Pyrogram Client"]

    CREATE -->|"❌ Gagal"| ERR_CONFIG["❌ API ID/Hash Missing"]
    CREATE -->|"✅ Berhasil"| CONNECT["🔌 Step 1: Connect<br/>(Timeout 15 detik)"]

    CONNECT -->|"Timeout"| ERR_NET["❌ Connection Timeout"]
    CONNECT -->|"ApiIdInvalid"| ERR_API["❌ API ID/Hash Salah"]
    CONNECT -->|"✅ Terhubung"| CHECK_SESSION["🔍 Step 2: Cek Session Lama<br/>(get_me)"]

    CHECK_SESSION -->|"✅ Session Valid"| SUCCESS_EXISTING["✅ Login Otomatis!<br/>(Session Tersimpan)"]
    CHECK_SESSION -->|"Session Expired"| DELETE_SESSION["🗑️ Hapus Session Lama"]

    DELETE_SESSION --> RECREATE["Buat Ulang Client"]
    CHECK_SESSION -->|"Belum Login"| ASK_PHONE

    RECREATE --> ASK_PHONE{"📱 Step 3: Nomor HP<br/>Sudah Diisi?"}
    ASK_PHONE -->|"Tidak"| POPUP_PHONE["💬 Tampilkan Popup:<br/>'Masukkan Nomor HP'"]
    POPUP_PHONE --> NORMALIZE["Normalisasi Format<br/>(0812... → +62812...)"]
    ASK_PHONE -->|"Ya"| NORMALIZE

    NORMALIZE --> SEND_OTP["📨 Step 4: Kirim OTP<br/>(send_code)"]
    SEND_OTP -->|"ApiIdInvalid"| ERR_API
    SEND_OTP -->|"✅ OTP Terkirim"| POPUP_OTP["💬 Step 5: Popup OTP<br/>'Masukkan Kode Verifikasi'"]

    POPUP_OTP --> SIGN_IN["🔐 Step 6: Sign In<br/>(phone + hash + OTP)"]

    SIGN_IN -->|"✅ Berhasil"| SUCCESS_NEW["✅ Login Berhasil!<br/>Session Tersimpan"]
    SIGN_IN -->|"PhoneCodeInvalid"| ERR_OTP["❌ Kode OTP Salah"]
    SIGN_IN -->|"PhoneCodeExpired"| ERR_EXPIRED["❌ OTP Kedaluwarsa"]
    SIGN_IN -->|"SessionPasswordNeeded"| ASK_2FA["🔒 Step 7: Popup 2FA<br/>'Masukkan Password Telegram'"]

    ASK_2FA --> CHECK_2FA["Verifikasi Password 2FA"]
    CHECK_2FA -->|"✅ Benar"| SUCCESS_2FA["✅ Login 2FA Berhasil!"]
    CHECK_2FA -->|"❌ Salah"| ERR_2FA["❌ Password 2FA Salah"]

    SUCCESS_EXISTING --> CLEANUP["🧹 Disconnect Client<br/>Simpan Session File"]
    SUCCESS_NEW --> CLEANUP
    SUCCESS_2FA --> CLEANUP

    CLEANUP --> UPDATE_UI["🎨 Update Status UI:<br/>● Validated (Nama)"]

    style TEST fill:#6366f1,color:#fff
    style SUCCESS_EXISTING fill:#10b981,color:#fff
    style SUCCESS_NEW fill:#10b981,color:#fff
    style SUCCESS_2FA fill:#10b981,color:#fff
    style ERR_CONFIG fill:#f85149,color:#fff
    style ERR_API fill:#f85149,color:#fff
    style ERR_OTP fill:#f85149,color:#fff
    style ASK_2FA fill:#d29922,color:#000
```

---

## 6. Alur Monitor & Broadcaster (VIP)

Background loop yang memantau posisi terbuka dan menyiarkan trade baru ke Telegram (fitur VIP).

### 📋 Visual: Siklus Monitor

| Step | Proses | Keterangan |
|------|--------|------------|
| 1 | 🔌 Cek MT5 Service | Jika tidak aktif → sleep 1 detik, coba lagi |
| 2 | 📊 Ambil posisi terbuka | Semua posisi dari `get_positions()` |
| 3 | 📡 Cek mode Broadcaster | `SPC_MODE == "BROADCAST"` (VIP only) |
| 4 | 🔄 Loop setiap posisi | Periksa satu per satu |
| 5 | 🔍 Cek cache ticket | Sudah pernah dikirim? → Skip |
| 6 | 📤 Kirim via BridgeController | Bot Token + Chat ID → Telegram |
| 7 | ✅ Tambah ke cache | Mencegah pengiriman ganda |
| 8 | 🧹 Bersihkan cache | Jika > 1000 → trim ke 100 terakhir |
| 9 | ⏰ Sleep 2 detik | Kembali ke Step 1 |

```
Loop Tanpa Henti:

  ┌──────────────────────────────────────────────────┐
  │                                                  │
  ▼                                                  │
  🔌 MT5 Aktif? ──No──▶ Sleep 1s ───────────────────┤
  │ Yes                                              │
  ▼                                                  │
  📊 Ambil Posisi ──▶ 📡 Broadcaster ON? ──No──▶ Sleep 2s
  │ Yes                                              │
  ▼                                                  │
  🔄 Loop Posisi ──▶ Cached? ──Yes──▶ Next ─────────┤
  │ No (Baru)                                        │
  ▼                                                  │
  📤 Kirim ke TG ──▶ ✅ Cache ──▶ Sleep 2s ─────────┘
```

### 🔗 Diagram Mermaid (untuk renderer)

```mermaid
flowchart TD
    START(["🔁 monitor_trades()<br/>Loop Setiap 2 Detik"]) --> INIT_MT5{"MT5 Service<br/>Aktif?"}
    INIT_MT5 -->|"Tidak"| SLEEP_ERR["Sleep 1 detik<br/>→ Coba Lagi"]
    INIT_MT5 -->|"Ya"| GET_POS["Ambil Semua Posisi<br/>Terbuka di MT5"]

    GET_POS --> CHECK_BC{"Mode Broadcaster<br/>Aktif? (VIP)"}
    CHECK_BC -->|"Tidak"| SKIP_BC["Skip Broadcasting"]
    CHECK_BC -->|"Ya"| LOOP_POS["Loop Setiap Posisi"]

    LOOP_POS --> CHECK_CACHE{"Ticket Sudah<br/>Pernah Dikirim?"}
    CHECK_CACHE -->|"Ya (Cached)"| NEXT_POS["Posisi Berikutnya"]
    CHECK_CACHE -->|"Tidak (Baru)"| FORMAT["Format Sinyal:<br/>Symbol, Type, Entry, SL, TP"]

    FORMAT --> RELAY["📤 Kirim via BridgeController<br/>(Bot Token + Chat ID)"]
    RELAY -->|"✅ Berhasil"| ADD_CACHE["Tambah Ticket ke Cache"]
    RELAY -->|"❌ Gagal"| NEXT_POS

    ADD_CACHE --> NEXT_POS
    NEXT_POS --> CACHE_CLEAN{"Cache > 1000?"}
    CACHE_CLEAN -->|"Ya"| TRIM["Trim: Simpan 100 Terakhir"]
    CACHE_CLEAN -->|"Tidak"| SLEEP["⏰ Sleep 2 Detik"]
    TRIM --> SLEEP
    SKIP_BC --> SLEEP

    SLEEP --> INIT_MT5

    style START fill:#6366f1,color:#fff
    style RELAY fill:#0088cc,color:#fff
    style FORMAT fill:#10b981,color:#fff
```

---

## 7. Sistem Keamanan (Guard System)

Tiga lapisan pelindung yang mencegah eksekusi trade dalam kondisi berisiko.

### 📋 Visual: 3 Lapisan Pelindung

| Layer | Guard | Fungsi | Rumus / Logika | Aksi Jika Gagal |
|-------|-------|--------|----------------|-----------------|
| 🔶 1 | ⏰ **Filter Waktu** | Cek jam trading | `TRADE_START_HOUR <= jam_sekarang < TRADE_END_HOUR` | 🚫 Trade diblokir |
| 🔴 2 | 💰 **Equity Guard** | Cek batas kerugian | `DD = (Balance - Equity) / Balance × 100` | 🚫 Trade diblokir jika DD ≥ `DAILY_LOSS_LIMIT` |
| 🟣 3 | 🎫 **Tier Limit** | Cek kuota harian | `trade_hari_ini >= limit_tier?` | 🚫 Blokir + saran upgrade |

**Kuota per Tier:**

| Tier | Batas Trade Harian |
|------|-------------------|
| STANDARD | 5 trade / hari |
| GOLD | Unlimited |
| PRO | Unlimited |

```
Pipeline Guard:

  📊 Sinyal ──▶ [ ⏰ Layer 1 ] ──▶ [ 💰 Layer 2 ] ──▶ [ 🎫 Layer 3 ] ──▶ ✅ Eksekusi
                     │                    │                    │
                     ❌                   ❌                   ❌
                 "Di Luar Jam"       "Loss Limit"        "Kuota Habis"
```

### 🔗 Diagram Mermaid (untuk renderer)

```mermaid
flowchart LR
    subgraph "Layer 1"
        T["⏰ Filter Waktu"]
        T_DESC["Cek apakah dalam<br/>jam trading yang diizinkan<br/>(TRADE_START_HOUR - TRADE_END_HOUR)"]
    end

    subgraph "Layer 2"
        E["💰 Equity Guard"]
        E_DESC["Hitung drawdown:<br/>(Balance - Equity) ÷ Balance × 100<br/>Tolak jika ≥ DAILY_LOSS_LIMIT"]
    end

    subgraph "Layer 3"
        L["🎫 Tier Limit"]
        L_DESC["Cek kuota trade harian<br/>berdasarkan tier user:<br/>STANDARD: 5x/hari<br/>GOLD/PRO: Unlimited"]
    end

    T --> E --> L

    style T fill:#f59e0b,color:#000
    style E fill:#ef4444,color:#fff
    style L fill:#a855f7,color:#fff
```

---

## 8. Siklus Hidup Client Telegram

### 📋 Visual: Tabel Transisi Status

| Status Awal | Aksi / Event | Status Baru | Keterangan |
|-------------|-------------|-------------|------------|
| **Idle** | Klik Test Connection | **Testing** | Mulai uji koneksi |
| **Testing** | ✅ Session valid / OTP berhasil | **Validated** | Siap untuk start |
| **Testing** | ❌ Auth gagal | **Failed** | Kembali ke idle |
| **Failed** | Reset otomatis | **Idle** | Bisa coba lagi |
| **Validated** | Klik START COPIER | **Running** | Client aktif |
| **Running** | Client terhubung | **Listening** | Mendengarkan sinyal |
| **Listening** | Loop 1 detik | **Listening** | Terus berjalan |
| **Listening** | Klik STOP COPIER | **Stopping** | Memulai shutdown |
| **Running** | Exception terjadi | **Error** | Crash handling |
| **Stopping** | `client.stop()` selesai | **Disconnected** | Client bersih |
| **Error** | Cleanup selesai | **Disconnected** | Otomatis cleanup |
| **Disconnected** | Reset flag | **Idle** | Kembali ke awal |
| **Validated** | Tidak jadi start | **Idle** | User batal |

```
Diagram Status:

  ┌────────────────────────────────────────────────────────────┐
  │                                                            │
  │   ┌──────┐  Test   ┌─────────┐  ✅   ┌───────────┐       │
  │   │ IDLE │───────▶│ TESTING │──────▶│ VALIDATED │       │
  │   └──┬───┘         └────┬────┘       └─────┬─────┘       │
  │      ▲                  │ ❌                │ START        │
  │      │            ┌─────▼─────┐             │             │
  │      │            │  FAILED   │             │             │
  │      │            └───────────┘             ▼             │
  │      │                              ┌───────────┐         │
  │      │                              │  RUNNING  │         │
  │      │                              └─────┬─────┘         │
  │      │                                    │               │
  │      │                              ┌─────▼─────┐         │
  │      │           STOP ◀────────────│ LISTENING │◀──┐     │
  │      │             │                └───────────┘   │     │
  │      │             ▼                    loop 1s ────┘     │
  │      │     ┌───────────┐                                  │
  │      │     │ STOPPING  │                                  │
  │      │     └─────┬─────┘                                  │
  │      │           │                                        │
  │      │     ┌─────▼────────┐                               │
  │      └─────│ DISCONNECTED │                               │
  │            └──────────────┘                               │
  └────────────────────────────────────────────────────────────┘
```

### 🔗 Diagram Mermaid (untuk renderer)

```mermaid
stateDiagram-v2
    [*] --> Idle: Aplikasi Dibuka

    Idle --> Testing: Klik Test Connection
    Testing --> Validated: ✅ Session Valid / OTP Berhasil
    Testing --> Failed: ❌ Auth Gagal
    Failed --> Idle: Reset

    Validated --> Running: Klik START COPIER
    Running --> Listening: 📡 Mendengarkan Sinyal
    Listening --> Listening: Loop (1 detik)

    Listening --> Stopping: Klik STOP COPIER
    Stopping --> Disconnected: client.stop()
    Disconnected --> Idle: Reset Flag

    Running --> Error: Exception
    Error --> Disconnected: Cleanup

    Validated --> Idle: Tidak Jadi Start
```

---

## 9. Ringkasan File & Tanggung Jawab

| File | Tanggung Jawab |
|------|---------------|
| `src/index.py` | Core engine: `create_telegram_client()`, `parse_signal()`, `ai_parse_signal()`, `execute_trade()`, `monitor_trades()` |
| `src/modules/logic/copier_controller.py` | Lifecycle management: `start_copier()`, `run_telegram()`, `test_telegram()`, `emergency_close()` |
| `src/modules/logic/config_aggregator.py` | Konfigurasi terpusat: kumpulkan semua env vars untuk eksekusi |
| `src/modules/logic/settings_manager.py` | Simpan/muat konfigurasi user ke `.env` |
| `src/modules/mt5/mt5_service.py` | Singleton MT5 service: inisialisasi, order, posisi, info akun |
| `src/modules/ai/smart_fill.py` | AI Waterfall: Groq → Cloudflare → OpenRouter |
| `src/modules/ui/telegram_view.py` | UI input: API ID, API Hash, Phone, Channels |

---

## 10. Glossary

| Istilah | Penjelasan |
|---------|-----------|
| **Pyrogram** | Library Python untuk mengakses Telegram API (MTProto) |
| **Signal** | Sinyal trading berisi: Symbol, Type (Buy/Sell), Entry, SL, TP |
| **Regex Parser** | Parsing cepat menggunakan pola/pattern text |
| **AI Parser** | Parsing lanjutan menggunakan AI jika regex gagal |
| **Equity Guard** | Pelindung yang menolak trade jika kerugian melebihi batas |
| **Magic Number** | Identifikasi unik untuk trade yang dibuat oleh ITC |
| **Broadcast Cache** | Cache mencegah pengiriman duplikat sinyal ke Telegram |
| **Session File** | File `itc_copier_session.session` menyimpan login Telegram |
| **Waterfall** | Strategi fallback: coba provider AI satu per satu |
| **IOC/FOK/RETURN** | Mode pengisian order MT5 (tergantung broker) |

---

*Dokumen ini dihasilkan berdasarkan analisis kode sumber ITC +AI v4.9.5*
*© 2026 ITC - Intelligence Telegram CopyTrade*
