import sys
from math import gcd
import ast

# Hàm tính nghịch đảo modulo
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

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

# Kiểm tra tính hợp lệ của mã nguồn Python
def is_python_source(text):
    try:
        source_code = text.decode('utf-8')
        ast.parse(source_code)
        return True
    except (UnicodeDecodeError, SyntaxError):
        return False

# Kiểm tra tính hợp lệ của văn bản tiếng Anh (đơn giản)
def is_english_text(text):
    common_words = ['the', 'and', 'is', 'in', 'to']
    for word in common_words:
        if word in text:  # text is already a string here
            return True
    return False

# Vét cạn các giá trị của (a, b)
def brute_force_affine(cipherText, check_function):
    results = []  # List to store valid keys and decrypted texts
    for a in range(1, 29):
        if gcd(a, 29) == 1:  # Ensure a has an inverse
            for b in range(29):
                decrypted_text = affine_decrypt(cipherText, a, b)
                if decrypted_text and check_function(decrypted_text):  # Use as a string
                    results.append((a, b, decrypted_text))  # Store the result
    # Print all valid keys and decrypted texts
    if results:
        for a, b, text in results:
            print(f"Khóa khả thi: a={a}, b={b}")
            print("Nội dung giải mã:", text)
    else:
        print("Không tìm thấy khóa phù hợp.")
    return results  # Return all results

# Đọc tập tin đã mã hóa và thực hiện giải mã
if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise TypeError("Cần truyền vào 2 đối số: tên tập tin mã hóa và loại nội dung (english/python).")
    encrypted_file = sys.argv[1]
    content_type = sys.argv[2]
    
    # Đọc nội dung mã hóa từ tệp
    with open(encrypted_file, "r") as file:
        cipherText = file.read()
    
    print("Ciphertext read from file:", cipherText)  # Debug line
    
    # Chọn hàm kiểm tra phù hợp
    if content_type == 'english':
        check_function = is_english_text
    elif content_type == 'python':
        check_function = is_python_source
    else:
        raise ValueError("Loại nội dung không hợp lệ. Chọn 'english' hoặc 'python'.")
    
    # Thực hiện vét cạn
    decrypted_text = brute_force_affine(cipherText, check_function)
    if decrypted_text:
        with open("decrypted_output.txt", "w") as file:
            file.write(decrypted_text)
