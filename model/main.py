import requests
import time


def get_output(id):

    headers = {
            'authority': 'homepage.replicate.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ja;q=0.8',
            'origin': 'https://replicate.com',
            'referer': 'https://replicate.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

    params = {
            'id': id,
        }

    response = requests.get('https://homepage.replicate.com/api/prediction', params=params, headers=headers)

    data = response.json()
    
    print("[SUCCESS] Fetching data complete: ")
            
    return data


def get_comments(prompt):
    headers = {
        'authority': 'homepage.replicate.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ja;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://replicate.com',
        'referer': 'https://replicate.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    json_data = {
        'model': 'mistralai/mistral-7b-instruct-v0.1',
        'version': '83b6a56e7c828e667f21fd596c338fd4f0039b46bcfa18d973e8e70e455fda70',
        'input': {
            'prompt': prompt,
        },
        'stream': True,
    }

    response = requests.post('https://homepage.replicate.com/api/prediction', headers=headers, json=json_data)

    id = response.json()["id"]
    print("[SUCCESS]" + id)
    
    while True:
        res = get_output(id)

        if res["status"] == "succeeded":
            output = res["output"]
            poem_string = ''.join(output)
            print(poem_string)
            return poem_string
        
        elif res["status"] == "failed":
            print("Prediction failed. Check the logs for more information.")
            return None
        else:
            print("Processing, please wait...")
            time.sleep(5)  # Add a delay before checking the status again