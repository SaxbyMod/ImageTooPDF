import os
import logging
from PIL import Image, ImageDraw

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Function to generate the composite image
def generate_composite_image(old_folder, rightsides_image_path, output_folder):
    # Load the right-side image
    rightside_image = Image.open(rightsides_image_path).convert("RGBA")

    # Get the dimensions of the right-side image
    rightside_width, rightside_height = rightside_image.size

    # Get the dimensions of the images in the "Old" folder
    image_width, image_height = Image.open(os.path.join(old_folder, os.listdir(old_folder)[0])).size

    # Calculate the total width and height of the composite image
    total_width = 2 * (image_width + rightside_width) + 327  # Spacing between columns
    total_height = 2 * (image_height + rightside_height) + 127  # Spacing between rows

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Counter for numbering the images
    counter = 1

    # Generate multiple composite images
    for filename in os.listdir(old_folder):
        # Create a new composite image with transparent background
        composite_image = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(composite_image)

        # Draw the composite image with the required layout
        for i in range(2):
            for j in range(2):
                # Calculate the position of the Imported Image
                imported_x = j * (image_width + rightside_width) + 327 * j
                imported_y = i * (image_height + rightside_height) + 127 * i

                # Load the old image from the "Old" folder
                old_image_path = os.path.join(old_folder, filename)
                old_image = Image.open(old_image_path)

                # Paste the Imported Image onto the composite image
                composite_image.paste(old_image, (imported_x, imported_y))
                logging.info(f"Image '{filename}' imported and added to the composite image.")

                # Calculate the position to place the Rightside Image
                rightside_x = imported_x + image_width
                rightside_y = imported_y

                # Paste the Rightside Image onto the composite image
                composite_image.alpha_composite(rightside_image, (rightside_x, rightside_y))

                # Draw the "Card Imported" label on the composite image
                label_x = imported_x
                label_y = imported_y + image_height + 5
                draw.text((label_x, label_y), "Card Imported", fill="black")

                # Increment the counter
                counter += 1

        # Save the generated composite image
        output_path = os.path.join(output_folder, f"composite_image_{counter}.png")
        composite_image.save(output_path)
        logging.info(f"Composite image '{output_path}' exported.")

# Example usage
script_folder = os.path.dirname(__file__)
old_folder = os.path.join(script_folder, "Old")
rightsides_image_path = os.path.join(script_folder, "Rightside_Image.png")
output_folder = os.path.join(script_folder, "New")

generate_composite_image(old_folder, rightsides_image_path, output_folder)
