# program ini untuk mendownload gambar yang ada di url dengan 
# jumlah thread sesuai parameter splitBy di main() defaultnya 3

# os untuk menggunakan disk
import os
# requests untuk set request data (dalam hal ini headernya)
import requests
# threading untuk membuat.. threading :)
import threading
# urllib.request untuk melakukan http call,
# urllib.error untuk catching exception, tapi di sini tidak dipakai, diganti dengan boolean juggling dari hasil download
# urllib.parse untuk melakukan parsing url, tapi di sini tidak dipakai, dan diganti dengan split()
import urllib.request, urllib.error, urllib.parse
# time untuk menghitung time elapsed
import time

# url datanya
url = "https://apod.nasa.gov/apod/image/1901/LOmbradellaTerraFinazzi.jpg"

# fungsi untuk membuat range byte data untuk thread
def buildRange(value, numsplits):
    lst = []
    # untuk tiap threadnya
    for i in range(numsplits):
        # untuk thread pertama
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
        # untuk thread selanjutnya
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    # return semua byte range
    return lst

# class SplitBufferThreads extends threading.Thread
class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """
    # constructor
    def __init__(self, url, byteRange):
        # construct parent class
        super(SplitBufferThreads, self).__init__()
        # set attribute: url, __byteRange, req
        self.__url = url
        self.__byteRange = byteRange
        self.req = None

    # jalankan downloadnya
    def run(self):
        # mendownload file dengan range yang disesuaikan yang diinfokan menggunakan header range
        self.req = urllib.request.Request(self.__url,  headers={'Range': 'bytes=%s' % self.__byteRange})

    # mendapatkan hasil datanya
    def getFileData(self):
        # read dari hasil url yang diset di run()
        return urllib.request.urlopen(self.req).read()


def main(url=None, splitBy=3):
    # untuk menghitung elapsed time
    start_time = time.time()

    #jika url kosong
    if not url:
        # tampilkan error msg
        print("Please Enter some url to begin download.")
        # stop
        return

    # mendapatkan nama file berdasarkan url (setelah karakter / terakhir sampai akhir string)
    fileName = url.split('/')[-1]
    # mendapatkan ukuran file yang akan didownload berdasarkan header content-length. kalau kosong, ukurannya None
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
    # tampilkan ukurannya
    print("%s bytes to download." % sizeInBytes)
    # kalau None
    if not sizeInBytes:
        # tampilkan pesan error
        print("Size cannot be determined.")
        # stop
        return

    # mempersiapkan data yang akan displit
    dataLst = []
    # mendownload pada masing-masing thread
    for idx in range(splitBy):
        # mendapatkan range data untuk thread ini
        byteRange = buildRange(int(sizeInBytes), splitBy)[idx]
        # mempersiapkan buffer untuk didownload (berdasarkan range di baris sebelumnya)
        bufTh = SplitBufferThreads(url, byteRange)
        # start downloading
        bufTh.start()
        # tunggu download selesai
        bufTh.join()
        # append hasil download-nya
        dataLst.append(bufTh.getFileData())

    # append sebagai byte
    content = b''.join(dataLst)

    # jika download berhasil
    if dataLst:
        # jika sudah ada file yang namanya sama
        if os.path.exists(fileName):
            # hapus file yang sudah ada
            os.remove(fileName)
        # print time elapsed
        print("--- %s seconds ---" % str(time.time() - start_time))
        # buat object file dengan akses write as byte
        with open(fileName, 'wb') as fh:
            # write di disk
            fh.write(content)
        #print berhasil menyimpan
        print("Finished Writing file %s" % fileName)

# jika kode dijalankan langsung dari terminal
if __name__ == '__main__':
    # jalankan main() dengan url sesuai di atas
    main(url)