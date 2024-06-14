import g4f.Provider
from g4f.client import Client
import g4f
import g4f.providers
import requests
import time

def create_response(post):
    
    try:
        api_key = "vuBNqJtRhbu5ot6CgZXh" 

        request_payload = {
            "key": api_key,
            "prompt": post,
            "model": "mistralai/mistral-7b-instruct-v0.1",
        }

        response = requests.post("https://www.chipling.xyz/api/request", params=request_payload)
        response_data = response.json()

        if "error" in response_data:
            print(f"Error: {response_data['error']}")
        else:
            response_id = response_data
            print(f"Response ID: {response_id}")

            while True:
                response_payload = {"id": response_id}
                response = requests.get("https://www.chipling.xyz/api/response", params=response_payload)
                response_data = response.json()

                if response_data["status"] == "succeeded":
                    output_url = response_data["output"]
                    sentence = ""
                    for i in output_url:
                        sentence = sentence + i
                    
                    if (sentence.startswith('"') and sentence.endswith('"')) or \
                        (sentence.startswith("'") and sentence.endswith("'")):
                            # Remove the enclosing quotes
                            cleaned_sentence = sentence[1:-1]
                    else:
                            # If the string doesn't start and end with quotes, keep it unchanged
                            cleaned_sentence = sentence    
                            
                    return cleaned_sentence
                else:
                    print(f"API Request Status: {response_data['status']}")
                    time.sleep(2) 
    
    except Exception as e:
      client = Client(
        provider=g4f.Provider.RetryProvider([
            g4f.Provider.Acytoo,
            g4f.Provider.You,
            g4f.Provider.Vercel,
            g4f.Provider.PerplexityLabs,
            g4f.Provider.H2o,
            g4f.Provider.HuggingChat,
            g4f.Provider.HuggingFace,
            g4f.Provider.AiChatOnline,
            g4f.Provider.DeepInfra,
            g4f.Provider.Llama,
            g4f.Provider.Liaobots,
            g4f.Provider.MetaAI,
            g4f.Provider.Hashnode,
            g4f.Provider.ChatgptFree,
        ])
    )

    chat_completion = client.chat.completions.create(
        model=g4f.models.default,
        messages=[{"role": "user", "content": post}],
        stream=True
    )

    response = ""

    for completion in chat_completion:
        data = completion.choices[0].delta.content or ""
        response =  response + data

    if response.startswith('"') and response.endswith('"'):
        # Remove the enclosing quotes
        response = response[1:-1]

    return response
    
    