import requests
from django.conf import settings

PAYPAL_API_URL = "https://api.sandbox.paypal.com" if settings.PAYPAL_ENV == "sandbox" else "https://api.paypal.com"

def get_paypal_access_token():
    url = f"{PAYPAL_API_URL}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(
        url,
        headers=headers,
        data=data,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)  # <- Aquí deben ir las credenciales
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Error retrieving PayPal access token: {response.json()}")
		