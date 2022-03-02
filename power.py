import random
import numpy as np

SBox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 8, 0x4, 0x7, 0x1, 0x2]
KEY = 0xb

nibbles = []
keys = []
for i in range(50):
    nibbles.append(random.getrandbits(4))

for i in range(16):
    keys.append(i)

def enc(plain_text, key):
    u = plain_text ^ key
    c = SBox[u]
    return c

def generate_ciphers(nibbles, key):
    ciphers = []
    for plain_text in nibbles:
        ciphers.append(enc(plain_text, key))
    return ciphers

def generate_hamming(ciphers):
    consumption = []
    for cipher in ciphers:
        consumption.append(bin(cipher).count("1"))
    return consumption

true_ciphers = generate_ciphers(nibbles, KEY)
true_hamming = np.array(generate_hamming(true_ciphers))


for key in keys:
    ciphers = generate_ciphers(nibbles, key)
    hamming = np.array(generate_hamming(ciphers))
    if (np.allclose(true_hamming, hamming)):
        print("found")
        print(key)
