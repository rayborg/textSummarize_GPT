# textSummarize_GPT
## Summarizes a text only file using GPT 3.5 turbo model
- Reads a file at path and filename = "TextPapers/file.txt" which can be changed in the code
- Splits the text only file it into appropriately sized chunks for GPT 3.5 Turbo model processing and then summarizes it and prints the short summary to screen
- You need to request an OpenAI API key and paste it in your code here: os.environ["OPENAI_API_KEY"] = 'Your OpenAI API key goes here'


## The openai.ChatCompletion.create() function is used to generate a summary of the input text using the GPT-3.5-turbo model. 
### Here's a breakdown of the parameters:
- These parameters control the behavior of the model and allow you to fine-tune the generated summaries according to your requirements.

1. model: This specifies the language model to use for the task. In this case, the GPT-3.5-turbo model is used.
2. messages: This is a list of messages to simulate a conversation between the user and the AI model. It usually starts with a system message setting the context, followed by alternating user and AI messages. In this case, the user message contains the prompt to summarize the research paper.
3. temperature: This is a parameter controlling the randomness of the model's output. Higher values (e.g., 1) make the output more random, while lower values (e.g., 0.5) make it more focused and deterministic.
4. max_tokens: This parameter sets the maximum number of tokens (words or word pieces) in the model's response. Here, it's set to 500 tokens.
5. top_p: This is the nucleus sampling parameter. It helps control the diversity of the generated text. A value of 1 means all tokens are considered, while lower values like 0.9 would only consider the top 90% probable tokens. In this case, it's set to 1, meaning all tokens are considered.
6. frequency_penalty: This parameter penalizes tokens based on their frequency in the training data. A positive value makes the model less likely to generate frequent tokens, while a negative value makes it more likely. Here, it's set to 0, meaning no penalty is applied.
7. presence_penalty: This parameter penalizes tokens based on their presence in the text generated so far. A positive value discourages repetition, while a negative value encourages it. Here, it's set to 0, meaning no penalty is applied.

