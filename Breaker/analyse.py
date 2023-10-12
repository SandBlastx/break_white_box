import numpy as np
import matplotlib.pyplot as plt
import random 

#https://eprint.iacr.org/2018/301.pdf (3: Differential Computational Analysis) page 7/26

#TO DO
# Si à la dernière étape, deux pics sont de hauteur égale (donc que leur probalitité soit égale, que faire?)
#  -> actuellement on prend le premiers

# #[
#         0x47, 0x47, 0xf0, 0x09, 0x0e, 0x22, 0x77, 0xb3, 0xb6, 0x9a, 0x78, 0xe1, 0xe7, 0xcb, 0x9e,
#         0x3f,
#     ];

r_key = [0x47, 0x47, 0xf0, 0x09, 0x0e, 0x22, 0x77, 0xb3, 0xb6, 0x9a, 0x78, 0xe1, 0xe7, 0xcb, 0x9e, 0x3f ]


Sbox = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
        ]


def sel(p, k, j):#Step 2
    """Selection function return j bit from state ;
    P: int plain text as hex
    k : hp Key bytes
    j : bit to select 
    """

    f = bin(Sbox[k ^ p])[2:]
    
    if len(f) < j  : 
        f  = 0
    else :
        f = f[(len(f)-1) - j ]
    return f


def sorting_traces(Se, Pe, key, j):#Step 3
    a_0 = []
    a_1 = []
    for s, p in zip(Se, Pe):
        if sel(p, key, j) == '1':
            a_1.append(s)
        else:
            a_0.append(s)
    return (a_0, a_1)


def mean_trace(A, v ):#Step 4

    A_0 = np.array(A[0])
    A_1 = np.array(A[1])


    A_0  =  A_0.mean(axis=0)
    A_1  =  A_1.mean(axis=0)


    if v:
        fig, axs = plt.subplots(2, figsize=(20, 10))

        plt.title("Mean of  trace for each set ")

        axs[0].legend("Mean A_0")
        axs[0].plot(A_0)

        axs[1].legend("Mean A_1")
        axs[1].plot(A_1)

        plt.show()

    return (A_0, A_1)


def difference_means(A,v):#Step 5

   

    D = np.diff([A[0],A[1]],axis = 0)


    if v:
        fig,axs = plt.subplots(2, figsize=(20, 10))

        plt.title("Difference  of  set ")

        axs[0].plot(D[0])

        plt.show()
    return np.amax(D) , D 



def best_target_bit(key ,T ,v):#Step 6

    H = []
    D = []
    Se = T[0]
    Pe = T[1]
    
    for j in range(8) :
        A = sorting_traces (Se , Pe  , key , j )
        A = mean_trace(A, v)
        h , d = difference_means(A ,v )
        H.append(h)
        D.append(d)
        v = False
    
    J = np.argmax(H)
    
    H_np = np.array(H)
    if H[J] > 0.3 :
        return H[J]
    if H[J] <= 0.3 and H[J]>= 0.2 : 
        tmp = np.absolute(H_np - 0.25)
        I = np.argmin(tmp)
        return H[I]
        #closest to 0.25
    if H[J] < 0.2 :
        tmp = np.absolute(H_np)
        I = np.argmin(tmp)
        return H[I]
        #closest to 0 
     

    # print( f"[*] best bit is {J} for kh {key} with value  : {H[J]} ")
    # return res
dic = { 0 : 'H' , 1 : 'M' , 2 : 'L'}
    
def best_key_byte(T , real_key):#Step 7
    K = []
    v = False
    flag = 0
    for k in range(256):

        h = best_target_bit(k ,T , v)
        K.append(h)
        v = False

    J = np.argmax(K)
    K_np = np.array(K)
    if K[J] > 0.3 :
        tmp = K_np
        candidate = np.argwhere(K_np == K_np[J])
        if len(candidate) > 1 : 
            print(f"[!] more than one candidate {[i[0] for i in candidate]}")
        key =  J
    elif K[J] <= 0.3 and K[J]>= 0.2 : 
        tmp = np.absolute(K_np - 0.25)
        I = np.argmin(tmp)
        candidate = np.argwhere(tmp == tmp[I])
        if len(candidate) > 1 : 
            print(f"[!] more than one candidate {[i[0] for i in candidate]}")
        key =  I
        flag = 1
        #closest to 0.25
    elif K[J] < 0.2 :
        tmp = np.absolute(K_np)
        I = np.argmin(tmp)
        candidate = np.argwhere(tmp == tmp[I])
        if len(candidate) > 1 : 
            print(f"[!] more than one candidate {[i[0] for i in candidate]}")
        key =  I
        flag = 2

    if flag > 0 :
        position = np.argwhere(np.argsort(tmp) == real_key)[0]
    else :
        position = np.argwhere(np.argsort(tmp)[::-1] == real_key)[0]
    
    print( f"[*K*] [{dic[flag]}] best key hyp is {key} vs {real_key} | [P] real_key:{position} [H] real_key :{K[real_key]} hyp_key:{K[key]}")
    return key 

# dim_trace = 100
# nb_trace = 600 

# Se = np.array ( [random.choices(range(0,2), k=dim_trace) for i in range(nb_trace)])

# Pe = random.choices(range(0,255), k=nb_trace)

# T = (Se , Pe)

# best_key_byte(T)


