# import mpi4py
from mpi4py import MPI

# buat COMM
comm = MPI.COMM_WORLD

# dapatkan rank proses
rank = comm.Get_rank()

# dapatkan total proses berjalan
size = comm.Get_size()

# jika saya rank terbesar maka saya akan mengirimkan pesan ke proses yang mempunyai rank 0 s.d rank terbesar-1
if rank == 0:
	for i in range(1, size):
		data = 'Hello world!'
		comm.send(data, dest=i)
		print('Proc {} sent to: {} | data: {}'.format(rank, i, data))

# jika saya bukan rank terbesar maka saya akan menerima pesan yang berasal dari proses dengan rank terbesar
else:
	data = comm.recv(source=0)
	print('Proc {} received from: {} | data: {}'.format(rank, 0, data))