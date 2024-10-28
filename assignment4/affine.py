import sys

def affine_encrypt(text, a, b, outputFile):
  """
  encrypts the plaintext 'text', using an affine transformation key (a, b)
  :param text: str type; plaintext as a string of letters
  :param a: int type; #integer satisfying gcd(a, 29) = 1
  :param b: int type; shift value
  :param outputFile: str type; a string of output file name
  """
  text = text.lower()
  codeTable = "abcdefghijklmnopqrstuvwxyz,. "
  cipherText = ""
  for letter in text:
    if letter in codeTable:
      # Convert letter to its corresponding number (‘A’=0, ‘B’=1, ‘C’=2 ...)
      num = codeTable.index(letter)
      # Apply the affine transformation: (a * num + b) % 29
      cipher = codeTable[(a * num + b) % 29]
    else:
      cipher = letter
    # Append the encrypted letter to the cipher text
    cipherText += cipher
    # Write cipherText to outputFile
    with open(outputFile, "w") as file:
      file.write(cipherText)
# --------------------------------------------------------------------------


def extended_gcd(a, b):
  if (a == 0):
    return b, 0, 1
  gcd, x1, y1 = extended_gcd(b % a, a)
  x = y1 - (b // a) * x1
  y = x1
  return gcd, x, y

def affine_decrypt(inputFile, a, b):
  """
  decrypts the given cipher, assuming it was encrypted using an affine
  transformation key (a, b)
  :param inputFile: str type; a string of input file name
  :param a: int type; #integer satisfying gcd(a, 29) = 1.
  :param b: int type; shift value
  :return: str type; the decrypted message (as a string of uppercase letters)
  """
  # Read cipherText from file
  with open(inputFile, "r") as file:
    cipherText = file.read()
  _, a_inv, _ = extended_gcd(a, 29) # a_inv holds the inverse of a under modulo 29
  a_inv = a_inv % 29

  codeTable = "abcdefghijklmnopqrstuvwxyz,. "
  text = ""
  for cipher in cipherText:
    if cipher in codeTable:
      # Convert letter to its corresponding number (‘A’=0, ‘B’=1, ‘C’=2 ...)
      num = codeTable.index(cipher)
      # Apply the affine_transformation-1: (a_*(C-b)) % 29
      letter = codeTable[(a_inv * (num - b)) % 29]
    else:
      letter = cipher
  # Append the letter to the text
    text += letter
  return text

if __name__ == "__main__" : 
  if len(sys.argv) != 6:
    raise TypeError("Invalid Arguments. Proper arguments: plaintext_file_name a b cipher_file_name plaintext_decrypted_name")
  else:
    infile, outfile1, outfile2 = sys.argv[1], sys.argv[4], sys.argv[5]
    a, b = int(sys.argv[2]), int(sys.argv[3])
    with open(infile, "r") as file:
      plain = file.read()

    affine_encrypt(plain, a, b, outfile1)

    plaintext = affine_decrypt(outfile1, a, b)
    with open(outfile2, "w") as file:
      file.write(plaintext)
