import json
import re
from typing import Dict, List, Any

language_phonemes_file = "language_phonemes.json"
phoneme_features_file = "phoneme_features.json"

def load_json(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_phoneme_features(phoneme_inventory: List[str], phoneme_features_file: str) -> Dict[str, Dict[str, str]]:
    """
    Get the features for a given phoneme inventory.
    
    Args:
    phoneme_inventory (List[str]): List of phonemes.
    phoneme_features_file (str): Path to the phoneme_features.json file.
    
    Returns:
    Dict[str, Dict[str, str]]: A dictionary mapping each phoneme to its features.
    """
    all_phoneme_features = load_json(phoneme_features_file)
    inventory_features = {}
    missing_phonemes = []
    
    for phoneme in phoneme_inventory:
        if phoneme in all_phoneme_features:
            inventory_features[phoneme] = all_phoneme_features[phoneme]
        else:
            missing_phonemes.append(phoneme)
    
    if missing_phonemes:
        print(f"Warning: The following phonemes were not found in the features database: {', '.join(missing_phonemes)}")
    
    return inventory_features

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

def get_phoneme_inventory(language_code: str, language_phonemes_file: str) -> List[str]:
    """
    Get the phoneme inventory for a specific language.
    
    Args:
    language_code (str): The Glottocode or unique identifier for the language.
    language_phonemes_file (str): Path to the language_phonemes.json file.
    
    Returns:
    List[str]: A list of phonemes in the language's inventory.
    """
    language_phonemes = load_json(language_phonemes_file)
    
    if language_code not in language_phonemes:
        raise ValueError(f"Language code '{language_code}' not found in the phoneme database.")
    
    return language_phonemes[language_code]

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
    def __init__(self, language_code):
        phoneme_inventory = get_phoneme_inventory(language_code, language_phonemes_file)
        self.phoneme_inventory = sorted(phoneme_inventory, key=len, reverse=True)
        self.phoneme_pattern = re.compile('|'.join(map(ipa_to_regex, self.phoneme_inventory)))
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into phonemes."""
        return self.phoneme_pattern.findall(text)

