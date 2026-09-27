import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "stok_atribut.db"

def init_db():
    """Membuat tabel master_barang dan transaksi_stok jika belum ada"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabel Master Barang
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_barang (
            kode_barang TEXT PRIMARY KEY,
            nama_barang TEXT NOT NULL,
            kategori TEXT NOT NULL,
            ukuran TEXT NOT NULL,
            harga REAL DEFAULT 0,
            stok_min INTEGER DEFAULT 5,
            deskripsi TEXT
        )
    ''')
    
    # Tabel Transaksi (Barang Masuk / Keluar)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi_stok (
            id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            kode_barang TEXT NOT NULL,
            tipe_transaksi TEXT NOT NULL, -- 'MASUK' atau 'KELUAR'
            jumlah INTEGER NOT NULL,
            penerima_suplier TEXT,
            keterangan TEXT,
            FOREIGN KEY (kode_barang) REFERENCES master_barang (kode_barang)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_master_barang():
    """Mengambil semua data barang beserta sisa stok real-time"""
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT 
            m.kode_barang,
            m.nama_barang,
            m.kategori,
            m.ukuran,
            m.harga,
            m.stok_min,
            COALESCE(SUM(CASE WHEN t.tipe_transaksi = 'MASUK' THEN t.jumlah ELSE 0 END), 0) -
            COALESCE(SUM(CASE WHEN t.tipe_transaksi = 'KELUAR' THEN t.jumlah ELSE 0 END), 0) AS stok_sekarang,
            m.deskripsi
        FROM master_barang m
        LEFT JOIN transaksi_stok t ON m.kode_barang = t.kode_barang
        GROUP BY m.kode_barang
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def tambah_barang_baru(kode, nama, kategori, ukuran, harga, stok_min, deskripsi):
    """Menambahkan master barang baru"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO master_barang (kode_barang, nama_barang, kategori, ukuran, harga, stok_min, deskripsi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (kode, nama, kategori, ukuran, harga, stok_min, deskripsi))
        conn.commit()
        return True, "Barang berhasil ditambahkan!"
    except sqlite3.IntegrityError:
        return False, "Kode barang sudah ada!"
    finally:
        conn.close()

def catat_transaksi(kode_barang, tipe, jumlah, penerima_suplier, keterangan):
    """Mencatat transaksi barang masuk atau keluar"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transaksi_stok (kode_barang, tipe_transaksi, jumlah, penerima_suplier, keterangan)
        VALUES (?, ?, ?, ?, ?)
    ''', (kode_barang, tipe, jumlah, penerima_suplier, keterangan))
    conn.commit()
    conn.close()

def get_riwayat_transaksi():
    """Mengambil riwayat transaksi barang"""
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT 
            t.id_transaksi,
            t.tanggal,
            m.nama_barang,
            m.ukuran,
            t.tipe_transaksi,
            t.jumlah,
            t.penerima_suplier,
            t.keterangan
        FROM transaksi_stok t
        JOIN master_barang m ON t.kode_barang = m.kode_barang
        ORDER BY t.tanggal DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
