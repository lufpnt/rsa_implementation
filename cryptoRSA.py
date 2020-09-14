from mathRSA import *
import numpy as np
from matplotlib import pyplot as plt
import cv2

CHUNK_SIZE = 0


def encrypt_text(msg):
    # Encrypting string 'msg' by chunks of CHUNK_SIZE bytes
    fo = open('publicKey.txt', 'r')
    e = int(fo.readline())
    n = int(fo.readline())
    fo.close()
    fin = False
    offset = 0

    cipher = ""
    while not fin:
        # Iterating over 'msg'
        chunk = msg[offset:offset + CHUNK_SIZE]
        if len(chunk) % CHUNK_SIZE != 0: fin = True
        # Perform encoding with 'utf-8' on the bytes and converting the bytes to long  .
        cipher += str(pow(btl(chunk.encode('utf-8')), e, n)) + " "
        offset += CHUNK_SIZE
    cipher = cipher[:len(cipher) - 1]
    return cipher


def encrypt_tensor(tensor):
    # Splitting the tensor to r,g,b and perform encryption with tensor_power() function
    b, g, r = cv2.split(tensor)
    fo = open('publicKey.txt', 'r')
    e = int(fo.readline())
    n = int(fo.readline())
    fo.close()
    enc = np.zeros((tensor.shape[0], tensor.shape[1], 3))
    print("\n\nEncrypting the image...\n\nIt might takes few minutes...\n")
    eb = tensor_power(b, e, n)
    eg = tensor_power(g, e, n)
    er = tensor_power(r, e, n)
    # Performing module on the encrypted ndarrays in order to present the encrypted image
    enc = cv2.merge((np.uint8(er % 256), np.uint8(eg % 256), np.uint8(eb % 256)))

    plt.figure("Encrypted image")
    plt.imshow(enc)
    plt.axis('off')
    plt.show()

    return tuple(eb, eg, er)


def encrypt_integer(num):
    fo = open('publicKey.txt', 'r')
    e = int(fo.readline())
    n = int(fo.readline())
    fo.close()
    cipher = pow(num, e, n)
    return cipher


def decrypt_integer(cipher):
    fo = open('privateKey.txt', 'r')
    d = int(fo.readline())
    n = int(fo.readline())
    fo.close()
    decipher = pow(cipher, d, n)
    return decipher


def decrypt_text(cipher):
    # Decrypting string 'msg' by chunks of CHUNK_SIZE bytes
    fo = open('privateKey.txt', 'r')
    d = int(fo.readline())
    n = int(fo.readline())
    fo.close()

    array = cipher.split(" ")
    msg = ""
    for chunk in array:
        # Perform decoding with 'utf-8' on the bytes after converting the long to bytes.
        msg += ltb((pow(int(chunk), d, n))).decode('utf-8')
    return msg


def decrypt_tensor(tensor):
    # Splitting the tuple of tensor to r,g,b and perform decryption with tensor_power() function
    eb, eg, er = tensor
    fo = open('privateKey.txt', 'r')
    d = int(fo.readline())
    n = int(fo.readline())
    fo.close()
    clear = np.zeros((eb.shape[0], eb.shape[1], 3))
    print("\n\nDecrypting the image...\n\nIt might takes few minutes...\n")
    b = tensor_power(eb, d, n)
    g = tensor_power(eg, d, n)
    r = tensor_power(er, d, n)
    clear = cv2.merge((np.uint8(r), np.uint8(g), np.uint8(b)))
    plt.figure("Decrypted image")
    plt.imshow(clear)
    plt.show()


def decrypt_bin(cipher):
    # Decrypting binary file by chunks of CHUNK_SIZE size.
    fo = open('privateKey.txt', 'r')
    d = int(fo.readline())
    n = int(fo.readline())
    fo.close()

    array = cipher.split(" ")

    msg = bytes()
    for chunk in array:
        clear = ltb(pow(int(chunk), d, n))
        # Padding of null bytes for the last chunk if required.
        clear = (CHUNK_SIZE-len(clear))*b'\x00' + clear
        msg += clear

    # Removing the unnecessary null bytes that were added in the encryption process
    while msg[::-1] == b'\x00':
        msg = msg[:len(msg) - 1]

    return msg


def encrypt_bin(msg):
    # Encrypting binary file by chunks of CHUNK_SIZE size.
    fo = open('publicKey.txt', 'r')
    e = int(fo.readline())
    n = int(fo.readline())
    fo.close()

    fin = False
    offset = 0
    cipher = ""
    while not fin:
        chunk = msg[offset:offset + CHUNK_SIZE]
        if chunk == b'':
            fin = True
        elif len(chunk) % CHUNK_SIZE != 0:
            fin = True
            # Padding of null bytes for the last chunk if required.
            chunk += (CHUNK_SIZE - len(chunk)) * b'\x00'
        cipher += str(pow(btl(chunk), e, n)) + " "
        offset += CHUNK_SIZE
    cipher = cipher[:len(cipher) - 1]
    return cipher


def init_chunk_size():
    global CHUNK_SIZE
    fo = open('publicKey.txt', 'r')
    fo.readline()
    n = len(ltb(fo.readline())) * 8
    CHUNK_SIZE = chunk_dic[n]
