from Crypto.Util import number as num
from Crypto.Util.number import bytes_to_long as btl, long_to_bytes as ltb
import random
import math
import libnum as lb

key_sizes = (128, 256, 512, 1024, 2048, 4096)
chunk_dic = {128: 15, 256: 30, 512: 62, 1024: 126, 2048: 254, 4096: 510}


def gen_prime(length=128):
    # Generating prime number
    primeNum = num.getPrime(length)
    return primeNum


def calc_n(prime1, prime2):
    # returning a list with n[0] = n, n[1] = phi(n)
    n = [prime1 * prime2, (prime1 - 1) * (prime2 - 1)]
    return n


def gen_e(phi):
    # Generating the public key
    while True:
        e = random.randrange(2, phi)
        if math.gcd(e, phi) == 1:
            return e


def gen_d(phi, e):
    # Generating the private key
    d = lb.invmod(e, phi)
    return d


def gen_keys(length):
    # Generating public and private key based on the length supplied by the user
    p = gen_prime(length)
    q = gen_prime(length)
    narr = calc_n(p, q)
    e = gen_e(narr[1])
    d = gen_d(narr[1], e)

    fo = open('publicKey.txt', 'w')
    fo.write(str(e) + '\n')
    fo.write(str(narr[0]) + '\n')
    fo.close()
    fo = open('privateKey.txt', 'w')
    fo.write(str(d) + '\n')
    fo.write(str(narr[0]) + '\n')
    fo.close()

    print("\n\nKeys generated successfully ! \n\nexit...\n\n")


def tensor_power(t, d, n):
    res = 1
    while d != 0:
        if d % 2 == 1:
            res = ((res % n) * (t % n)) % n
        t = ((t % n) * (t % n)) % n
        d >>= 1
    return res
