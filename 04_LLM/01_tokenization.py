import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! My name is Arun K R"
tokens = enc.encode(text)

# Tokens [25216, 3274, 0, 3673, 1308, 382, 186039, 658, 460]
print("Tokens:", tokens)

decoded = enc.decode([25216, 3274, 0, 3673, 1308, 382, 186039, 658, 460])
print("Decoded:", decoded)