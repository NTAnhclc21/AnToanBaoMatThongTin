import sys
from math import gcd
import ast

# Bảng mã 29 ký tự
CODETABLE = "abcdefghijklmnopqrstuvwxyz,. "

# Hàm tính nghịch đảo modulo
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Hàm giải mã với khóa (a, b)
def affine_decrypt(cipherText, a, b):
    a_inv = mod_inverse(a, 29)
    if a_inv is None:
        return None
    text = ""
    for char in cipherText:
        if char in CODETABLE:
            num = CODETABLE.index(char)
            decrypted_char = CODETABLE[(a_inv * (num - b)) % 29]
            text += decrypted_char
        else:
            text += char
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
