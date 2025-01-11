import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers.modeling_outputs import BaseModelOutput 

from services.embeddings_service import EmbeddingsService

class FLANT5EmbeddingsService(EmbeddingsService):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
        self.model.eval()

    @torch.no_grad()
    def encode(self, text: str) -> torch.Tensor:
        """
        Encodes input text into embeddings using the T5 encoder.
        Args:
            text (str): Input text to encode.
        Returns:
            torch.Tensor: Encoded embeddings.
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        encoder_outputs = self.model.encoder(**inputs)
        embeddings = encoder_outputs.last_hidden_state
        return embeddings
    
    @torch.no_grad()
    def encode_batch(self, texts: list[str]) -> torch.Tensor:
        """
        Encode a list of strings into a batched tensor.
        texts: list[str]
        returns: torch.Tensor shaped [batch_size, seq_len, hidden_size]
        """
        inputs = self.tokenizer(texts, return_tensors="pt", truncation=True, padding=True)
        encoder_outputs = self.model.encoder(**inputs)
        embeddings = encoder_outputs.last_hidden_state
        return embeddings


    @torch.no_grad()
    def decode(self, embedding: torch.Tensor) -> str:
        """
        Decodes embeddings back into text using the T5 decoder.
        Args:
            embedding (torch.Tensor): Manipulated embedding to decode.
        Returns:
            str: Decoded text.
        """
        embedding_tensor = torch.tensor(embedding, dtype=torch.float32)

        encoder_outputs = BaseModelOutput(last_hidden_state=embedding_tensor)
        decoder_input_ids = torch.tensor([[self.tokenizer.pad_token_id]])

        outputs = self.model.generate(
            input_ids=decoder_input_ids,
            encoder_outputs=encoder_outputs,
            max_length=512,
            num_beams=5,
            early_stopping=True
        )

        decoded_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded_text