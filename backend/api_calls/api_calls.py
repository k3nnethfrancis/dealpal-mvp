import requests

def run_selenium(category):
    api_url = 'http://localhost:8001/run_selenium'
    response = requests.post(api_url, json={'category': category})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}")
