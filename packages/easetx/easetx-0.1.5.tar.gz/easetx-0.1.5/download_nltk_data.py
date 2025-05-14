import nltk
import os

def download_nltk_data():
    """Download all required NLTK data packages for EASE-TX"""
    # List of all required NLTK resources
    resources = [
        'punkt',        # Sentence tokenizer
        'wordnet',      # Lexical database
        'stopwords',    # Common stopwords
    ]
    
    # Download all required resources
    for resource in resources:
        try:
            nltk.download(resource, quiet=False)
        except Exception as e:
            print(f"Error downloading {resource}: {e}")
    
    # Additional fix for punkt_tab issue
    try:
        # Create path for punkt_tab if needed
        nltk_data_path = os.path.expanduser('~/nltk_data')
        punkt_tab_path = os.path.join(nltk_data_path, 'tokenizers', 'punkt_tab')
        os.makedirs(os.path.join(punkt_tab_path, 'english'), exist_ok=True)
        
        # Copy punkt to punkt_tab as a workaround
        punkt_path = os.path.join(nltk_data_path, 'tokenizers', 'punkt')
        if os.path.exists(punkt_path):
            from shutil import copytree, copy2
            # Copy files from punkt to punkt_tab
            for item in os.listdir(punkt_path):
                src = os.path.join(punkt_path, item)
                dst = os.path.join(punkt_tab_path, item)
                if os.path.isdir(src):
                    copytree(src, dst, dirs_exist_ok=True)
                else:
                    copy2(src, dst)
            print("Created punkt_tab resource successfully")
    except Exception as e:
        print(f"Warning: Could not create punkt_tab resource: {e}")
    
    print("NLTK data setup completed!")

if __name__ == "__main__":
    download_nltk_data()