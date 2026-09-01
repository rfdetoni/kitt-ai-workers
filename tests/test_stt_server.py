import unittest

import kitt_workers.stt_server as stt_server
from kitt_workers.stt_server import (
    _MAX_REQUEST_BYTES,
    _browser_origin_forbidden,
    _parse_multipart,
    _validate_loopback_host,
    _validated_content_length,
    transcribe_audio_file,
)


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

    def test_mock_transcribe_returns_empty_when_file_is_missing(self):
        result = transcribe_audio_file("/nonexistent/file.wav")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

    def test_loopback_validation_rejects_network_bind(self):
        self.assertEqual(_validate_loopback_host("127.0.0.1"), "127.0.0.1")
        self.assertEqual(_validate_loopback_host("localhost"), "localhost")
        with self.assertRaises(ValueError):
            _validate_loopback_host("0.0.0.0")
        with self.assertRaises(ValueError):
            _validate_loopback_host("192.168.1.10")
        with self.assertRaises(ValueError):
            _validate_loopback_host("example.com")

    def test_content_length_is_bounded(self):
        self.assertEqual(_validated_content_length("123"), 123)
        with self.assertRaises(ValueError):
            _validated_content_length(None)
        with self.assertRaises(ValueError):
            _validated_content_length("-1")
        with self.assertRaises(ValueError):
            _validated_content_length("not-a-number")
        with self.assertRaises(OverflowError):
            _validated_content_length(str(_MAX_REQUEST_BYTES + 1))

    def test_browser_origin_is_rejected_for_machine_api(self):
        self.assertFalse(_browser_origin_forbidden(None))
        self.assertTrue(_browser_origin_forbidden("http://localhost:3000"))
        self.assertTrue(_browser_origin_forbidden("https://evil.example"))
        self.assertTrue(_browser_origin_forbidden("null"))

    def test_engine_readiness_requires_loaded_real_engine(self):
        original_instance = stt_server._WHISPER_MODEL_INSTANCE
        original_name = stt_server._ENGINE_NAME
        try:
            stt_server._WHISPER_MODEL_INSTANCE = None
            stt_server._ENGINE_NAME = "unavailable"
            self.assertFalse(stt_server._engine_ready())

            stt_server._WHISPER_MODEL_INSTANCE = object()
            stt_server._ENGINE_NAME = "faster-whisper (base)"
            self.assertTrue(stt_server._engine_ready())

            stt_server._ENGINE_NAME = "whisper (base)"
            self.assertTrue(stt_server._engine_ready())
        finally:
            stt_server._WHISPER_MODEL_INSTANCE = original_instance
            stt_server._ENGINE_NAME = original_name


if __name__ == "__main__":
    unittest.main()
