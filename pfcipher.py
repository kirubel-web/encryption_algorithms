import tkinter as tk
from tkinter import messagebox

class PlayfairCipherGUI:
    # This is initial page text label will be updated.
    def __init__(self, master):
        self.master = master
        self.master.title("Playfair Cipher")

        self.key_label = tk.Label(master, text="Enter Key:")
        self.key_label.grid(row=0, column=0, padx=5, pady=5)

        self.key_entry = tk.Entry(master)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)

        self.plain_text_label = tk.Label(master, text="Enter Plain Text:")
        self.plain_text_label.grid(row=1, column=0, padx=5, pady=5)

        self.plain_text_entry = tk.Entry(master)
        self.plain_text_entry.grid(row=1, column=1, padx=5, pady=5)

        self.encrypt_button = tk.Button(master, text="Encrypt", command=self.encrypt_text)
        self.encrypt_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.decrypt_button = tk.Button(master, text="Decrypt", command=self.decrypt_text)
        self.decrypt_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def prepare_key(self, key):
        key = key.replace(" ", "").upper() # replace space with nothing and change to upper.
        print(type(key))
        key_without_duplicates = "".join(dict.fromkeys(key))
        print(key_without_duplicates)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in key_without_duplicates:
            alphabet = alphabet.replace(char, "")
        print(key_without_duplicates + alphabet)
        return key_without_duplicates + alphabet

    def prepare_text(self, text):
        text = text.replace(" ", "").upper() # replace space with nothing and change to upper.
        # Replace 'J' with 'I'
        text = text.replace("J", "I")
        # Split text into digraphs
        digraphs = []
        i = 0
        while i < len(text):
            if i == len(text) - 1 or text[i] == text[i+1]:
                digraphs.append(text[i] + "X")
                i += 1
            else:
                digraphs.append(text[i:i+2])
                i += 2
        return digraphs

    def generate_matrix(self, key):
        matrix = [[0]*5 for _ in range(5)]
        key = self.prepare_key(key)
        k = 0
        for i in range(5):
            for j in range(5):
                matrix[i][j] = key[k]
                k += 1
        return matrix

    def find_position(self, matrix, char):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return i, j

    def encrypt_pair(self, matrix, pair):
        a_row, a_col = self.find_position(matrix, pair[0])
        b_row, b_col = self.find_position(matrix, pair[1])

        if a_row == b_row:  # same row
            return matrix[a_row][(a_col + 1) % 5] + matrix[b_row][(b_col + 1) % 5]
        elif a_col == b_col:  # same column
            return matrix[(a_row + 1) % 5][a_col] + matrix[(b_row + 1) % 5][b_col]
        else:  # rectangle
            return matrix[a_row][b_col] + matrix[b_row][a_col]

    def encrypt_text(self):
        key = self.key_entry.get()
        plain_text = self.plain_text_entry.get()

        if not key or not plain_text:
            messagebox.showerror("Error", "Please enter both key and plain text.")
            return

        matrix = self.generate_matrix(key)
        prepared_text = self.prepare_text(plain_text)

        encrypted_text = ""
        for pair in prepared_text:
            encrypted_text += self.encrypt_pair(matrix, pair)

        self.result_label.config(text="Encrypted Text: " + encrypted_text)

    def decrypt_text(self):
        key = self.key_entry.get()
        cipher_text = self.plain_text_entry.get()

        if not key or not cipher_text:
            messagebox.showerror("Error", "Please enter both key and cipher text.")
            return

        matrix = self.generate_matrix(key)
        prepared_text = self.prepare_text(cipher_text)

        decrypted_text = ""
        for pair in prepared_text:
            decrypted_text += self.decrypt_pair(matrix, pair)

        self.result_label.config(text="Decrypted Text: " + decrypted_text)

    def decrypt_pair(self, matrix, pair):
        a_row, a_col = self.find_position(matrix, pair[0])
        b_row, b_col = self.find_position(matrix, pair[1])

        if a_row == b_row:  # same row
            return matrix[a_row][(a_col - 1) % 5] + matrix[b_row][(b_col - 1) % 5]
        elif a_col == b_col:  # same column
            return matrix[(a_row - 1) % 5][a_col] + matrix[(b_row - 1) % 5][b_col]
        else:  # rectangle
            return matrix[a_row][b_col] + matrix[b_row][a_col]

def main():
    root = tk.Tk()
    playfair_cipher_gui = PlayfairCipherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
