# import mpi4py
from mpi4py import MPI

# import library random untuk generate angka integer secara random
from random import randint

# buat COMM
comm = MPI.COMM_WORLD

# dapatkan rank proses
rank = comm.Get_rank()

# dapatkan total proses berjalan
size = comm.Get_size()

# generate angka integer secara random untuk setiap proses
data = randint(0,10)
print("Value from rank",rank,"is :",data)

# lakukam penjumlahan dengan teknik reduce, root reduce adalah proses dengan rank 0
sum = comm.reduce(data,op=MPI.SUM,root=0)

# jika saya proses dengan rank 0 maka saya akan menampilkan hasilnya
if rank==0:
    print("Sum from all value is :",sum)