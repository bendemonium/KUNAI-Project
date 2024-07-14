import unittest
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.core import (
    PhonemeTokenizer, FeatureAnalyzer, PhonemeConverter,
    get_phoneme_inventory, get_phoneme_features
)
from src.core.utils import (
    load_json, get_data_file_path, ipa_to_regex,
    language_phonemes, language_allophones, prosodic_features, phoneme_features
)

# Glottocodes for English and Spanish
ENGLISH_GLOTTOCODE = 'stan1293'
SPANISH_GLOTTOCODE = 'stan1288'

class TestUtils(unittest.TestCase):
    def test_load_json(self):
        input_file = 'language_inventories/language_phonemes.json'
        print(f"\nInput for load_json: {input_file}")
        data = load_json(get_data_file_path(input_file))
        print(f"Output of load_json: {list(data.keys())[:5]}...")
        self.assertIsInstance(data, dict)
        self.assertIn(ENGLISH_GLOTTOCODE, data)

    def test_get_data_file_path(self):
        input_file = 'test.json'
        print(f"\nInput for get_data_file_path: {input_file}")
        path = get_data_file_path(input_file)
        print(f"Output of get_data_file_path: {path}")
        self.assertTrue(path.endswith('data/test.json'))

    def test_get_phoneme_features(self):
        phoneme_inventory = ['p', 'b', 't', 'd']
        print(f"\nInput for get_phoneme_features: {phoneme_inventory}")
        features = get_phoneme_features(phoneme_inventory, 'phoneme_features/phoneme_features.json')
        print(f"Output of get_phoneme_features for 'p': {features['p']}")
        self.assertIsInstance(features, dict)
        self.assertIn('p', features)
        self.assertIn('SegmentClass', features['p'])

    def test_get_phoneme_inventory(self):
        print(f"\nInput for get_phoneme_inventory: {ENGLISH_GLOTTOCODE}")
        inventory = get_phoneme_inventory(ENGLISH_GLOTTOCODE)
        print(f"Output of get_phoneme_inventory: {inventory[:10]}...")
        self.assertIsInstance(inventory, list)
        self.assertIn('p', inventory)

    def test_ipa_to_regex(self):
        input_ipa = 'p*'
        print(f"\nInput for ipa_to_regex: {input_ipa}")
        regex = ipa_to_regex(input_ipa)
        print(f"Output of ipa_to_regex: {regex}")
        self.assertEqual(regex, 'p\\*')

    def test_phoneme_tokenizer(self):
        input_text = 'pɪg'
        print(f"\nInput for phoneme_tokenizer: {input_text}")
        tokenizer = PhonemeTokenizer(ENGLISH_GLOTTOCODE)
        tokens = tokenizer.tokenize(input_text)
        print(f"Output of phoneme_tokenizer: {tokens}")
        self.assertEqual(tokens, ['p', 'ɪ', 'g'])

    def test_global_data_loaded(self):
        print("\nChecking global data loaded:")
        print(f"language_phonemes keys: {list(language_phonemes.keys())[:5]}...")
        print(f"language_allophones keys: {list(language_allophones.keys())[:5]}...")
        print(f"prosodic_features keys: {list(prosodic_features.keys())[:5]}...")
        print(f"phoneme_features keys: {list(phoneme_features.keys())[:5]}...")
        self.assertIsInstance(language_phonemes, dict)
        self.assertIsInstance(language_allophones, dict)
        self.assertIsInstance(prosodic_features, dict)
        self.assertIsInstance(phoneme_features, dict)

class TestFeatureAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = FeatureAnalyzer()

    def test_get_language_features(self):
        print(f"\nInput for get_language_features: {ENGLISH_GLOTTOCODE}")
        features = self.analyzer.get_language_features(ENGLISH_GLOTTOCODE)
        print(f"Output of get_language_features: {list(features.keys())[:5]}...")
        self.assertIsInstance(features, dict)
        self.assertIn('p', features)

    def test_compare_phonemes(self):
        phoneme1, phoneme2 = 'p', 'b'
        print(f"\nInput for compare_phonemes: {phoneme1}, {phoneme2}")
        similar, different = self.analyzer.compare_phonemes(phoneme1, phoneme2)
        print(f"Output of compare_phonemes - similar: {similar[:5]}..., different: {different[:5]}...")
        self.assertIsInstance(similar, list)
        self.assertIsInstance(different, list)
        self.assertTrue(len(similar) > 0)
        self.assertTrue(len(different) > 0)

    def test_find_similar_phonemes(self):
        target_phoneme = 'θ'
        source_language = ENGLISH_GLOTTOCODE
        target_language = SPANISH_GLOTTOCODE
        print(f"\nInput for find_similar_phonemes: phoneme={target_phoneme}, source_language={source_language}, target_language={target_language}")
        similar = self.analyzer.find_similar_phonemes(target_phoneme, source_language, target_language)
        print(f"Output of find_similar_phonemes: {similar[:5]}...")
        self.assertIsInstance(similar, list)
        self.assertTrue(all(isinstance(x, tuple) and len(x) == 2 for x in similar))

    def test_analyze_language_inventory(self):
        print(f"\nInput for analyze_language_inventory: {ENGLISH_GLOTTOCODE}")
        analysis = self.analyzer.analyze_language_inventory(ENGLISH_GLOTTOCODE)
        print(f"Output of analyze_language_inventory: {list(analysis.keys())[:5]}...")
        self.assertIsInstance(analysis, dict)
        self.assertTrue(len(analysis) > 0)

