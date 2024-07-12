from django.shortcuts import render
from core.feature_analyzer import FeatureAnalyzer
from core.phoneme_converter import PhonemeConverter
from core.utils import language_phonemes, language_allophones, prosodic_features, phoneme_features

def convert_view(request):
    result = None
    if request.method == 'POST':
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        input_text = request.POST.get('input_text')

        analyzer = FeatureAnalyzer('data/language_inventories/language_phonemes.json', 
                                   'data/phoneme_features/phoneme_features.json')
        converter = PhonemeConverter('data/language_inventories/language_phonemes.json', 
                                     'data/phoneme_features/phoneme_features.json', 
                                     'data/language_inventories/prosodic_features.json')

        # Simple tokenization (split by spaces)
        input_phonemes = input_text.split()
        
        try:
            converted_phonemes, prosody = converter.convert_word_with_prosody(input_phonemes, source_lang, target_lang)
            result = ' '.join(converted_phonemes)
        except Exception as e:
            result = f"Error: {str(e)}"

    return render(request, 'converter.html', {'result': result})