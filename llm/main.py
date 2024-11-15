import time
import g4f.Provider
from g4f.client import Client
import g4f

def create_response(post):
    try:
        # Initialize g4f client with a RetryProvider
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

        max_retries = 5  # Maximum number of retries
        attempt = 0

        while attempt < max_retries:
            try:
                # Generate chat completion using g4f
                chat_completion = client.chat.completions.create(
                    model=g4f.models.default,
                    messages=[{"role": "user", "content": post}],
                    stream=True
                )

                # Concatenate response chunks
                response = ""
                for completion in chat_completion:
                    data = completion.choices[0].delta.content or ""
                    response += data

                # Remove enclosing quotes if present
                if response.startswith('"') and response.endswith('"'):
                    response = response[1:-1]

                return response

            except Exception as e:
                if "402" in str(e):  # Check if error 402 occurred
                    attempt += 1
                    print(f"Error 402 encountered. Retrying... ({attempt}/{max_retries})")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise e  # Re-raise other exceptions

        print("Max retries reached. Could not process the request.")
        return None

    except Exception as final_error:
        print(f"An unexpected error occurred: {final_error}")
        return None
