import sys
from core import PhonemeTokenizer, PhonemeConverter

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <source_text> <source_language> <target_language>")
        sys.exit(1)

    source_text = sys.argv[1]
    source_language = sys.argv[2]
    target_language = sys.argv[3]

    tokenizer = PhonemeTokenizer(source_language)
    converter = PhonemeConverter()

    try:
        source_phonemes = tokenizer.tokenize(source_text)
        converted_phonemes, prosody = converter.convert_word_with_prosody(source_phonemes, source_language, target_language)

        print(f"Source text: {source_text}")
        print(f"Source language: {source_language}")
        print(f"Target language: {target_language}")
        print(f"Converted phonemes: {' '.join(converted_phonemes)}")
        print("Prosody:")
        for syllable in prosody:
            print(syllable)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
