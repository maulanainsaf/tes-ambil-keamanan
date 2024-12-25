import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

# Fungsi untuk enkripsi
def encrypt():
    try:
        key = key_entry.get().encode('utf-8')
        plaintext = plaintext_entry.get("1.0", tk.END).strip()

        if len(key) != 8:
            messagebox.showerror("Error", "Kunci harus 8 karakter!")
            return

        cipher = DES.new(key, DES.MODE_ECB)
        padded_text = pad(plaintext.encode('utf-8'), DES.block_size)
        encrypted_text = cipher.encrypt(padded_text)
        encrypted_base64 = base64.b64encode(encrypted_text).decode('utf-8')

        ciphertext_entry.delete("1.0", tk.END)
        ciphertext_entry.insert(tk.END, encrypted_base64)
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Fungsi untuk dekripsi
def decrypt():
    try:
        key = key_entry.get().encode('utf-8')
        ciphertext = ciphertext_entry.get("1.0", tk.END).strip()

        if len(key) != 8:
            messagebox.showerror("Error", "Kunci harus 8 karakter!")
            return

        cipher = DES.new(key, DES.MODE_ECB)
        encrypted_bytes = base64.b64decode(ciphertext)
        decrypted_text = unpad(cipher.decrypt(encrypted_bytes), DES.block_size)

        plaintext_entry.delete("1.0", tk.END)
        plaintext_entry.insert(tk.END, decrypted_text.decode('utf-8'))
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("DES Encryption/Decryption")

# Frame untuk input kunci
key_frame = tk.Frame(root)
key_frame.pack(pady=10)
tk.Label(key_frame, text="Kunci (8 karakter):").pack(side=tk.LEFT)
key_entry = tk.Entry(key_frame, show="*", width=20)
key_entry.pack(side=tk.LEFT, padx=5)

# Frame untuk plaintext
plaintext_frame = tk.Frame(root)
plaintext_frame.pack(pady=10)
tk.Label(plaintext_frame, text="Plaintext:").pack(anchor=tk.W)
plaintext_entry = tk.Text(plaintext_frame, height=5, width=50)
plaintext_entry.pack()

# Frame untuk ciphertext
ciphertext_frame = tk.Frame(root)
ciphertext_frame.pack(pady=10)
tk.Label(ciphertext_frame, text="Ciphertext:").pack(anchor=tk.W)
ciphertext_entry = tk.Text(ciphertext_frame, height=5, width=50)
ciphertext_entry.pack()

# Frame untuk tombol
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
encrypt_button = tk.Button(button_frame, text="Encrypt", command=encrypt, bg="lightblue")
encrypt_button.pack(side=tk.LEFT, padx=5)
decrypt_button = tk.Button(button_frame, text="Decrypt", command=decrypt, bg="lightgreen")
decrypt_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
