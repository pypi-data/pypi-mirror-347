"""
Handles sets of text documents for feature extraction and analysis
"""
import numpy as np
import nltk
import re
from . import util_functions

class TextSet(object):
    def __init__(self):
        self._type = None
        self._text = []
        self._tokens = []
        self._pos = []
        self._clean_stem_text = []
        self._spelling_errors = []
        self._markup_text = []
        self._numeric_features = []
        self._prompt = ""
        self._score = []  # Added score attribute for FeatureExtractor compatibility
    
    def _safe_tokenize(self, text):
        """
        A completely self-contained tokenizer that doesn't rely on NLTK resources.
        This is a failsafe tokenizer that's used when NLTK resources aren't available.
        """
        # Simple regex-based tokenizer for words
        tokens = re.findall(r'\b[a-zA-Z0-9_\-\']+\b', text)
        return tokens
        
    def add_text(self, text_content, score=None):
        """
        Add a text document to the set
        text_content: string containing the text
        score: optional numeric score or metadata
        """
        # Clean the text
        cleaned_text = util_functions.sub_chars(text_content)
        self._text.append(cleaned_text)
        
        # Tokenize using independent tokenizer to avoid NLTK resource issues
        tokens = self._safe_tokenize(cleaned_text)
        self._tokens.append(tokens)
        
        # POS tagging - use a simplified approach when NLTK isn't fully available
        try:
            pos = nltk.pos_tag(tokens)
        except:
            # Simple fallback - just tag everything as a noun
            pos = [(token, "NN") for token in tokens]
        self._pos.append(pos)
        
        # Stem text
        clean_stem_text = util_functions.stem_text(cleaned_text)
        self._clean_stem_text.append(clean_stem_text)
        
        # Get spelling errors
        _, error_count, markup = util_functions.spell_correct(cleaned_text)
        self._spelling_errors.append(error_count)
        self._markup_text.append(markup)
        
        # Store score if provided
        if score is not None:
            self._numeric_features.append([score])
            self._score.append(score)
        else:
            # Use default score of 1.0 for feature extraction compatibility
            self._score.append(1.0)