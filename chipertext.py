import tkinter as tk
from tkinter import ttk, messagebox

class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher")
        self.root.geometry("400x400")
        
        # Nilai pergeseran default
        self.shift_value = tk.IntVar(value=3)  # default shift 3

        # Frame untuk nilai pergeseran
        shift_frame = ttk.Frame(self.root)
        shift_frame.pack(pady=10)

        tk.Label(shift_frame, text="Jumlah Pergeseran:").pack(side=tk.LEFT)
        shift_spinbox = ttk.Spinbox(
            shift_frame,
            from_=1,
            to=25,
            width=5,
            textvariable=self.shift_value
        )
        shift_spinbox.pack(side=tk.LEFT, padx=5)

        # Label dan input untuk plainteks
        tk.Label(self.root, text="Masukkan Plainteks:").pack(pady=5)
        self.plaintext_input = tk.Text(self.root, height=5, width=50, wrap=tk.WORD)
        self.plaintext_input.pack(pady=5)

        # Frame untuk tombol enkripsi dan dekripsi
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        # Button enkripsi
        tk.Button(button_frame, text="Enkripsi", command=self.encrypt).pack(side=tk.LEFT, padx=10)

        # Button dekripsi
        tk.Button(button_frame, text="Dekripsi", command=self.decrypt).pack(side=tk.LEFT, padx=10)

        # Label dan input untuk cipherteks
        tk.Label(self.root, text="Cipherteks:").pack(pady=5)
        self.cipher_output = tk.Text(self.root, height=5, width=50, wrap=tk.WORD)
        self.cipher_output.pack(pady=5)

    def shift_character(self, char, shift, encrypt=True):
        if not char.isalpha():
            return char

        # Menentukan ASCII base (97 untuk lowercase, 65 untuk uppercase)
        ascii_base = 97 if char.islower() else 65

        # Jika dekripsi, balik arah pergeseran
        if not encrypt:
            shift = -shift

        # Lakukan pergeseran dan pastikan tetap dalam range alfabet (0-25)
        shifted = (ord(char) - ascii_base + shift) % 26

        # Kembalikan ke bentuk karakter
        return chr(shifted + ascii_base)

    def process_text(self, text, encrypt=True):
        shift = self.shift_value.get()
        result = ''

        for char in text:
            result += self.shift_character(char, shift, encrypt)

        return result

    def encrypt(self):
        # Ambil teks dari input
        plaintext = self.plaintext_input.get("1.0", tk.END).strip()

        # Proses enkripsi
        ciphertext = self.process_text(plaintext, encrypt=True)

        # Tampilkan hasil
        self.cipher_output.delete("1.0", tk.END)
        self.cipher_output.insert("1.0", ciphertext)

    def decrypt(self):
        # Ambil teks dari output cipher
        ciphertext = self.cipher_output.get("1.0", tk.END).strip()

        # Proses dekripsi
        plaintext = self.process_text(ciphertext, encrypt=False)

        # Tampilkan hasil
        self.plaintext_input.delete("1.0", tk.END)
        self.plaintext_input.insert("1.0", plaintext)

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherApp(root)
    root.mainloop()