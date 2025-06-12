import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")  # corrected method name
tokens = enc.encode("my name is zaid")
print("encoded: ",tokens)


decoded = enc.decode(tokens)
print("decoded:",decoded)