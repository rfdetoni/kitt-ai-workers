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
            f'Content-Disposition: form-data; name="prompt"\r\n\r\n'
            f"KITT. Ei KITT.\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="audio.wav"\r\n'
            f"Content-Type: audio/wav\r\n\r\n"
            f"RIFFmockwavcontent\r\n"
            f"--{boundary}--\r\n"
        ).encode("utf-8")

        file_bytes, language, model, prompt = _parse_multipart(content_type, body)
        self.assertEqual(file_bytes, b"RIFFmockwavcontent")
        self.assertEqual(language, "pt")
        self.assertEqual(model, "base")
        self.assertEqual(prompt, "KITT. Ei KITT.")

    def test_mock_transcribe_returns_empty_when_file_is_missing(self):
        result = transcribe_audio_file("/nonexistent/file.wav", "configured-model")
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

    def test_models_endpoint_reports_only_loaded_model(self):
        class FakeHandler(stt_server.LocalSTTRequestHandler):
            def __init__(self):
                self.sent_status = None
                self.sent_data = None

            def _send_json(self, status, data):
                self.sent_status = status
                self.sent_data = data

        original = stt_server._SERVER_MODEL_NAME
        try:
            stt_server._SERVER_MODEL_NAME = "configured-model"
            handler = FakeHandler()
            handler.path = "/v1/models"
            handler.do_GET()
            self.assertEqual(handler.sent_status, 200)
            self.assertEqual(
                [model["id"] for model in handler.sent_data["data"]],
                ["configured-model"],
            )

            stt_server._SERVER_MODEL_NAME = None
            empty = FakeHandler()
            empty.path = "/v1/models"
            empty.do_GET()
            self.assertEqual(empty.sent_data["data"], [])
        finally:
            stt_server._SERVER_MODEL_NAME = original

    def test_health_endpoint_reports_busy_and_stats(self):
        class FakeHandler(stt_server.LocalSTTRequestHandler):
            def __init__(self):
                self.sent_status = None
                self.sent_data = None

            def _send_json(self, status, data, headers=None):
                self.sent_status = status
                self.sent_data = data

        handler = FakeHandler()
        handler.path = "/health"
        handler.do_GET()
        self.assertEqual(handler.sent_status, 200)
        self.assertIn("busy", handler.sent_data)
        self.assertIn("requests_total", handler.sent_data)
        self.assertIn("last_transcription_ms", handler.sent_data)
        self.assertFalse(handler.sent_data["busy"])

        # Test busy state when lock is held
        with stt_server._TRANSCRIPTION_LOCK:
            busy_handler = FakeHandler()
            busy_handler.path = "/health"
            busy_handler.do_GET()
            self.assertTrue(busy_handler.sent_data["busy"])

    def test_transcribe_returns_rich_metadata_dict(self):
        result = transcribe_audio_file(
            "/nonexistent/file.wav",
            "test-model",
            return_metadata=True,
        )
        self.assertIsInstance(result, dict)
        self.assertIn("text", result)
        self.assertIn("language", result)
        self.assertIn("duration_ms", result)


if __name__ == "__main__":
    unittest.main()
