from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("google-t5/t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google-t5/t5-small")

# Prepare input text
input_text = "translate English to French: The weather is nice today."
inputs = tokenizer(input_text, return_tensors="pt")

# Generate output
outputs = model.generate(**inputs)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(result)
