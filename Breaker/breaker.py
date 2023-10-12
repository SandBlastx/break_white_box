import argparse
import re
import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm
import numpy as np
import os
from ast import literal_eval
import time
from analyse import best_key_byte
import subprocess


# r_key = [0x47, 0x47, 0xf0, 0x09, 0x0e, 0x22, 0x77, 0xb3, 0xb6, 0x9a, 0x78, 0xe1, 0xe7, 0xcb, 0x9e, 0x3f ]
# r_key =[
#         0x37, 0x44, 0xf6, 0x59, 0x4e, 0x23, 0x47, 0x63, 0x86, 0x99, 0x48, 0x31, 0x27, 0x5b, 0x7e,
#         0x3f,
#     ]
r_key =  [
        0x34, 0x45, 0xf3, 0x19, 0x5e, 0x27, 0x89, 0x63, 0x96, 0x90, 0x38, 0x41, 0x77, 0x5c, 0xcc,
        0xcf
    ]

def Inv_shift(state):
    tmp = state[:]
    for i in enumerate([0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3]):
        state[i[0]] = tmp[i[1]]
    return state

def shift(state):
    tmp = state[:]
    for i in enumerate([0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]):
        state[i[0]] = tmp[i[1]]
    return state

    


def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] >> shift) & 0x1


def parse_file_2(path_log , address_read ,get_address , verbose ):
    for i in tqdm(range(256)):
        for g in range(1,5):
            bytes_buffer  = bytearray()
            file = open(f'{path_log}/player_wb_aes_{i}_{g}.log', 'r')
            lines = file.readlines()
            count = 0

            for line in lines :
                l_split = line.split()
                if l_split[0] == "[R]":
                    addr_current = l_split[1].split('x')[1]
                    if addr_current in address_read :
                        print(f"size :{l_split[4]}")
                        addr = bytearray.fromhex(l_split[2][2:])
                        value = bytearray.fromhex(l_split[-1].split('x')[1])
                        size = bytearray.fromhex("0"+l_split[4])
                        if get_address:
                            bytes_buffer += addr
                            bytes_buffer += size

                        bytes_buffer += value 
                        if verbose :
                            print(f"parsing read at {addr} value {value} size {size} ")
                        bit_buffer = np.array([access_bit(bytes_buffer, i) for i in range(len(bytes_buffer)*8)])
                        np.save(f"{path_se}/se_{count+ 4*(g-1)}_{i}.npy", bit_buffer, allow_pickle=True)
                        bytes_buffer= bytearray()
                        count+= 1

            if count != 4 : 
                exit(f"number of tyi output parsed {count} in {g} in {i} log ")



def generate_trace(nb_trace  ,path_log, path_pe  , path_tracer, path_player , mode  ):

    for i in tqdm(range(256)):
    
        pe = open(f'{path_pe}/pe_{i}','wb')
        for k in range(16) : 
            pe.write(i.to_bytes(1 , "little"))
        pe.close()
        os.system(f'{path_tracer} -o {path_log}/player_wb_aes_{i}.log -f 0x555555562a31-0x55555556368f -F 0x555555562a3d:0x555555562a31  -n 1 -- {path_player} --mode {mode} -a encrypt -f {path_pe}/pe_{i}')

def generate_trace_2(nb_trace  ,path_log, path_pe  , path_tracer, path_player , mode  ):

    for i in tqdm(range(256)):
    
        pe = open(f'{path_pe}/pe_{i}','wb')
        for k in range(16) : 
            pe.write(i.to_bytes(1 , "little"))
        pe.close()
        for g in range(1 ,5):
            os.system(f'{path_tracer} -o {path_log}/player_wb_aes_{i}_{g}.log -f 0x5555555653f0-0x000055555556560a -F 0x555555565460:0x55555556560a  -n {g} -- {path_player} --mode {mode} -a encrypt -f {path_pe}/pe_{i}')



    

def open_traces(nb_trace , path_pe , path_se , key ) : 

    Se = np.array([np.load(f"{path_se}/se_{key}_{0}.npy")])
    Pe = np.array([0])
    for i in range(1 , nb_trace):
        
        Se = np.append(Se, [np.load(f"{path_se}/se_{key}_{i}.npy")] , axis=0)
        Pe = np.append(Pe ,np.array ([i]) , axis=0)
  
    #print(f"Shape Se:{Se.shape} Pe:{Pe.shape}")
    return Se , Pe 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Breaker", description="Python script to parse log file from Tracer")
    # parser.add_argument('--range', type=str, required=False , )# exemple 0x00007fffffffd7d8
    parser.add_argument('-g', type=int, required=False)
    args = parser.parse_args()
    nb_trace = 256
    path_pe = Path("./Traces/Pe/")
    path_se = Path("./Traces/Se/")
    path_player = Path("./../tmp/player")
    path_tracer = Path("./../Tracer/TracerPIN/Tracer")
    path_log = Path("./../player_db/")
    mode = "white-box"

    addr_len = 0
    key = []
    tmp_rkey = r_key[:]
    tmp_rkey = shift(tmp_rkey)
    address_read = ["000055555556547f" , "0000555555565494", "00005555555654a8" , "00005555555654bb"]
    if args.g  == 1 :
        generate_trace_2(nb_trace , path_log , path_pe  , path_tracer , path_player , mode  )
        parse_file_2(path_log ,address_read  , True ,False)
    for k in range(16):
        T= open_traces(nb_trace , path_pe , path_se , k)
        key.append(best_key_byte(T , tmp_rkey[k]))

    print(f'Key found : {Inv_shift(key)}')
    print(f"Real key : {r_key}")




  
