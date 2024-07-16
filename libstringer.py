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
lib.to_uppercase.argtypes = [ctypes.c_char_p]
lib.to_lowercase.argtypes = [ctypes.c_char_p]
lib.replace_end_of_line.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_int,
]
lib.replace_start_of_line.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_int,
]
lib.sql_format.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_int,
]
lib.replace_sequence.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_int,
]
lib.find_all_occurrences.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_int,
]
lib.find_all_occurrences.restype = ctypes.c_int
lib.split_by_pattern.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_char_p),
    ctypes.c_int,
]
lib.split_by_pattern.restype = ctypes.c_int
lib.free_split_results.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.c_int]
lib.free_split_results.restype = None


# Helper function to create a mutable buffer
def create_buffer(s):
    encoded = s.encode("utf-8", "replace")
    buffer = ctypes.create_string_buffer(encoded, len(encoded) + 2)
    return buffer


# Generic function to calculate required buffer size
def calculate_required_size(
    s,
    start_replacement=None,
    end_replacement=None,
    eol_replacement=None,
    sequence=None,
    replacement=None,
):
    start_replacement = start_replacement.encode("utf-8") if start_replacement else None
    end_replacement = end_replacement.encode("utf-8") if end_replacement else None
    eol_replacement = eol_replacement.encode("utf-8") if eol_replacement else None
    sequence = sequence.encode("utf-8") if sequence else None
    replacement = replacement.encode("utf-8") if replacement else None
    return lib.calculate_required_size(
        s.encode("utf-8"),
        start_replacement,
        end_replacement,
        eol_replacement,
        sequence,
        replacement,
    )


# Python wrapper functions
def reverse_string(s):
    buffer = create_buffer(s)
    lib.reverse_string(buffer)
    return buffer.value.decode("utf-8", "replace")


def to_uppercase(s):
    buffer = create_buffer(s)
    lib.to_uppercase(buffer)
    return buffer.value.decode("utf-8", "replace")


def to_lowercase(s):
    buffer = create_buffer(s)
    lib.to_lowercase(buffer)
    return buffer.value.decode("utf-8", "replace")


def replace_end_of_line(s, replacement):
    buffer = create_buffer(s)
    required_size = calculate_required_size(s, eol_replacement=replacement)
    result_buffer = ctypes.create_string_buffer(required_size + len(s))
    lib.replace_end_of_line(
        buffer, replacement.encode("utf-8"), result_buffer, len(result_buffer)
    )
    return result_buffer.value.decode("utf-8", "replace")


def replace_start_of_line(s, replacement):
    buffer = create_buffer(s)
    required_size = calculate_required_size(s, start_replacement=replacement)
    result_buffer = ctypes.create_string_buffer(required_size + len(s))
    lib.replace_start_of_line(
        buffer, replacement.encode("utf-8"), result_buffer, len(result_buffer)
    )
    return result_buffer.value.decode("utf-8", "replace")


def sql_format(s):
    buffer = create_buffer(s)
    estimated_size = len(s) * 2
    result_buffer = ctypes.create_string_buffer(estimated_size)
    lib.sql_format(buffer, result_buffer, len(result_buffer))
    return result_buffer.value.decode("utf-8", "replace")


def replace_sequence(s, sequence, replacement):
    buffer = create_buffer(s)
    required_size = calculate_required_size(
        s, sequence=sequence, replacement=replacement
    )
    result_buffer = ctypes.create_string_buffer(required_size)
    lib.replace_sequence(
        buffer,
        sequence.encode("utf-8"),
        replacement.encode("utf-8"),
        result_buffer,
        len(result_buffer),
    )
    return result_buffer.value.decode("utf-8", "replace")


def find_all_occurrences(s, pattern):
    start_indices = (ctypes.c_int * len(s))()  # Array to store start indices of matches
    end_indices = (ctypes.c_int * len(s))()  # Array to store end indices of matches
    buffer_s = create_buffer(s)
    buffer_pattern = create_buffer(pattern)
    match_count = lib.find_all_occurrences(
        buffer_s, buffer_pattern, start_indices, end_indices, len(s)
    )
    return [(start_indices[i], end_indices[i]) for i in range(match_count)]


def split_by_pattern(s, pattern):
    results = (ctypes.c_char_p * len(s))()  # Array to store split results
    buffer_s = create_buffer(s)
    buffer_pattern = create_buffer(pattern)

    split_count = lib.split_by_pattern(buffer_s, buffer_pattern, results, len(s))

    return_result = [results[i].decode("utf-8") for i in range(split_count)]

    # Free the memory allocated by split_by_pattern
    lib.free_split_results(results, split_count)

    return return_result
