import os

# Common words used for scoring brute-force results
COMMON_WORDS = {"the", "and", "you", "that", "have", "is", "for", "not", "are", "this", "but", "with", "hello", "to", "a"}

def caesar_cipher(text, shift, mode):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            offset = (ord(char) - start + (shift if mode == 'encrypt' else -shift)) % 26
            result += chr(start + offset)
        else:
            result += char
    return result

def score_text(text):
    words = text.lower().split()
    return sum(1 for word in words if word.strip(",.!?") in COMMON_WORDS)

def brute_force_decrypt(encrypted_text):
    print("\n🔍 Brute-force Decryption Attempt:\n")
    best_score = 0
    best_result = ""
    for shift in range(1, 26):
        decrypted = caesar_cipher(encrypted_text, shift, 'decrypt')
        score = score_text(decrypted)
        print(f"[Shift {shift:2}] {decrypted[:60]}...")
        if score > best_score:
            best_score = score
            best_result = decrypted

    print("\n💡 Most likely correct decryption:")
    print(best_result)
    return best_result

def process_file(filepath, shift, mode, password=None):
    if not os.path.isfile(filepath):
        return None, f"File '{filepath}' not found."

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    if mode == 'decrypt':
        # Check password
        if content.startswith("::PWD::"):
            lines = content.split('\n', 1)
            stored_password = lines[0][7:].strip()
            if password != stored_password:
                return None, "❌ Incorrect password. Cannot decrypt."
            content = lines[1]

    if mode == 'encrypt':
        content = f"::PWD::{password}\n{content}"

    result = caesar_cipher(content, shift, mode)

    output_file = f"{mode}ed_output.txt"
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(result)

    return output_file, None

def main():
    print("=== Caesar Cipher Tool ===")
    history = []

    while True:
        print("\nOptions: encrypt | decrypt | file | brute | history | exit")
        mode = input("Choose mode: ").strip().lower()

        if mode == 'exit':
            print("Goodbye!")
            break
        elif mode == 'history':
            print("\n--- History ---")
            for h in history:
                print(h)
            continue
        elif mode == 'brute':
            msg = input("Enter the encrypted message: ")
            brute_force_decrypt(msg)
            history.append("Brute-force attempted.")
            continue
        elif mode == 'file':
            file_path = input("Enter path to the text file: ").strip()
            mode2 = input("Encrypt or Decrypt the file? ").strip().lower()
            if mode2 not in ['encrypt', 'decrypt']:
                print("Invalid operation.")
                continue

            try:
                shift = int(input("Enter shift value: "))
            except ValueError:
                print("Shift must be an integer.")
                continue

            password = input("Enter password: ")

            output_file, error = process_file(file_path, shift, mode2, password)
            if error:
                print("Error:", error)
            else:
                print(f"File processed. Output saved to: {output_file}")
                history.append(f"{mode2.title()}ed file '{file_path}' with shift {shift}")
            continue

        elif mode not in ['encrypt', 'decrypt']:
            print("Invalid mode.")
            continue

        msg = input("Enter your message: ")
        try:
            shift = int(input("Enter shift value: "))
        except ValueError:
            print("Shift must be an integer.")
            continue

        password = input("Enter password: ").strip()
        if mode == 'encrypt':
            msg = f"::PWD::{password}\n{msg}"
        elif mode == 'decrypt':
            if not msg.startswith("::PWD::"):
                print("⚠️ Warning: Message doesn't contain password header. Cannot check.")
            else:
                stored_pwd = msg.split('\n', 1)[0][7:].strip()
                if stored_pwd != password:
                    print("❌ Incorrect password. Cannot decrypt.")
                    continue
                msg = msg.split('\n', 1)[1]

        result = caesar_cipher(msg, shift, mode)
        print(f"\nResult ({mode}ed): {result}")
        history.append(f"{mode.title()}ed message with shift {shift}")

if __name__ == "__main__":
    main()
