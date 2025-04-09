import secrets
import string

def generate_password(length, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True):
    """Membuat kata sandi aman dengan pilihan karakter yang dapat disesuaikan."""

    if length < 8:
        return "Panjang kata sandi minimal 8 karakter untuk keamanan."

    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return "Setidaknya satu jenis karakter harus dipilih."

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def main():
    """Fungsi utama untuk menangani input pengguna dan pembuatan kata sandi."""
    try:
        length = int(input("Masukkan panjang kata sandi yang diinginkan: "))
        if length < 1:
            print("Panjang harus berupa bilangan bulat positif.")
            return
        use_uppercase = input("Sertakan huruf besar? (y/n): ").lower() == 'y'
        use_lowercase = input("Sertakan huruf kecil? (y/n): ").lower() == 'y'
        use_digits = input("Sertakan angka? (y/n): ").lower() == 'y'
        use_symbols = input("Sertakan simbol?(y/n): ").lower() == 'y'

        password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols)

        if isinstance(password, str):
            print("Kata Sandi yang Dihasilkan:", password)
        else:
            print(password)

    except ValueError:
        print("Input tidak valid. Silakan masukkan bilangan bulat yang valid untuk panjang kata sandi.")

if __name__ == "__main__":
    main()
