from typing import List, Tuple, Dict
from .utils import get_phoneme_inventory, get_phoneme_features

class FeatureAnalyzer:
    def __init__(self):
        pass

    def get_language_features(self, language_code: str) -> Dict[str, Dict[str, str]]:
        phoneme_inventory = get_phoneme_inventory(language_code)
        return get_phoneme_features(phoneme_inventory, 'phoneme_features/phoneme_features.json')

    def compare_phonemes(self, phoneme1: str, phoneme2: str) -> Tuple[List[str], List[str]]:
        features1 = get_phoneme_features([phoneme1], 'phoneme_features/phoneme_features.json')[phoneme1]
        features2 = get_phoneme_features([phoneme2], 'phoneme_features/phoneme_features.json')[phoneme2]
        
        similar_features = []
        different_features = []
        
        all_features = set(features1.keys()) | set(features2.keys())
        
        for feature in all_features:
            if features1.get(feature) == features2.get(feature):
                similar_features.append(feature)
            else:
                different_features.append(feature)
        
        return similar_features, different_features

    def find_similar_phonemes(self, target_phoneme: str, source_language: str, target_language: str) -> List[Tuple[str, int]]:
        source_features = get_phoneme_features([target_phoneme], 'phoneme_features/phoneme_features.json')[target_phoneme]
        target_inventory = get_phoneme_inventory(target_language)
        target_features = get_phoneme_features(target_inventory, 'phoneme_features/phoneme_features.json')
        
        similarity_scores = []
        
        for phoneme, features in target_features.items():
            score = sum(1 for f in source_features if f in features and source_features[f] == features[f])
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