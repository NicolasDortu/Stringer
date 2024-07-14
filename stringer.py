import threading
import tkinter as tk
from tkinter import simpledialog
from libstringer import *


class StringerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stringer")
        self.root.iconbitmap(default="./resources/icon.ico")
        self.root.configure(background="azure")
        self.create_widgets()
        self.center_window()
        self.root.resizable(False, False)

    def create_widgets(self):
        # Text area for input
        self.input_text = tk.Text(
            self.root,
            background="whitesmoke",
            foreground="dimgrey",
            insertbackground="pink",
            selectforeground="pink",
            selectbackground="lemonchiffon",
            height=10,
            width=50,
        )
        self.input_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.input_text.insert(tk.INSERT, "Enter text here...")
        self.input_text.bind(
            "<FocusIn>",
            lambda event: (
                self.input_text.delete("1.0", tk.END)
                if self.input_text.get("1.0", tk.END).strip() == "Enter text here..."
                else None
            ),
        )

        self.import_button = tk.Button(
            self.root,
            text="Import File",
            command=self.import_file,
            background="Pink",
            font=("Arial", 10),
        )
        self.import_button.grid(row=1, columnspan=3, padx=10, pady=5, sticky="ew")

        # Buttons for string manipulation functions
        self.reverse_button = tk.Button(
            self.root,
            text="Reverse Text",
            command=self.reverse_string,
            background="lemonchiffon",
        )
        self.reverse_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.upper_button = tk.Button(
            self.root,
            text="To Uppercase",
            command=self.to_uppercase,
            background="lemonchiffon",
        )
        self.upper_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.lower_button = tk.Button(
            self.root,
            text="To Lowercase",
            command=self.to_lowercase,
            background="lemonchiffon",
        )
        self.lower_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        self.replace_eol_button = tk.Button(
            self.root,
            text="Replace End of Line",
            command=self.replace_end_of_line,
            background="lemonchiffon",
        )
        self.replace_eol_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.replace_start_button = tk.Button(
            self.root,
            text="Replace Start of Line",
            command=self.replace_start_of_line,
            background="lemonchiffon",
        )
        self.replace_start_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.sql_button = tk.Button(
            self.root,
            text="Format to SQL",
            command=self.sql_format,
            background="lemonchiffon",
        )
        self.sql_button.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

        self.replace_sequence_button = tk.Button(
            self.root,
            text="Replace Sequence",
            command=self.replace_sequence,
            background="lemonchiffon",
        )
        self.replace_sequence_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.find_all_button = tk.Button(
            self.root,
            text="Find All Matches",
            command=self.find_all_occurrences,
            background="lemonchiffon",
        )
        self.find_all_button.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.split_by_pattern_button = tk.Button(
            self.root,
            text="Split by Pattern",
            command=self.split_by_pattern,
            background="lemonchiffon",
        )
        self.split_by_pattern_button.grid(row=4, column=2, padx=10, pady=5, sticky="ew")

        # Text area for output
        self.output_text = tk.Text(
            self.root,
            background="whitesmoke",
            foreground="dimgrey",
            insertbackground="pink",
            selectforeground="pink",
            selectbackground="lemonchiffon",
            height=10,
            width=50,
        )
        self.output_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.copy_to_clipboard_button = tk.Button(
            self.root,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            background="lemonchiffon",
        )
        self.copy_to_clipboard_button.grid(
            row=6, column=1, padx=10, pady=10, sticky="ew"
        )

        self.edit_output_text_button = tk.Button(
            self.root,
            text="Edit Output Text",
            command=self.edit_output_text,
            background="lemonchiffon",
        )
        self.edit_output_text_button.grid(
            row=6, column=0, padx=10, pady=10, sticky="ew"
        )

        self.export_button = tk.Button(
            self.root,
            text="Export Text",
            command=self.export_text,
            background="pink",
        )
        self.export_button.grid(row=6, column=2, padx=10, pady=10, sticky="ew")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y))

    def get_input_text(self):
        return self.input_text.get("1.0", tk.END).strip()

    def set_output_text(self, text):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get("1.0", tk.END))

    def edit_output_text(self):
        text = self.output_text.get("1.0", tk.END)
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, text)

    def import_file(self):
        pass

    def export_text(self):
        pass

    def reverse_string(self):
        text = self.get_input_text()
        threading.Thread(target=self.run_reverse_string, args=(text,)).start()

    def run_reverse_string(self, text):
        result = reverse_string(text)
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

    def sql_format(self):
        text = self.get_input_text()
        threading.Thread(target=self.run_sql_format, args=(text,)).start()

    def run_sql_format(self, text):
        result = sql_format(text)
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

    def find_all_occurrences(self):
        text = self.get_input_text()
        pattern = simpledialog.askstring(
            "Input", "Enter the pattern to find all occurrences:"
        )
        threading.Thread(
            target=self.run_find_all_occurrences, args=(text, pattern)
        ).start()

    def run_find_all_occurrences(self, text, pattern):
        matches = find_all_occurrences(text, pattern)
        result = "\n".join(
            [
                f"Match {i+1}: Start={start}, End={end}"
                for i, (start, end) in enumerate(matches)
            ]
        )
        self.root.after(0, lambda: self.set_output_text(result))

    def split_by_pattern(self):
        text = self.get_input_text()
        pattern = simpledialog.askstring("Input", "Enter the pattern to split by:")
        threading.Thread(target=self.run_split_by_pattern, args=(text, pattern)).start()

    def run_split_by_pattern(self, text, pattern):
        parts = split_by_pattern(text, pattern)
        result = "\n".join([f"{part}" for i, part in enumerate(parts)])
        self.root.after(0, lambda: self.set_output_text(result))


if __name__ == "__main__":
    root = tk.Tk()
    app = StringerGUI(root)
    root.mainloop()
