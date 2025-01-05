import torch

from transformers import BartTokenizer, BartForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers.modeling_outputs import BaseModelOutput 

from services.embeddings_service import EmbeddingsService

class DistilBARTEmbeddingsService(EmbeddingsService):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
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
        encoder_outputs = self.model.model.encoder(**inputs)
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
        # Generate text
        outputs = self.model.generate(
            input_ids=decoder_input_ids,
            encoder_outputs=encoder_outputs,
            max_length=512,
            num_beams=1,
            early_stopping=True,
            temperature=0.1,
        )

        decoded_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded_text