import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Define Paths
# Assuming this script is in kanji_project/scripts/
# So, BASE_DIR is kanji_project/scripts, .parent is kanji_project
BASE_DIR = Path(__file__).resolve().parent 
SVG_DIR = BASE_DIR.parent / 'data' / 'kanjivg_svgs'

# Namespace for SVG files (KanjiVG uses the standard SVG namespace)
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
# Register globally for cleaner output XML (no ns0: prefixes if default ns)
ET.register_namespace('', SVG_NAMESPACE) 

def set_animation_to_loop():
    if not SVG_DIR.exists():
        print(f"SVG directory not found: {SVG_DIR}")
        return

    svg_files = list(SVG_DIR.glob('*.svg'))
    if not svg_files:
        print(f"No SVG files found in {SVG_DIR}")
        return

    total_files = len(svg_files)
    print(f"Found {total_files} SVG files to process in {SVG_DIR}...")
    modified_count = 0
    error_count = 0

    for i, svg_file_path in enumerate(svg_files):
        try:
            # Print progress sparsely
            if (i + 1) % 500 == 0 or (i + 1) == total_files:
                print(f"Processing file {i + 1}/{total_files}: {svg_file_path.name}...")
            
            tree = ET.parse(str(svg_file_path))
            root = tree.getroot()
            
            animations_found_in_file = False
            
            # Find all <animate> elements
            for anim_element in root.findall(f".//{{{SVG_NAMESPACE}}}animate"):
                anim_element.set("repeatCount", "indefinite")
                animations_found_in_file = True
            
            # Find all <animateMotion> elements
            for anim_motion_element in root.findall(f".//{{{SVG_NAMESPACE}}}animateMotion"):
                anim_motion_element.set("repeatCount", "indefinite")
                animations_found_in_file = True

            # Find all <animateTransform> elements
            for anim_transform_element in root.findall(f".//{{{SVG_NAMESPACE}}}animateTransform"):
                anim_transform_element.set("repeatCount", "indefinite")
                animations_found_in_file = True

            if animations_found_in_file:
                # Overwrite the file with the modified XML tree,
                # including XML declaration and UTF-8 encoding.
                tree.write(str(svg_file_path), encoding="utf-8", xml_declaration=True)
                modified_count += 1
            
        except ET.ParseError as e:
            print(f"Error parsing XML in {svg_file_path.name}: {e}")
            error_count += 1
        except Exception as e:
            print(f"An unexpected error occurred with {svg_file_path.name}: {e}")
            error_count += 1
            
    print(f"\nProcessing complete.")
    print(f"Successfully modified animation loops in {modified_count} SVG files.")
    if error_count > 0:
        print(f"Encountered errors with {error_count} SVG files.")

if __name__ == '__main__':
    print("Starting SVG animation loop modification...")
    # Need to ensure correct working directory if running this script directly
    # For now, assuming it's run from the project root or paths are correctly resolved by Path(__file__)
    set_animation_to_loop()
    print("SVG animation loop modification finished.") 