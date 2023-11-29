from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from tqdm import tqdm

# Configuration Parameters
SAMPLE_RATE = 0.07
FONT_PATH = "SourceCodePro-Bold.ttf"
SOURCE_FOLDER = "source"
OUTPUT_FOLDER = "out"
ASCII_SYMBOLS = "8&WM#*ozh"

def load_font(font_path, font_size=38):
    return ImageFont.truetype(font_path, size=font_size)

def process_image(file, source_folder, output_folder, font, symbols):
    try:
        # Load image
        im = Image.open(os.path.join(source_folder, file))

        # Calculate aspect ratio
        aspect_ratio = font.getbbox("x")[2] / font.getbbox("x")[3]
        new_im_size = np.array([im.size[0] * SAMPLE_RATE, im.size[1] * SAMPLE_RATE * aspect_ratio]).astype(int)

        # Downsample the image
        im = im.resize(new_im_size)

        # Keep a copy of the image for color sampling
        im_color = np.array(im)

        # Convert to a numpy array for image manipulation
        im = np.array(im.convert("L"))

        # Normalize minimum and maximum to [0, max_symbol_index)
        if im.max() != im.min():
            im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

        # Generate the ASCII art
        ascii_art_matrix = symbols[im.astype(int)]

        # Create an output image for drawing ASCII text
        letter_size = font.getbbox("x")[2:]
        im_out_size = new_im_size * letter_size
        bg_color = "gray"
        output_image = Image.new("RGB", tuple(im_out_size), bg_color)
        draw = ImageDraw.Draw(output_image)

        # Draw text
        y = 0
        for i, line in enumerate(ascii_art_matrix):
            for j, color in enumerate(im_color[i]):
                ch = line[j]
                draw.text((letter_size[0] * j, y), ch[0], fill=tuple(color), font=font)
            y += letter_size[1]  # increase y by letter height

        # Save image file
        output_image.save(os.path.join(output_folder, file))

    except (FileNotFoundError, OSError, Image.UnidentifiedImageError) as e:
        print(f"Error processing {file}: {e}")

def main():
    # Ensure the target folder exists
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    font = load_font(FONT_PATH)
    source_files = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    total_files = len(source_files)

    count = 0
    for file in tqdm(source_files, desc="Converting images", unit="image", ncols=80):
        process_image(file, SOURCE_FOLDER, OUTPUT_FOLDER, font, np.array(list(reversed(ASCII_SYMBOLS))))
        count += 1

    print(f"\nConversion completed for {count}/{total_files} images.")


if __name__ == "__main__":
    main()