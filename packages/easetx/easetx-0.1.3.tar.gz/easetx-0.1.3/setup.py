from setuptools import setup, find_packages

def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        with open(path) as reqs:
            requirements.update(
                line.split('#')[0].strip() for line in reqs
                if is_requirement(line.strip())
            )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, a URL, or an included file.
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))

# Use a simpler description instead of reading from Readme.md
long_description = """
EASE-TX: Enhanced AI Scoring Engine for Text Analysis
====================================================

A lightweight, text-only version of the Enhanced AI Scoring Engine (EASE) that provides
advanced text comparison and similarity analysis capabilities.

- Calculate EASE scores for any text
- Get detailed metrics about text quality
- Compare texts based on their EASE scores
- JSON output for easy integration
"""

setup(
    name="easetx",
    version="0.1.3",
    packages=find_packages(),
    package_data={
        'easetx': ['data/*.p', 'data/*.txt'],
    },
    install_requires=[
        'numpy>=1.16.5,<1.23.0',  # Specify version range for NumPy to fix SciPy compatibility
        'scipy>=1.7.0,<1.9.0',    # Add explicit SciPy dependency with compatible version
        'scikit-learn>=0.24.0',
        'nltk>=3.6.0',
        'python-Levenshtein>=0.12.0',  # Added for improved string comparison
    ],
    extras_require={
        'spell': ['aspell-python-py3>=1.15.0'],  # Optional dependency for spell checking
    },
    author="Islam A. Hassan",
    author_email="mohamedi@tcd.ie",
    description="EASE-TX: Enhanced AI Scoring Engine for Text Analysis",
    long_description=long_description,
    long_description_content_type="text/plain",
    license="Apache 2.0",
    keywords="machine learning nlp essay scoring education text analysis",
    url="https://github.com/mogaio/EASE-TX",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Linguistic',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    scripts=[
        'download-nltk-corpus.sh',
    ],
)