import re
import string
import logging
import contractions
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from nltk import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from textblob import TextBlob
from joblib import Parallel, delayed
from sklearn.utils.validation import check_is_fitted

# Auto-download NLTK resources
try:
    word_tokenize("test")
except LookupError:
    import nltk
    nltk.download('punkt')

try:
    WordNetLemmatizer().lemmatize("test")
except LookupError:
    import nltk
    nltk.download('wordnet')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)

class TextPreprocessor(BaseEstimator, TransformerMixin):
    """
    A flexible and efficient transformer for cleaning tasks including URL removal, 
    contraction expansion, punctuation removal, spell checking, stemming, lemmatization, 
    and more. Supports parallel processing for faster transformations on large datasets.
    For new updates: github.com/hoom4n/hoomanmltk
    Parameters:
    ----------
    url_remove : bool, default=True
        If True, removes URLs from the text.

    numbers : {"remove", "replace", "leave_them_be", None}, default="remove"
        Specifies how to handle numbers (remove, replace with "NUMBER", or leave unchanged).

    expand_contractions : bool, default=False
        If True, expands contractions like "don't" to "do not".

    spell_checking : bool, default=False
        If True, applies spell correction using TextBlob.

    stemming : bool, default=False
        If True, applies Porter Stemming.

    lemmatize : bool, default=False
        If True, applies WordNet Lemmatization.

    markdown_remove : bool, default=True
        If True, removes markdown formatting from the text.

    remove_punctuation : bool, default=True
        If True, removes punctuation characters from the text.

    output_mode : {"text", "tokens"}, default="text"
        If "text", outputs preprocessed text; if "tokens", outputs tokenized words.

    n_jobs : int, default=1
        Number of jobs for parallel processing (set >1 for multi-core).

    raise_errors : bool, default=False
        If True, raises errors during processing; if False, logs a warning.

    Methods:
    -------
    fit(X, y=None) : Fit the transformer to the input data.
    transform(X) : Preprocess the text data.
    """
    def __init__(self, url_remove=True, numbers="remove", expand_contractions=False, spell_checking=False,stemming=False, lemmatize=False,
                 markdown_remove=True, remove_punctuation=True,output_mode="text", n_jobs=1, raise_errors=False):
        self.url_remove = url_remove
        if numbers not in ["remove", "replace", "leave_them_be" ,None]:
            raise ValueError("numbers must be 'remove', 'replace', 'leave_them_be' or None")
        self.numbers = numbers
        self.stemming = stemming
        self.lemmatize = lemmatize
        self.markdown_remove = markdown_remove
        self.remove_punctuation = remove_punctuation
        self.expand_contractions = expand_contractions
        self.spell_checking = spell_checking
        if output_mode not in ["text", "tokens"]:
            raise ValueError("output_mode must be 'text' or 'tokens'")
        self.output_mode = output_mode
        self.n_jobs = n_jobs
        self.raise_errors = raise_errors

        self.lemmatizer_ = WordNetLemmatizer() if lemmatize else None
        self.stemmer_ = PorterStemmer() if stemming else None
        self._url_pattern = re.compile(
            r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
        ) if url_remove else None
        self._markdown_pattern = re.compile(
            r'(\#{1,6}\s*)|(\*{1,2})|(__)|(\~\~)|`{1,3}|!\[.*?\]\(.*?\)|\[.*?\]\(.*?\)|<.*?>'
        ) if markdown_remove else None


    def fit(self, X, y=None):
        self._validate_input(X)
        self.n_features_in_ = 1
        return self

    def transform(self, X):
        check_is_fitted(self)
        X = self._validate_input(X)
        if self.n_jobs == 1:
            return np.array([self._preprocess_text(text) for text in X], dtype=object)
        else:
            return np.array(Parallel(n_jobs=self.n_jobs)(
                delayed(self._preprocess_text)(text) for text in X), dtype=object)

    def _validate_input(self, X):
        if isinstance(X, pd.DataFrame):
            if X.shape[1] != 1:
                raise ValueError("DataFrame must have exactly one column")
            return X.squeeze().astype(str).tolist()
        elif isinstance(X, (pd.Series, np.ndarray)):
            return pd.Series(X).astype(str).tolist()
        elif isinstance(X, list):
            return [str(x) for x in X]
        else:
            raise ValueError(f"Unsupported input type: {type(X)}")

    def _preprocess_text(self, text):
        try:
            if self.markdown_remove:
                text = self._markdown_pattern.sub(' ', text)
            if self.url_remove:
                text = self._url_pattern.sub(' ', text)
            if self.expand_contractions:
                text = contractions.fix(text)
            text = text.lower()
            if self.remove_punctuation:
                text = text.translate(str.maketrans('', '', string.punctuation))
            tokens = word_tokenize(text)
            if self.spell_checking:
                tokens = [TextBlob(token).correct().string for token in tokens]
            if self.numbers == "remove":
                tokens = [t for t in tokens if not re.search(r'\d', t)]
            elif self.numbers == "replace":
                tokens = ["NUMBER" if re.search(r'\d', t) else t for t in tokens]
            if self.stemming and self.lemmatize:
                raise ValueError("Both Stemming & Lemmatizing can not be applied at same time!")
            if self.stemming:
                tokens = [self.stemmer_.stem(t) for t in tokens]
            elif self.lemmatize:
                tokens = [self.lemmatizer_.lemmatize(t) for t in tokens]
            return ' '.join(tokens) if self.output_mode == "text" else tokens

        except Exception as e:
            if self.raise_errors:
                raise
            else:
                logger.warning(f"Error processing text: {str(e)}")
                return "" if self.output_mode == "text" else []

    def get_feature_names_out(self, input_features=None):
        return np.array(['processed_text'])
