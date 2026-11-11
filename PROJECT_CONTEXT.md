# BELOVE APP — PROJECT CONTEXT

## 1. Overview
Sistem manajemen pemesanan kaos, sablon, dan konveksi. Customer melihat katalog di WEB, memesan dan berkonsultasi via **WhatsApp** (bot + admin). Admin mengelola semua lewat panel web.

## 2. Keputusan Teknis (jangan diubah tanpa persetujuan)
- Frontend: React + Vite + TypeScript, React Router, TanStack Query (Tailwind ditambah di Tahap 4).
- Backend: FastAPI + SQLAlchemy 2.0 + Alembic + Pydantic v2. Modular monolith.
- Database: PostgreSQL 16. Uang = integer Rupiah.
- Docker Compose (dev & prod). Prod: Nginx serve React + proxy /api (satu origin).
- WhatsApp: **Meta Cloud API resmi**, webhook ke FastAPI. Tanpa Celery/Redis (pakai BackgroundTasks).
- Bot: rule-based (menu, FAQ, cek status, handoff ke admin). AI/LLM menyusul nanti.
- **Customer tanpa akun/login web**, diidentifikasi dari nomor WA (62xxx). Progres lewat WA + halaman publik `/track/{token}`.
- Auth hanya Admin/staff: JWT access 15 mnt + refresh 7 hari (cookie httpOnly), argon2, RBAC `require_role`. Admin dibuat via seed/CLI.
- Admin membalas chat lewat inbox di panel web (nomor Cloud API tidak dipakai bersamaan di app WA HP).
- Pembayaran: transfer manual, bukti dari WA, lunas satu invoice (tanpa DP/termin, tanpa gateway).
- Stok dicek saat invoice dibuat, dipotong saat Paid (transaksi, `SELECT FOR UPDATE`).
- Pengiriman: kurir & resi input manual. Email notifikasi tidak dipakai.

## 3. Roles
- **Admin**: produk/stok/harga, customer, order (input dari chat WA), cek DTF, invoice & receipt, konfirmasi pembayaran, produksi, pengiriman, inbox WA.
- **Customer** (via WA/web publik): lihat katalog, pesan & konsultasi via WA, setujui/revisi invoice lewat tombol WA, kirim bukti bayar, pantau progres via WA & /track.

## 4. Business Flow
Web katalog → "Pesan via WA" → WA (bot / handoff admin) → Admin input order → Invoice (PDF + tombol Setuju/Revisi via WA) → Revisi: invoice versi baru / Setuju → bukti bayar via WA → Admin konfirmasi (Paid) → Produksi (stock_receipt → patch_cutting → printing → folding_accessories → finishing → packing) → Shipped (resi via WA) → Completed. Setiap perubahan status memicu notifikasi WA.

## 5. Status Order
Pending, Waiting Approval, Revision, Approved, Waiting Payment, Paid, In Production, Finishing, Packing, Shipped, Completed, Cancelled.
Semua transisi lewat satu fungsi `change_status()` di `services/order_flow.py` (validasi transisi + role + catat `order_status_history`).

| Dari → Ke | Pemicu |
|---|---|
| Pending → Waiting Approval | Admin buat invoice |
| Waiting Approval → Approved/Revision | Customer (tombol WA) / admin catat manual |
| Revision → Waiting Approval | Admin kirim invoice versi baru |
| Approved → Waiting Payment | Customer kirim bukti bayar |
| Waiting Payment → Paid | Admin konfirmasi (stok dipotong, 6 langkah produksi dibuat) |
| Paid → In Production → Finishing → Packing | Admin update langkah produksi |
| Packing → Shipped → Completed | Admin isi resi → customer/admin |
| Pending..Paid → Cancelled | Admin |

## 6. Skema Database
users (admin only), customers, products, product_variants, stock_movements, orders (+public_token), order_items (snapshot harga), order_files (dtf_status), wa_conversations (mode bot/human, last_inbound_at), wa_messages (wa_msg_id unique), invoices (version per revisi), invoice_items, payments, production_steps, shipments, order_status_history.
Receipt = turunan payment confirmed (tanpa tabel). Produk soft-delete (`is_active`). Timestamp UTC.

## 7. API (`/api/v1`)
- Publik: `GET /health`, `GET /products`, `GET /track/{token}`
- Auth: `/auth/login|refresh|logout`, `GET /auth/me`
- Webhook: `GET|POST /webhook/wa` (signature `X-Hub-Signature-256`, idempotent)
- Admin: products/variants/stock, customers, orders (+files, DTF check), invoices (+pdf), payments (confirm/reject, receipt), production-steps, shipment/complete, conversations (list, messages, send, mode)

## 8. Struktur Folder
```
belove/
├─ docker-compose.yml, .env.example, PROJECT_CONTEXT.md
├─ backend/  Dockerfile, requirements.txt, alembic.ini, alembic/
│  └─ app/  main.py, core/(config, db, security, deps), models/, schemas/, routers/, services/(order_flow, stock, pdf, whatsapp, bot)
├─ frontend/ Dockerfile, vite.config.ts, src/(api, components, pages/{public,admin}, auth)
└─ uploads/  (volume, privat, disajikan via endpoint terotorisasi)
```

## 9. Keamanan
Verifikasi signature webhook; upload whitelist png/jpg/pdf + batas ukuran + nama UUID; file tidak static publik; rate limit login & webhook; `/track` tanpa data sensitif; secret hanya via env; error tanpa stack trace.

## 10. Tahapan & Progres
| # | Tahap | Status |
|---|---|---|
| 1 | Setup (Docker, FastAPI, React, Postgres, Alembic) | **Selesai (teruji Docker)** |
| 2 | Database & migrasi, seed admin | Selesai |
| 3 | Auth admin | Belum |
| 4 | Produk, stok, katalog publik + "Pesan via WA" | Belum |
| 5 | Customers & order, upload desain | Belum |
| 6 | WhatsApp: webhook, inbox, bot + handoff | Belum |
| 7 | Invoice & pembayaran | Belum |
| 8 | Produksi & notifikasi otomatis | Belum |
| 9 | Pengiriman, /track, Completed | Belum |
| 10 | Testing & deployment (docker-compose.prod.yml, Nginx, backup) | Belum |

## 11. Aturan Kerja
Plan first, build step by step, kode minimal, jangan overengineering, baca hanya file relevan, jangan tampilkan ulang kode yang tidak diminta, perbarui dokumen tiap perubahan penting.
