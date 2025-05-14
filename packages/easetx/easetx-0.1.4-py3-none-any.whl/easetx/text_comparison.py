"""
Text comparison utility
"""
from .text_set import TextSet
from .feature_extractor import FeatureExtractor  # Use FeatureExtractor directly
from .scorer import TextScorer
import numpy as np

def compare_texts(text1, text2):
    """
    Compare two texts and return similarity and confidence scores
    
    Args:
        text1 (str): First text to compare
        text2 (str): Second text to compare
    
    Returns:
        tuple: (similarity_score, confidence_score)
    """
    # Create text sets
    text_set1, text_set2 = TextSet(), TextSet()
    
    # Add texts and set type to "train" (required for FeatureExtractor)
    text_set1.add_text(text1)
    text_set2.add_text(text2)
    text_set1._type = text_set2._type = "train"  # Changed from "analysis" to "train"
    
    # Initialize extractor and get features
    extractor = FeatureExtractor()
    extractor.initialize_dictionaries(text_set1)
    
    features1 = extractor.gen_feats(text_set1)
    features2 = extractor.gen_feats(text_set2)
    
    # Calculate similarity
    scorer = TextScorer()
    result = scorer.score_texts(features1, features2, method='weighted')
    
    return result['score'], result['confidence']

def calculate_ease_score(text):
    """
    Calculate the EASE score for a single text
    
    Args:
        text (str): Text to calculate EASE score for
    
    Returns:
        float: EASE score between 0 and 1
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("Text cannot be empty")
    
    # Create text set and add the text
    text_set = TextSet()
    text_set.add_text(text)
    text_set._type = "train"  # Changed from "analysis" to "train" for FeatureExtractor
    
    # Initialize extractor and extract features directly using FeatureExtractor
    extractor = FeatureExtractor()
    extractor.initialize_dictionaries(text_set)
    features = extractor.gen_feats(text_set)
    
    # EASE score is calculated based on feature quality and completeness
    # Higher values in features generally indicate better text quality
    # Normalize feature values and average them for a final score
    
    # Get non-zero feature values and normalize
    feature_values = features.flatten()
    non_zero_values = feature_values[feature_values != 0]
    
    if len(non_zero_values) == 0:
        return 0.0
    
    # Calculate mean of features as the EASE score
    ease_score = np.mean(non_zero_values)
    
    # Normalize to 0-1 range if needed
    if ease_score > 1.0:
        ease_score = 1.0 / (1.0 + np.log(ease_score))
        
    return float(ease_score)

def get_detailed_ease_score(text):
    """
    Calculate a detailed breakdown of the EASE score for a single text
    
    Args:
        text (str): Text to calculate EASE score for
    
    Returns:
        dict: Detailed breakdown of EASE score components including:
            - overall_score: The overall EASE score
            - length_metrics: Metrics related to text length and structure
            - prompt_metrics: Metrics related to prompt relevance
            - content_metrics: Metrics related to vocabulary and content
            - error_metrics: Metrics related to grammar and spelling errors
            - raw_features: The raw feature vector for advanced analysis
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("Text cannot be empty")
    
    # Create text set and add the text
    text_set = TextSet()
    text_set.add_text(text)
    text_set._type = "train"
    
    # Initialize extractor and extract features
    extractor = FeatureExtractor()
    extractor.initialize_dictionaries(text_set)
    features = extractor.gen_feats(text_set)
    
    # Break down features into categories
    # The feature array contains three types of features concatenated:
    # 1. length_feats (first 8 features)
    # 2. prompt_feats (next 4 features)
    # 3. bag_feats (remaining features)
    
    # Extract specific feature values
    length_features = features[0, 0:8]
    prompt_features = features[0, 8:12]
    content_features = features[0, 12:]
    
    # Get feedback for error analysis
    feedback = extractor.gen_feedback(text_set, features)
    
    # Create dictionary with detailed metrics
    detail = {
        "overall_score": float(calculate_ease_score(text)),
        
        "length_metrics": {
            "text_length": int(length_features[0]),
            "word_count": int(length_features[1]),
            "comma_count": int(length_features[2]),
            "apostrophe_count": int(length_features[3]),
            "punctuation_count": int(length_features[4]),
            "chars_per_word": float(length_features[5]),
            "grammar_errors": float(length_features[6]),
            "grammar_errors_per_word": float(length_features[7])
        },
        
        "prompt_metrics": {
            "prompt_overlap": float(prompt_features[0]),
            "prompt_overlap_proportion": float(prompt_features[1]),
            "expanded_synonym_overlap": float(prompt_features[2]),
            "expanded_synonym_proportion": float(prompt_features[3])
        },
        
        "error_metrics": {
            "grammar_issues": feedback[0]['grammar'],
            "spelling_issues": feedback[0]['spelling'],
            "grammar_errors_per_char": float(feedback[0]['grammar_per_char']),
            "spelling_errors_per_char": float(feedback[0]['spelling_per_char']),
            "too_similar_to_prompt": feedback[0]['too_similar_to_prompt']
        },
        
        "content_metrics": {
            "vocabulary_diversity": float(np.count_nonzero(content_features) / max(len(content_features), 1)),
            "vocabulary_size": int(np.count_nonzero(content_features)),
            "content_score": float(np.mean(content_features[content_features > 0]) if np.any(content_features > 0) else 0)
        },
        
        # For advanced users who want the raw feature vector
        "raw_features": features.tolist()
    }
    
    # Add any additional feedback items that might be present
    if 'topicality' in feedback[0]:
        detail["error_metrics"]["topicality"] = feedback[0]['topicality']
    
    if 'prompt_overlap' in feedback[0]:
        detail["error_metrics"]["prompt_overlap_warning"] = feedback[0]['prompt_overlap']
    
    return detail

def compare_texts_by_ease_score(text1, text2):
    """
    Compare two texts based on how similar their EASE scores are
    
    Args:
        text1 (str): First text to compare
        text2 (str): Second text to compare
    
    Returns:
        tuple: (score_similarity, confidence, ease_score1, ease_score2)
            - score_similarity: How similar the EASE scores are (0-1)
            - confidence: Confidence in the comparison (0-1)
            - ease_score1: EASE score for text1
            - ease_score2: EASE score for text2
    """
    # Calculate individual EASE scores
    ease_score1 = calculate_ease_score(text1)
    ease_score2 = calculate_ease_score(text2)
    
    # Calculate similarity between scores (closer to 1 means more similar)
    # Use a scaled difference to make the similarities more distinct
    score_diff = abs(ease_score1 - ease_score2)
    # Apply scaling to make differences more pronounced (multiplying by 10 will make a 0.01 difference become 0.1)
    scaled_diff = min(score_diff * 10, 1.0)  # Cap at 1.0 to keep within 0-1 range
    score_similarity = 1.0 - scaled_diff
    
    # Calculate confidence - higher when both texts have substantial content
    # and their feature distributions are meaningful
    content_factor = min(len(text1), len(text2)) / max(len(text1), len(text2))
    confidence = content_factor * (0.8 + 0.2 * score_similarity)
    
    return score_similarity, confidence, ease_score1, ease_score2