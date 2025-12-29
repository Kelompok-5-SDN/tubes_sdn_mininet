# Analisis QoS Jaringan SDN Topologi Ring

Proyek ini adalah simulasi jaringan SDN (Software-Defined Networking) menggunakan topologi Ring untuk menganalisis performa QoS (Quality of Service) di bawah kondisi beban tinggi.

Simulasi dilakukan menggunakan Mininet dan Ryu Controller, dengan memvariasikan kapasitas Bandwidth Link (500-1000 Mbps) melawan Traffic Load Konstan yang sangat masif (1000 Mbps).

## 📋 Fitur Utama

- **Topologi:** Ring (5 Switch, 5 Host)
- **Protokol:** OpenFlow 13
- **Controller:** Ryu (Mendukung STP untuk mencegah looping)
- **Traffic Generator:** Iperf3
- **Metode Pengukuran:** Parsing Output JSON
- **Parameter QoS:** Throughput, Packet Loss, dan Latency (Ping)

## 🛠 Prasarat (Requirements)

Pastikan sistem operasi Anda (Ubuntu 20.04/22.04 atau VM) sudah memiliki:

1. Python 3
2. Mininet (Emulator jaringan)
3. Ryu Controller (SDN Controller)
4. Iperf3

## 📦 Instalasi & Setup

Jalankan perintah berikut di terminal Ubuntu untuk menyiapkan lingkungan pengujian:

### 1. Update Repository
```bash
sudo apt-get update
```

### 2. Install Mininet
```bash
sudo apt-get install mininet
```

### 3. Install Ryu Controller

Pastikan pip sudah terinstall, lalu install Ryu:
```bash
sudo apt-get install python3-pip
pip3 install ryu
```

### 4. Install Iperf3 (PENTING)

Proyek ini mewajibkan Iperf3 agar data bisa dibaca oleh Python. Jangan gunakan iperf versi lama (iperf2).
```bash
sudo apt-get install iperf3
```

### 5. Clone Repository
```bash
git clone https://github.com/VerindraHernandaPutra/tubes_sdn_mininet.git
cd tubes_sdn_mininet
```

## 📂 Konfigurasi Skenario

Script dalam repository ini dirancang untuk menguji Kapasitas Link yang berbeda-beda terhadap Traffic Load Konstan (1000 Mbps) untuk melihat perilaku jaringan saat macet (Congestion).

| Nama File | Kapasitas Link (Jalan) | Traffic Load |
|-----------|------------------------|--------------|
| bw_500.py | 500 Mbps | 1000 Mbps |
| bw_600.py | 600 Mbps | 1000 Mbps |
| bw_700.py | 700 Mbps | 1000 Mbps |
| bw_800.py | 800 Mbps | 1000 Mbps |
| bw_900.py | 900 Mbps | 1000 Mbps |
| bw_1000.py | 1000 Mbps | 1000 Mbps |

**Catatan:** Ubah variabel bandwidth di baris awal setiap file python untuk membuat skenario kustom.

## 🚀 Cara Menjalankan Simulasi

Simulasi ini membutuhkan 2 Terminal yang berjalan secara bersamaan.

### Terminal 1: Jalankan Ryu Controller

Karena menggunakan Topologi Ring, WAJIB menggunakan aplikasi Ryu yang mendukung STP (Spanning Tree Protocol) agar tidak terjadi looping (broadcast storm).
```bash
ryu-manager ryu.app.simple_switch_stp_13
```

Biarkan terminal ini tetap terbuka dan menampilkan log.

### Terminal 2: Jalankan Script Simulasi

Pilih skenario bandwidth yang ingin diuji, misalnya 500 Mbps. Gunakan sudo.
```bash
sudo python3 bw_500.py
```

## ⏳ Alur Proses Otomatis

Script akan berjalan otomatis dengan tahapan berikut:

1. **Setup Topologi:** Membangun Switch, Host, dan Link
2. **Convergence Time:** Script akan menunggu selama 40 detik (time.sleep(40))
   - **Penting:** Jangan batalkan proses ini. Waktu ini diperlukan agar protokol STP di Controller selesai menghitung jalur terbaik dan memblokir port yang menyebabkan loop
3. **Stress Testing:** Mengirim trafik UDP sebesar 1000 Mbps dari Host 1 ke Host 5
4. **Data Collection:** Mengambil 10 sampel Throughput, Packet Loss, dan Latency secara otomatis

## 📊 Contoh Output Data

Script akan menghasilkan tabel data real-time di terminal:
```
=== MULAI PENGAMBILAN DATA (Bandwidth: 500 Mbps vs Traffic Load: 1000 Mbps) ===

Sampel | Throughput (Mbps) | Packet Loss (%) | Latency Ping (ms)
#1     | 498.50            | 50.15 %         | 15.20
#2     | 499.10            | 49.90 %         | 14.80
...
```

**Analisis:** Karena Beban (1000 Mbps) lebih besar dari Kapasitas Link (500 Mbps), maka Packet Loss akan tinggi (~50%), yang menunjukkan simulasi berjalan benar.

## 🔧 Troubleshooting

### 1. Latency tertulis "RTO"

- Ini wajar jika jaringan sangat padat.
- Script menggunakan timeout 5 detik (-W 5) untuk mencoba mendapatkan angka latency sebisa mungkin sebelum terjadi RTO

### 2. Script diam lama di awal ("Menunggu Ryu Controller...")

- Script diprogram tidur selama 40 detik agar jaringan stabil sebelum pengambilan data dimulai

### 3. Error "JSONDecodeError" atau "Connection Refused"

- Biasanya terjadi jika Server Iperf3 di Host 5 gagal menyala
- **Solusi:** Bersihkan sisa-sisa proses mininet dengan perintah:
```bash
sudo mn -c
sudo pkill -9 iperf3
```

Lalu jalankan script kembali.

---

**Dibuat oleh:** Verindra Hernanda Putra
