import unittest

from engine.lecture_engine import LectureEngine


TRANSCRIPT = (
    "Supervised learning uses labelled examples to learn a relationship between features and targets. "
    "Training data teaches the model, while validation data helps select settings and testing data checks final performance. "
    "Testing data must remain separate because using it during development causes data leakage. "
    "Classification predicts a category, whereas regression predicts a continuous value. "
    "Overfitting happens when a model memorises training noise and performs poorly on unseen data. "
    "Regularisation and representative data can reduce overfitting."
)


class LectureEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = LectureEngine()

    def test_analysis_contains_grounded_assets(self):
        result = self.engine.analyze(TRANSCRIPT, "ML Basics", "Machine Learning")
        self.assertEqual(result["title"], "ML Basics")
        self.assertGreaterEqual(len(result["summary"]), 2)
        self.assertTrue(all(1 <= item["source"] <= len(result["sources"]) for item in result["summary"]))
        self.assertEqual(result["metrics"]["external_calls"], 0)

    def test_analysis_identifies_the_local_engine(self):
        result = self.engine.analyze(TRANSCRIPT)
        self.assertEqual(result["engine"]["version"], "0.1.0-local")
        self.assertEqual(result["engine"]["mode"], "portable-reference")
        self.assertEqual(result["engine"]["data_uploaded"], "0 bytes")

    def test_glossary_uses_terms_present_in_the_transcript(self):
        result = self.engine.analyze(TRANSCRIPT)
        terms = {item["term"].lower() for item in result["glossary"]}
        self.assertIn("classification", terms)
        self.assertIn("regression", terms)

    def test_answer_is_linked_to_source(self):
        result = self.engine.answer(TRANSCRIPT, "Why should testing data remain separate?")
        self.assertTrue(result["supported"])
        self.assertIsInstance(result["source"], int)
        self.assertIn("data", result["answer"].lower())

    def test_refuses_unsupported_question(self):
        result = self.engine.answer(TRANSCRIPT, "What is the capital of France?")
        self.assertFalse(result["supported"])
        self.assertIsNone(result["source"])

    def test_rejects_short_input(self):
        with self.assertRaises(ValueError):
            self.engine.analyze("Too short.")

    def test_rejects_oversized_input(self):
        with self.assertRaises(ValueError):
            self.engine.analyze("word " * 25_000)


if __name__ == "__main__":
    unittest.main()
