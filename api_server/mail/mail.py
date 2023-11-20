from flask import Flask, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Sostituisci con una chiave segreta reale

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Solo per testing, rimuovi in produzione

GOOGLE_CLIENT_ID = "your_google_client_id"
GOOGLE_CLIENT_SECRET = "your_google_client_secret"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
#https://chat.openai.com/share/c67fe487-ada5-40ae-9f25-3c95eec4e0ef how to setup email sent

flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
        }
    },
    scopes=["https://www.googleapis.com/auth/gmail.send"],
    redirect_uri="http://localhost:5000/callback"
)

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']:
        abort(500)  # State does not match!

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('send_email'))

@app.route('/send_email')
def send_email():
    # qui potresti avere una logica per comporre e inviare l'email
    return 'Email sent!'

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

if __name__ == "__main__":
    app.run('localhost', 5000)
