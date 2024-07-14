from .utils import load_json, get_data_file_path
from .feature_analyzer import FeatureAnalyzer
from typing import List, Dict, Any, Tuple

class PhonemeConverter:
    def __init__(self):
        self.feature_analyzer = FeatureAnalyzer()
        self.prosodic_features = load_json(get_data_file_path('language_inventories/prosodic_features.json'))

    def convert_phoneme(self, source_phoneme: str, source_language: str, target_language: str) -> str:
        if source_language == target_language:
            return source_phoneme

        similar_phonemes = self.feature_analyzer.find_similar_phonemes(source_phoneme, target_language)
        return similar_phonemes[0][0] if similar_phonemes else source_phoneme

    def convert_word(self, word: List[str], source_language: str, target_language: str) -> List[str]:
        return [self.convert_phoneme(phoneme, source_language, target_language) for phoneme in word]

    def apply_prosody(self, phonemes: List[str], language_code: str) -> List[Dict[str, Any]]:
        language_prosody = self.prosodic_features.get(language_code, {})
        if not language_prosody:
            return [{'phoneme': p} for p in phonemes]
        
        syllables = self.analyze_syllable_structure(phonemes, language_prosody)
        syllables = self.apply_stress_pattern(syllables, language_prosody)
        syllables = self.apply_tone_pattern(syllables, language_prosody)
        
        return syllables

    def analyze_syllable_structure(self, phonemes: List[str], language_prosody: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Placeholder implementation
        return [{'onset': [], 'nucleus': [p], 'coda': []} for p in phonemes]

    def apply_stress_pattern(self, syllables: List[Dict[str, Any]], language_prosody: Dict[str, Any]) -> List[Dict[str, Any]]:
        stress_system = language_prosody.get('stress_system', 'none')
        if stress_system == 'dynamic':
            for i, syllable in enumerate(syllables):
                syllable['stress'] = 'primary' if i % 2 == 0 else 'secondary'
        return syllables

    def apply_tone_pattern(self, syllables: List[Dict[str, Any]], language_prosody: Dict[str, Any]) -> List[Dict[str, Any]]:
        tone_system = language_prosody.get('tone_system', 'non-tonal')
        if tone_system == 'tonal':
            tones = language_prosody.get('tones', [])
            for i, syllable in enumerate(syllables):
                syllable['tone'] = tones[i % len(tones)] if tones else 'neutral'
        return syllables

    def convert_word_with_prosody(self, word: List[str], source_language: str, target_language: str) -> Tuple[List[str], List[Dict[str, Any]]]:
        converted_phonemes = self.convert_word(word, source_language, target_language)
        target_prosody = self.apply_prosody(converted_phonemes, target_language)
        return converted_phonemes, target_prosody