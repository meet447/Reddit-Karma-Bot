import g4f.Provider
from g4f.client import Client
import g4f
import g4f.providers

def create_response(post):
    
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
         
    return response

        
