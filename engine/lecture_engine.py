"""Transparent local reference engine for transcript intelligence.

This module uses deterministic NLP so the product remains useful without a
downloaded model. Its output contract can be retained when optional speech and
local language-model adapters are connected.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable


STOPWORDS = {
    "a", "about", "after", "again", "all", "also", "am", "an", "and", "any",
    "are", "as", "at", "be", "because", "been", "before", "being", "between",
    "both", "but", "by", "can", "could", "did", "do", "does", "doing", "during",
    "each", "for", "from", "further", "had", "has", "have", "having", "he", "her",
    "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in",
    "into", "is", "it", "its", "itself", "just", "more", "most", "no", "nor",
    "not", "now", "of", "off", "on", "once", "only", "or", "other", "our",
    "ours", "out", "over", "own", "same", "she", "should", "so", "some", "such",
    "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there",
    "these", "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "we", "were", "what", "when", "where", "which", "while", "who",
    "why", "will", "with", "would", "you", "your", "today", "let", "us"
}

MALAYALAM_GLOSSARY = {
    "algorithm": "അൽഗോരിതം — പ്രശ്നം പരിഹരിക്കുന്ന ഘട്ടങ്ങളുടെ ക്രമം",
    "classification": "വർഗ്ഗീകരണം — ഡാറ്റയെ വിഭാഗങ്ങളിലാക്കൽ",
    "dataset": "ഡാറ്റാസെറ്റ് — ക്രമപ്പെടുത്തിയ ഡാറ്റയുടെ ശേഖരം",
    "feature": "ഫീച്ചർ — മോഡൽ പഠിക്കാൻ ഉപയോഗിക്കുന്ന ഇൻപുട്ട് ഗുണം",
    "inference": "ഇൻഫറൻസ് — പരിശീലിച്ച മോഡൽ ഉപയോഗിച്ച് പ്രവചിക്കൽ",
    "machine learning": "മെഷീൻ ലേണിംഗ് — ഡാറ്റയിൽ നിന്ന് മാതൃകകൾ പഠിക്കുന്ന രീതികൾ",
    "model": "മോഡൽ — പഠിച്ച ബന്ധങ്ങളെ പ്രതിനിധീകരിക്കുന്ന സംവിധാനം",
    "overfitting": "ഓവർഫിറ്റിംഗ് — പരിശീലന ഡാറ്റയെ അതിയായി ഓർമ്മിക്കുന്ന അവസ്ഥ",
    "regression": "റിഗ്രഷൻ — തുടർച്ചയായ സംഖ്യാ മൂല്യം പ്രവചിക്കൽ",
    "supervised learning": "സൂപ്പർവൈസ്ഡ് ലേണിംഗ് — ലേബൽ ചെയ്ത ഉദാഹരണങ്ങളിൽ നിന്ന് പഠിക്കൽ",
    "testing data": "ടെസ്റ്റിംഗ് ഡാറ്റ — അന്തിമ വിലയിരുത്തലിന് മാറ്റിവെച്ച ഡാറ്റ",
    "training data": "ട്രെയിനിംഗ് ഡാറ്റ — മോഡൽ പഠിക്കാൻ ഉപയോഗിക്കുന്ന ഡാറ്റ",
    "validation data": "വാലിഡേഷൻ ഡാറ്റ — മോഡൽ തിരഞ്ഞെടുപ്പിനും ട്യൂണിംഗിനും ഉപയോഗിക്കുന്ന ഡാറ്റ",
}

CUE_WORDS = {
    "important": 1.35,
    "remember": 1.4,
    "therefore": 1.2,
    "means": 1.15,
    "defined": 1.25,
    "because": 1.1,
    "exam": 1.3,
    "key": 1.25,
    "difference": 1.15,
}


@dataclass(frozen=True)
class Sentence:
    index: int
    text: str
    tokens: tuple[str, ...]


class LectureEngine:
    """Generate evidence-linked learning assets from a transcript."""

    version = "0.1.0-local"

    def _sentences(self, transcript: str) -> list[Sentence]:
        cleaned = re.sub(r"\s+", " ", transcript).strip()
        if not cleaned:
            return []
        parts = re.split(r"(?<=[.!?])\s+|\n+", cleaned)
        result: list[Sentence] = []
        for part in parts:
            part = part.strip(" -\t")
            if len(part.split()) < 3:
                continue
            tokens = tuple(self._content_tokens(part))
            result.append(Sentence(len(result), part, tokens))
        return result

    @staticmethod
    def _words(text: str) -> list[str]:
        return re.findall(r"[a-zA-Z][a-zA-Z0-9'-]*", text.lower())

    def _content_tokens(self, text: str) -> Iterable[str]:
        for word in self._words(text):
            if word not in STOPWORDS and len(word) > 2:
                yield word

    @staticmethod
    def _timestamp(word_offset: int, words_per_minute: int = 130) -> str:
        seconds = round((word_offset / words_per_minute) * 60)
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def _concepts(self, sentences: list[Sentence], limit: int = 10) -> list[dict]:
        unigrams: Counter[str] = Counter()
        bigrams: Counter[str] = Counter()
        first_seen: dict[str, int] = {}

        for sentence in sentences:
            for token in sentence.tokens:
                unigrams[token] += 1
                first_seen.setdefault(token, sentence.index)
            for left, right in zip(sentence.tokens, sentence.tokens[1:]):
                phrase = f"{left} {right}"
                bigrams[phrase] += 1
                first_seen.setdefault(phrase, sentence.index)

        candidates: list[tuple[str, float, int]] = []
        for term, count in unigrams.items():
            candidates.append((term, float(count), first_seen[term]))
        for phrase, count in bigrams.items():
            if count >= 2 or phrase in MALAYALAM_GLOSSARY:
                candidates.append((phrase, count * 1.8, first_seen[phrase]))

        candidates.sort(key=lambda item: (-item[1], item[2], item[0]))
        selected: list[dict] = []
        covered: set[str] = set()
        for term, score, first in candidates:
            words = set(term.split())
            if len(words) == 1 and words & covered:
                continue
            selected.append(
                {
                    "term": term.title(),
                    "mentions": max(1, int(round(score if " " not in term else score / 1.8))),
                    "first_source": first + 1,
                }
            )
            covered.update(words)
            if len(selected) >= limit:
                break
        return selected

    def _score_sentences(self, sentences: list[Sentence]) -> list[tuple[float, Sentence]]:
        frequencies = Counter(token for sentence in sentences for token in sentence.tokens)
        if not frequencies:
            return [(0.0, sentence) for sentence in sentences]
        maximum = max(frequencies.values())
        weights = {word: count / maximum for word, count in frequencies.items()}
        scored: list[tuple[float, Sentence]] = []
        for sentence in sentences:
            if not sentence.tokens:
                scored.append((0.0, sentence))
                continue
            base = sum(weights[token] for token in sentence.tokens) / math.sqrt(len(sentence.tokens))
            lower = sentence.text.lower()
            cue_boost = max((boost for cue, boost in CUE_WORDS.items() if cue in lower), default=1.0)
            length_penalty = 0.82 if len(sentence.tokens) > 34 else 1.0
            scored.append((base * cue_boost * length_penalty, sentence))
        return scored

    def _summary(self, sentences: list[Sentence]) -> list[dict]:
        scored = self._score_sentences(sentences)
        count = min(5, max(2, round(len(sentences) * 0.28)))
        chosen = sorted(sorted(scored, key=lambda item: item[0], reverse=True)[:count], key=lambda item: item[1].index)
        return [
            {"text": sentence.text, "source": sentence.index + 1, "relevance": round(score, 2)}
            for score, sentence in chosen
        ]

    def _review_flags(self, sentences: list[Sentence]) -> list[dict]:
        flags: list[dict] = []
        word_offset = 0
        for sentence in sentences:
            word_count = len(self._words(sentence.text))
            density = len(set(sentence.tokens)) / max(1, word_count)
            reasons: list[str] = []
            if word_count >= 27:
                reasons.append("long explanation")
            if density >= 0.62 and len(sentence.tokens) >= 12:
                reasons.append("high concept density")
            if re.search(r"\b(?:however|except|unless|whereas|difference|trade-off|bias|variance)\b", sentence.text, re.I):
                reasons.append("contrast or exception")
            if reasons:
                flags.append(
                    {
                        "time": self._timestamp(word_offset),
                        "source": sentence.index + 1,
                        "reason": ", ".join(reasons),
                        "text": sentence.text,
                    }
                )
            word_offset += word_count
        return flags[:5]

    def _quiz(self, sentences: list[Sentence], concepts: list[dict]) -> list[dict]:
        terms = [item["term"] for item in concepts]
        questions: list[dict] = []
        for concept in concepts:
            term = concept["term"]
            source = next((s for s in sentences if term.lower() in s.text.lower()), None)
            if source is None:
                continue
            prompt = re.sub(re.escape(term), "_____", source.text, count=1, flags=re.I)
            if prompt == source.text:
                continue
            distractors = [candidate for candidate in terms if candidate != term][:3]
            if len(distractors) < 3:
                continue
            options = [term, *distractors]
            rotation = source.index % len(options)
            options = options[rotation:] + options[:rotation]
            questions.append(
                {
                    "question": f"Complete the idea: {prompt}",
                    "options": options,
                    "answer": term,
                    "source": source.index + 1,
                }
            )
            if len(questions) >= 4:
                break
        return questions

    def _glossary(self, transcript: str, concepts: list[dict]) -> list[dict]:
        lower = transcript.lower()
        glossary: list[dict] = []
        selected = {item["term"].lower() for item in concepts}
        for term, explanation in MALAYALAM_GLOSSARY.items():
            if term in lower or term in selected:
                glossary.append({"term": term.title(), "malayalam": explanation})
        return glossary[:8]

    def analyze(self, transcript: str, title: str = "Untitled lecture", subject: str = "General") -> dict:
        transcript = transcript.strip()
        if len(transcript) < 80:
            raise ValueError("Please provide at least 80 characters of lecture transcript.")
        if len(transcript) > 120_000:
            raise ValueError("Transcript is too large for this release (maximum 120,000 characters).")

        sentences = self._sentences(transcript)
        if len(sentences) < 2:
            raise ValueError("The transcript needs at least two complete sentences.")

        concepts = self._concepts(sentences)
        word_count = len(self._words(transcript))
        return {
            "title": title.strip() or "Untitled lecture",
            "subject": subject.strip() or "General",
            "summary": self._summary(sentences),
            "concepts": concepts,
            "review_flags": self._review_flags(sentences),
            "quiz": self._quiz(sentences, concepts),
            "glossary": self._glossary(transcript, concepts),
            "sources": [{"id": s.index + 1, "text": s.text} for s in sentences],
            "metrics": {
                "words": word_count,
                "sentences": len(sentences),
                "reading_minutes": max(1, round(word_count / 180)),
                "concepts": len(concepts),
                "review_flags": len(self._review_flags(sentences)),
                "external_calls": 0,
            },
            "engine": {
                "name": "LectureLens Extractive Edge Engine",
                "version": self.version,
                "mode": "portable-reference",
                "data_uploaded": "0 bytes",
            },
        }

    def answer(self, transcript: str, question: str) -> dict:
        sentences = self._sentences(transcript)
        question_tokens = set(self._content_tokens(question))
        if not sentences or not question_tokens:
            return {
                "answer": "I need a clearer question and a lecture transcript.",
                "supported": False,
                "source": None,
                "score": 0,
            }

        ranked: list[tuple[float, Sentence]] = []
        for sentence in sentences:
            sentence_tokens = set(sentence.tokens)
            overlap = question_tokens & sentence_tokens
            coverage = len(overlap) / len(question_tokens)
            specificity = len(overlap) / max(1, len(sentence_tokens))
            ranked.append((coverage * 0.8 + specificity * 0.2, sentence))

        score, best = max(ranked, key=lambda item: item[0])
        if score < 0.12:
            return {
                "answer": "The lecture does not contain enough evidence to answer that. Try asking about a named concept from the notes.",
                "supported": False,
                "source": None,
                "score": round(score, 2),
            }
        return {
            "answer": best.text,
            "supported": True,
            "source": best.index + 1,
            "score": round(score, 2),
        }
