import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from main import SamCam, MAX_HISTORY
from models import DogAnalysis, DogState

class TestSamCam(unittest.TestCase):
    def setUp(self):
        # Create a SamCam instance with mocked components
        with patch('main.setup_camera'), \
             patch('main.genai.Client'), \
             patch('main.SamCam._create_tmp_dir', return_value='/mock/tmp'):
            self.samcam = SamCam()

        # Clear the analysis history
        self.samcam.analysis_history = []
        self.samcam.last_alert_time = None

    def test_should_alert_insufficient_history(self):
        """Test that alert is not triggered when history is insufficient"""
        # Add fewer entries than MAX_HISTORY
        self.samcam.analysis_history = [
            DogAnalysis(is_dog=True, dog_state=DogState.STANDING, probability_is_panting=0.8)
        ]

        self.assertFalse(self.samcam.should_alert())

    def test_should_alert_dog_lying_not_panting(self):
        """Test that alert is not triggered when dog is lying down and not panting"""
        # Fill history with MAX_HISTORY entries
        self.samcam.analysis_history = [
            DogAnalysis(is_dog=True, dog_state=DogState.LYING_DOWN, probability_is_panting=0.2)
        ] * MAX_HISTORY

        self.assertFalse(self.samcam.should_alert())

    def test_should_alert_no_dog_detected(self):
        """Test that alert is not triggered when no dog is detected"""
        # Fill history with MAX_HISTORY entries
        self.samcam.analysis_history = [
            DogAnalysis(is_dog=False, dog_state=DogState.NONE, probability_is_panting=0.0)
        ] * MAX_HISTORY

        self.assertFalse(self.samcam.should_alert())

    def test_should_alert_dog_standing(self):
        """Test that alert is triggered when dog is standing for threshold duration"""
        # Fill history with MAX_HISTORY entries of dog standing
        self.samcam.analysis_history = [
            DogAnalysis(is_dog=True, dog_state=DogState.STANDING, probability_is_panting=0.3)
        ] * MAX_HISTORY

        self.assertTrue(self.samcam.should_alert())

    def test_should_alert_dog_sitting(self):
        """Test that alert is triggered when dog is sitting for threshold duration"""
        # Fill history with MAX_HISTORY entries of dog sitting
        self.samcam.analysis_history = [
            DogAnalysis(is_dog=True, dog_state=DogState.SITTING, probability_is_panting=0.3)
        ] * MAX_HISTORY

        self.assertTrue(self.samcam.should_alert())

    def test_should_alert_dog_panting(self):
        """Test that alert is triggered when dog is panting for threshold duration"""
        # Fill history with MAX_HISTORY entries of dog panting while lying down
        self.samcam.analysis_history = [
            DogAnalysis(is_dog=True, dog_state=DogState.LYING_DOWN, probability_is_panting=0.8)
        ] * MAX_HISTORY

        self.assertTrue(self.samcam.should_alert())

    def test_should_alert_mixed_states(self):
        """Test alert logic with mixed states in history"""
        # Create a history with mostly concerning states but one entry that's fine
        concerning_entry = DogAnalysis(is_dog=True, dog_state=DogState.STANDING, probability_is_panting=0.7)
        normal_entry = DogAnalysis(is_dog=True, dog_state=DogState.LYING_DOWN, probability_is_panting=0.1)

        self.samcam.analysis_history = [concerning_entry] * (MAX_HISTORY - 1) + [normal_entry]

        self.assertFalse(self.samcam.should_alert())

    @patch('main.sync_turn_on_light')
    def test_handle_alert_first_time(self, mock_turn_on_light):
        """Test alert handling for the first alert"""
        self.samcam.last_alert_time = None

        self.samcam.handle_alert()

        mock_turn_on_light.assert_called_once()
        self.assertIsNotNone(self.samcam.last_alert_time)

    @patch('main.sync_turn_on_light')
    def test_handle_alert_too_soon(self, mock_turn_on_light):
        """Test alert is not triggered if previous alert was too recent"""
        self.samcam.last_alert_time = datetime.now() - timedelta(seconds=60)  # 1 minute ago

        self.samcam.handle_alert()

        mock_turn_on_light.assert_not_called()

    @patch('main.sync_turn_on_light')
    def test_handle_alert_sufficient_delay(self, mock_turn_on_light):
        """Test alert is triggered if previous alert was sufficiently long ago"""
        self.samcam.last_alert_time = datetime.now() - timedelta(seconds=301)  # Just over 5 minutes ago

        self.samcam.handle_alert()

        mock_turn_on_light.assert_called_once()


if __name__ == '__main__':
    unittest.main()
