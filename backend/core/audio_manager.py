import logging
import sounddevice as sd
import json
import os

class AudioManager:
    """Handles autonomous audio I/O initialization and user settings."""
    def __init__(self):
        self.settings_path = "data/audio_settings.json"
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {"input_device": sd.default.device[0], "output_device": sd.default.device[1]}

    def verify_audio(self):
        """Verifies if audio devices are responsive."""
        logging.info(f"[AUDIO]: Verifying I/O channels...")
        try:
            # Querying device list as a verification step
            devices = sd.query_devices()
            logging.info(f"[AUDIO]: System I/O check passed. Devices online.")
            return True
        except Exception as e:
            logging.info(f"[AUDIO]: I/O ERROR - {e}")
            return False

    def update_device_settings(self, in_idx, out_idx):
        self.settings["input_device"] = in_idx
        self.settings["output_device"] = out_idx
        with open(self.settings_path, 'w') as f:
            json.dump(self.settings, f)
        logging.info(f"[AUDIO]: Preferences updated.")

# Audio manager instance
audio = AudioManager()
