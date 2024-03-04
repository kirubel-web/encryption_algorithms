import numpy as np
import tkinter as tk
from tkinter import messagebox

class HillCipherGUI:
    """
    A graphical user interface for the Hill Cipher encryption and decryption algorithm.

    Attributes:
        master (tk.Tk): The root window of the GUI.
        key_size_label (tk.Label): The label for entering the key size.
        key_size_entry (tk.Entry): The entry field for entering the key size.
        key_size_button (tk.Button): The button for generating key entries.
        key_entries (list): A 2D list of Entry fields for entering the key matrix.
        key_label (list): A list of labels for displaying the key matrix.
        plain_text_label (tk.Label): The label for entering the plain text.
        plain_text_entry (tk.Entry): The entry field for entering the plain text.
        encrypt_button (tk.Button): The button for encrypting the plain text.
        decrypt_button (tk.Button): The button for decrypting the cipher text.
        result_label (tk.Label): The label for displaying the result (encrypted or decrypted text).

    Methods:
        create_key_entries: Creates the Entry fields for entering the key matrix based on the key size.
        prepare_key: Prepares the key matrix from the entered values and performs error checking.
        prepare_text: Prepares the plain text or cipher text for encryption or decryption.
        encrypt_text: Encrypts the plain text using the Hill Cipher algorithm.
        modinv: Calculates the modular inverse of a number.
        decrypt_text: Decrypts the cipher text using the Hill Cipher algorithm.
    """

    def __init__(self, master):
        self.master = master
        self.master.title("Hill Cipher")

        self.key_size_label = tk.Label(master, text="Enter Key Size (2-8):")
        self.key_size_label.grid(row=0, column=0, padx=5, pady=5)

        self.key_size_entry = tk.Entry(master)
        self.key_size_entry.grid(row=0, column=1, padx=5, pady=5)

        self.key_size_button = tk.Button(master, text="Generate Key Entries", command=self.create_key_entries)
        self.key_size_button.grid(row=0, column=2, padx=5, pady=5)

        self.key_entries = []
        self.key_label = []

        self.plain_text_label = tk.Label(master, text="Enter Plain Text:")
        self.plain_text_label.grid(row=9, column=0, padx=5, pady=5)

        self.plain_text_entry = tk.Entry(master)
        self.plain_text_entry.grid(row=9, column=1, columnspan=2, padx=5, pady=5)
        self.encrypt_button = tk.Button(master, text="Encrypt", command=self.encrypt_text)
        self.encrypt_button.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

        self.decrypt_button = tk.Button(master, text="Decrypt", command=self.decrypt_text)
        self.decrypt_button.grid(row=11, column=0, columnspan=3, padx=5, pady=5)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=12, column=0, columnspan=3, padx=5, pady=5)

    def create_key_entries(self):
        """
        Creates the Entry fields for entering the key matrix based on the key size.

        Raises:
            ValueError: If the entered key size is not a valid integer or is not between 2 and 8.
        """
        try:
            size = int(self.key_size_entry.get())
            if size < 2 or size > 8:
                messagebox.showerror("Error", "Key size must be between 2 and 8.")
                return
            for i in range(size):
                row = []
                for j in range(size):
                    entry = tk.Entry(self.master, width=5)
                    entry.grid(row=i+1, column=j, padx=5, pady=5)
                    row.append(entry)
                self.key_entries.append(row)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid key size.")

    def prepare_key(self):
        """
        Prepares the key matrix from the entered values and performs error checking.

        Returns:
            numpy.ndarray: The key matrix if it is valid, None otherwise.
        """
        key_matrix = []
        for row in self.key_entries:
            for entry in row:
                try:
                    val = int(entry.get())
                    key_matrix.append(val)
                except ValueError:
                    messagebox.showerror("Error", "Key must be integer values.")
                    return None
        size = len(self.key_entries)
        key_matrix = np.array(key_matrix).reshape(size, size)
        if np.linalg.det(key_matrix) == 0:
            messagebox.showerror("Error", "Key matrix is singular. Please enter a valid key.")
            return None
        return key_matrix

    def prepare_text(self, text):
        """
        Prepares the plain text or cipher text for encryption or decryption.

        Args:
            text (str): The plain text or cipher text to be prepared.

        Returns:
            list: A list of integers representing the prepared text.
        """
        text = text.replace(" ", "").upper()
        while len(text) % len(self.key_entries) != 0:
            text += 'X'
        return [ord(char) - 65 for char in text]

    def encrypt_text(self):
        """
        Encrypts the plain text using the Hill Cipher algorithm.
        """
        key = self.prepare_key()
        if key is None:
            return

        plain_text = self.plain_text_entry.get()
        if not plain_text:
            messagebox.showerror("Error", "Please enter plain text.")
            return

        plain_text = self.prepare_text(plain_text)
        cipher_text = ""

        for i in range(0, len(plain_text), len(key)):
            chunk = np.array(plain_text[i:i+len(key)])
            result = np.dot(key, chunk) % 26
            for val in result:
                cipher_text += chr(val + 65)

        self.result_label.config(text="Encrypted Text: " + cipher_text)

    def modinv(self, a, m):
        """
        Calculates the modular inverse of a number.

        Args:
            a (int): The number for which the modular inverse is to be calculated.
            m (int): The modulus.

        Returns:
            int or None: The modular inverse of a if it exists, None otherwise.
        """
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    def decrypt_text(self):
        """
        Decrypts the cipher text using the Hill Cipher algorithm.
        """
        key = self.prepare_key()
        if key is None:
            return

        key_inv = np.linalg.inv(key)
        det = int(round(np.linalg.det(key)))
        det_inv = self.modinv(det, 26)

        if det_inv is None:
            messagebox.showerror("Error", "Determinant has no multiplicative inverse modulo 26. Key is not invertible.")
            return

        key_inv_det_inv = (key_inv * det * det_inv) % 26

        cipher_text = self.plain_text_entry.get()
        if not cipher_text:
            messagebox.showerror("Error", "Please enter cipher text.")
            return

        cipher_text = self.prepare_text(cipher_text)
        decrypted_text = ""

        for i in range(0, len(cipher_text), len(key)):
            chunk = np.array(cipher_text[i:i+len(key)])
            result = np.dot(key_inv_det_inv, chunk) % 26
            for val in result:
                decrypted_text += chr(val + 65)

        self.result_label.config(text="Decrypted Text: " + decrypted_text)

def main():
    root = tk.Tk()
    hill_cipher_gui = HillCipherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
