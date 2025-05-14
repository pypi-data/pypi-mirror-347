import re
import os
import tempfile
import logging
import nltk
from nltk.stem.porter import PorterStemmer

log = logging.getLogger(__name__)

# Paths
base_path = os.path.dirname(__file__)
if not base_path.endswith("/"):
    base_path = base_path + "/"
    
# Path to essay corpus used for POS tag sequence generation
ESSAY_CORPUS_PATH = base_path + "../data/essaycorpus.txt"

# Path to aspell spell checker
aspell_path = "aspell"

# Robust tokenizer that doesn't rely on NLTK resources
def robust_tokenize(text):
    """
    A reliable tokenizer that works without NLTK resources
    """
    # Clean punctuation to create better tokens
    text = re.sub(r'([.,;!?()])', r' \1 ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Find words, numbers, and basic punctuation
    tokens = re.findall(r'\b[a-zA-Z0-9_\-\']+\b|[.,;!?()]', text)
    return tokens

def sub_chars(string):
    """
    Substitute special characters and normalize text
    
    Args:
        string (str): Input text
        
    Returns:
        str: Cleaned text with special characters handled
    """
    # Replace common special characters
    string = re.sub(r'[,;]', ' ', string)
    string = re.sub(r'\.', ' . ', string)
    string = re.sub(r'[^A-Za-z0-9\.\s]', '', string)
    string = re.sub(r'\s+', ' ', string)
    return string.strip().lower()

def stem_text(string):
    """
    Stem the text using Porter stemmer
    
    Args:
        string (str): Input text
        
    Returns:
        str: Stemmed text
    """
    stemmer = PorterStemmer()
    try:
        tokens = nltk.word_tokenize(string.lower())
    except:
        # Fallback to robust tokenizer if NLTK fails
        tokens = robust_tokenize(string.lower())
    
    stems = [stemmer.stem(token) for token in tokens]
    return " ".join(stems)

def spell_correct(string):
    """
    Uses aspell to spell correct an input string.
    Requires aspell to be installed and added to the path.
    Returns the spell corrected string if aspell is found, original string if not.
    string - string
    """
    # If aspell is not available, return the original string with no errors
    try:
        # Try a simple command to check if aspell is installed
        check_result = os.system("which aspell > /dev/null 2>&1")
        if check_result != 0:
            return string, 0, string
    except Exception:
        log.warning("aspell is not installed or not in PATH")
        return string, 0, string

    # Create a temp file so that aspell could be used
    # By default, tempfile will delete this file when the file handle is closed.
    f = tempfile.NamedTemporaryFile(mode='w')
    f.write(string)
    f.flush()
    f_path = os.path.abspath(f.name)
    try:
        p = os.popen(aspell_path + " -a < " + f_path + " --sug-mode=ultra")

        # Aspell returns a list of incorrect words with the above flags
        incorrect = p.readlines()
        p.close()

    except Exception:
        log.exception("aspell process failed; could not spell check")
        # Return original string if aspell fails
        return string, 0, string

    finally:
        f.close()

    incorrect_words = list()
    correct_spelling = list()
    for i in range(1, len(incorrect)):
        if(len(incorrect[i]) > 10):
            #Reformat aspell output to make sense
            match = re.search(":", incorrect[i])
            if hasattr(match, "start"):
                begstring = incorrect[i][2:match.start()]
                begmatch = re.search(" ", begstring)
                begword = begstring[0:begmatch.start()]

                sugstring = incorrect[i][match.start() + 2:]
                sugmatch = re.search(",", sugstring)
                if hasattr(sugmatch, "start"):
                    sug = sugstring[0:sugmatch.start()]

                    incorrect_words.append(begword)
                    correct_spelling.append(sug)

    #Create markup based on spelling errors
    newstring = string
    markup_string = string
    already_subbed=[]
    for i in range(0, len(incorrect_words)):
        sub_pat = r"\b" + incorrect_words[i] + r"\b"
        sub_comp = re.compile(sub_pat, flags=re.ASCII)
        newstring = re.sub(sub_comp, correct_spelling[i], newstring)
        if incorrect_words[i] not in already_subbed:
            markup_string=re.sub(sub_comp,'<bs>' + incorrect_words[i] + "</bs>", markup_string)
            already_subbed.append(incorrect_words[i])

    return newstring,len(incorrect_words),markup_string


def ngrams(tokens, min_n, max_n):
    """
    Generates ngrams(word sequences of fixed length) from an input token sequence.
    tokens is a list of words.
    min_n is the minimum length of an ngram to return.
    max_n is the maximum length of an ngram to return.
    returns a list of ngrams (words separated by a space)
    """
    all_ngrams = list()
    n_tokens = len(tokens)
    for i in range(n_tokens):
        for j in range(i + min_n, min(n_tokens, i + max_n) + 1):
            all_ngrams.append(" ".join(tokens[i:j]))
    return all_ngrams

def regenerate_good_tokens(string):
    """
    Given an input string, part of speech tags the string, then generates a list of
    ngrams that appear in the string.
    Used to define grammatically correct part of speech tag sequences.
    Returns a list of part of speech tag sequences.
    """
    try:
        toks = nltk.word_tokenize(string)
        pos_string = nltk.pos_tag(toks)
    except:
        # Fallback to robust tokenizer if NLTK fails
        toks = robust_tokenize(string)
        # Simple POS tagging (just tag everything as a noun)
        pos_string = [(token, "NN") for token in toks]
    
    pos_seq = [tag[1] for tag in pos_string]
    pos_ngrams = ngrams(pos_seq, 2, 4)
    sel_pos_ngrams = f7(pos_ngrams)
    return sel_pos_ngrams

def f7(seq):
    """
    Makes a list unique
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]


def edit_distance(s1, s2):
    """
    Calculates string edit distance between string 1 and string 2.
    Deletion, insertion, substitution, and transposition all increase edit distance.
    """
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1, # deletion
                d[(i, j - 1)] + 1, # insertion
                d[(i - 1, j - 1)] + cost, # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost) # transposition

    return d[lenstr1 - 1, lenstr2 - 1]


class Error(Exception):
    pass


class InputError(Error):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

def get_vocab(text_list, score_list=None, max_feats2=200):
    """
    Gets vocabulary for a list of texts, optionally weighted by scores
    
    Args:
        text_list (list): List of text strings
        score_list (list): Optional list of scores for weighting
        max_feats2 (int): Maximum number of features to return
        
    Returns:
        list: List of vocabulary terms
    """
    from sklearn.feature_extraction.text import CountVectorizer
    import numpy as np
    
    # Create vocabulary from all texts
    vectorizer = CountVectorizer(ngram_range=(1, 2), max_features=max_feats2)
    features = vectorizer.fit_transform(text_list)
    
    # If scores are provided, weight features by score
    if score_list is not None:
        # Normalize scores to 0-1 range
        scores_array = np.array(score_list).reshape(-1, 1)
        if len(np.unique(scores_array)) > 1:
            scores_array = (scores_array - np.min(scores_array)) / (np.max(scores_array) - np.min(scores_array))
        
        # Weight feature occurrences by scores
        weighted_features = features.multiply(scores_array)
        vocabulary_weights = np.sum(weighted_features, axis=0)
    else:
        # Just count occurrences if no scores
        vocabulary_weights = np.sum(features, axis=0)
    
    # Sort terms by weight
    vocabulary = vectorizer.get_feature_names_out()
    term_weights = list(zip(vocabulary, np.array(vocabulary_weights)[0]))
    term_weights.sort(key=lambda x: x[1], reverse=True)
    
    # Return top terms
    top_terms = [term for term, weight in term_weights[:max_feats2]]
    return top_terms

def get_wordnet_syns(word):
    """
    Utilize wordnet (installed with nltk) to get synonyms for words
    word is the input word
    returns a list of unique synonyms
    """
    synonyms = []
    regex = r"_"
    pat = re.compile(regex)
    synset = nltk.wordnet.wordnet.synsets(word)
    for ss in synset:
        for swords in ss.lemma_names():
            synonyms.append(pat.sub(" ", swords.lower()))
    synonyms = f7(synonyms)
    return synonyms