# This script converts an ACO color palette to CLRS format, but has a basic UI (asks for input file and for the output location). 
# The output file bears the name of the source ACO file (but with the .clrs suffix of course)

import tkinter as tk
from tkinter import filedialog
import struct
import csv
import json
import os

def convert_to_hex_and_twos_complement(color_integer):
    # Convert the color integer to hex and to two's complement negative integer.
    hex_value = hex(color_integer)
    if color_integer > 0x7FFFFFFF:
        twos_complement_value = color_integer - 0x100000000
    else:
        twos_complement_value = color_integer
    return hex_value, twos_complement_value

def read_rgb_aco_file_with_omitted_count(aco_file_path):
    colors = []
    omitted_count = 0
    with open(aco_file_path, 'rb') as file:
        version, count = struct.unpack('>HH', file.read(4))
        for _ in range(count * 2 if version == 1 else count):
            color_space_id, c1, c2, c3, c4 = struct.unpack('>HHHHH', file.read(10))
            if color_space_id == 0:  # RGB color space
                converted_c1 = (c1 >> 8) & 0xFF
                converted_c2 = (c2 >> 8) & 0xFF
                converted_c3 = (c3 >> 8) & 0xFF
                color_integer = (0xFF << 24) | (converted_c1 << 16) | (converted_c2 << 8) | converted_c3
                hex_value, twos_complement_value = convert_to_hex_and_twos_complement(color_integer)
                colors.append({'color_integer': color_integer, 'hex_value': hex_value, 'twos_complement_value': twos_complement_value})
            else:
                omitted_count += 1
    return colors, omitted_count

def generate_json_with_colors_and_comment(colors, output_folder_path, input_file_name, omitted_count):
    color_values = [color['twos_complement_value'] for color in colors]
    data = {"colors": color_values, "name": input_file_name}
    if omitted_count > 0:
        comment = f"The original palette {input_file_name} contained {omitted_count} color swatches in non-RGB format that have been omitted."
        data['comment'] = comment
    output_file_path = os.path.join(output_folder_path, input_file_name.replace('.aco', '.clrs'))  # Ensure correct file extension
    with open(output_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

def select_file_and_convert():
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter root window
    aco_file_path = filedialog.askopenfilename(title="Select ACO File", filetypes=[("ACO Files", "*.aco")])
    if not aco_file_path:
        print("No file selected. Exiting...")
        return
    output_folder_path = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder_path:
        print("No output folder selected. Exiting...")
        return
    
    input_file_name = os.path.basename(aco_file_path)  # Extract just the file name
    colors_with_hex_and_complement, omitted_count = read_rgb_aco_file_with_omitted_count(aco_file_path)
    generate_json_with_colors_and_comment(colors_with_hex_and_complement, output_folder_path, input_file_name, omitted_count)

if __name__ == "__main__":
    select_file_and_convert()
