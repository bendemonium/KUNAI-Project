import json
from collections import defaultdict

class FeatureAnalyzer:
    def __init__(self, phoneme_features_file, language_phonemes_file):
        with open(phoneme_features_file, 'r', encoding='utf-8') as f:
            self.phoneme_features = json.load(f)
        with open(language_phonemes_file, 'r', encoding='utf-8') as f:
            self.language_phonemes = json.load(f)

    def get_phoneme_features(self, phoneme):
        return self.phoneme_features.get(phoneme, {})

    def compare_phonemes(self, phoneme1, phoneme2):
        features1 = self.get_phoneme_features(phoneme1)
        features2 = self.get_phoneme_features(phoneme2)
        
        similar_features = []
        different_features = []
        
        for feature in features1.keys():
            if feature in features2:
                if features1[feature] == features2[feature]:
                    similar_features.append(feature)
                else:
                    different_features.append(feature)
        
        return similar_features, different_features

    def find_similar_phonemes(self, target_phoneme, language_code):
        target_features = self.get_phoneme_features(target_phoneme)
        language_phonemes = self.language_phonemes.get(language_code, [])
        
        similarity_scores = {}
        
        for phoneme in language_phonemes:
            phoneme_features = self.get_phoneme_features(phoneme)
            score = sum(1 for f in target_features if f in phoneme_features and target_features[f] == phoneme_features[f])
            similarity_scores[phoneme] = score
        
        return sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

    def analyze_language_inventory(self, language_code):
        phonemes = self.language_phonemes.get(language_code, [])
        feature_counts = defaultdict(lambda: defaultdict(int))
        
        for phoneme in phonemes:
            features = self.get_phoneme_features(phoneme)
            for feature, value in features.items():
                feature_counts[feature][value] += 1
        
        return dict(feature_counts)

# # Usage example
# if __name__ == "__main__":
#     analyzer = FeatureAnalyzer('phoneme_features.json', 'language_phonemes.json')
    
#     # Example: Compare two phonemes
#     similar, different = analyzer.compare_phonemes('p', 'b')
#     print(f"Similar features of 'p' and 'b': {similar}")
#     print(f"Different features of 'p' and 'b': {different}")
    
#     # Example: Find similar phonemes in a language
#     similar_phonemes = analyzer.find_similar_phonemes('θ', 'eng1234')  # Replace with actual Glottocode
#     print(f"Phonemes similar to 'θ' in English: {similar_phonemes[:5]}")  # Top 5 similar phonemes
    
#     # Example: Analyze language inventory
#     inventory_analysis = analyzer.analyze_language_inventory('eng1234')  # Replace with actual Glottocode
#     print("English phoneme inventory analysis:")
#     for feature, values in inventory_analysis.items():
#         print(f"{feature}: {values}")