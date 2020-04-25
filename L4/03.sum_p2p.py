# import mpi4py
from mpi4py import MPI

# import library random untuk generate angka integer secara random
import random

# buat COMM
comm = MPI.COMM_WORLD

# dapatkan rank proses
rank = comm.Get_rank()

# dapatkan total proses berjalan
size = comm.Get_size()

# generate angka integer secara random untuk setiap proses
rand = random.randint(0,10)

# jika saya adalah proses dengan rank 0 maka:
# saya menerima nilai dari proses 1 s.d proses dengan rank terbesar
# menjumlah semua nilai yang didapat (termasuk nilai proses saya)
if rank == 0:
    print('This is rank ', rank,' send value ', rand)
    sum = rand
    for i in range(1,size):
        recvMsg = comm.recv(source=i)
        sum = sum + recvMsg
    print('Total sum of all of the proses  = ',sum)
# jika bukan proses dengan rank 0, saya akan mengirimkan nilai proses saya ke proses dengan rank=0
else:
#     sendMsg = rand
    print('This is rank ', rank,' send value ', rand)
    comm.send(rand, dest=0)
