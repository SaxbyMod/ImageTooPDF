import os
from PIL import Image, ImageDraw

def generate_composite_images(old_folder, rightside_image_path, output_folder, max_copies):
    # Load the right-side image
    rightside_image = Image.open(rightside_image_path).convert("RGBA")

    # Get the dimensions of the right-side image
    rightside_width, rightside_height = rightside_image.size

    # Calculate the separations
    x_separation = 327
    y_separation = 127

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize counters
    composite_index = 1

    # Generate composite images
    for filename in os.listdir(old_folder):
        # Load the imported image from the "Old" folder
        imported_image_path = os.path.join(old_folder, filename)
        imported_image = Image.open(imported_image_path).convert("RGBA")

        # Calculate the number of new images needed based on the number of copies
        num_new_images = max_copies // 2

        # Generate new images
        for _ in range(num_new_images):
            # Calculate the number of rows for the composite image
            num_rows = 2

            # Calculate the image width and height
            image_width = (
                imported_image.width
                + rightside_width
                + x_separation
                + imported_image.width
            )
            image_height = max(imported_image.height, rightside_height)

            # Calculate the canvas width and height
            canvas_width = image_width * 2
            canvas_height = image_height * num_rows + y_separation

            # Create a new composite image with transparent background
            composite_image = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(composite_image)

            # Draw the composite image with the required layout
            for i in range(num_rows):
                for j in range(2):
                    # Calculate the position of the imported image
                    imported_x = j * (image_width + x_separation)
                    imported_y = i * (image_height + y_separation)

                    # Paste the imported image onto the composite image
                    composite_image.alpha_composite(imported_image, (imported_x, imported_y))

                    # Calculate the position of the right-side image
                    rightside_x = imported_x + imported_image.width + x_separation
                    rightside_y = imported_y

                    # Paste the right-side image onto the composite image
                    composite_image.alpha_composite(rightside_image, (rightside_x, rightside_y))

            # Save the composite image
            output_filename = f"composite_{composite_index}.png"
            output_path = os.path.join(output_folder, output_filename)
            composite_image.save(output_path)
            composite_index += 1

        # Generate remaining images if any
        remaining_copies = max_copies % 2
        if remaining_copies > 0:
            # Calculate the number of rows for the composite image
            num_rows = 1

            # Calculate the image width and height
            image_width = imported_image.width + rightside_width + x_separation
            image_height = max(imported_image.height, rightside_height)

            # Calculate the canvas width and height
            canvas_width = image_width * remaining_copies
            canvas_height = image_height * num_rows

            # Create a new composite image with transparent background
            composite_image = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(composite_image)

            # Draw the composite image with the required layout
            for i in range(num_rows):
                for j in range(remaining_copies):
                    # Calculate the position of the imported image
                    imported_x = j * (image_width + x_separation)
                    imported_y = i * (image_height + y_separation)

                    # Paste the imported image onto the composite image
                    composite_image.alpha_composite(imported_image, (imported_x, imported_y))

                    # Calculate the position of the right-side image
                    rightside_x = imported_x + imported_image.width + x_separation
                    rightside_y = imported_y

                    # Paste the right-side image onto the composite image
                    composite_image.alpha_composite(rightside_image, (rightside_x, rightside_y))

            # Save the composite image
            output_filename = f"composite_{composite_index}.png"
            output_path = os.path.join(output_folder, output_filename)
            composite_image.save(output_path)
            composite_index += 1

# Configuration
old_folder = "Old"
rightside_image_path = "rightside_image.png"
output_folder = "New"

# Even Numbers Required
max_copies = 1

# Generate composite images
generate_composite_images(old_folder, rightside_image_path, output_folder, max_copies)
