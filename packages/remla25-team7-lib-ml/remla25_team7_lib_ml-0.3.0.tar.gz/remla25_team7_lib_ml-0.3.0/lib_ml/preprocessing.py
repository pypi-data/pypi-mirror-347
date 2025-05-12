import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download("stopwords", quiet=True)

STOPWORDS = set(stopwords.words("english"))
STOPWORDS.discard("not")         # keep “not” to preserve polarity
STEMMER = PorterStemmer()

def clean_review(text: str) -> str:
    """
    Lowercase, remove punctuation, keep only alphanumerics & spaces.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text

def tokenize_review(text: str) -> list[str]:
    """
    Split on whitespace, remove stopwords, apply Porter stemmer.
    """
    cleaned = clean_review(text)
    return [
        STEMMER.stem(tok)
        for tok in cleaned.split()
        if tok not in STOPWORDS
    ]
