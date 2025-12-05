"""Word Manager Class

Responsibilities:
- Load 20 sub-dictionary files `subdict_01.txt`..`subdict_20.txt` from the `dictionaries` folder.
- Provide random selection from a single dictionary.
- Provide three-word selection for the three clouds (consecutive dictionaries: level, level+1, level+2).
- Track how many times each dictionary is pulled from and how many correct guesses came from each dictionary.
- Progress difficulty (increase base level) after a configurable number of correct guesses (default = 5).

This module intentionally keeps behavior simple and in-memory (no persistence).
"""

from __future__ import annotations

import os
import random
from typing import List, Tuple, Dict, Optional

from .word import Word


class WordManager:
    def __init__(self,
                 dict_dir: str = "dictionaries",
                 start_level: int = 1,
                 difficulty_threshold: int = 5,
                 seed: Optional[int] = None):
        """Initialize the WordManager.

        Args:
            dict_dir: directory containing `subdict_XX.txt` files.
            start_level: starting base difficulty level (1..18).
            difficulty_threshold: number of correct guesses across the current triple required to increase level.
            seed: optional random seed for deterministic selection (useful for testing).
        """
        self.dict_dir = dict_dir
        self.min_level = 1
        self.max_level = 18  # base level; clouds use level, level+1, level+2 up to 20
        # clamp start level
        self.current_level = max(self.min_level, min(start_level, self.max_level))

        self.difficulty_threshold = max(1, int(difficulty_threshold))

        # Internal storage
        self.dicts: List[List[Tuple[str, int]]] = []  # index 0 -> subdict_01.txt

        # Simplified progression: count total correct guesses in-session.
        self._global_corrects: int = 0

        # Randomness
        self._rand = random.Random(seed)

        # Load dictionaries
        self.load_dictionaries(self.dict_dir)

    # ------------------ Loading ------------------
    def load_dictionaries(self, dict_dir: Optional[str] = None) -> None:
        """Load the 20 subdict files into memory.

        Files are expected to be named `subdict_01.txt`..`subdict_20.txt` and contain lines `word|score`.
        Missing files will be treated as empty dictionaries.
        """
        if dict_dir is None:
            dict_dir = self.dict_dir
        self.dicts = []
        for i in range(1, 21):
            filename = os.path.join(dict_dir, f"subdict_{i:02d}.txt")
            entries: List[Tuple[str, int]] = []
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        if "|" in line:
                            w, s = line.split("|", 1)
                            try:
                                score = int(s)
                            except Exception:
                                # skip malformed score lines
                                continue
                            entries.append((w, score))
                        else:
                            # fallback: if file contains plain words (no score), assign default score
                            entries.append((line, 0))
            except FileNotFoundError:
                entries = []
            self.dicts.append(entries)

    # ------------------ Selection ------------------
    def _find_nearest_nonempty_index(self, idx: int) -> Optional[int]:
        """If requested index is empty, find nearest non-empty dictionary index.

        Returns 0-based index or None if none available.
        """
        n = len(self.dicts)
        if 0 <= idx < n and self.dicts[idx]:
            return idx
        # expand outwards
        for dist in range(1, n):
            hi = idx + dist
            lo = idx - dist
            if hi < n and self.dicts[hi]:
                return hi
            if lo >= 0 and self.dicts[lo]:
                return lo
        return None

    def get_random_from_dict(self, dict_num: int) -> Word:
        """Return a random `Word` from a single dictionary numbered 1..20.

        The returned `Word` object will have an additional attribute `source_dict` (1-based index).
        This function updates internal `pull_counts` and `_last_pulled_map`.
        """
        if not (1 <= dict_num <= 20):
            raise ValueError("dict_num must be between 1 and 20 (inclusive)")
        idx = dict_num - 1
        found = self._find_nearest_nonempty_index(idx)
        if found is None:
            raise RuntimeError("No dictionaries available to select from")

        word_text, score = self._rand.choice(self.dicts[found])
        w = Word(score, word_text)
        # attach metadata for downstream consumers
        try:
            setattr(w, "source_dict", found + 1)
        except Exception:
            # best-effort - Word is a plain object so this should succeed
            pass
        return w

    def get_three_cloud_words(self, increment_correct: bool = False) -> List[Word]:
        """Return three Word objects for the three clouds based on `current_level`.

        The cloud dictionaries are `current_level`, `current_level+1`, `current_level+2` (1-based).
        Ensures attempts to avoid duplicate word texts among the three selected words.

        If `increment_correct` is True, treat this call as the result of a correct guess and
        apply the global-correct increment (which may increase difficulty before selecting words).
        """
        # If requested, count this call as the result of a correct guess and possibly increase difficulty
        if increment_correct:
            self._apply_correct_increment()

        words: List[Word] = []
        seen: set[str] = set()
        for offset in range(3):
            dict_num = self.current_level + offset
            # clamp to 20
            if dict_num > 20:
                dict_num = 20
            attempts = 0
            chosen: Optional[Word] = None
            while attempts < 10:
                candidate = self.get_random_from_dict(dict_num)
                if candidate.word not in seen:
                    chosen = candidate
                    break
                attempts += 1
            # if duplicate persisted, accept last candidate
            if chosen is None:
                chosen = candidate
            words.append(chosen)
            seen.add(chosen.word)
        return words

    def _apply_correct_increment(self) -> bool:
        """Internal helper: increment the global correct counter and increase level when threshold reached.

        Returns True if the difficulty level was increased.
        """
        self._global_corrects += 1
        if self._global_corrects >= self.difficulty_threshold:
            increased = self._increment_level()
            if increased:
                self._global_corrects = 0
                return True
        return False

    # ------------------ Progression ------------------

    def _increment_level(self) -> bool:
        """Increment base difficulty level by 1 (keeping triple adjacency). Returns True if changed."""
        if self.current_level < self.max_level:
            self.current_level += 1
            return True
        return False

    # ------------------ Utilities ------------------
    def get_status(self) -> Dict[str, object]:
        """Return diagnostic information for UI/logging."""
        return {
            "current_level": self.current_level,
            "difficulty_threshold": self.difficulty_threshold,
            "global_corrects": self._global_corrects,
        }

    def reset_progress(self) -> None:
        """Reset pull/correct counters and set level back to minimum."""
        self._global_corrects = 0
        self.current_level = self.min_level
