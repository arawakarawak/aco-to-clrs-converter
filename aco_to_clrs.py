import struct
import csv
import json

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

def generate_json_with_colors_and_comment(colors, json_file_path, input_file_name, omitted_count):
    color_values = [color['twos_complement_value'] for color in colors]
    data = {"colors": color_values, "name": input_file_name}
    if omitted_count > 0:
        comment = f"The original palette {input_file_name} contained {omitted_count} color swatches in non-RGB format that have been omitted."
        data['comment'] = comment
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

# Example usage:
new_aco_file_path = '/path/to/aco/file.aco'  # Replace with the actual ACO file path
json_file_path = '/path/to/output/file.clrs'  # Replace with the desired output JSON file path
input_file_name = 'file.aco' # this is obviously redundant (pk)
colors_with_hex_and_complement, omitted_count = read_rgb_aco_file_with_omitted_count(new_aco_file_path)
generate_json_with_colors_and_comment(colors_with_hex_and_complement, json_file_path, input_file_name, omitted_count)
