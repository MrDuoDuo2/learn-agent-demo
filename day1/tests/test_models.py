import unittest

from pydantic import ValidationError

from models import StructuredAnswer


class StructuredAnswerTests(unittest.TestCase):
    def test_parses_valid_json_into_typed_fields(self) -> None:
        """Removing JSON parsing or field mapping must fail this test."""
        result = StructuredAnswer.model_validate_json(
            '{"answer": "hello", "confidence": 0.8}'
        )

        self.assertEqual(result.answer, "hello")
        self.assertEqual(result.confidence, 0.8)

    def test_rejects_confidence_above_one(self) -> None:
        """Removing the confidence upper bound must fail this test."""
        with self.assertRaises(ValidationError):
            StructuredAnswer.model_validate_json(
                '{"answer": "hello", "confidence": 1.1}'
            )

    def test_rejects_blank_answer(self) -> None:
        """Removing the required non-empty answer constraint must fail this test."""
        with self.assertRaises(ValidationError):
            StructuredAnswer.model_validate_json('{"answer": ""}')