class TestPhonemeConverter(unittest.TestCase):
    def setUp(self):
        self.converter = PhonemeConverter()

    def test_convert_phoneme(self):
        phoneme = 'θ'
        print(f"\nInput for convert_phoneme: {phoneme}, {ENGLISH_GLOTTOCODE}, {SPANISH_GLOTTOCODE}")
        converted = self.converter.convert_phoneme(phoneme, ENGLISH_GLOTTOCODE, SPANISH_GLOTTOCODE)
        print(f"Output of convert_phoneme: {converted}")
        self.assertIsInstance(converted, str)
        self.assertTrue(len(converted) > 0)

    def test_convert_word(self):
        word = ['θ', 'ɪ', 'ŋ', 'k']
        print(f"\nInput for convert_word: {word}, {ENGLISH_GLOTTOCODE}, {SPANISH_GLOTTOCODE}")
        converted = self.converter.convert_word(word, ENGLISH_GLOTTOCODE, SPANISH_GLOTTOCODE)
        print(f"Output of convert_word: {converted}")
        self.assertIsInstance(converted, list)
        self.assertEqual(len(converted), len(word))

    def test_apply_prosody(self):
        phonemes = ['θ', 'ɪ', 'ŋ', 'k']
        print(f"\nInput for apply_prosody: {phonemes}, {ENGLISH_GLOTTOCODE}")
        prosody = self.converter.apply_prosody(phonemes, ENGLISH_GLOTTOCODE)
        print(f"Output of apply_prosody: {prosody}")
        self.assertIsInstance(prosody, list)
        self.assertEqual(len(prosody), len(phonemes))

    def test_analyze_syllable_structure(self):
        phonemes = ['θ', 'ɪ', 'ŋ', 'k']
        language_prosody = {}
        print(f"\nInput for analyze_syllable_structure: {phonemes}, {language_prosody}")
        syllables = self.converter.analyze_syllable_structure(phonemes, language_prosody)
        print(f"Output of analyze_syllable_structure: {syllables}")
        self.assertIsInstance(syllables, list)
        self.assertEqual(len(syllables), len(phonemes))

    def test_apply_stress_pattern(self):
        syllables = [{'onset': [], 'nucleus': ['a'], 'coda': []}]
        language_prosody = {'stress_system': 'dynamic'}
        print(f"\nInput for apply_stress_pattern: {syllables}, {language_prosody}")
        stressed = self.converter.apply_stress_pattern(syllables, language_prosody)
        print(f"Output of apply_stress_pattern: {stressed}")
        self.assertIn('stress', stressed[0])

    def test_apply_tone_pattern(self):
        syllables = [{'onset': [], 'nucleus': ['a'], 'coda': []}]
        language_prosody = {'tone_system': 'tonal', 'tones': ['high', 'low']}
        print(f"\nInput for apply_tone_pattern: {syllables}, {language_prosody}")
        toned = self.converter.apply_tone_pattern(syllables, language_prosody)
        print(f"Output of apply_tone_pattern: {toned}")
        self.assertIn('tone', toned[0])

    def test_convert_word_with_prosody(self):
        word = ['θ', 'ɪ', 'ŋ', 'k']
        print(f"\nInput for convert_word_with_prosody: {word}, {ENGLISH_GLOTTOCODE}, {SPANISH_GLOTTOCODE}")
        converted, prosody = self.converter.convert_word_with_prosody(word, ENGLISH_GLOTTOCODE, SPANISH_GLOTTOCODE)
        print(f"Output of convert_word_with_prosody - converted: {converted}, prosody: {prosody}")
        self.assertIsInstance(converted, list)
        self.assertIsInstance(prosody, list)
        self.assertEqual(len(converted), len(word))
        self.assertEqual(len(prosody), len(word))

if __name__ == '__main__':
    unittest.main()