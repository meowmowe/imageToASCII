import os
from PIL import Image
import numpy as np

def get_ascii_char(intensity):
    # Using fewer, more distinct characters
    chars = ' ·+OØ'
    index = int((intensity / 255) * (len(chars) - 1))
    return chars[max(0, min(index, len(chars) - 1))]

def convert_to_ascii_art(input_path, output_path, whatsapp_output_path, output_width, output_height):
    try:
        with Image.open(input_path) as img:
            img_gray = img.convert('L').resize((output_width, output_height), Image.LANCZOS)
            img_array = np.array(img_gray)
            
            # Create ASCII art
            ascii_art = [[get_ascii_char(img_array[i, j]) for j in range(output_width)] for i in range(output_height)]
            
            # Regular ASCII art
            ascii_str = '\n'.join([''.join(row) for row in ascii_art])
            
            # WhatsApp-friendly version
            whatsapp_str = '\n'.join([''.join(row) for row in ascii_art])
            whatsapp_str = f"```\n{whatsapp_str}\n```"
            
            # Save regular version
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(ascii_str)
            
            # Save WhatsApp-friendly version
            with open(whatsapp_output_path, 'w', encoding='utf-8') as f:
                f.write(whatsapp_str)
        
        return True
    except Exception as e:
        print(f"Error converting {input_path} to ASCII art: {str(e)}")
        return False

def process_directory(input_dir, output_dir, ascii_output_dir, whatsapp_output_dir, output_width, output_height):
    for dir in [output_dir, ascii_output_dir, whatsapp_output_dir]:
        if not os.path.exists(dir):
            os.makedirs(dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_dir, filename)
            gray_output_path = os.path.join(output_dir, f"gray_{filename}")
            ascii_output_path = os.path.join(ascii_output_dir, f"ascii_{os.path.splitext(filename)[0]}.txt")
            whatsapp_output_path = os.path.join(whatsapp_output_dir, f"whatsapp_ascii_{os.path.splitext(filename)[0]}.txt")
            
            try:
                Image.open(input_path).convert('L').resize((output_width, output_height), Image.LANCZOS).save(gray_output_path)
                
                if convert_to_ascii_art(input_path, ascii_output_path, whatsapp_output_path, output_width, output_height):
                    print(f"Converted {filename} to grayscale, ASCII art, and WhatsApp-friendly ASCII art")
                else:
                    print(f"Failed to convert {filename} to ASCII art")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

# User-adjustable variables
input_directory = "input_images"
output_directory = "output_images"
ascii_output_directory = "ascii_output"
whatsapp_output_directory = "whatsapp_ascii_output"
output_width = 64  # Reduced width for better WhatsApp display
output_height = 32  # Reduced height for better WhatsApp display

process_directory(input_directory, output_directory, ascii_output_directory, whatsapp_output_directory, output_width, output_height)
print(f"Image processing completed. Check the output directories for results.")