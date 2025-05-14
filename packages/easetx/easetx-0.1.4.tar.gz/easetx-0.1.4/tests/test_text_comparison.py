import pytest
import numpy as np
from easetx.text_set import TextSet
from easetx.predictor_extractor import PredictorExtractor
from easetx.scorer import TextScorer
from easetx.text_comparison import compare_texts

def test_text_set_initialization():
    text_set = TextSet()
    assert text_set._type is None
    assert len(text_set._text) == 0
    assert len(text_set._tokens) == 0

def test_text_set_add_text():
    text_set = TextSet()
    sample_text = "This is a test text."
    text_set.add_text(sample_text)
    
    assert len(text_set._text) == 1
    assert len(text_set._tokens) == 1
    assert len(text_set._pos) == 1
    assert text_set._text[0].strip() == sample_text.strip()

def test_predictor_extractor():
    extractor = PredictorExtractor()
    text_set = TextSet()
    text_set.add_text("Sample text for testing.")
    text_set._type = "analysis"
    
    assert extractor._initialized == False
    extractor.initialize_dictionaries(text_set)
    assert extractor._initialized == True

def test_text_scorer():
    scorer = TextScorer()
    features1 = np.array([[1, 0, 1, 0]])
    features2 = np.array([[1, 1, 1, 0]])
    
    result = scorer.score_texts(features1, features2)
    assert 'score' in result
    assert 'confidence' in result
    assert 'success' in result
    assert result['success'] == True
    assert 0 <= result['score'] <= 1
    assert 0 <= result['confidence'] <= 1

def test_compare_texts_similar():
    text1 = "Machine learning is a subset of artificial intelligence."
    text2 = "AI includes machine learning as one of its components."
    
    similarity, confidence = compare_texts(text1, text2)
    assert 0 <= similarity <= 1
    assert 0 <= confidence <= 1
    assert similarity > 0.5  # Should be relatively similar

def test_compare_texts_different():
    text1 = "Machine learning is a subset of artificial intelligence."
    text2 = "The weather is nice today."
    
    similarity, confidence = compare_texts(text1, text2)
    assert 0 <= similarity <= 1
    assert 0 <= confidence <= 1
    assert similarity < 0.5  # Should be relatively different

def test_compare_texts_identical():
    text = "Machine learning is a subset of artificial intelligence."
    
    similarity, confidence = compare_texts(text, text)
    assert similarity == pytest.approx(1.0, abs=1e-5)
    assert 0 <= confidence <= 1

def test_compare_texts_empty():
    with pytest.raises(Exception):
        compare_texts("", "")

def test_compare_texts_special_chars():
    text1 = "Text with special chars: @#$%"
    text2 = "More special chars: &*()"
    
    similarity, confidence = compare_texts(text1, text2)
    assert 0 <= similarity <= 1
    assert 0 <= confidence <= 1

def test_scorer_methods():
    scorer = TextScorer()
    features1 = np.array([[1, 0, 1, 0]])
    features2 = np.array([[1, 1, 1, 0]])
    
    # Test different similarity methods
    methods = ['cosine', 'jaccard', 'weighted']
    for method in methods:
        result = scorer.score_texts(features1, features2, method=method)
        assert 0 <= result['score'] <= 1
        assert 0 <= result['confidence'] <= 1
        assert result['success'] == True