import requests

def run_selenium(category):
    api_url = 'http://localhost:8001/run_selenium'
    response = requests.post(api_url, json={'category': category})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}")


def run_search(query):
    api_url = 'http://localhost:8001/run_search'
    response = requests.post(api_url, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}")


def send_email(sender_email, receiver_email, subject, text):
    # Address of the API endpoint to send emails
    api_url = 'http://localhost:8001/send_email'

    print("api calls, send email")

    # Data to be sent in the API call
    data = {
        "sender_email": sender_email,
        "receiver_email": receiver_email,
        "subject": subject,
        "text": text
    }

    # Perform the POST request to the API with the email data
    response = requests.post(api_url, json=data)

    # Check the status of the response
    if response.status_code == 200:
        # Return the content of the response if the call is successful
        return "200"#response.json()
    else:
        # Raise an exception if the API call fails
        raise Exception(f"API call failed with status code {response.status_code}")
