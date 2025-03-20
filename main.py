from google import genai
import os

from analysis import analyzeImage
from light import sync_turn_on_light

from env import GEMINI_API_KEY, is_debug
from cam import setup_camera, take_photo

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create tmp directory relative to the script location
    tmp_dir = os.path.join(script_dir, ".tmp")
    os.makedirs(tmp_dir, exist_ok=True)

    cap = setup_camera()
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        filename, image_data = take_photo(cap)

        if is_debug:
            # Save image to ./tmp relative to script location for debugging
            debug_filename = os.path.basename(filename)
            debug_path = os.path.join(tmp_dir, debug_filename)
            with open(debug_path, "wb") as f:
                f.write(image_data)
            print(f"Debug image saved to: {debug_path}")

        print(f"Analyzing image: {filename}")
        analysis = analyzeImage(client, image_data)
        print(analysis)

        sync_turn_on_light()
    finally:
        if cap is not None:
            cap.release()

        import cv2
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
