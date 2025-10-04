from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

"""
AutoTokenizer → automatically loads the tokenizer corresponding to your model. A tokenizer converts text into numbers (tokens) that the model can understand.

AutoModelForSeq2SeqLM → loads a sequence-to-sequence (Seq2Seq) model, which is useful for tasks like translation, summarization, and text generation.

torch → PyTorch, the backend library used for tensor computations and running the model.
"""

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("google-t5/t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google-t5/t5-small")

"""
google/t5/t5-small is a T5 model (Text-To-Text Transfer Transformer) from Google.

from_pretrained() downloads the pretrained weights and tokenizer for the model.

The small version is lighter and faster, but less accurate than larger T5 variants.

At this point, you have:
- tokenizer → for converting text ↔ tokens.
- model → ready to generate text outputs.
"""

# Prepare input text
input_text = "translate English to French: The weather is nice today."
inputs = tokenizer(input_text, return_tensors="pt")

"""
input_text is your prompt. T5 uses a prefix (like "translate English to French:") to tell the model what task to perform.

tokenizer(input_text, return_tensors="pt") does:
- Converts text into input IDs (numbers representing words/subwords).
- Returns a PyTorch tensor (pt stands for PyTorch) ready for the model.
"""

# Generate output
outputs = model.generate(**inputs)
"""
- model.generate() is the main text generation function for seq2seq models.
- It takes the input tokens and predicts the output sequence, token by token.
- Here, it will generate the French translation of your input text.
"""

result = tokenizer.decode(outputs[0], skip_special_tokens=True)

"""
outputs[0] → the first generated sequence (tensor of token IDs).
tokenizer.decode() → converts token IDs back to human-readable text.
skip_special_tokens=True → removes tokens like <pad>, <eos> etc.
"""

print(result)
