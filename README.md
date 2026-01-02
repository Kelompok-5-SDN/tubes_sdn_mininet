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

Script dalam repository ini dirancang untuk menguji Kapasitas Link yang berbeda-beda terhadap Traffic Inject Konstan (60 Mbps) untuk melihat perilaku jaringan saat macet (Congestion).

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

## ⏳ Alur Proses Kerja Script

Script akan berjalan dengan tahapan berikut:

1. **Setup Topologi:** Membangun Switch, Host, dan Link sesuai spesifikasi (Otomatis dari script)
2. **CLI(Net):** Script akan membuka terminal mininet (Disini kita akan melakukan berbagai testing secara manual)
   - **Note:** jalankan "exit" jika sudah selesai pengujian untuk testing skenario lain atau finish
  
## ⏳🛠️ Alur Proses Kerja di dalam CLI(Net) untuk masing-masing skenario

Jalankan tahapan berikut untuk satu skenario, setelah selesai ulangi langkah dari awal lagi untuk skenario baru:

1. Pastikan Ryu Controller sudah running pada terminal lainnya
2. Jalankan **"pingall"** untuk memastikan topologi sudah tersambung dengan benar
   <img width="407" height="167" alt="image" src="https://github.com/user-attachments/assets/e28bfbbf-155b-41f1-b3cf-41d3fe6762b0" />
   - Contoh Jika Benar ✅ : ... Results: 0% dropped (20/20 received)
   - Contoh Jika Salah ❌ : ... Results: >0% dropped (<20/20 received) (Dropped diatas 0% dan Received kurang dari maksimal)
3. Jalankan **links** untuk memastikan struktur topologi sudah sesuai dengan yang kita rancang (Opsional)
   <img width="265" height="223" alt="image" src="https://github.com/user-attachments/assets/3b8f99e1-be3b-42f1-9e60-24e75aedd358" />
4. Jalankan **xterm h1 h5** untuk membuka terminal xterm pada host 1 dan host 5
   <img width="1094" height="356" alt="image" src="https://github.com/user-attachments/assets/711293cb-71cd-4070-8c59-3833d46142a2" />
   - **Note:** skenario akan ditest dengan h1 sebagai sender dan h5 sebagai receiver
5. Pada h1, jalankan command berikut untuk mendapatkan delay (Ambil nilai rtt avg sebagai variabel Delay | Jalankan sebanyak 10 kali)
   ```bash
     ping 10.0.0.5 -c 10
   ```
   <img width="391" height="211" alt="image" src="https://github.com/user-attachments/assets/0c027568-ff7a-4c88-bbff-2c38f80ae480" />
6. Pada h5 (sebagai receiver | 10.0.0.5), jalankan
   ```bash
     iperf3 -s -i 1
   ```
   -s: Server, memerintahkan iperf untuk diam dan mendengarkan (listen) koneksi yang masuk
   -i 1: menampilkan laporan di terminal client setiap 1 detik.
   - **Note:** jika selama pengujian terjadi error, misalkan "File Descriptor Error" dll. ctrl+c lalu jalankan ulang langkah ini "iperf3 -s -i 1"
7. Pada h1 (sebagai sender | 10.0.0.1), jalankan
   ```bash
     iperf3 -c 10.0.0.5 -u -b 60M -t 30 -i 1
   ```
     -c 10.0.0.5: Connect ke h5.
     -u: Mode UDP.
     -b 60M: Nilai Konstan (Inject 60 Mbps).
     -t 20: Durasi 30 detik.
     -i 1: menampilkan laporan di terminal client setiap 1 detik.
8. Ulangi langkah 6 dan 7 sebanyak 10 kali, lalu ambil nilai akhir Bitrate pada Receiver sebagai variabel **Throughtput** dan nilai akhir presentase Lost/TotalDatagrams sebagai variabel **Packet Loss**
     <img width="497" height="541" alt="image" src="https://github.com/user-attachments/assets/2ef0854e-aa26-4782-96c0-c2d1062df859" />
9. Dari 10 sampel tersebut ambil rata-rata masing-masing variabel QoS
10. Selesai

**Note:**
- Jalankan command berikut pada terminal Lubuntu (bukan pada xterm atau mininet>) setelah uji coba satu skenario selesai dan ingin berganti ke skenario lain untuk refresh ulang topologi dan jaringan
```bash
     sudo mn -c
```
