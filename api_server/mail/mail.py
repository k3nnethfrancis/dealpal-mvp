import requests

def send_email(sender_email, receiver_email, subject, text):
    print("nextjs email API called! Hey")
    api_url = "https://localhost:8000/send_email/"
    data = {
        "sender": sender_email,
        "receiver": receiver_email,
        "subject": subject,
        "text": text
    }

    try:
        response = requests.post(api_url, json=data, verify=False)
        if response.status_code == 200:
            return {"status": "success", "message": "Email sent successfully"}
        else:
            return {"status": "error",
                    "message": f"Error in sending the email: {response.status_code}, {response.text}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
