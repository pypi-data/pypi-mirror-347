# EASE-TX: Enhanced AI Scoring Engine for Text Analysis

EASE-TX is a lightweight, text-only version of the Enhanced AI Scoring Engine (EASE). It provides advanced text comparison and similarity analysis capabilities, combining multiple NLP techniques to analyze and compare text documents effectively.

## Installation

```bash
pip install easetx
```

After installation, you'll need to download the required NLTK data:

```bash
# Use the provided utility script
python download_nltk_data.py
```

Note: For spell-checking functionality, you'll need to install aspell on your system. This is optional, and the package will work without it.

## Requirements

- Python 3.7+
- NumPy (1.16.5 - 1.23.0)
- SciPy (1.7.0 - 1.9.0)
- scikit-learn
- NLTK
- python-Levenshtein

Dependencies are automatically installed when you install the package via pip.

## Quick Start

```python
from easetx import calculate_ease_score, get_detailed_ease_score, compare_texts

# Calculate a simple EASE score (0-1 scale)
text = "Machine learning is a subset of artificial intelligence that focuses on developing systems that can learn from data."
score = calculate_ease_score(text)
print(f"EASE Score: {score:.4f}")

# Get detailed metrics about the text
details = get_detailed_ease_score(text)
print(f"Text length: {details['length_metrics']['text_length']}")
print(f"Word count: {details['length_metrics']['word_count']}")
print(f"Grammar issues: {details['error_metrics']['grammar_issues']}")

# Compare two texts directly
text2 = "AI and machine learning enable computers to improve through experience."
similarity, confidence = compare_texts(text, text2)
print(f"Similarity: {similarity:.4f}")
print(f"Confidence: {confidence:.4f}")
```

## Features

- **EASE Score Calculation**: Get a quality score for any text
- **Detailed Metrics**: Analyze text complexity, grammar, vocabulary diversity and more
- **Text Comparison**: Compare texts based on their quality metrics
- **JSON Output**: All metrics available in structured JSON format for easy integration

## Examples

The `examples` directory contains sample code demonstrating various features:

- `basic_usage.py`: Shows how to calculate basic and detailed EASE scores
- `text_comparison.py`: Demonstrates text comparison functionality
- `advanced_usage.py`: Shows more advanced features like batch processing and JSON export

Run examples from the project root directory:

```bash
python examples/basic_usage.py
python examples/text_comparison.py
python examples/advanced_usage.py
```

## Project Structure

```
EASE-TX/
├── LICENSE               # Apache 2.0 license file
├── Readme.md             # This file
├── download_nltk_data.py # Utility to download required NLTK resources
├── pyproject.toml        # Python project configuration
├── requirements.txt      # Project dependencies
├── setup.py              # Package installation configuration
├── data/                 # Data files used by the package
├── easetx/               # Core package code
├── examples/             # Example usage files
└── tests/                # Unit tests
```

## Overview

EASE-TX provides functions that can score arbitrary free text.
It is licensed under the Apache 2.0, please see LICENSE for details.
The goal is to provide a high-performance, scalable solution that can analyze text quality and similarity.

## Questions?

Feel free to open an issue in the issue tracker.

## How to Contribute

Contributions are very welcome. The easiest way is to fork this repo, and then
make a pull request from your fork. The first time you make a pull request, you
may be asked to sign a Contributor Agreement.

The current backlog is in the issues section. Please feel free to open new issues or work on existing ones.

## Reporting Security Issues

Please do not report security issues in public. Please email mohamedi<<_at_>tcd<_dot_>>ie

---
*Last Updated: May 2025*