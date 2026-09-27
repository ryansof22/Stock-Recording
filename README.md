# Stock-Recording
# 📦 Sistem Stok Atribut Mahasiswa UBS PPNI

Aplikasi web berbasis Python dan Streamlit untuk pencatatan mutasi barang (inbound/outbound), pemantauan ketersediaan stok real-time, serta pelaporan riwayat atribut mahasiswa pada kemitraan pengadaan UBS PPNI Mojokerto.

---

## 🚀 Fitur Utama

- **📝 Form Transaksi Mutasi (In/Out):** Pencatatan barang masuk dari vendor dan barang keluar ke mahasiswa dengan fitur *switch toggle* yang intuitif.
- **📊 Dashboard Stok Real-Time:** Ringkasan metrik total ketersediaan barang, indikator status stok (🟢 Aman, 🟡 Menipis, 🔴 Habis), serta filter kategori.
- **📜 Riwayat Transaksi Lanjutan:** Pencatatan log terperinci mengenai pengirim (suplier) dan penerima (mahasiswa/angkatan) beserta timestamp otomatis.
- **📥 Ekspor Data (CSV):** Fitur unduh laporan data stok dan riwayat transaksi dalam format CSV untuk kebutuhan audit/laporan bulanan.

---

## 🛠️ Tech Stack & Alat

- **Bahasa Pemrograman:** Python 3.x
- **Framework Web:** Streamlit
- **Database:** SQLite3
- **Data Processing:** Pandas
- **Deployment:** Streamlit Community Cloud

---

## 📋 Struktur Repositori

```text
├── app.py              # File antarmuka utama Streamlit
├── database.py         # Skrip pengolahan database SQLite & query SQL
├── requirements.txt    # Daftar pustaka Python yang dibutuhkan
├── README.md           # Dokumentasi proyek
└── LICENSE             # Lisensi MIT
