import sys
import csv
import numpy as np
import scipy.linalg
from numpy import linalg as LA
import struct
import os
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def analyze_bin(sz_path, base_tsv_path, num):
    file_baseline = base_tsv_path + '/state-' + str(num) + '.bin'
    file_sz_tsv = sz_path + '/state-' + str(num) + '.bin'
    base_real = []
    base_img = []
    sz_real = []
    sz_img = []
    err = []

    with open(file_baseline,'rb') as base_bin:
        f_slice = int(os.fstat(base_bin.fileno()).st_size / size)
        f_start = rank * f_slice
        f_end = (rank + 1) * f_slice - 1
        if f_end > os.fstat(base_bin.fileno()).st_size:
            f_end = os.fstat(base_bin.fileno()).st_size
        base_bin.seek(f_start, 0)
        while base_bin.tell() < f_end:
            real, = struct.unpack('d',base_bin.read(8))
            imag, = struct.unpack('d',base_bin.read(8))
            base_real.append(float(real))
            base_img.append(float(imag))
    if rank == 0:
        print("read baseline file finished\n")
    comm.Barrier()
    with open(file_sz_tsv,'rb') as sz_bin:
        f_slice = int(os.fstat(sz_bin.fileno()).st_size / size)
        f_start = rank * f_slice
        f_end = (rank + 1) * f_slice - 1
        if f_end > os.fstat(sz_bin.fileno()).st_size:
            f_end = os.fstat(sz_bin.fileno()).st_size
        sz_bin.seek(f_start, 0)
        while sz_bin.tell() < f_end:
            real, = struct.unpack('d',sz_bin.read(8))
            imag, = struct.unpack('d',sz_bin.read(8))
            sz_real.append(float(real))
            sz_img.append(float(imag))
    
    if rank == 0:
        print("read sz file finished\n")
    base_vec = np.ones((len(base_real), 1), dtype=np.complex)
    sz_vec = np.ones((len(sz_real), 1), dtype=np.complex)

    for i in range(len(base_real)):
        base_vec[i, 0] = complex(base_real[i], base_img[i])
        sz_vec[i, 0] = complex(sz_real[i], sz_img[i])

    base_vec_cj = np.conjugate(base_vec)
    fidelity = abs(np.inner(base_vec_cj.T, sz_vec.T))
    recv_fid = comm.gather(fidelity[0,0], root = 0)
    if rank == 0:
        return sum(recv_fid)
    else:
        return 0

def analyze_out(sz_path):
    comp_time = []
    decomp_time = []
    comp_ratio = []
    out_filename = sz_path + "/output.log"
    file_comp_ratio = sz_path + "/compression_ratio.txt"
    file = open(file_comp_ratio,"w")
    with open(out_filename, "r") as fp:
        for line in fp:
            if ("Compression time: " in line[0:18]):
                num = line.replace("Compression time: ", "").split(" ")[-1]
                comp_time.append(float(num))
            elif ("Decompression time: " in line[0:20]):
                num = line.replace("Decompression time: ", "").split(" ")[-1]
                decomp_time.append(float(num))
            if ("Compression ratio: " in line[0:19]):
                num = line.replace("Compression ratio: ", "").split(" ")[-1]
                comp_ratio.append(float(num))
                file.write(num)

    file.close()

    file_comp_analysis = sz_path + "/compression_analysis.txt"
    file = open(file_comp_analysis,"w") 
    print("Max Compression Time = {}".format(max(comp_time)))
    print("Average Compression Time = {}".format(sum(comp_time)/len(comp_time)))
    print("Max Decompression Time = {}".format(max(decomp_time)))
    print("Average Decompression Time = {}".format(sum(decomp_time)/len(decomp_time)))
    print("Max Compression Ratio = {}".format(max(comp_ratio)))
    print("Min Compression Ratio = {}".format(min(comp_ratio)))
    print("Average Compression Ratio = {}".format(sum(comp_ratio)/len(comp_ratio)))
    file.write("Max Compression Time = {}\n".format(max(comp_time)))
    file.write("Average Compression Time = {}\n".format(sum(comp_time)/len(comp_time)))
    file.write("Max Decompression Time = {}\n".format(max(decomp_time)))
    file.write("Average Decompression Time = {}\n".format(sum(decomp_time)/len(decomp_time)))
    file.write("Max Compression Ratio = {}\n".format(max(comp_ratio)))
    file.write("Min Compression Ratio = {}\n".format(min(comp_ratio)))
    file.write("Average Compression Ratio = {}\n".format(sum(comp_ratio)/len(comp_ratio)))
    file.close()


def main(argv):
    sz_path = argv[1]
    base_tsv_path = argv[2]
    
    if rank == 0:
        print('---- start analyze ----')
        print('size = ' + str(size))
        analyze_out(sz_path)

    comm.Barrier()

    if rank == 0:
        file_err_analysis = sz_path + "/error_analysis.tsv"
        file = open(file_err_analysis,"w")
        file.write("Fidelity\n")

    for i in range(9999999, 9999999+1):
        fid = analyze_bin(sz_path, base_tsv_path, i)
        if rank == 0:
            results = str(fid) + "\n"
            file.write(results)
    if rank == 0:
        file.close()

def numpy_test():
    file = open('test.bin','rb')
    for i in range(2):
        print("{}: {}".format(i, struct.unpack('d',file.read(8))))
    file.close()
    i = 0
    real = []
    imag = []
    q_sum = 0
    with open('test.bin','rb') as base_bin:
        while base_bin.tell() < os.fstat(base_bin.fileno()).st_size:
            tmp, = struct.unpack('d',base_bin.read(8))
            tmp2, = struct.unpack('d',base_bin.read(8))
            q_sum = q_sum +  float(tmp) * float(tmp) + float(tmp2) * float(tmp2)
            #real.append(float(tmp))
            #imag.append(float(tmp2))
    print(q_sum)

if __name__ == "__main__":
    #numpy_test()
    main(sys.argv)
        
