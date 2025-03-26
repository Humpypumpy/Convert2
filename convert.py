from PIL import Image
import os
import pillow_avif
import pyheif

def convert_image(input_path, output_format, scale_percent=100, quality=90):
    with Image.open(input_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        if scale_percent != 100:
            width = int(img.width * scale_percent / 100)
            height = int(img.height * scale_percent / 100)
            img = img.resize((width, height))

        output_file = f"{os.path.splitext(input_path)[0]}.{output_format.lower()}"
        if output_format.lower() in ['jpeg', 'jpg', 'webp']:
            img.save(output_file, output_format.upper(), quality=quality)
        else:
            img.save(output_file, output_format.upper())
        return output_file