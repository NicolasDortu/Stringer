import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from libstringer import *


class StringManipulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stringer")
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

        self.replace_eol_button = tk.Button(
            self.root, text="Replace End of Line", command=self.replace_end_of_line
        )
        self.replace_eol_button.pack()

        self.replace_start_button = tk.Button(
            self.root, text="Replace Start of Line", command=self.replace_start_of_line
        )
        self.replace_start_button.pack()

        self.replace_sequence_button = tk.Button(
            self.root, text="Replace Sequence", command=self.replace_sequence
        )
        self.replace_sequence_button.pack()

        self.replace_all_newlines_button = tk.Button(
            self.root, text="Replace All Newlines", command=self.replace_all_newlines
        )
        self.replace_all_newlines_button.pack()

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

    def replace_end_of_line(self):
        text = self.get_input_text()
        replacement = simpledialog.askstring(
            "Input", "Enter the replacement text for end of line:"
        )
        threading.Thread(
            target=self.run_replace_end_of_line, args=(text, replacement)
        ).start()

    def run_replace_end_of_line(self, text, replacement):
        result = replace_end_of_line(text, replacement)
        self.root.after(0, lambda: self.set_output_text(result))

    def replace_all_newlines(self):
        text = self.get_input_text()
        replacement = simpledialog.askstring(
            "Input", "Enter the replacement text for all newlines:"
        )
        threading.Thread(
            target=self.run_replace_all_newlines, args=(text, replacement)
        ).start()

    def run_replace_all_newlines(self, text, replacement):
        result = replace_all_newlines(text, replacement)
        self.root.after(0, lambda: self.set_output_text(result))

    def replace_start_of_line(self):
        text = self.get_input_text()
        replacement = simpledialog.askstring(
            "Input", "Enter the replacement text for start of line:"
        )
        threading.Thread(
            target=self.run_replace_start_of_line, args=(text, replacement)
        ).start()

    def run_replace_start_of_line(self, text, replacement):
        result = replace_start_of_line(text, replacement)
        self.root.after(0, lambda: self.set_output_text(result))

    def replace_sequence(self):
        text = self.get_input_text()
        sequence = simpledialog.askstring("Input", "Enter the sequence to replace:")
        replacement = simpledialog.askstring("Input", "Enter the replacement text:")
        threading.Thread(
            target=self.run_replace_sequence, args=(text, sequence, replacement)
        ).start()

    def run_replace_sequence(self, text, sequence, replacement):
        result = replace_sequence(text, sequence, replacement)
        self.root.after(0, lambda: self.set_output_text(result))


if __name__ == "__main__":
    root = tk.Tk()
    app = StringManipulationGUI(root)
    root.mainloop()
