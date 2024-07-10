import json
from feature_analyzer import FeatureAnalyzer

class PhonemeConverter:
    def __init__(self, phoneme_features_file, language_phonemes_file, language_allophones_file):
        self.feature_analyzer = FeatureAnalyzer(phoneme_features_file, language_phonemes_file)
        with open(language_allophones_file, 'r', encoding='utf-8') as f:
            self.language_allophones = json.load(f)

    def convert_phoneme(self, source_phoneme, source_language, target_language):
        if source_language == target_language:
            return source_phoneme

        target_phonemes = self.feature_analyzer.language_phonemes.get(target_language, [])
        if not target_phonemes:
            return None

        similar_phonemes = self.feature_analyzer.find_similar_phonemes(source_phoneme, target_language)
        if not similar_phonemes:
            return None

        return similar_phonemes[0][0]  # Return the most similar phoneme

    def convert_word(self, word, source_language, target_language):
        converted_word = []
        for phoneme in word:
            converted_phoneme = self.convert_phoneme(phoneme, source_language, target_language)
            if converted_phoneme:
                converted_word.append(converted_phoneme)
            else:
                converted_word.append(phoneme)  # Keep original if no conversion found
        return converted_word

    def apply_allophone_rules(self, phonemes, language):
        result = []
        for phoneme in phonemes:
            allophones = self.language_allophones.get(language, {}).get(phoneme, [])
            if allophones:
                # For simplicity, we're just using the first allophone.
                # In a more advanced system, you'd apply context-dependent rules here.
                result.append(allophones[0])
            else:
                result.append(phoneme)
        return result

# # Usage example
# if __name__ == "__main__":
#     converter = PhonemeConverter('phoneme_features.json', 'language_phonemes.json', 'language_allophones.json')
    
#     # Example: Convert a word from one language to another
#     source_word = ['θ', 'ɪ', 'ŋ', 'k']  # "think" in English
#     source_language = 'eng1234'  # Replace with actual Glottocode for English
#     target_language = 'spa1234'  # Replace with actual Glottocode for Spanish
    
#     converted_word = converter.convert_word(source_word, source_language, target_language)
#     print(f"Original word: {source_word}")
#     print(f"Converted word: {converted_word}")
    
#     # Apply allophone rules
#     final_word = converter.apply_allophone_rules(converted_word, target_language)
#     print(f"After applying allophone rules: {final_word}")