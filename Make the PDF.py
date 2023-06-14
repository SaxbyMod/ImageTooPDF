import os
import logging
import img2pdf

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Function to generate the PDF from the images
def generate_pdf_from_images(image_folder, output_path):
    # Sort the image files in the folder based on their names
    image_files = sorted(os.listdir(image_folder))

    # Create a list to store image paths
    image_paths = []

    # Generate list of image paths
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        image_paths.append(image_path)
        logging.info(f"Image '{image_file}' added to the list.")

    # Generate PDF from the image paths
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))
        logging.info(f"PDF exported to '{output_path}'.")

# Example usage
script_folder = os.path.dirname(__file__)
new_folder = os.path.join(script_folder, "New")
pdf_output_path = os.path.join(script_folder, "Exported_PDF.pdf")

generate_pdf_from_images(new_folder, pdf_output_path)
