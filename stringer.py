import threading
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import json
import csv
import xml.etree.ElementTree as ET
from libstringer import *


class StringerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stringer")
        self.root.iconbitmap(default="./resources/icon.ico")
        self.root.configure(background="azure")
        self.root.option_add("*Foreground", "hotpink")
        self.root.option_add("*Background", "lemonchiffon")
        self.create_widgets()
        self.center_window()
        self.root.resizable(False, False)
        self.file_path = None
        self.file_type = None

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

        self.input_text.tag_configure(
            "highlight", background="pink", foreground="ivory"
        )

        self.import_button = tk.Button(
            self.root,
            text="Import File",
            command=self.import_file,
            background="Pink",
            foreground="ivory",
            font=("Arial", 10, "bold"),
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
            foreground="ivory",
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
        file_path = filedialog.askopenfilename(
            filetypes=(
                ("All Files", "*.*"),
                ("CSV Files", "*.csv"),
                ("JSON Files", "*.json"),
                ("XML Files", "*.xml"),
                ("Text Files", "*.txt"),
                ("SQL Files", "*.sql"),
                ("HTML Files", "*.html"),
            )
        )
        if not file_path:
            return

        self.file_path = file_path
        self.file_type = file_path.split(".")[-1].lower()

        try:
            if self.file_type == "csv":
                with open(file_path, newline="", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    content = "\n".join([",".join(row) for row in reader])
            elif self.file_type == "json":
                with open(file_path, "r", encoding="utf-8") as jsonfile:
                    content = json.dumps(json.load(jsonfile), indent=4)
            elif self.file_type == "xml":
                tree = ET.parse(file_path)
                content = ET.tostring(tree.getroot(), encoding="unicode")
            elif self.file_type == "txt":
                with open(file_path, "r", encoding="utf-8") as txtfile:
                    content = txtfile.read()
            elif self.file_type == "sql":
                with open(file_path, "r", encoding="utf-8") as sqlfile:
                    content = sqlfile.read()
            elif self.file_type == "html":
                with open(file_path, "r", encoding="utf-8") as htmlfile:
                    content = htmlfile.read()
            else:
                content = ""
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import file: {str(e)}")
            return

        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, "File imported!")

        self.input_content = content

    def export_text(self):
        if not self.file_path or not self.file_type:
            messagebox.showwarning("Warning", "No file to export.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{self.file_type}",
            filetypes=(
                ("All Files", "*.*"),
                ("CSV Files", "*.csv"),
                ("JSON Files", "*.json"),
                ("XML Files", "*.xml"),
                ("Text Files", "*.txt"),
                ("SQL Files", "*.sql"),
                ("HTML Files", "*.html"),
            ),
        )
        if not save_path:
            return

        output_text = self.output_text.get("1.0", tk.END).strip()

        try:
            if self.file_type == "csv":
                with open(save_path, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    for row in output_text.split("\n"):
                        writer.writerow(row.split(","))
            elif self.file_type == "json":
                with open(save_path, "w", encoding="utf-8") as jsonfile:
                    json.dump(json.loads(output_text), jsonfile, indent=4)
            elif self.file_type == "xml":
                root = ET.ElementTree(ET.fromstring(output_text))
                root.write(save_path)
            elif self.file_type == "txt":
                with open(save_path, "w", encoding="utf-8") as txtfile:
                    txtfile.write(output_text)
            elif self.file_type == "sql":
                with open(save_path, "w", encoding="utf-8") as sqlfile:
                    sqlfile.write(output_text)
            elif self.file_type == "html":
                with open(save_path, "w", encoding="utf-8") as htmlfile:
                    htmlfile.write(output_text)
            else:
                messagebox.showwarning("Warning", "Unsupported file type.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export file: {str(e)}")

    def reverse_string(self):
        threading.Thread(target=self.run_reverse_string).start()

    def run_reverse_string(self):
        text = self.get_input_text()
        if text != "File imported!":
            result = reverse_string(text)
        else:
            result = reverse_string(self.input_content)
        self.root.after(0, lambda: self.set_output_text(result))

    def to_uppercase(self):
        threading.Thread(target=self.run_to_uppercase).start()

    def run_to_uppercase(self):
        text = self.get_input_text()
        if text != "File imported!":
            result = to_uppercase(text)
        else:
            result = to_uppercase(self.input_content)
        self.root.after(0, lambda: self.set_output_text(result))

    def to_lowercase(self):
        threading.Thread(target=self.run_to_lowercase).start()

    def run_to_lowercase(self):
        text = self.get_input_text()
        if text != "File imported!":
            result = to_lowercase(text)
        else:
            result = to_lowercase(self.input_content)
        self.root.after(0, lambda: self.set_output_text(result))

    def replace_end_of_line(self):
        replacement = simpledialog.askstring(
            "Input", "Enter the replacement text for end of line:"
        )
        threading.Thread(
            target=self.run_replace_end_of_line, args=(replacement,)
        ).start()

    def run_replace_end_of_line(self, replacement):
        text = self.get_input_text()
        if text != "File imported!":
            result = replace_end_of_line(text, replacement)
        else:
            result = replace_end_of_line(self.input_content, replacement)
        self.root.after(0, lambda: self.set_output_text(result))

    def sql_format(self):
        threading.Thread(target=self.run_sql_format).start()

    def run_sql_format(self):
        text = self.get_input_text()
        if text != "File imported!":
            result = sql_format(text)
        else:
            result = sql_format(self.input_content)
        self.root.after(0, lambda: self.set_output_text(result))

    def replace_start_of_line(self):
        replacement = simpledialog.askstring(
            "Input", "Enter the replacement text for start of line:"
        )
        threading.Thread(
            target=self.run_replace_start_of_line, args=(replacement,)
        ).start()

    def run_replace_start_of_line(self, replacement):
        text = self.get_input_text()
        if text != "File imported!":
            result = replace_start_of_line(text, replacement)
        else:
            result = replace_start_of_line(self.input_content, replacement)
        self.root.after(0, lambda: self.set_output_text(result))

    def replace_sequence(self):
        sequence = simpledialog.askstring(
            "Input", "Enter the sequence to replace:", parent=self.root
        )
        replacement = simpledialog.askstring(
            "Input", "Enter the replacement text:", parent=self.root
        )
        threading.Thread(
            target=self.run_replace_sequence, args=(sequence, replacement)
        ).start()

    def run_replace_sequence(self, sequence, replacement):
        text = self.get_input_text()
        if text != "File imported!":
            result = replace_sequence(text, sequence, replacement)
        else:
            result = replace_sequence(self.input_content, sequence, replacement)
        self.root.after(0, lambda: self.set_output_text(result))

    def find_all_occurrences(self):
        pattern = simpledialog.askstring(
            "Input", "Enter the pattern to find all occurrences:"
        )
        threading.Thread(target=self.run_find_all_occurrences, args=(pattern,)).start()

    def run_find_all_occurrences(self, pattern):
        text = self.get_input_text()
        if text != "File imported!":
            matches = find_all_occurrences(text, pattern)
            result = f"Total matches : {len(matches)}\n"
            result = result + "\n".join(
                [
                    f"Match {i+1}: Start={start}, End={end}"
                    for i, (start, end) in enumerate(matches)
                ]
            )
            self.root.after(
                0, lambda: self.highlight_matches_and_set_output(result, matches)
            )
        else:
            matches = find_all_occurrences(self.input_content, pattern)
            result = f"Total matches : {len(matches)}\n"
            result = result + "\n".join(
                [
                    f"Match {i+1}: Start={start}, End={end}"
                    for i, (start, end) in enumerate(matches)
                ]
            )
            self.root.after(0, lambda: self.set_output_text(result))

    def highlight_matches_and_set_output(self, result, matches):
        self.set_output_text(result)
        self.input_text.tag_remove("highlight", "1.0", tk.END)
        for start, end in matches:
            self.input_text.tag_add(
                "highlight", f"1.0 + {start} chars", f"1.0 + {end} chars"
            )

    def split_by_pattern(self):
        pattern = simpledialog.askstring("Input", "Enter the pattern to split by:")
        threading.Thread(target=self.run_split_by_pattern, args=(pattern,)).start()

    def run_split_by_pattern(self, pattern):
        text = self.get_input_text()
        if text != "File imported!":
            parts = split_by_pattern(text, pattern)
        else:
            parts = split_by_pattern(self.input_content, pattern)
        result = "\n".join([f"{part}" for i, part in enumerate(parts)])
        self.root.after(0, lambda: self.set_output_text(result))


if __name__ == "__main__":
    root = tk.Tk()
    app = StringerGUI(root)
    root.mainloop()
