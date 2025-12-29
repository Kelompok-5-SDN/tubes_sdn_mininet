from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController, Host
from mininet.link import TCLink
from mininet.log import setLogLevel, info
import time
import json

def run():
    bandwidth = 700 # Variabel Bebas
    traffic_load = 1000 # Nilai Konstan

    info("Menyiapkan Jaringan Mininet...\n")
    net = Mininet(
        topo=None,
        build=False,
        ipBase='10.0.0.0/8',
        switch=OVSSwitch, 
        link=TCLink)
    
    info("Menambahkan Controller...\n")
    c0 = net.addController(name='c0', controller=RemoteController, ip='127.0.0.1', protocol='tcp', port=6633)

    info("Menambahkan Switch...\n")
    s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
    s2 = net.addSwitch('s2', cls=OVSSwitch, protocols='OpenFlow13')
    s3 = net.addSwitch('s3', cls=OVSSwitch, protocols='OpenFlow13')
    s4 = net.addSwitch('s4', cls=OVSSwitch, protocols='OpenFlow13')
    s5 = net.addSwitch('s5', cls=OVSSwitch, protocols='OpenFlow13')

    info("Menambahkan Host...\n")
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    
    info(f"Konfigurasi Link: Bandwidth {bandwidth} Mbps, Delay 1ms...\n")
    link_config = {'bw': bandwidth, 'delay': '1ms', 'max_queue_size': 100}

    info("Menambahkan Link Host ke Switch...\n")
    net.addLink(h1, s1, **link_config)
    net.addLink(h2, s2, **link_config)
    net.addLink(h3, s3, **link_config)
    net.addLink(h4, s4, **link_config)
    net.addLink(h5, s5, **link_config)

    info("Menambahkan Link antar Switch...\n")
    net.addLink(s1, s2, **link_config)
    net.addLink(s2, s3, **link_config)
    net.addLink(s3, s4, **link_config)
    net.addLink(s4, s5, **link_config)
    net.addLink(s5, s1, **link_config)

    info("Memulai Jaringan...\n")
    net.build()

    info("Memulai Controller...\n")
    for controller in net.controllers:
        controller.start()
    
    info("Memulai Switch...\n")
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])

    print("-> Menunggu Ryu Controller...")
    time.sleep(40)

    info("Menyalakan server iperf3...\n")
    h5.cmd('iperf3 -s -D') 
    time.sleep(2)

    info("\nMenyiapkan Pengujian Throughput dan Delay...\n")
    print(f"=== MULAI PENGAMBILAN DATA (Bandwidth: {bandwidth} Mbps vs Traffic Load: {traffic_load} Mbps) ===")
    print(" Sampel | Throughput (Mbps) | Packet Loss (%) | Latency Ping (ms) ")

    for i in range(1, 11):
        cmd_iperf = f'iperf3 -c 10.0.0.5 -u -b {traffic_load}M -t 4 -J'
        json_output = h1.cmd(cmd_iperf)
        rx_throughput = 0
        loss_pct = 0
        
        try:
            data = json.loads(json_output)
            
            if 'end' in data and 'sum' in data['end']:
                summary = data['end']['sum']
                rx_throughput = summary['bits_per_second'] / 1000000
                loss_pct = summary['lost_percent']
            else:
                print(f"  #{i:<2}   |   Gagal mendapatkan data summary (Network Down?)")
                continue
                
        except json.JSONDecodeError:
            print(f"  #{i:<2}   |   Error Parsing JSON (Cek apakah server H5 menyala)")
            continue

        hasil_ping = h1.cmd('ping -c 1 -W 5 10.0.0.5')
        
        try:
            p_time = hasil_ping.find('time=')
            if p_time != -1:
                end_pos = hasil_ping.find(' ms', p_time)
                delay = hasil_ping[p_time+5 : end_pos].strip()
            else:
                delay = "RTO"
        except:
            delay = "Err"

        print(f"  #{i:<2}   |      {rx_throughput:6.2f}       |     {loss_pct:6.2f} %   |     {delay}")
        
        time.sleep(1)

    print("\n=== SELESAI ===")
    
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()