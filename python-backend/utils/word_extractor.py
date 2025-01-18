import json
import sys
from pathlib import Path
from itertools import islice
from tqdm import tqdm

sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.word_service_chromadb import WordService

def load_words_from_json(file_path: str) -> dict:
    """Load words and their definitions from a JSON file."""
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

def add_words_in_batches_to_chroma(words: dict, word_service: WordService, batch_size=100):
    """Encodes and adds words to ChromaDB in batches with progress bar."""
    total_batches = len(words) / (batch_size)
    
    with tqdm(total=total_batches, desc="Adding words to ChromaDB") as pbar:
        for chunk in chunk_dict(words, batch_size):
            word_list = list(chunk.keys())
            definition_list = list(chunk.values())
            
            word_service.batch_add_words(word_list, definition_list)

            pbar.update(1)
            

if __name__ == "__main__":
    # Load words from JSON file
    words = load_words_from_json('../data/words.json')
    
    # Initialize WordService with ChromaDB
    word_service = WordService(collection_name="the-embeddings")
    
    # Add words to ChromaDB in batches
    print(f"Processing {len(words)} words...")
    add_words_in_batches_to_chroma(words, word_service, batch_size=10)
    print("Finished adding words to ChromaDB")