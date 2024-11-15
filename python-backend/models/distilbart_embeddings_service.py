import torch

from transformers import BartTokenizer, BartForConditionalGeneration

class DistilBARTEmbeddingsService(EmbeddingsService):
    def __init__(self):
        self.tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
        self.model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")

    def encode(self, text: str):
        """Encodes a text into an embedding."""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        encoder_outputs = self.model.model.encoder(**inputs)
        embeddings = encoder_outputs.last_hidden_state.mean(dim=1)
        return embeddings

    def decode(self, embedding_or_text: str):
        """Decodes text into a description."""
        inputs = self.tokenizer(embedding_or_text, return_tensors="pt")
        outputs = self.model.generate(inputs.input_ids, max_length=30)
        decoded_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded_text
