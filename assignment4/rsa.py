import random
import sys
from sympy import isprime

def gcd(a, b):
    """Helper function to compute Greatest Common Divisor"""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
  if (a == 0):
    return b, 0, 1
  gcd, x1, y1 = extended_gcd(b % a, a)
  x = y1 - (b // a) * x1
  y = x1
  return gcd, x, y

"""
Generate the RSA key
:param p: int type; prime number used as part of the key n = p * q to encrypt the ciphertext
:param q: int type; prime number used as part of the key n = p * q to encrypt the ciphertext
:return: tuple type; publicKey=(n,e) and privateKey=(n,d)
"""
def generate_rsa_keys(p, q):
  if not (isprime(p) and isprime(q)):
    raise ValueError("p or q is not prime.")
  n = p * q
  phi = (p - 1) * (q - 1)
  e = random.choice([x for x in range(2, phi) if gcd(x, phi) == 1])
  _, d, _ = extended_gcd(e, phi) # Compute the inverse of e (mod phi)
  d = d % phi # Ensure d is positive
  publicKey = (n, e)
  privateKey = (n, d)
  return publicKey, privateKey
"""
encrypts the plainText using RSA and the key (p*q, e)
:param plainText: str type; the orignal message as a string of letters
:param publicKey: tuple type; the key (n, e) to encrypt the plainText
:param outputFile: str type; a string of output file name
"""
def rsa_encrypt(plainText, publicKey, outputFile):
  n, e = publicKey
  plainTextBytes = [ord(char) for char in plainText]
  cipherText = [pow(byte, e, n) for byte in plainTextBytes]
  with open(outputFile, "w") as file:
     file.write(','.join(map(str, cipherText)))
"""
decrypts the cipherText in the inputFile, which was encrypted using RSA and the key (p*q, e)
:param inputFile: str type; as a string of input file name
:param privateKey: tuple type; the key (n, d) to decrypt the ciphertext
:return: str type; the decrypted message as a string of letters
"""
def rsa_decrypt(inputFile, privateKey):
  n, d = privateKey
  with open(inputFile, 'r') as file:
    cipherText = [int(x) for x in file.read().split(',')]
  decryptedBytes = [pow(char, d, n) for char in cipherText]
  plainText = ''.join([chr(byte) for byte in decryptedBytes])
  return plainText

if __name__ == "__main__":
  if len(sys.argv) != 6:
    raise TypeError("Invalid Arguments. Proper arguments: plaintext_file_name p q cipher_file_name plaintext_decrypted_name")
  infile, outfile1, outfile2 = sys.argv[1], sys.argv[4], sys.argv[5]
  p, q = int(sys.argv[2]), int(sys.argv[3])
  publicKey, privateKey = generate_rsa_keys(p, q)
  with open(infile, "r") as file:
    plainText = file.read()
  rsa_encrypt(plainText, publicKey, outfile1)

  dec_plaintext = rsa_decrypt(outfile1, privateKey)
  with open(outfile2, "w") as file:
    file.write(dec_plaintext)