import torch

from transformers import T5Tokenizer, T5ForConditionalGeneration


class FLANT5EmbeddingsService(EmbeddingsService):
    def __init__(self):
        # Initialize FLAN-T5
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

    def encode(self, text: str):
        """Encodes a text into an embedding."""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        encoder_outputs = self.model.encoder(**inputs)
        embeddings = encoder_outputs.last_hidden_state.mean(dim=1)  # Mean pooling
        return embeddings

    def decode(self, embedding_or_text: str):
        """Decodes text into a description."""
        inputs = self.tokenizer(embedding_or_text, return_tensors="pt")
        outputs = self.model.generate(inputs.input_ids, max_length=30)
        decoded_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded_text
