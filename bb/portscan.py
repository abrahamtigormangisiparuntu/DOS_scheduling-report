import socket
import errno #buat baca error code
import threading

START_PORT = 0
END_PORT = 5000
opened_list =[]
thread_list =[]

def check_port(host, port):
    global opened_list
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #ganti jenis socketnya jika mau melihat port terbuka pada koneksi lain / bukan tcp
    s.settimeout(3)
    result= s.connect_ex((host, port))
    
    #kalau result 0 berarti portnya open
    if result == 0:
        print(f"port {port} is opened")
    # else:
    #     print (f"{port} is closed: {errno.errorcode[result]}")
host = "http://localhost/" # ganti url ke url yang mau dites untuk dilihat port apa yang terbuka
#check_port(host, port)

for port in range(START_PORT, END_PORT+1):
    t = threading.Thread(target=check_port, args=(host, port))
    t.start()
    
for t in thread_list:
    t.join()
    
print(f"opened promt: {opened_list}")
