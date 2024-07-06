import subprocess
import ctypes
import os


def compile(input_file, output_file):
    compile_command = [
        "tcc",
        "-shared",
        "-rdynamic",
        "-Wall",
        input_file,
        "-o",
        output_file,
    ]

    try:
        result = subprocess.run(
            compile_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e.stderr.decode()}")


# Define the paths
input_file = "libstringer.c"
output_file = "libstringer.dll"

compile(input_file, output_file)

# Load the shared library
dll_absolute_path = os.path.abspath(output_file)
lib = ctypes.CDLL(dll_absolute_path)

# Define the argument and return types for the C functions
lib.reverse_string.argtypes = [ctypes.c_char_p]
lib.concatenate_strings.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.find_substring.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.find_substring.restype = ctypes.c_int
lib.to_uppercase.argtypes = [ctypes.c_char_p]
lib.to_lowercase.argtypes = [ctypes.c_char_p]


# Helper function to create a mutable buffer
def create_buffer(s):
    encoded = s.encode("utf-8", "replace")
    buffer = ctypes.create_string_buffer(encoded, len(encoded) + 1)
    return buffer


# Python wrapper functions
def reverse_string(s):
    buffer = create_buffer(s)
    lib.reverse_string(buffer)
    return buffer.value.decode("utf-8", "replace")


def concatenate_strings(dest, src):
    buffer_dest = create_buffer(dest)
    buffer_src = create_buffer(src)
    lib.concatenate_strings(buffer_dest, buffer_src)
    return buffer_dest.value.decode("utf-8", "replace")


def find_substring(s, substr):
    buffer_s = create_buffer(s)
    buffer_substr = create_buffer(substr)
    return lib.find_substring(buffer_s, buffer_substr)


def to_uppercase(s):
    buffer = create_buffer(s)
    lib.to_uppercase(buffer)
    return buffer.value.decode("utf-8", "replace")


def to_lowercase(s):
    buffer = create_buffer(s)
    lib.to_lowercase(buffer)
    return buffer.value.decode("utf-8", "replace")
