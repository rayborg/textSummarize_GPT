#Uses GPT-2 to tokenize but GPT-3.5-turbo to summarize
import os
import openai
from transformers import AutoTokenizer

def count_tokens(filename, max_length=1024):
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    with open(filename, 'r') as f:
        text = f.read()
    tokens = []
    for i in range(0, len(text), max_length):
        tokens += tokenizer.encode(text[i:i+max_length], add_special_tokens=False)
    num_tokens = len(tokens)
    return num_tokens

def break_up_file_to_chunks(filename, chunk_size=2000, overlap=100):
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    with open(filename, 'r') as f:
        text = f.read()
    tokens = tokenizer.encode(text, max_length=chunk_size, truncation=True)
    num_tokens = len(tokens)
    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

filename = "TextPapers/file.txt"

os.environ["OPENAI_API_KEY"] = 'Your OpenAI API key goes here'
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_response = []
chunks = break_up_file_to_chunks(filename)

for i, chunk in enumerate(chunks):
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    decoded_chunk = tokenizer.decode(chunk, skip_special_tokens=True)
    prompt_request = "Summarize this publication transcript: " + decoded_chunk
    messages = [{"role": "system", "content": "This is text summarization."}]
    messages.append({"role": "user", "content": prompt_request})
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )
    prompt_response.append(response["choices"][0]["message"]['content'].strip())

prompt_request = "Consolidate these paper summaries: " + str(prompt_response)
response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_request,
        temperature=.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
paper_summary = response["choices"][0]["text"].strip()
print(paper_summary)
