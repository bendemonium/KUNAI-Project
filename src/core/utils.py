import json
import os
import re
from typing import Dict, List, Any

def load_json(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_data_file_path(file_name: str) -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', file_name)

def get_phoneme_features(phoneme_inventory: List[str], phoneme_features_file: str) -> Dict[str, Dict[str, str]]:
    all_phoneme_features = load_json(get_data_file_path(phoneme_features_file))
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

def get_phoneme_inventory(language_code: str) -> List[str]:
    language_phonemes = load_json(get_data_file_path('language_inventories/language_phonemes.json'))
    
    if language_code not in language_phonemes:
        raise ValueError(f"Language code '{language_code}' not found in the phoneme database.")
    
    return language_phonemes[language_code]

def ipa_to_regex(ipa_string: str) -> str:
    special_chars = r'[](){}?*+|^$.\\'
    return ''.join('\\' + char if char in special_chars else char for char in ipa_string)

class PhonemeTokenizer:
    def __init__(self, language_code: str):
        phoneme_inventory = get_phoneme_inventory(language_code)
        self.phoneme_inventory = sorted(phoneme_inventory, key=len, reverse=True)
        self.phoneme_pattern = re.compile('|'.join(map(ipa_to_regex, self.phoneme_inventory)))
    
    def tokenize(self, text: str) -> List[str]:
        return self.phoneme_pattern.findall(text)

# Load global data
language_phonemes = load_json(get_data_file_path('language_inventories/language_phonemes.json'))
language_allophones = load_json(get_data_file_path('language_inventories/language_allophones.json'))
prosodic_features = load_json(get_data_file_path('language_inventories/prosodic_features.json'))
phoneme_features = load_json(get_data_file_path('phoneme_features/phoneme_features.json'))