import unittest
from youtube_url_parser.parser import parse_youtube_url

class TestYouTubeURLParser(unittest.TestCase):
    def test_standard_url(self):
        url = "https://www.youtube.com/watch?v=AFY8JsZCzuE"
        self.assertEqual(parse_youtube_url(url), "AFY8JsZCzuE")

    def test_short_url_with_params(self):
        url = "https://youtu.be/AFY8JsZCzuE?si=alQdRsCVkziANbQx"
        self.assertEqual(parse_youtube_url(url), "AFY8JsZCzuE")

    def test_short_url(self):
        url = "https://youtu.be/_iJ5dWHvh1A"
        self.assertEqual(parse_youtube_url(url), "_iJ5dWHvh1A")

    def test_shared_short_url(self):
        url = "https://youtu.be/AFY8JsZCzuE?feature=shared"
        self.assertEqual(parse_youtube_url(url), "AFY8JsZCzuE")

    def test_invalid_url(self):
        url = "https://example.com/watch?v=dQw4w9WgXcQ"
        self.assertIsNone(parse_youtube_url(url))

    def test_mobile_url(self):
        url = "https://m.youtube.com/watch?v=XnpeaG7ORJI"
        self.assertEqual(parse_youtube_url(url), "XnpeaG7ORJI")

if __name__ == "__main__":
    unittest.main()