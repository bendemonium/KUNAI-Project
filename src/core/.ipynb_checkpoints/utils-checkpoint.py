import json
import re
from typing import Dict, List, Any

def find_phoneme_context(text: str, phoneme: str, context_size: int = 1) -> List[str]:
    """Find all occurrences of a phoneme in the text and return its context."""
    pattern = f"(?=(.{{{context_size}}}{ipa_to_regex(phoneme)}.{{{context_size}}}))"
    return re.findall(pattern, text)

def get_language_name(glottocode: str, language_data: Dict[str, Dict[str, str]]) -> str:
    """Get the language name for a given Glottocode."""
    return language_data.get(glottocode, {}).get('LanguageName', 'Unknown')

class PhonemeTokenizer:
    def __init__(self, phoneme_inventory: List[str]):
        self.phoneme_inventory = sorted(phoneme_inventory, key=len, reverse=True)
        self.phoneme_pattern = re.compile('|'.join(map(ipa_to_regex, self.phoneme_inventory)))
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into phonemes."""
        return self.phoneme_pattern.findall(text)