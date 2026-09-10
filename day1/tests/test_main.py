import tempfile
import unittest
from pathlib import Path

from main import load_config


class MainConfigTests(unittest.TestCase):
    def test_load_config_reads_required_values_from_json(self) -> None:
        """Replacing file configuration with environment lookup must fail this test."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            config_path = Path(temporary_directory) / "config.json"
            config_path.write_text(
                """{
  "api_url": "https://example.test/v1/chat/completions",
  "api_key": "test-key",
  "model": "test-model"
}""",
                encoding="utf-8",
            )

            config = load_config(config_path)

        self.assertEqual(config.api_url, "https://example.test/v1/chat/completions")
        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(config.model, "test-model")

    def test_load_config_rejects_missing_json_value(self) -> None:
        """Removing configuration validation must fail this test."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            config_path = Path(temporary_directory) / "config.json"
            config_path.write_text(
                """{
  "api_url": "https://example.test/v1/chat/completions",
  "api_key": "",
  "model": "test-model"
}""",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "api_key"):
                load_config(config_path)

    def test_load_config_rejects_invalid_json(self) -> None:
        """Removing JSON parsing must fail this test."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            config_path = Path(temporary_directory) / "config.json"
            config_path.write_text("not JSON", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "valid JSON"):
                load_config(config_path)
