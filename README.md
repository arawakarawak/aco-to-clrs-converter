# aco-to-clrs-converter

aco_to_clrs.py:
This is a test script to convert Adobe ACO color swatch palettes to the native .clrs format. The script in this version ignores colors defined in non-RGB color spaces. In most cases it works.

aco_to_csv.py:
Intended as a testing tool. This script reads all colors from an ACO file and lists them as a csv table.
The structure of the output file is:
color_space	(RGB, HSB, CMYK, Lab, Grayscale or "custom color space")
color_name	(if provided in the source file)
c1	
c2	
c3	
c4,
where c1..c4 are the integer values of meaning depending on the color_space.

The specification of the values is listed in the "Specification of ACO file format.docx" file.
-----------------

Known issues: Photoshop seems to always export pure white and pure black as Grayscale, so these colors will be omitted by the aco_to_clrs.py script.

There  are still errors in the script, hopefully they may be easily fixed.

------------------
Links to sources:
http://www.selapa.net/swatches/colors/fileformats.php#adobe_acb
https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/#50577411_pgfId-1055819
