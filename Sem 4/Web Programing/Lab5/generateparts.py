from PIL import Image
import sys
import os

def split_image(image_path):
    try:
        # Open the image
        img = Image.open(image_path)
        width, height = img.size

        # Crop the image to a square
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        upper = (height - min_dim) // 2
        right = left + min_dim
        lower = upper + min_dim
        img = img.crop((left, upper, right, lower))

        # Save the cropped image as original.png
        output_dir = "output_parts"
        os.makedirs(output_dir, exist_ok=True)
        original_path = os.path.join(output_dir, "original.png")
        img.save(original_path)

        # Update dimensions after cropping
        width, height = img.size

        # Calculate dimensions for each part
        part_width = width // 4
        part_height = height // 4

        # Split and save parts
        count = 1
        for row in range(4):
            for col in range(4):
                left = col * part_width
                upper = row * part_height
                right = left + part_width
                lower = upper + part_height

                part = img.crop((left, upper, right, lower))
                part_name = f"{count}.png"
                part.save(os.path.join(output_dir, part_name))
                count += 1

        print(f"Image successfully split into 9 parts and saved in '{output_dir}' directory.")
        print(f"Original image saved as 'original.png' in '{output_dir}' directory.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generateparts.py <path_to_image>")
    else:
        image_path = sys.argv[1]
        split_image(image_path)
