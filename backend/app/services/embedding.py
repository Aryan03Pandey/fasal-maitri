from transformers import AutoTokenizer, AutoModel
import torch

model = AutoModel.from_pretrained("ai4bharat/indic-bert", torch_dtype="auto"),

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
