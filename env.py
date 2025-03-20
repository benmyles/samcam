from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

VIDEO_DEVICE = os.getenv('VIDEO_DEVICE')

LIGHT_IP = os.getenv('LIGHT_IP')
LIGHT_PORT = os.getenv('LIGHT_PORT')
SKIP_LIGHT = os.getenv('SKIP_LIGHT')

DEBUG = os.getenv('DEBUG')

def is_debug():
    return DEBUG == '1'
