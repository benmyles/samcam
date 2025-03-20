import os
import time
import logging
from datetime import datetime
from typing import List, Optional

from google import genai

from analysis import analyzeImage
from light import sync_turn_on_light
from env import GEMINI_API_KEY, is_debug
from cam import setup_camera, take_photo
from models import DogAnalysis, DogState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger("samcam")

# Constants
CHECK_INTERVAL_SECONDS = 60
ALERT_THRESHOLD_MINUTES = 5
MAX_HISTORY = ALERT_THRESHOLD_MINUTES * (60 // CHECK_INTERVAL_SECONDS)  # Number of entries to keep in history


class SamCam:
    def __init__(self):
        self.tmp_dir = self._create_tmp_dir()
        self.analysis_history: List[DogAnalysis] = []
        self.last_alert_time: Optional[datetime] = None
        self.genai_client = genai.Client(api_key=GEMINI_API_KEY)
        self.camera = setup_camera()

    def _create_tmp_dir(self) -> str:
        """Create a temporary directory for debug images"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tmp_dir = os.path.join(script_dir, ".tmp")
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir

    def capture_and_analyze_image(self) -> DogAnalysis:
        """Capture an image and analyze it"""
        filename, image_data = take_photo(self.camera)

        if is_debug:
            # Save image to ./tmp for debugging
            debug_filename = os.path.basename(filename)
            debug_path = os.path.join(self.tmp_dir, debug_filename)
            with open(debug_path, "wb") as f:
                f.write(image_data)
            logger.debug(f"Debug image saved to: {debug_path}")

        logger.info(f"Analyzing image: {filename}")
        analysis = analyzeImage(self.genai_client, image_data)
        logger.info(f"Analysis: {analysis}")

        return analysis

    def should_alert(self) -> bool:
        """
        Determine if we should alert based on analysis history.
        Alerts if the dog has been sitting, standing, or panting for the threshold duration.
        """
        if len(self.analysis_history) < MAX_HISTORY:
            return False

        # Check if all recent analyses show concerning behavior
        for analysis in self.analysis_history:
            # Skip if no dog detected
            if not analysis.is_dog:
                return False

            # If the dog is lying down and not panting, this is fine
            if (analysis.dog_state == DogState.LYING_DOWN and
                analysis.probability_is_panting < 0.5):
                return False

        # If we got here, all recent analyses show concerning behavior
        return True

    def handle_alert(self):
        """Handle alerting when concerning behavior is detected"""
        now = datetime.now()

        # Only alert once every 5 minutes to avoid spamming
        if (self.last_alert_time is None or
            (now - self.last_alert_time).total_seconds() >= 300):

            logger.warning("ALERT: Dog has been active for too long!")
            sync_turn_on_light()
            self.last_alert_time = now

    def run(self):
        """Main run loop for SamCam"""
        try:
            logger.info("Starting SamCam monitoring")

            while True:
                # Capture and analyze image
                analysis = self.capture_and_analyze_image()

                # Update history
                self.analysis_history.append(analysis)
                if len(self.analysis_history) > MAX_HISTORY:
                    self.analysis_history.pop(0)

                # Check if we need to alert
                if self.should_alert():
                    self.handle_alert()

                # Wait for next check
                time.sleep(CHECK_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            logger.info("SamCam monitoring stopped by user")
        except Exception as e:
            logger.exception(f"Error in SamCam: {e}")
        finally:
            if self.camera is not None:
                self.camera.release()

            import cv2
            cv2.destroyAllWindows()


def main():
    """Main entry point for SamCam application"""
    samcam = SamCam()
    samcam.run()


if __name__ == "__main__":
    main()
