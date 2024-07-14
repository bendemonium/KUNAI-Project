import unittest
from core import (
    PhonemeTokenizer, FeatureAnalyzer, PhonemeConverter,
    get_phoneme_inventory, get_phoneme_features
)
from core.utils import (
    load_json, get_data_file_path, ipa_to_regex,
    language_phonemes, language_allophones, prosodic_features, phoneme_features
)

class TestUtils(unittest.TestCase):
    def test_load_json(self):
        data = load_json(get_data_file_path('language_inventories/language_phonemes.json'))
        self.assertIsInstance(data, dict)
        self.assertIn('eng', data)

    def test_get_data_file_path(self):
        path = get_data_file_path('test.json')
        self.assertTrue(path.endswith('data/test.json'))

    def test_get_phoneme_features(self):
        phoneme_inventory = ['p', 'b', 't', 'd']
        features = get_phoneme_features(phoneme_inventory, 'phoneme_features/phoneme_features.json')
        self.assertIsInstance(features, dict)
        self.assertIn('p', features)
        self.assertIn('place', features['p'])

    def test_get_phoneme_inventory(self):
        inventory = get_phoneme_inventory('eng')
        self.assertIsInstance(inventory, list)
        self.assertIn('p', inventory)

    def test_ipa_to_regex(self):
        regex = ipa_to_regex('p*')
        self.assertEqual(regex, 'p\\*')

    def test_phoneme_tokenizer(self):
        tokenizer = PhonemeTokenizer('eng')
        tokens = tokenizer.tokenize('pɪg')
        self.assertEqual(tokens, ['p', 'ɪ', 'g'])

    def test_global_data_loaded(self):
        self.assertIsInstance(language_phonemes, dict)
        self.assertIsInstance(language_allophones, dict)
        self.assertIsInstance(prosodic_features, dict)
        self.assertIsInstance(phoneme_features, dict)

class TestFeatureAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = FeatureAnalyzer()

    def test_get_language_features(self):
        features = self.analyzer.get_language_features('eng')
        self.assertIsInstance(features, dict)
        self.assertIn('p', features)

    def test_compare_phonemes(self):
        similar, different = self.analyzer.compare_phonemes('p', 'b')
        self.assertIsInstance(similar, list)
        self.assertIsInstance(different, list)
        self.assertIn('place', similar)
        self.assertIn('voice', different)

    def test_find_similar_phonemes(self):
        similar = self.analyzer.find_similar_phonemes('θ', 'eng')
        self.assertIsInstance(similar, list)
        self.assertTrue(all(isinstance(x, tuple) and len(x) == 2 for x in similar))

    def test_analyze_language_inventory(self):
        analysis = self.analyzer.analyze_language_inventory('eng')
        self.assertIsInstance(analysis, dict)
        self.assertIn('place', analysis)

class TestPhonemeConverter(unittest.TestCase):
    def setUp(self):
        self.converter = PhonemeConverter()

    def test_convert_phoneme(self):
        converted = self.converter.convert_phoneme('θ', 'eng', 'spa')
        self.assertIsInstance(converted, str)

    def test_convert_word(self):
        word = ['θ', 'ɪ', 'ŋ', 'k']
        converted = self.converter.convert_word(word, 'eng', 'spa')
        self.assertIsInstance(converted, list)
        self.assertEqual(len(converted), len(word))

    def test_apply_prosody(self):
        phonemes = ['θ', 'ɪ', 'ŋ', 'k']
        prosody = self.converter.apply_prosody(phonemes, 'eng')
        self.assertIsInstance(prosody, list)
        self.assertEqual(len(prosody), len(phonemes))

    def test_analyze_syllable_structure(self):
        phonemes = ['θ', 'ɪ', 'ŋ', 'k']
        language_prosody = {}
        syllables = self.converter.analyze_syllable_structure(phonemes, language_prosody)
        self.assertIsInstance(syllables, list)
        self.assertEqual(len(syllables), len(phonemes))

    def test_apply_stress_pattern(self):
        syllables = [{'onset': [], 'nucleus': ['a'], 'coda': []}]
        language_prosody = {'stress_system': 'dynamic'}
        stressed = self.converter.apply_stress_pattern(syllables, language_prosody)
        self.assertIn('stress', stressed[0])

    def test_apply_tone_pattern(self):
        syllables = [{'onset': [], 'nucleus': ['a'], 'coda': []}]
        language_prosody = {'tone_system': 'tonal', 'tones': ['high', 'low']}
        toned = self.converter.apply_tone_pattern(syllables, language_prosody)
        self.assertIn('tone', toned[0])

    def test_convert_word_with_prosody(self):
        word = ['θ', 'ɪ', 'ŋ', 'k']
        converted, prosody = self.converter.convert_word_with_prosody(word, 'eng', 'spa')
        self.assertIsInstance(converted, list)
        self.assertIsInstance(prosody, list)
        self.assertEqual(len(converted), len(word))
        self.assertEqual(len(prosody), len(word))

if __name__ == '__main__':
    unittest.main()