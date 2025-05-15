from mlx_lm import load
_, tokenizer = load('mlx-community/Llama-3.2-3B-Instruct-4bit')

print(tokenizer.encode("ACTION: LIST_DIR(path='.')<|eot_id|>"))
print(tokenizer.encode("='.')<|eot_id|>"))
print(tokenizer.decode([1151, 55128, 128009]))
print(tokenizer.decode([52886, 873, 128009]))
