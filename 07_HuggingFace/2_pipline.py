# Use a pipeline as a high-level helper

"""
In Hugging Face, a pipeline is a high-level, easy-to-use interface for common NLP tasks.

Instead of manually tokenizing, running the model, and decoding the output, a pipeline does all that under the hood.

You can use it for tasks like:
- Translation
- Text generation
- Summarization
- Question answering
- Sentiment analysis
- Named entity recognition

Basically, pipelines wrap the tokenizer + model + decoding logic into a single callable object.
"""

from transformers import pipeline

# Use a proper translation model
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")

english_sentences = [
    "The weather is nice today.",
    "I love programming in Python.",
    "Transformers make NLP tasks easy."
]

translations = translator(english_sentences)

for i, translation in enumerate(translations):
    print(f"English: {english_sentences[i]}")
    print(f"French: {translation['translation_text']}")
    print("-" * 40)
