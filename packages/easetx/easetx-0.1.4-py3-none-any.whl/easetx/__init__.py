"""
EASE-TX: Enhanced AI Scoring Engine for Text Analysis
==================================================

A lightweight, text-only version of the Enhanced AI Scoring Engine (EASE) that provides
advanced text comparison and similarity analysis capabilities.

Key Functions:
-------------
calculate_ease_score: Calculate the EASE score for a text
get_detailed_ease_score: Get detailed metrics about a text's EASE score
compare_texts_by_ease_score: Compare two texts based on their EASE scores

"""

__version__ = "0.1.3"

# Import key functions for easy access
from .text_comparison import (
    calculate_ease_score,
    get_detailed_ease_score,
    compare_texts_by_ease_score,
    compare_texts
)

# For backwards compatibility
from .text_set import TextSet
from .feature_extractor import FeatureExtractor
from .scorer import TextScorer

__all__ = [
    'calculate_ease_score',
    'get_detailed_ease_score',
    'compare_texts_by_ease_score',
    'compare_texts',
    'TextSet',
    'FeatureExtractor',
    'TextScorer',
]