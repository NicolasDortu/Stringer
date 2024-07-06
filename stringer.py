import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from libstringer import *


class StringManipulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("String Manipulation Utilities")
        self.create_widgets()

    def create_widgets(self):
        # Text area for input
        self.input_text = tk.Text(self.root, height=10, width=50)
        self.input_text.pack()

        # Buttons for string manipulation functions
        self.reverse_button = tk.Button(
            self.root, text="Reverse String", command=self.reverse_string
        )
        self.reverse_button.pack()

        self.concat_button = tk.Button(
            self.root, text="Concatenate Strings", command=self.concatenate_strings
        )
        self.concat_button.pack()

        self.find_button = tk.Button(
            self.root, text="Find Substring", command=self.find_substring
        )
        self.find_button.pack()

        self.upper_button = tk.Button(
            self.root, text="To Uppercase", command=self.to_uppercase
        )
        self.upper_button.pack()

        self.lower_button = tk.Button(
            self.root, text="To Lowercase", command=self.to_lowercase
        )
        self.lower_button.pack()

        # Text area for output
        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.pack()

    def get_input_text(self):
        return self.input_text.get("1.0", tk.END).strip()

    def set_output_text(self, text):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)

    def reverse_string(self):
        text = self.get_input_text()
        threading.Thread(target=self.run_reverse_string, args=(text,)).start()

    def run_reverse_string(self, text):
        result = reverse_string(text)
        self.root.after(0, lambda: self.set_output_text(result))

    def concatenate_strings(self):
        text1 = self.get_input_text()
        text2 = simpledialog.askstring("Input", "Enter the string to concatenate:")
        threading.Thread(
            target=self.run_concatenate_strings, args=(text1, text2)
        ).start()

    def run_concatenate_strings(self, text1, text2):
        result = concatenate_strings(text1, text2)
        self.root.after(0, lambda: self.set_output_text(result))

    def find_substring(self):
        text = self.get_input_text()
        substr = simpledialog.askstring("Input", "Enter the substring to find:")
        threading.Thread(target=self.run_find_substring, args=(text, substr)).start()

    def run_find_substring(self, text, substr):
        index = find_substring(text, substr)
        result = (
            f"Substring found at index: {index}"
            if index != -1
            else "Substring not found"
        )
        self.root.after(0, lambda: self.set_output_text(result))

    def to_uppercase(self):
        text = self.get_input_text()
        threading.Thread(target=self.run_to_uppercase, args=(text,)).start()

    def run_to_uppercase(self, text):
        result = to_uppercase(text)
        self.root.after(0, lambda: self.set_output_text(result))

    def to_lowercase(self):
        text = self.get_input_text()
        threading.Thread(target=self.run_to_lowercase, args=(text,)).start()

    def run_to_lowercase(self, text):
        result = to_lowercase(text)
        self.root.after(0, lambda: self.set_output_text(result))


if __name__ == "__main__":
    root = tk.Tk()
    app = StringManipulationGUI(root)
    root.mainloop()
