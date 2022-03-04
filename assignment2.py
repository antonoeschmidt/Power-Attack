import csv
from numpy import transpose

# For testing
from scipy.stats.stats import pearsonr

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
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
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

def read_data():
    input = []
    with open('inputs8.dat') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            input = row

    data = []
    with open('T8.dat') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data.append(row)
    
    return input, data

def generate_keys():
    keys = [x for x in range(256)]
    return keys

def encrypt(input, key):
    cipher = []
    for i in input:
        cipher.append(Sbox[int(i) ^ key])
    return cipher

def calculate_hamming(ciphers):
    consumption = []
    for cipher in ciphers:
        cipher = int(float(cipher)) # Converting strings to numbers and then to integers
        consumption.append(bin(cipher).count("1"))
    return consumption

def generate_h(input, keys):
    ciphers = []
    for key in keys:
        ciphers.append(encrypt(input, key))
    
    h = []
    for c in ciphers:
        h.append(calculate_hamming(c))
    return h

def generate_t(data):
    data = transpose(data)
    t = []
    for d in data:
        t.append(calculate_hamming(d))
    return t

def pearson_coef(x, y):
  N = len(x)
  
  sum_x = float(sum(x))
  sum_y = float(sum(y))
  sum_x_sq = sum(x_i * x_i for x_i in x)
  sum_y_sq = sum(y_i * y_i for y_i in y)
  psum = sum(x_i * y_i for x_i, y_i in zip(x, y))
  
  # Top of fraction
  top = psum - (sum_x * sum_y/N)
  # Buttom of fraction
  buttom = pow((sum_x_sq - pow(sum_x, 2) / N) * (sum_y_sq - pow(sum_y, 2) / N), 0.5)

  return top / buttom

def find_best_match(h, t):
    max = 0
    key = -1
    for i in range(len(h)):
        for j in range(len(t)):
            # corr = pearson_coef(h[i], t[j])

            # Testing with Scipy pearson
            corr, _ = pearsonr(h[i], t[j])
            if (abs(corr) > max):
                max = abs(corr)
                key = i

    return max, key

input, data = read_data()
keys = generate_keys()
h = generate_h(input, keys) # 256x600
t = generate_t(data) # 600 x 55
max, key = find_best_match(h, t)

print(f'Max pearson: {max}')
print(f'Best key-match: {key}')