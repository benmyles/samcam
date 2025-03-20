# SamCam

## Overview

SamCam is a monitoring system designed to help dog owners detect when their dog might need to go outside. It uses a camera and AI to monitor a dog's behavior in a crate, and triggers an alert (by turning on smart lights) when the dog shows signs of needing to go out.

Specifically, SamCam watches for dogs that are:
- Sitting or standing for an extended period
- Panting while lying down
- Generally showing signs of restlessness or discomfort

This helps prevent accidents in the crate by alerting you when your dog might be trying to signal they need to go out.

## How It Works

1. A camera captures periodic images of your dog's crate
2. Google's Gemini AI analyzes each image to detect:
   - If a dog is present
   - The dog's position (sitting, standing, lying down)
   - Whether the dog appears to be panting
3. If concerning behavior is detected for a continuous period (default: 5 minutes), an alert is triggered
4. The alert turns on connected WiZ smart lights to notify you

## Setup

### Prerequisites

- Python 3.9+
- A webcam or USB camera
- (Optional) WiZ smart lights for alerts

### Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd samcam
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy the sample environment file and edit it with your configuration:
   ```
   cp .env.sample .env
   ```

4. Edit `.env` file with the following settings:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   LIGHT_IP=your_wiz_light_ip
   LIGHT_PORT=38899
   SKIP_LIGHT=0  # Set to 1 to skip light control
   VIDEO_DEVICE=0  # Camera device ID
   DEBUG=0  # Set to 1 for debug mode with image saving
   ```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create or sign in to your Google account
3. Go to API Keys section
4. Create a new API key
5. Copy the key into your `.env` file

## Usage

Run the app with:

```
python -m samcam.main
```

The system will:
- Capture an image every minute (configurable)
- Analyze the dog's behavior
- Alert you if concerning behavior is detected continuously for 5 minutes

### Configuration Options

You can adjust the following settings in `main.py`:

- `CHECK_INTERVAL_SECONDS`: Time between image captures (default: 60 seconds)
- `ALERT_THRESHOLD_MINUTES`: Duration of concerning behavior before alerting (default: 5 minutes)

## Debugging

If you enable debug mode by setting `DEBUG=1` in your `.env` file, the system will save captured images to a `.tmp` directory. This can be helpful for troubleshooting or reviewing what the camera sees.

## Testing

Run the tests with:

```
python -m unittest samcam.test_samcam
```

## Notes on Camera Setup

For best results:
- Position the camera to have a clear view of the entire crate
- For night vision, the app automatically adjusts camera settings for low-light conditions
- A small infrared light source can improve night vision if your camera supports it

## Troubleshooting

- **Camera not found**: Check your `VIDEO_DEVICE` setting. Try different numbers (0, 1, 2) if unsure which device ID is your camera.
- **Light not turning on**: Verify your WiZ light IP address and ensure it's on the same network as your computer.
- **AI not detecting dog correctly**: Try improving lighting conditions or camera positioning.

## License

This project is licensed under the MIT License.
