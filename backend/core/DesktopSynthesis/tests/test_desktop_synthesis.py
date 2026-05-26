import unittest
import logging
from backend.core.DesktopSynthesis.nativefire_shard import NativefireShard
from backend.core.DesktopSynthesis.nativefier_shard import NativefierShard

class DesktopSynthesisTest(unittest.TestCase):
    def setUp(self):
        self.fire = NativefireShard()
        self.fier = NativefierShard()

    def test_nativefire_logic(self):
        logging.info("[TEST]: Validating Nativefire shard logic...")
        result = self.fire.synthesize_native("https://google.com", "linux")
        self.assertTrue(result)

    def test_nativefier_logic(self):
        logging.info("[TEST]: Validating Nativefier shard logic...")
        result = self.fier.synthesize_app("https://google.com")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
