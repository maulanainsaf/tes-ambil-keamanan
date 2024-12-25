import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# Fungsi untuk menyisipkan pesan
def encode_message():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.bmp;*.jpg;*.jpeg")])
        if not file_path:
            return

        image = Image.open(file_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        message = message_entry.get("1.0", tk.END).strip()

        if not message:
            messagebox.showerror("Error", "Pesan tidak boleh kosong!")
            return

        encoded_image = encode_image(image, message)
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if save_path:
            encoded_image.save(save_path)
            messagebox.showinfo("Sukses", "Pesan berhasil disisipkan!")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Fungsi untuk membaca pesan
def decode_message():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.bmp;*.jpg;*.jpeg")])
        if not file_path:
            return

        image = Image.open(file_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        message = decode_image(image)

        if message:
            message_entry.delete("1.0", tk.END)
            message_entry.insert(tk.END, message)
            messagebox.showinfo("Sukses", "Pesan berhasil dibaca!")
        else:
            messagebox.showinfo("Info", "Tidak ada pesan yang ditemukan.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Fungsi untuk menyisipkan pesan ke dalam gambar
def encode_image(image, message):
    encoded = image.copy()
    width, height = image.size
    pixels = encoded.load()

    message += "\0"  # Penanda akhir pesan
    binary_message = ''.join([format(ord(char), '08b') for char in message])

    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index < len(binary_message):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary_message[data_index])
                data_index += 1
                pixels[x, y] = (r, g, b)

    if data_index < len(binary_message):
        raise ValueError("Gambar terlalu kecil untuk menyisipkan pesan.")

    return encoded

# Fungsi untuk membaca pesan dari gambar
def decode_image(image):
    pixels = image.load()
    width, height = image.size

    binary_message = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)

    # Mengonversi pesan biner ke teks
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = "".join([chr(int(char, 2)) for char in chars])

    # Memotong pesan pada penanda akhir \0
    return message.split("\0")[0]

# GUI Setup
root = tk.Tk()
root.title("Steganografi - LSB Method")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

# Label dan Text untuk pesan
tk.Label(frame, text="Pesan Rahasia:").pack(anchor=tk.W)
message_entry = tk.Text(frame, height=5, width=40)
message_entry.pack(pady=5)

# Tombol untuk Encode dan Decode
button_frame = tk.Frame(frame)
button_frame.pack(pady=10)

encode_button = tk.Button(button_frame, text="Sisipkan Pesan", command=encode_message, bg="lightblue")
encode_button.pack(side=tk.LEFT, padx=10)

decode_button = tk.Button(button_frame, text="Baca Pesan", command=decode_message, bg="lightgreen")
decode_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
