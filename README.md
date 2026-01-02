# Analisis QoS Jaringan SDN Topologi Ring

Proyek ini adalah simulasi jaringan SDN (Software-Defined Networking) menggunakan topologi Ring untuk menganalisis performa QoS (Quality of Service) berupa Throughtput, Delay, dan Packet Loss.

Simulasi dilakukan menggunakan Mininet dan Ryu Controller, dengan memvariasikan kapasitas Bandwidth Link (10-50 Mbps) dengan Input Bandwidth konstan sebesar (60Mbps).

## 🧬 Variabel Penelitian

- **Variabel Bebas (Independent Variable):** Kapasitas Bandwidth Link (10, 20, 30, 40, 50 Mbps).
- **Variabel Terikat (Dependent Variable):** Parameter QoS (Throughput, Delay, dan Packet Loss).
- **Variabel Kontrol (Controlled Variable):**
     - Topologi: Ring (5 Switch, 5 Host).
     - Beban Trafik: UDP 60 Mbps (Konstan).
     - Ukuran Paket: Default.

## ❓ Research Questions

1. Bagaimana pengaruh perubahan kapasitas bandwidth terhadap nilai **Throughput** pada jaringan SDN dengan topologi Ring saat mengalami beban trafik?
2. Bagaimana dampak peningkatan bandwidth terhadap persentase **Packet Loss** ketika jaringan dibebani trafik melebihi kapasitas link?
3. Apakah terdapat perubahan signifikan pada nilai **Delay** (Latency) seiring dengan bertambahnya kapasitas bandwidth pada arsitektur SDN?

## 🔬 Hipotesis

1. Hipotesis 1 :
   "Semakin besar kapasitas bandwidth link yang dikonfigurasi, maka nilai Throughput yang dihasilkan akan semakin meningkat mendekati nilai bandwidth tersebut, karena kapasitas pipa penyaluran data menjadi lebih luas."
2. Hipotesis 2 :
   "Terdapat hubungan berbanding terbalik antara bandwidth dan packet loss. Semakin besar bandwidth, maka persentase Packet Loss akan semakin kecil. Hal ini karena antrian (queue) pada switch dapat mengalirkan data lebih cepat, sehingga mengurangi jumlah paket yang dibuang (drop) akibat buffer penuh."
3. Hipotesis 3 :
   "Peningkatan bandwidth akan menurunkan nilai Delay, khususnya pada delay antrian (queuing delay). Dengan bandwidth yang lebih besar, waktu tunggu paket di dalam antrian switch menjadi lebih singkat sebelum ditransmisikan."

## 📋 Fitur Utama

- **Topologi:** Ring (5 Switch, 5 Host)
- **Protokol:** OpenFlow 13
- **Controller:** Ryu (Mendukung STP untuk mencegah looping)
- **Traffic Generator:** Iperf3 dan Iperf
- **Metode Pengukuran:** Manual dengan **CLI(Net)** untuk hasil  yang lebih akurat dan teruji langsung dengan **xterm** dengan **10 sampel** (pengujian berulang sebanyak 10 kali) untuk hasil yang valid
- **Parameter QoS:** Throughput, Delay, dan Packet Loss

## 🛠 Prasarat (Requirements)

Pastikan sistem operasi Anda (Ubuntu 20.04/22.04 atau VM) sudah memiliki:

1. Python 3
2. Mininet (Emulator jaringan)
3. Ryu Controller (SDN Controller)
4. Iperf3 dan Iperf

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

Proyek ini mewajibkan Iperf3 agar bisa membaca variabel Packet Loss dengan lebih jelas (Versi Terbaru lebih bagus).
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

| Nama File | Kapasitas Link (Jalan) | Traffic Injected |
|-----------|------------------------|--------------|
| bw_10.py | 10 Mbps | 60 Mbps |
| bw_20.py | 20 Mbps | 60 Mbps |
| bw_30.py | 30 Mbps | 60 Mbps |
| bw_40.py | 40 Mbps | 60 Mbps |
| bw_50.py | 50 Mbps | 60 Mbps |

**Catatan:** Jalankan bw_custom.py membuat skenario kustom.

## 🚀 Cara Menjalankan Simulasi

Simulasi ini membutuhkan 2 Terminal yang berjalan secara bersamaan.

### Terminal 1: Jalankan Ryu Controller

Karena menggunakan Topologi Ring, WAJIB menggunakan aplikasi Ryu yang mendukung STP (Spanning Tree Protocol) agar tidak terjadi looping (broadcast storm).
```bash
ryu-manager ryu.app.simple_switch_stp_13
```

Biarkan terminal ini tetap terbuka dan menampilkan log.

### Terminal 2: Jalankan Script Simulasi

Pilih skenario bandwidth yang ingin diuji, misalnya 10 Mbps. Gunakan sudo.
```bash
sudo python3 bw_10.py
```

## ⏳ Alur Proses secara Manual

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
