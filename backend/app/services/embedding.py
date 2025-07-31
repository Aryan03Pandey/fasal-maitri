from transformers import AutoTokenizer, AutoModel
import torch

MODEL_NAME = "ai4bharat/IndicBERT-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

def get_embedding(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        last_hidden = outputs.last_hidden_state  # (1, seq_len, hidden)
        mask = inputs.attention_mask.unsqueeze(-1)
        summed = (last_hidden * mask).sum(1)
        counts = mask.sum(1).clamp(min=1e-9)
        embedding = summed / counts
        return embedding.squeeze(0)  # vector
