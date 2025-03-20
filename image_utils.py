import os
import random
from pathlib import Path

def get_random_image() -> tuple[str | None, bytes | None]:
    """
    Returns a random image filename and data as bytes from the mocks directory.

    Returns:
        tuple: (filename, bytes) containing the filename and binary content of a randomly
               selected image file, or (None, None) if no jpg files exist
    """
    # Get the directory containing jpg files
    image_dir = Path("mocks")

    # List all jpg files in the directory
    jpg_files = [f for f in os.listdir(image_dir) if f.lower().endswith('.jpg')]

    # Return filename and bytes of a random image if any exist
    if jpg_files:
        random_image = random.choice(jpg_files)
        image_path = image_dir / random_image

        # Read the image file as bytes
        with open(image_path, 'rb') as f:
            image_bytes = f.read()

        return random_image, image_bytes
    else:
        return None, None
