"""
util.py - Utility functions and classes for RiTa

Provides helper functions for:
- Syllable and phoneme manipulation
- Regular expression patterns for inflection
- Number/word conversions
- Phone data (consonants, vowels, onsets)
"""

import re
from typing import List, Optional, Any, Dict

class RE:
    """Regular expression pattern for word transformations (inflection, conjugation)"""

    def __init__(self, regex: str, offset: int, suffix: str = ''):
        """
        Create a regex-based word transformation rule

        Args:
            regex: Pattern to match against word
            offset: Number of characters to remove from end of word
            suffix: String to append after truncation
        """
        self.raw = regex
        self.regex = re.compile(regex)
        self.offset = offset
        self.suffix = suffix

    def applies(self, word: str) -> bool:
        """Check if this rule applies to the given word"""
        return bool(self.regex.search(word))

    def fire(self, word: str) -> str:
        """Apply the transformation to the word"""
        return self.truncate(word) + self.suffix

    def truncate(self, word: str) -> str:
        """Remove offset characters from end of word"""
        return word if self.offset == 0 else word[:-self.offset]

    def __repr__(self) -> str:
        return f'/{self.raw}/'

class Util:
    """Utility functions for phonetic and syllabic operations"""

    # Phoneme data
    CONSONANTS = [
        'b', 'ch', 'd', 'dh', 'f', 'g', 'hh', 'jh', 'k', 'l', 'm',
        'n', 'ng', 'p', 'r', 's', 'sh', 't', 'th', 'v', 'w', 'y', 'z', 'zh'
    ]

    VOWELS = [
        'aa', 'ae', 'ah', 'ao', 'aw', 'ax', 'ay', 'eh', 'er', 'ey', 'ih',
        'iy', 'ow', 'oy', 'uh', 'uw'
    ]

    ONSETS = [
        'p', 't', 'k', 'b', 'd', 'g', 'f', 'v', 'th', 'dh', 's', 'z',
        'sh', 'ch', 'jh', 'm', 'n', 'r', 'l', 'hh', 'w', 'y', 'p r', 't r',
        'k r', 'b r', 'd r', 'g r', 'f r', 'th r', 'sh r', 'p l', 'k l', 'b l',
        'g l', 'f l', 's l', 't w', 'k w', 'd w', 's w', 's p', 's t', 's k',
        's f', 's m', 's n', 'g w', 'sh w', 's p r', 's p l', 's t r', 's k r',
        's k w', 's k l', 'th w', 'zh', 'p y', 'k y', 'b y', 'f y', 'hh y',
        'v y', 'th y', 'm y', 's p y', 's k y', 'g y', 'hh w', ''
    ]

    # Number word mappings
    NUMBERS_FROM_WORDS = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
        'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
        'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
    }

    NUMBERS_TO_WORDS = {
        0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
        6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
        11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
        15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
        19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty',
        50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety'
    }

    @staticmethod
    def syllables_to_phones(syllables: List) -> str:
        """
        Convert syllabification structure to phone string

        Args:
            syllables: List of syllable structures [stress, onset, nucleus, coda]

        Returns:
            String of phonemes with dashes between phones, spaces between syllables
        """
        result = []
        for syl in syllables:
            stress, onset, nucleus, coda = syl[0], syl[1], syl[2], syl[3]

            # Add stress marker to first nucleus phone if present
            if stress and stress[0] and nucleus:
                nucleus = nucleus.copy()
                nucleus[0] = nucleus[0] + str(stress[0])

            # Combine onset + nucleus + coda
            data = onset + nucleus + coda
            result.append('-'.join(data))

        return ' '.join(result)

    @staticmethod
    def syllables_from_phones(phones_input: str) -> str:
        """
        Convert phone string to syllabified phone string
        Adapted from FreeTTS syllabification algorithm

        Args:
            phones_input: String of phones separated by dashes or spaces

        Returns:
            Syllabified phone string with spaces between syllables
        """
        if not phones_input:
            return ''

        syllables = []
        internuclei = []  # Consonants between nuclei

        # Split input into individual phonemes
        phones = phones_input.replace('-', ' ').split()

        for phoneme in phones:
            phoneme = phoneme.strip()
            if not phoneme:
                continue

            # Check for stress marker
            stress = None
            if phoneme and phoneme[-1].isdigit():
                stress = phoneme[-1]
                phoneme = phoneme[:-1]

            # Vowel - create new syllable
            if phoneme in Util.VOWELS:
                # Split internuclei into coda (for previous syllable) and onset (for this one)
                coda, onset = [], []

                # Find the best split point (maximize onset validity)
                for split in range(len(internuclei) + 1):
                    coda = internuclei[:split]
                    onset = internuclei[split:]

                    # Valid onset, or first syllable, or no more options
                    onset_str = ' '.join(onset)
                    if onset_str in Util.ONSETS or len(syllables) == 0 or len(onset) == 0:
                        break

                # Attach coda to previous syllable
                if syllables:
                    syllables[-1][3].extend(coda)

                # Create new syllable: [stress, onset, nucleus, coda]
                syllables.append([[stress], onset, [phoneme], []])
                internuclei = []

            # Consonant
            elif phoneme in Util.CONSONANTS or phoneme == ' ':
                if phoneme != ' ':
                    internuclei.append(phoneme)

            # Invalid phoneme
            else:
                raise ValueError(f'Invalid phoneme: {phoneme}')

        # Handle remaining consonants at end
        if internuclei:
            if not syllables:
                syllables.append([[None], internuclei, [], []])
            else:
                syllables[-1][3].extend(internuclei)

        return Util.syllables_to_phones(syllables)

    @staticmethod
    def is_num(value: Any) -> bool:
        """Check if value is a number"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def num_opt(opts: Optional[Dict], name: str, default: float = 0) -> float:
        """
        Get numeric option from dict with fallback

        Args:
            opts: Options dictionary (can be None)
            name: Key to look up
            default: Default value if not found or not numeric

        Returns:
            Numeric value or default
        """
        if opts is None:
            return default
        value = opts.get(name)
        return value if Util.is_num(value) else default

# For backwards compatibility with JS API
Phones = {
    'consonants': Util.CONSONANTS,
    'vowels': Util.VOWELS,
    'onsets': Util.ONSETS
}

Numbers = {
    'fromWords': Util.NUMBERS_FROM_WORDS,
    'toWords': Util.NUMBERS_TO_WORDS
}
