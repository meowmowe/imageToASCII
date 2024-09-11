import os
from PIL import Image
import numpy as np

def get_ascii_char(intensity):
    chars = ' .:-=+*#%@'
    index = int((intensity / 255) * (len(chars) - 1))
    return chars[max(0, min(index, len(chars) - 1))]

def convert_to_ascii_art(input_path, output_path, output_width, output_height):
    try:
        with Image.open(input_path) as img:
            # Convert to grayscale and resize
            img_gray = img.convert('L').resize((output_width, output_height), Image.LANCZOS)
            
            # Convert image to numpy array
            img_array = np.array(img_gray)
            
            # Create ASCII art
            ascii_art = [[get_ascii_char(img_array[i, j]) for j in range(output_width)] for i in range(output_height)]
            
            # Join characters and create final string
            ascii_str = '\n'.join([''.join(row) for row in ascii_art])
            
            # Save to text file
            with open(output_path, 'w') as f:
                f.write(ascii_str)
        return True
    except Exception as e:
        print(f"Error converting {input_path} to ASCII art: {str(e)}")
        return False

def process_directory(input_dir, output_dir, ascii_output_dir, output_width, output_height):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(ascii_output_dir):
        os.makedirs(ascii_output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_dir, filename)
            gray_output_path = os.path.join(output_dir, f"gray_{filename}")
            ascii_output_path = os.path.join(ascii_output_dir, f"ascii_{os.path.splitext(filename)[0]}.txt")
            
            try:
                # Convert to grayscale
                Image.open(input_path).convert('L').resize((output_width, output_height), Image.LANCZOS).save(gray_output_path)
                
                # Convert to ASCII art
                if convert_to_ascii_art(input_path, ascii_output_path, output_width, output_height):
                    print(f"Converted {filename} to grayscale and ASCII art")
                else:
                    print(f"Failed to convert {filename} to ASCII art")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

# User-adjustable variables
input_directory = "input_images"
output_directory = "output_images"
ascii_output_directory = "ascii_output"
output_width = 80  # Adjust this to your desired output width
output_height = 40  # Adjust this to your desired output height

process_directory(input_directory, output_directory, ascii_output_directory, output_width, output_height)
print(f"Image processing completed. Check the output directories for results.")