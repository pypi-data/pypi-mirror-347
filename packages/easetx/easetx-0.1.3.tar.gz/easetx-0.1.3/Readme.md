# EASE-TX: Enhanced AI Scoring Engine for Text Analysis

EASE-TX is a lightweight, text-only version of the Enhanced AI Scoring Engine (EASE). It provides advanced text comparison and similarity analysis capabilities, combining multiple NLP techniques to analyze and compare text documents effectively.

## Installation

```bash
pip install easetx
```

After installation, you'll need to download the required NLTK data:

```bash
# Either run this script
python -m nltk.downloader stopwords maxent_treebank_pos_tagger wordnet punkt

# Or use the provided script
bash download-nltk-corpus.sh
```

Note: For spell-checking functionality, you'll need to install aspell on your system. This is optional, and the package will work without it.

## Quick Start

```python
from easetx import calculate_ease_score, get_detailed_ease_score, compare_texts_by_ease_score

# Calculate a simple EASE score (0-1 scale)
text = "Machine learning is a subset of artificial intelligence that focuses on developing systems that can learn from data."
score = calculate_ease_score(text)
print(f"EASE Score: {score:.4f}")

# Get detailed metrics about the text
details = get_detailed_ease_score(text)
print(f"Text length: {details['length_metrics']['text_length']}")
print(f"Word count: {details['length_metrics']['word_count']}")
print(f"Grammar issues: {details['error_metrics']['grammar_issues']}")

# Compare two texts based on their EASE scores
text2 = "AI and machine learning enable computers to improve through experience."
similarity, confidence, score1, score2 = compare_texts_by_ease_score(text, text2)
print(f"Text 1 EASE Score: {score1:.4f}")
print(f"Text 2 EASE Score: {score2:.4f}")
print(f"Similarity: {similarity:.4f}")
print(f"Confidence: {confidence:.4f}")
```

## Features

- **EASE Score Calculation**: Get a quality score for any text
- **Detailed Metrics**: Analyze text complexity, grammar, vocabulary diversity and more
- **Text Comparison**: Compare texts based on their quality metrics
- **JSON Output**: All metrics available in structured JSON format for easy integration

## Advanced Usage

See the examples in the `ease_score_comparison.py` and `ease_score_details.py` files for more advanced usage patterns.

## Overview
---------------------
EASE-TX provides functions that can score arbitrary free text.
It is licensed under the Apache 2.0, please see LICENSE.txt for details.
The goal is to provide a high-performance, scalable solution that can predict targets from arbitrary values.

## Questions?
---------------------
Feel free to open an issue in the issue tracker.

## How to Contribute
-----------------
Contributions are very welcome. The easiest way is to fork this repo, and then
make a pull request from your fork. The first time you make a pull request, you
may be asked to sign a Contributor Agreement.

The current backlog is in the issues section. Please feel free to open new issues or work on existing ones.

## Reporting Security Issues
--------------------------
Please do not report security issues in public. Please email mohamedi@tcd.ie