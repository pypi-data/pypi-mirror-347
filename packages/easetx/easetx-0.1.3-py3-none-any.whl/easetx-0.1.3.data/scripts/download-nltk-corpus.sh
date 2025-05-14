#!/bin/bash
# Script to download NLTK corpora required for EASE-TX

echo "Downloading required NLTK data for EASE-TX..."
python -m nltk.downloader stopwords
python -m nltk.downloader maxent_treebank_pos_tagger
python -m nltk.downloader wordnet
python -m nltk.downloader punkt

echo "NLTK data download complete."
echo "Note: For spell-checking functionality, you'll also need to install 'aspell' on your system."