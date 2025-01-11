import json
import sys
from pathlib import Path
from itertools import islice
from tqdm import tqdm

# Add the parent directory to the sys.path to allow imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.word_service import WordService

def load_words_from_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def chunk_dict(data_dict, batch_size):
    """Yield successive batches of items from data_dict."""
    keys = iter(data_dict)
    while True:
        batch_slice = list(islice(keys, batch_size))
        if not batch_slice:
            break
        yield {k: data_dict[k] for k in batch_slice}

def add_words_in_batches_to_qdrant(words: dict, word_service: WordService, batch_size=100):
    """Encodes and adds words to Qdrant in batches."""
    for chunk in chunk_dict(words, batch_size):
        # chunk is a dict of word->definition
        word_list = list(chunk.keys())
        definition_list = list(chunk.values())
        word_service.batch_add_words(word_list, definition_list)
        for w in word_list:
            print(f"Added word: {w}")

if __name__ == "__main__":
    # Load words from JSON file
    words = load_words_from_json('../data/words.json')
    
    # Initialize WordService
    word_service = WordService()
    word_service._init_collection()

    # Add words to Qdrant in batches
    add_words_in_batches_to_qdrant(words, word_service, batch_size=50)