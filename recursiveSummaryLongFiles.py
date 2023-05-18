# Install Python Packages
#!pip install openai tiktoken

# Import Python Packages
import platform
import os
import openai
import tiktoken
import time

print('Python: ', platform.python_version())

# Count the Number of Tokens
def count_tokens(filename):
    encoding = tiktoken.get_encoding("gpt2")
    with open(filename, 'r') as f:
        text = f.read()

    input_ids = encoding.encode(text)
    num_tokens = len(input_ids)
    return num_tokens

# Count the Number of Tokens in a String
def count_tokens_in_string(text):
    encoding = tiktoken.get_encoding("gpt2")
    input_ids = encoding.encode(text)
    num_tokens = len(input_ids)
    return num_tokens

filename = "inputFile.txt"
num_tokens = count_tokens(filename=filename)
print("Number of tokens:  ", num_tokens)

# Break up text into chunks of 2000 tokens with an overlap of 100 tokens
def break_up_file_to_chunks(filename, chunk_size=2000, overlap=100):
    encoding = tiktoken.get_encoding("gpt2")
    with open(filename, 'r') as f:
        text = f.read()

    tokens = encoding.encode(text)
    num_tokens = len(tokens)
    
    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks

# Modified the function break_up_file_to_chunks to work with a list of strings
def break_up_text_to_chunks(text_list, chunk_size=2000, overlap=100):
    encoding = tiktoken.get_encoding("gpt2")
    
    tokens = [encoding.encode(text) for text in text_list]
    tokens = [token for sublist in tokens for token in sublist]  # Flatten the list
    num_tokens = len(tokens)
    
    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks

chunks = break_up_file_to_chunks(filename)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {len(chunk)} tokens")

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = 'OPENAI_API_KEY goes HERE'
openai.api_key = os.getenv("OPENAI_API_KEY")

# Recursive function to handle API rate limits and large texts
def summarize_text(text_list, max_tokens):
    if count_tokens_in_string(str(text_list)) > max_tokens:
        text_list = break_up_text_to_chunks(text_list)

        summary_list = []
        for text_chunk in text_list:
            prompt_request = "Summarize this long summary section: " + encoding.decode(text_chunk)

            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt_request,
                    temperature=.5,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                summary_list.append(response["choices"][0]["text"].strip())
                time.sleep(1)  # Add a delay between each API request to avoid hitting rate limits
            except openai.api_resources.completion.CompletionError as e:
                if e.args[0]['error']['message'] == 'Rate limit exceeded':
                    print('Rate limit exceeded. Waiting for 60 seconds.')
                    time.sleep(60)
                    return summarize_text(text_list, max_tokens)
                elif e.args[0]['error']['message'] == 'Token limit exceeded':
                    print('Token limit exceeded. Breaking the text into smaller chunks.')
                    text_chunks = break_up_text_to_chunks([text_list])
                    summarized_text = []
                    for chunk in text_chunks:
                        summarized_text.append(summarize_text(encoding.decode(chunk), max_tokens))
                    return ' '.join(summarized_text)

        return summarize_text(summary_list, max_tokens)  # Recursive call to handle the case where the summarized text still exceeds the maximum token limit
    else:
        prompt_request = "Consolidate these paper summaries: " + str(text_list)

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt_request,
                temperature=.5,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response["choices"][0]["text"].strip()
        except openai.api_resources.completion.CompletionError as e:
            if e.args[0]['error']['message'] == 'Rate limit exceeded':
                print('Rate limit exceeded. Waiting for 60 seconds.')
                time.sleep(60)
                return summarize_text(text_list, max_tokens)
            elif e.args[0]['error']['message'] == 'Token limit exceeded':
                print('Token limit exceeded. Breaking the text into smaller chunks.')
                text_chunks = break_up_text_to_chunks([text_list])
                summarized_text = []
                for chunk in text_chunks:
                    summarized_text.append(summarize_text(encoding.decode(chunk), max_tokens))
                return ' '.join(summarized_text)


# Summarize the text one chunk at a time
prompt_response = []
encoding = tiktoken.get_encoding("gpt2")
chunks = break_up_file_to_chunks(filename)

for i, chunk in enumerate(chunks):
    prompt_request = "Summarize this partial section of a paper: " + encoding.decode(chunks[i])
    summary = summarize_text(prompt_request, 2000)
    prompt_response.append(summary)
    
    #Print to the user the partial section summaries
    print("Summary of each part ",i,": ",summary)

#print("These are the aggregated chunk summaries:\n")
#print(prompt_response)

# Consolidate the summaries
prompt_request = "Consolidate these paper summaries: " + ' '.join(prompt_response)
paper_summary = summarize_text(prompt_request, 2000)

# Summary of Summaries
print("This is the final overall summary: \n")
print(paper_summary)
