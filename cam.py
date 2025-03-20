import cv2
import datetime
from env import VIDEO_DEVICE

ramp_frames = 30 # Number of frames to discard

def setup_camera() -> cv2.VideoCapture:
    if VIDEO_DEVICE is None:
        raise ValueError("VIDEO_DEVICE is None. Please provide a valid camera device ID.")

    try:
        # Ensure VIDEO_DEVICE is an integer
        device_id = int(VIDEO_DEVICE)
        cap = cv2.VideoCapture(device_id)
        if not cap.isOpened():
            raise ValueError(f"Could not open video device {device_id}")

        # Optimize for night vision
        # Increase brightness
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 1.0)  # Max brightness

        # Increase contrast
        cap.set(cv2.CAP_PROP_CONTRAST, 1.0)    # Max contrast

        # Set a higher gain
        cap.set(cv2.CAP_PROP_GAIN, 1.0)        # Max gain

        # Increase the exposure (negative values mean longer exposure time)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual exposure
        cap.set(cv2.CAP_PROP_EXPOSURE, -6)    # Longer exposure time

        # If available on the camera, turn off auto white balance
        cap.set(cv2.CAP_PROP_AUTO_WB, 0)

        # Set frame resolution if needed (can help with low light)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        return cap
    except ValueError as e:
        if "could not convert string to float" in str(e).lower() or "invalid literal for int" in str(e).lower():
            raise ValueError(f"VIDEO_DEVICE must be an integer, got: {VIDEO_DEVICE}")
        else:
            raise

def take_photo(cap: cv2.VideoCapture) -> tuple[str, bytes]:
    """
    Take a photo using the camera device and return a tuple of filename and image bytes.

    Args:
        cap: OpenCV VideoCapture object

    Returns:
        tuple[str, bytes]: A tuple containing the generated filename and JPG image bytes

    Raises:
        RuntimeError: If frame capture fails or image encoding fails
    """

    # Discard initial frames
    for i in range(ramp_frames):
        _, _ = cap.read()

    # Capture a frame
    ret, frame = cap.read()

    # If capture failed, raise an exception
    if not ret or frame is None:
        raise RuntimeError("Failed to capture frame from camera")

    # Generate filename based on current time
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{timestamp}.jpg"

    # Encode the frame as jpg bytes
    success, buffer = cv2.imencode(".jpg", frame)
    if not success:
        raise RuntimeError("Failed to encode image as JPEG")

    # Convert to bytes
    jpg_bytes = buffer.tobytes()

    return filename, jpg_bytes
