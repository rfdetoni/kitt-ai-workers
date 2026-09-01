import io
import unittest

import kitt_workers.stt_server as stt_server
from kitt_workers.stt_server import (
    _MAX_REQUEST_BYTES,
    _browser_origin_forbidden,
    _env_port,
    _parse_multipart,
    _shutdown_on_parent_stdin_eof,
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

    def test_parent_stdin_eof_stops_supervised_server(self):
        class FakeServer:
            def __init__(self):
                self.shutdown_calls = 0

            def shutdown(self):
                self.shutdown_calls += 1

        server = FakeServer()
        _shutdown_on_parent_stdin_eof(server, io.BytesIO(b""))
        self.assertEqual(server.shutdown_calls, 1)

    def test_env_port_parser(self):
        original = stt_server.os.environ.get("KITT_TEST_STT_PORT")
        try:
            stt_server.os.environ["KITT_TEST_STT_PORT"] = "8123"
            self.assertEqual(_env_port("KITT_TEST_STT_PORT", 8000), 8123)
            stt_server.os.environ["KITT_TEST_STT_PORT"] = "invalid"
            with self.assertRaises(ValueError):
                _env_port("KITT_TEST_STT_PORT", 8000)
        finally:
            if original is None:
                stt_server.os.environ.pop("KITT_TEST_STT_PORT", None)
            else:
                stt_server.os.environ["KITT_TEST_STT_PORT"] = original

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

    def test_models_endpoint_returns_whisper_models(self):
        class FakeHandler(stt_server.LocalSTTRequestHandler):
            def __init__(self):
                self.sent_status = None
                self.sent_data = None

            def _send_json(self, status, data):
                self.sent_status = status
                self.sent_data = data

        handler = FakeHandler()
        handler.path = "/v1/models"
        handler.do_GET()
        self.assertEqual(handler.sent_status, 200)
        self.assertIn("data", handler.sent_data)
        model_ids = [m["id"] for m in handler.sent_data["data"]]
        self.assertIn("whisper-1", model_ids)
        self.assertIn("base", model_ids)


if __name__ == "__main__":
    unittest.main()
