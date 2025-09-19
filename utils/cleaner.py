import re
from langdetect import detect, LangDetectException

def clean_text(text):
    # remove URLs
    text = re.sub(r"http\S+", "", text)
    # remove non-alphanumeric (except whitespace)
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)
    return text.strip()

def filter_english(records):
    filtered = []
    for r in records:
        try:
            if detect(r["text"]) == "en":
                filtered.append(r)
        except LangDetectException:
            # skip if detection fails (empty/short text)
            continue
    return filtered
