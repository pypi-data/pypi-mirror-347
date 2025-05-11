from re import compile
from itertools import count
from typing import Iterator, Tuple


class RangeSummarizer:
    """
    Examine text for integers and provide a method to summarize the contiguous ranges.

    @param initial_text: Text to examine immediately (instead of requiring it to be
        passed to the add() function.
    @param match_negatives: Look for hyphens before strings of digits so that negative
        numbers are identified. Note that if this is False, a string containing "abc-34"
        will result in the number 34 being collected. There is currently no way to
        completely ignore negative numbers.
    @param require_word_boundaries: Only collect numbers that do not appear as part of
        a word. So "abc34def" will not collect 34 unless False is passed for this option.
    """

    def __init__(
        self,
        initial_text=None,
        match_negatives: bool = True,
        require_word_boundaries: bool = True,
    ) -> None:
        self.numbers: set[int] = set()
        if require_word_boundaries:
            left = r"(?<!\w)"
            right = r"(?!\w)"
        else:
            left = right = ""
        negatives = "-?" if match_negatives else ""
        self.regex = compile(rf"{left}({negatives}\d+){right}")

        if initial_text:
            self.add(initial_text)

    def add(self, text: str) -> None:
        """
        Extract numbers from the given text and add them to self.
        """
        for match in self.regex.finditer(text):
            number = int(match.group(0))
            self.numbers.add(number)

    def ranges(self) -> Iterator[Tuple[int, int]]:
        """
        Return a generator that yields (low, high) tuples of integers
        indicating ranges of integers that have been seen in the provided
        text so far. Ranges are given according to the Python closed-open
        convention (the low value is included in the range, the high value is
        not). Ranges are yielded in increasing order of the tuple 'low'
        values.
        """
        numbers = set(self.numbers)
        while numbers:
            low = min(numbers)
            for number in count(low):
                if number in numbers:
                    numbers.remove(number)
                else:
                    yield (low, number)
                    break
