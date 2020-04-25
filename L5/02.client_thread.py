# import socket dan sys
import sys, socket

# fungsi utama
def main():
    # buat socket bertipe TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # tentukan IP server target
    TCP_IP = "192.168.43.63"
    
    # tentukan por server
    TCP_PORT = 14045

    # lakukan koneksi ke server
    try:
        s.connect((TCP_IP, TCP_PORT))
    except:
        # print error
        print("Koneksi error")
        # exit
        sys.exit()
    
    # tampilkan menu, enter quit to exit
    print("Masukkan 'quit' untuk keluar")
    message = input(" -> ")

    # selama pesan bukan "quit", lakukan loop forever
    while message != 'quit':
        # kirimkan pesan yang ditulis ke server
        s.send(message.encode())
        
        # menu (user interface)
        message = input(" -> ")

    # send "quit" ke server
    s.send(b'--quit--')

# panggil fungsi utama
if __name__ == "__main__":
    main()
