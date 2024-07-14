from .utils import get_phoneme_inventory, get_phoneme_features, load_json, get_data_file_path
from typing import List, Dict, Tuple

class FeatureAnalyzer:
    def __init__(self):
        self.language_phonemes = load_json(get_data_file_path('language_inventories/language_phonemes.json'))
        self.all_phoneme_features = load_json(get_data_file_path('phoneme_features/phoneme_features.json'))

    def get_language_features(self, language_code: str) -> Dict[str, Dict[str, str]]:
        phoneme_inventory = get_phoneme_inventory(language_code)
        return get_phoneme_features(phoneme_inventory, 'phoneme_features/phoneme_features.json')

    def compare_phonemes(self, phoneme1: str, phoneme2: str) -> Tuple[List[str], List[str]]:
        features1 = self.all_phoneme_features.get(phoneme1, {})
        features2 = self.all_phoneme_features.get(phoneme2, {})
        
        similar_features = []
        different_features = []
        
        all_features = set(features1.keys()) | set(features2.keys())
        
        for feature in all_features:
            if features1.get(feature) == features2.get(feature):
                similar_features.append(feature)
            else:
                different_features.append(feature)
        
        return similar_features, different_features

    def find_similar_phonemes(self, target_phoneme: str, language_code: str) -> List[Tuple[str, int]]:
        language_features = self.get_language_features(language_code)
        target_features = self.all_phoneme_features.get(target_phoneme, {})
        
        similarity_scores = []
        
        for phoneme, features in language_features.items():
            score = sum(1 for f in target_features if f in features and target_features[f] == features[f])
            similarity_scores.append((phoneme, score))
        
        return sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    def analyze_language_inventory(self, language_code: str) -> Dict[str, Dict[str, int]]:
        language_features = self.get_language_features(language_code)
        feature_counts = {}
        
        for phoneme, features in language_features.items():
            for feature, value in features.items():
                if feature not in feature_counts:
                    feature_counts[feature] = {}
                feature_counts[feature][value] = feature_counts[feature].get(value, 0) + 1
        
        return feature_counts