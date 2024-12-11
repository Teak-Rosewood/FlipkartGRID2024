import re

def remove_words_from_string(input_string, words_to_remove):
    pattern = r'\b(?:' + '|'.join(map(re.escape, words_to_remove)) + r')\b'
    result_string = re.sub(pattern, '', input_string, flags=re.IGNORECASE)
    result_string = re.sub(r'\s+', ' ', result_string).strip()
    return result_string