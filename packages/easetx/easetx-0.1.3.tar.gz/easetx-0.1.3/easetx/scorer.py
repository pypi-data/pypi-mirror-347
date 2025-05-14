"""
Functions to calculate similarity scores between texts
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
import logging

log = logging.getLogger(__name__)

class TextScorer:
    def __init__(self):
        self.metrics = {
            'cosine': self._cosine_similarity,
            'jaccard': self._jaccard_similarity,
            'weighted': self._weighted_similarity
        }

    def score_texts(self, features1, features2, method='weighted'):
        """
        Calculate similarity score between two texts using specified method
        features1, features2: Feature vectors extracted from texts
        method: Similarity calculation method ('cosine', 'jaccard', or 'weighted')
        """
        if method not in self.metrics:
            raise ValueError(f"Unknown scoring method: {method}")

        try:
            score = self.metrics[method](features1, features2)
            confidence = self._calculate_confidence(features1, features2)
            
            return {
                'score': float(score),
                'confidence': confidence,
                'success': True
            }
        except Exception as e:
            log.exception("Error calculating similarity score")
            return {
                'score': 0.0,
                'confidence': 0.0,
                'success': False,
                'error': str(e)
            }

    def _cosine_similarity(self, features1, features2):
        """Calculate cosine similarity between feature vectors"""
        return cosine_similarity(features1, features2)[0][0]

    def _jaccard_similarity(self, features1, features2):
        """Calculate Jaccard similarity between feature vectors"""
        # Convert continuous features to binary
        f1_binary = (features1 > 0).astype(int)
        f2_binary = (features2 > 0).astype(int)
        return jaccard_score(f1_binary.flatten(), f2_binary.flatten(), average='micro')

    def _weighted_similarity(self, features1, features2):
        """
        Calculate weighted similarity using multiple metrics
        Combines structural, lexical, and semantic features
        """
        # Calculate different similarity aspects
        cosine_sim = self._cosine_similarity(features1, features2)
        jaccard_sim = self._jaccard_similarity(features1, features2)
        
        # Weights for different similarity aspects
        weights = {
            'cosine': 0.6,  # More weight to semantic similarity
            'jaccard': 0.4   # Less weight to lexical similarity
        }
        
        return (weights['cosine'] * cosine_sim + 
                weights['jaccard'] * jaccard_sim)

    def _calculate_confidence(self, features1, features2):
        """
        Calculate confidence score for the similarity measurement
        Based on feature density and variance
        """
        # Calculate feature density
        density1 = np.count_nonzero(features1) / features1.size
        density2 = np.count_nonzero(features2) / features2.size
        
        # Calculate feature variance
        var1 = np.var(features1)
        var2 = np.var(features2)
        
        # Combine metrics for confidence score
        confidence = np.mean([density1, density2]) * 0.7 + \
                    np.mean([var1, var2]) * 0.3
        
        return min(1.0, confidence)