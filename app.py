import streamlit as st
import pandas as pd
import database as db

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Stok Atribut UBS PPNI",
    page_icon="📦",
    layout="wide"
)

# Inisialisasi Database
db.init_db()

st.title("📦 Sistem Stok Atribut Mahasiswa UBS PPNI")
st.caption("Pencatatan & Pemantauan Stok Atribut Kemakmuran Mahasiswa")

# Sidebar Navigation
menu = st.sidebar.radio("Navigasi Menu", ["📝 Form Transaksi Stok", "📊 Dashboard Data Stok", "➕ Tambah Master Barang"])

# ==========================================
# MENU 1: FORM TRANSAKSI (INPUT / OUTPUT)
# ==========================================
if menu == "📝 Form Transaksi Stok":
    st.subheader("Pencatatan Mutasi Barang")
    
    # Ambil data master barang untuk dropdown
    df_barang = db.get_master_barang()
    
    if df_barang.empty:
        st.warning("Belum ada data barang di sistem. Silakan tambah barang di menu 'Tambah Master Barang' terlebih dahulu.")
    else:
        # Topbar Switch Toggle Mode
        col_title, col_switch = st.columns([3, 1])
        with col_switch:
            mode_transaksi = st.radio("Tipe Transaksi:", ["🟢 BARANG MASUK", "🔴 BARANG KELUAR"], horizontal=True)
        
        tipe = "MASUK" if "MASUK" in mode_transaksi else "KELUAR"
        
        st.markdown("---")
        st.write(f"### Form Opsi: **{mode_transaksi}**")
        
        with st.form("form_mutasi"):
            # Format Pilihan Dropdown: Kode - Nama (Ukuran)
            opsi_barang = df_barang.apply(lambda x: f"{x['kode_barang']} - {x['nama_barang']} ({x['ukuran']}) | Stok: {x['stok_sekarang']}", axis=1)
            pilihan = st.selectbox("Pilih Atribut Barang", opsi_barang)
            
            kode_terpilih = pilihan.split(" - ")[0]
            
            col1, col2 = st.columns(2)
            with col1:
                jumlah = st.number_input("Jumlah (Qty)", min_value=1, step=1)
            with col2:
                label_penerima = "Nama Suplier / Vendor" if tipe == "MASUK" else "Penerima / Mahasiswa / Angkatan"
                penerima = st.text_input(label_penerima)
                
            keterangan = st.text_area("Keterangan Tambahan", placeholder="Contoh: Pengadaan Gelombang 1 / Rusak / Tukar Ukuran")
            
            submit = st.form_submit_button("Simpan Transaksi")
            
            if submit:
                db.catat_transaksi(kode_terpilih, tipe, jumlah, penerima, keterangan)
                st.success(f"Berhasil mencatat transaksi {tipe} sebanyak {jumlah} pcs!")
                st.rerun()

# ==========================================
# MENU 2: DASHBOARD DATA STOK (READ-ONLY)
# ==========================================
elif menu == "📊 Dashboard Data Stok":
    st.subheader("Ketersediaan Stok Atribut Real-Time")
    
    df_stok = db.get_master_barang()
    
    if df_stok.empty:
        st.info("Data stok masih kosong.")
    else:
        # Ringkasan Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Jenis Atribut", len(df_stok))
        col2.metric("Total Item Tersedia", int(df_stok['stok_sekarang'].sum()))
        stok_kritis = len(df_stok[df_stok['stok_sekarang'] <= df_stok['stok_min']])
        col3.metric("Peringatan Stok Kritis", stok_kritis, delta_color="inverse")
        
        st.markdown("---")
        
        # Filter Kategori
        kategori_list = ["Semua"] + list(df_stok['kategori'].unique())
        kat_pilihan = st.selectbox("Filter Kategori Barang", kategori_list)
        
        if kat_pilihan != "Semua":
            df_display = df_stok[df_stok['kategori'] == kat_pilihan]
        else:
            df_display = df_stok.copy()
            
        # Indikator Status Warna
        def status_stok(row):
            if row['stok_sekarang'] <= 0:
                return "🔴 Habis"
            elif row['stok_sekarang'] <= row['stok_min']:
                return "🟡 Menipis"
            else:
                return "🟢 Aman"
                
        df_display['Status'] = df_display.apply(status_stok, axis=1)
        
        # Tampilkan Tabel Read-Only
        st.dataframe(
            df_display[['kode_barang', 'nama_barang', 'kategori', 'ukuran', 'harga', 'stok_sekarang', 'Status', 'deskripsi']],
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# MENU 3: TAMBAH MASTER BARANG
# ==========================================
elif menu == "➕ Tambah Master Barang":
    st.subheader("Tambah Jenis Atribut Baru")
    
    with st.form("form_master"):
        col1, col2 = st.columns(2)
        with col1:
            kode = st.text_input("Kode Barang (Unik)", placeholder="Contoh: JAS-ALMA-L")
            nama = st.text_input("Nama Atribut", placeholder="Contoh: Jas Almamater UBS PPNI")
            kategori = st.selectbox("Kategori", ["Seragam", "Aksesoris", "Baju Praktek", "Atribut Khusus"])
        with col2:
            ukuran = st.selectbox("Ukuran", ["S", "M", "L", "XL", "XXL", "All Size"])
            harga = st.number_input("Harga Satuan (Rp)", min_value=0, step=1000)
            stok_min = st.number_input("Batas Stok Minimum Alert", min_value=1, value=5)
            
        deskripsi = st.text_area("Deskripsi Singkat")
        
        btn_tambah = st.form_submit_button("Tambah Master Barang")
        
        if btn_tambah:
            if not kode or not nama:
                st.error("Kode Barang dan Nama Atribut wajib diisi!")
            else:
                sukses, pesan = db.tambah_barang_baru(kode, nama, kategori, ukuran, harga, stok_min, deskripsi)
                if sukses:
                    st.success(pesan)
                else:
                    st.error(pesan)
