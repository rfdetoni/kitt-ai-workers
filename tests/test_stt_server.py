import unittest
from kitt_workers.stt_server import _parse_multipart, transcribe_audio_file


class TestSttServer(unittest.TestCase):
    def test_parse_multipart_extracts_fields(self):
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        content_type = f"multipart/form-data; boundary={boundary}"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="model"\r\n\r\n'
            f"base\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="language"\r\n\r\n'
            f"pt\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="audio.wav"\r\n'
            f"Content-Type: audio/wav\r\n\r\n"
            f"RIFFmockwavcontent\r\n"
            f"--{boundary}--\r\n"
        ).encode("utf-8")

        file_bytes, language, model = _parse_multipart(content_type, body)
        self.assertEqual(file_bytes, b"RIFFmockwavcontent")
        self.assertEqual(language, "pt")
        self.assertEqual(model, "base")

    def test_mock_transcribe_returns_empty_when_no_whisper(self):
        result = transcribe_audio_file("/nonexistent/file.wav")
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
