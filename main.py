'''Main input for the prompt data. this will call the local ollama engine to process the prompt and return a response.'''


from ollama_local_engine import prompt_ollama, eval_ollama_output

if __name__ == "__main__":
    while True:
        user_prompt = input("Enter your prompt (or 'exit' to quit): ")
        if user_prompt.lower() == 'exit':
            break
        response = prompt_ollama(user_prompt)
        print("Response from Ollama model:", response)
        evaluation = eval_ollama_output()
        #print("Evaluation of the response:", evaluation)