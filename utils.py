from constants import KEY_WORD_EXTENSIONS, NEGATIVE_DESCRIPTORS, OPERATOR_IS, OPERATOR_NOT, OVERRIDING_POSITIVE_DESCRIPTORS


def get_full_word_regex_pattern(word: str):
    return fr'\b{word}\b'

def is_negative_descriptor(descriptor: str):
    return descriptor in NEGATIVE_DESCRIPTORS

def is_overriding_positive_descriptor(descriptor: str):
    return descriptor in OVERRIDING_POSITIVE_DESCRIPTORS

def get_location_operator(negate: bool):
    return OPERATOR_NOT if negate else OPERATOR_IS

def extend_key_words(key_words: list[str]):
    return key_words + [ext for key_word in key_words for ext in KEY_WORD_EXTENSIONS.get(key_word.lower(), [])]
