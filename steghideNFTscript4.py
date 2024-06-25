import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
from stegano import lsb
import logging
from datetime import datetime

# Set up logging
# logging.basicConfig(filename='stegHideNFT.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StegHideNFTApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("StegHideNFT App")
        self.geometry("600x600")
        self.resizable(False, False)

        self.image_path = None
        self.mode = tk.StringVar(value="encryption")  # Default mode

        self.create_canvas()
        self.set_background()
        self.create_widgets()

    def create_canvas(self):
        # Create a canvas and set the background image
        self.canvas = tk.Canvas(self, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)

    def set_background(self):
        # Load the background image
        try:
            image_path = 'C:/Users/matto/Desktop/steghideNFT.png'  # Change this to the correct path of your image
            image = Image.open(image_path)
            image = image.resize((600, 600), Image.LANCZOS)  # Resize to fit the window
            self.background_photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        except Exception as e:
            logging.error(f'Error loading background image: {e}')
            print(f"Error loading background image: {e}")

    def create_widgets(self):
        # Create a frame for the widgets with a transparent background
        self.frame = tk.Frame(self.canvas, bg="#003B6F", relief='raised', bd=2)  # UCSD Blue color
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        # File selection label
        self.label = tk.Label(self.frame, text="Drag and drop an image here:", bg="#003B6F", fg="white", font=("Arial", 12))
        self.label.pack(pady=10)

        # Drop zone for drag and drop
        self.drop_zone = tk.Label(self.frame, text="Drop Zone", bg="#005691", fg="white", width=40, height=10)
        self.drop_zone.pack(pady=5)
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', self.drop_image)

        self.btn_browse = tk.Button(self.frame, text="Browse Image", command=self.browse_image, bg="#0072BB", fg="white")
        self.btn_browse.pack(pady=5)

        # Mode selection
        self.frame_mode = tk.Frame(self.frame, bg="#003B6F")
        self.frame_mode.pack(pady=10)

        self.radio_encryption = tk.Radiobutton(self.frame_mode, text="Encryption", variable=self.mode, value="encryption", bg="#003B6F", fg="white", selectcolor="black", font=("Arial", 12), indicatoron=0, width=10, height=1, padx=10, pady=5, relief="raised")
        self.radio_encryption.pack(side=tk.LEFT)

        self.radio_decryption = tk.Radiobutton(self.frame_mode, text="Decryption", variable=self.mode, value="decryption", bg="#003B6F", fg="white", selectcolor="black", font=("Arial", 12), indicatoron=0, width=10, height=1, padx=10, pady=5, relief="raised")
        self.radio_decryption.pack(side=tk.LEFT)

        # Secret message entry
        self.secret_message_label = tk.Label(self.frame, text="Enter secret message:", bg="#003B6F", fg="white", font=("Arial", 12))
        self.secret_message_label.pack(pady=5)

        self.secret_message_entry = tk.Entry(self.frame, width=50)
        self.secret_message_entry.pack(pady=5)

        # Process button
        self.btn_process = tk.Button(self.frame, text="Process", command=self.process_image, bg="#0072BB", fg="white")
        self.btn_process.pack(pady=10)

        # Initially hide the secret message entry for decryption mode
        self.update_mode()

    def update_mode(self):
        if self.mode.get() == "encryption":
            self.secret_message_label.pack(pady=5)
            self.secret_message_entry.pack(pady=5)
        else:
            self.secret_message_label.pack_forget()
            self.secret_message_entry.pack_forget()

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.update_drop_zone()

    def drop_image(self, event):
        file_path = event.data
        # Remove braces if present
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        self.image_path = file_path
        self.update_drop_zone()

    def update_drop_zone(self):
        if self.image_path:
            image = Image.open(self.image_path)
            image.thumbnail((300, 300))  # Resize large images for display
            photo = ImageTk.PhotoImage(image)
            self.drop_zone.config(image=photo, bg="#005691")
            self.drop_zone.image = photo
            self.label.config(text="")

    def process_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image selected!")
            return

        if self.mode.get() == "encryption":
            secret_data = self.secret_message_entry.get()
            if not secret_data:
                messagebox.showerror("Error", "No secret message entered!")
                return
            encrypted_image = lsb.hide(self.image_path, secret_data)
            encrypted_image.save("encrypted_image.png")
            messagebox.showinfo("Success", "Encryption successful! Image saved as 'encrypted_image.png'")
        elif self.mode.get() == "decryption":
            decrypted_data = lsb.reveal(self.image_path)
            if decrypted_data is None:
                messagebox.showerror("Error", "No hidden data found in the image.")
            else:
                self.secret_message_entry.delete(0, tk.END)
                self.secret_message_entry.insert(0, decrypted_data)
                messagebox.showinfo("Decrypted Data", decrypted_data)

if __name__ == "__main__":
    app = StegHideNFTApp()
    app.mainloop()
