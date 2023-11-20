# aco-to-clrs-converter

aco_to_clrs.py:
This is a test script to convert Adobe ACO color swatch palettes t onative .clrs format. The script ignores colors in non-RGB color spaces. 

aco_to_csv.py:
This script reads all colors from an ACO file and lists them as a csv table.
The structure of the output file is:
color_space	(RGB, HSB, CMYK, Lab, Grayscale or "custom color space")
color_name	(if provided in the source file)
c1	
c2	
c3	
c4,
where c1..c4 are the integer values of meaning depending on the color_space.
The specification of the values is listed in the "Specification of ACO file format.docx" doc.

