import struct
import csv

def read_aco_file_with_readable_color_space(aco_file_path):
    # Mapping of color space IDs to human-readable names
    color_space_mapping = {
        0: 'RGB',
        1: 'HSB',
        2: 'CMYK',
        7: 'Lab',
        8: 'Grayscale',
        # Add other mappings if necessary
    }

    colors = []

    with open(aco_file_path, 'rb') as file:
        # Read version and count
        version, count = struct.unpack('>HH', file.read(4))

        # Read color blocks for version 1
        for _ in range(count):
            color_space_id, c1, c2, c3, c4 = struct.unpack('>HHHHH', file.read(10))
            color_space = color_space_mapping.get(color_space_id, f'Unknown ({color_space_id})')
            colors.append({'color_space': color_space, 'color_name': '', 'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4})

        # Check if there is a version 2
        if version == 1:
            try:
                version2, count2 = struct.unpack('>HH', file.read(4))
                if version2 == 2:
                    for _ in range(count2):
                        color_space_id, c1, c2, c3, c4 = struct.unpack('>HHHHH', file.read(10))
                        length = struct.unpack('>I', file.read(4))[0]
                        color_name = file.read(length * 2).decode('utf-16be').rstrip('\x00')
                        color_space = color_space_mapping.get(color_space_id, f'Unknown ({color_space_id})')
                        colors.append({'color_space': color_space, 'color_name': color_name, 'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4})
            except struct.error:
                # End of file reached
                pass

    return colors

def write_csv(colors, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['color_space', 'color_name', 'c1', 'c2', 'c3', 'c4']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for color in colors:
            writer.writerow(color)

# Example usage:
# aco_file_path = '/path/to/aco/file.aco'  # Replace with the actual ACO file path
# csv_file_path = '/path/to/output/file.csv'  # Replace with the desired output CSV file path

# colors_with_readable_color_space = read_aco_file_with_readable_color_space(aco_file_path)
# write_csv(colors_with_readable_color_space, csv_file_path)
