# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore
import json

# Initialize the app with a service account, granting admin privileges
app = initialize_app()

# The on_request decorator is used to define an HTTP function
@https_fn.on_request()
def flw_webhook(request: https_fn.Request) -> https_fn.Response:

    # Get the request data
    data = request.get_json()

    # Check if data is present and valid
    if not data or not isinstance(data, dict):
        print("Error: Invalid request data")
        return
    
    # Extract relevant information from payload
    payload = data.get("payload", {})
    user_id = payload.get("customer", {}).get("id")
    transaction_data = {
        "txRef": payload.get("txRef"),
        "amount": payload.get("amount"),
        "status": payload.get("status"),
        "createdAt": payload.get("createdAt"),
    }

  # Check if user ID and transaction data are present



    # 
    return https_fn.Response("Hello world!")