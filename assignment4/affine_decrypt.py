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
    # Đọc nội dung mã hóa từ tệp
    with open(inputFile, "r") as file:
        cipherText = file.read()
    
    _, a_inv, _ = extended_gcd(a, 29)
    a_inv = a_inv % 29

    codeTable = "abcdefghijklmnopqrstuvwxyz,. "
    text = ""
    for cipher in cipherText:
        if cipher in codeTable:
            num = codeTable.index(cipher)
            letter = codeTable[(a_inv * (num - b)) % 29]
        else:
            letter = cipher
        text += letter
    return text

# Kiểm tra văn bản tiếng Anh
def is_english_text(text):
    common_words = ['the', 'and', 'is', 'in', 'to', 'hello', 'you', 'i', 'he', 'she', 'it',
                    'we', 'they', 'there', 'have', 'do', 'say', 'go', 'can', 'will', 'would']
    for word in common_words:
        if word in text:
            return True
    return False

# Vét cạn các giá trị của (a, b) và kiểm tra nội dung
def brute_force_affine(cipherText):
    results = []
    for a in range(1, 29):
        if gcd(a, 29) == 1:
            for b in range(29):
                decrypted_text = affine_decrypt(cipherText, a, b)
                if decrypted_text and is_english_text(decrypted_text):
                    print(f"Phát hiện văn bản tiếng Anh hợp lệ với khóa: a={a}, b={b}")
                    print("Nội dung giải mã:", decrypted_text)
                    results.append((a, b, decrypted_text))
    
    if not results:
        print("Không tìm thấy khóa phù hợp.")
    return results

# Đọc tập tin mã hóa và thực hiện giải mã
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise TypeError("Cần truyền vào 1 đối số: tên tập tin mã hóa.")
    encrypted_file = sys.argv[1]
    
    # Thực hiện vét cạn và kiểm tra nội dung
    brute_force_affine(encrypted_file)
