import os
import json
import hashlib

FILE_PATH = "users.json"

def create_hash(password, algorithm):
    """Fungsi untuk membuat hash berdasarkan algoritma yang dipilih"""
    encoded_password = password.encode('utf-8')
    if algorithm == 'md5':
        return hashlib.md5(encoded_password).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(encoded_password).hexdigest()
    return None

def load_users():
    """Membaca data user dari file JSON"""
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_users(users):
    """Menyimpan data user ke file JSON"""
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

def register_menu():
    print("\n--- REGISTRASI AKUN ---")
    username = input("Masukkan Username: ").strip()
    users = load_users()

    # Validasi apakah username sudah terdaftar
    if any(user['username'] == username for user in users):
        print("Error: Username sudah digunakan!")
        return

    password = input("Masukkan Password: ")
    print("\nPilih Algoritma Hashing:")
    print("1. MD5")
    print("2. SHA-256")
    algo_choice = input("Pilihan (1/2): ").strip()

    if algo_choice == '1':
        algorithm = 'md5'
    elif algo_choice == '2':
        algorithm = 'sha256'
    else:
        print("Pilihan algoritma tidak valid. Registrasi dibatalkan.")
        return

    # Proses Hashing
    hashed_password = create_hash(password, algorithm)

    # Menampilkan output sesuai ketentuan poin 4
    print("\n--- DETAIL DATA REGISTRASI ---")
    print(f"> Password Asli : {password}")
    print(f"> Algoritma     : {algorithm.upper()}")
    print(f"> Hasil Hash    : {hashed_password}")

    # Simpan ke database JSON dalam bentuk HASH (Poin 2 & 6)
    users.append({
        "username": username,
        "password": hashed_password,
        "algorithm": algorithm
    })
    save_users(users)
    print("\nRegistrasi Berhasil & Data Tersimpan!")

def login_menu():
    print("\n--- LOGIN PENGGUNA ---")
    username = input("Username: ").strip()
    password = input("Password: ")
    
    users = load_users()
    # Cari user berdasarkan username
    user = next((u for u in users if u['username'] == username), None)

    print("\n--- PROSES VERIFIKASI LOGIN ---")
    if not user:
        print("Hasil: Username tidak ditemukan. Login GAGAL.")
        return

    # Hashing password input menggunakan algoritma yang terdaftar di database
    hashed_input = create_hash(password, user['algorithm'])

    print(f"> Password Input (Asli) : {password}")
    print(f"> Hasil Hash Input       : {hashed_input}")
    print(f"> Hash di Database       : {user['password']}")

    # Proses Pencocokan Hash
    if hashed_input == user['password']:
        print("\nHasil: Password cocok. Login BERHASIL!")
    else:
        print("\nHasil: Password salah. Login GAGAL.")

def main():
    while True:
        print("\n=== SISTEM LOGIN KEAMANAN DATA ===")
        print("1. Registrasi Akun")
        print("2. Login Pengguna")
        print("3. Keluar")
        choice = input("Pilih menu (1-3): ").strip()

        if choice == '1':
            register_menu()
        elif choice == '2':
            login_menu()
        elif choice == '3':
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()