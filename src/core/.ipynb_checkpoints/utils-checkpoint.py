import json
import re
from typing import Dict, List, Any

def load_json(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def phoneme_to_feature_vector(phoneme: str, feature_data: Dict[str, Dict[str, str]]) -> List[int]:
    """Convert a phoneme to a binary feature vector."""
    if phoneme not in feature_data:
        return []
    
    features = feature_data[phoneme]
    return [1 if features.get(feature, '') == '+' else 0 for feature in sorted(features.keys())]

def feature_vector_to_phoneme(vector: List[int], feature_data: Dict[str, Dict[str, str]]) -> str:
    """Convert a binary feature vector back to the closest matching phoneme."""
    features = sorted(next(iter(feature_data.values())).keys())
    target_features = {feature: '+' if value == 1 else '-' for feature, value in zip(features, vector)}
    
    best_match = None
    best_score = -1
    
    for phoneme, phon_features in feature_data.items():
        score = sum(1 for f in features if phon_features.get(f, '') == target_features[f])
        if score > best_score:
            best_score = score
            best_match = phoneme
    
    return best_match

def ipa_to_regex(ipa_string: str) -> str:
    """Convert IPA string to a regex pattern, escaping special characters."""
    special_chars = r'[](){}?*+|^$.\\'
    return ''.join('\\' + char if char in special_chars else char for char in ipa_string)

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

