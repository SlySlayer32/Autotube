import unittest

from project_name.api.freesound_api import FreesoundAPI


class TestFreesoundAPI(unittest.TestCase):
    def setUp(self):
        self.api = FreesoundAPI(api_key="test_key")

    def test_search_freesound(self):
        # Test Freesound search functionality
        pass

    def test_download_freesound(self):
        # Test Freesound download functionality
        pass


if __name__ == "__main__":
    unittest.main()
