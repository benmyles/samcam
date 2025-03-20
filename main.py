from dotenv import load_dotenv

from google import genai
from google.genai.client import os

from image_utils import get_random_image
from analysis import analyzeImage

load_dotenv()

def main():
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    filename, image_data = get_random_image()
    if image_data is None:
        print("No JPG images found in the mocks directory")
        return

    print(f"Analyzing image: {filename}")

    analysis = analyzeImage(client, image_data)
    print(analysis)


if __name__ == "__main__":
    main()
