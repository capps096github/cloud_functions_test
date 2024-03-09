
# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore
import requests

# Initialize the app with a service account, granting admin privileges
app = initialize_app()

def verify_flutterwave_payment(transaction_id, expected_amount, expected_currency) -> bool:
    # Replace 'YOUR_FLW_SECRET_KEY' with your actual Flutterwave secret key
    flw_secret_key = 'FLWSECK_TEST-962ba5edd9d11a76fdf0cfa60f2542ab-X';
    verify_url = f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify'

    headers = {
        'Authorization': f'Bearer {flw_secret_key}',
        'Content-Type': 'application/json'
    }

    # Make a request to Flutterwave to verify the transaction
    response = requests.get(verify_url, headers=headers)
    response_data = response.json()

    if (
        response_data['data']['status'] == "successful"
        and response_data['data']['amount'] == expected_amount
        and response_data['data']['currency'] == expected_currency
    ):
        return True
    else:
        return False

# The on_request decorator is used to define an HTTP function
@https_fn.on_request()
def process_webhook(request: https_fn.Request) -> https_fn.Response:

    if request.method == 'POST' and request.is_json:
        try:
            payload = request.get_json()

            # Extract relevant information from the payload
            user_id = payload['payload']['meta']['flightID']
            transaction_ref = payload['payload']['txRef']
            trans_id = payload['payload']['id']
            expected_amount = payload['payload']['amount']
            expected_currency = payload['payload']['currency']

            # Verify the payment using Flutterwave API
            if verify_flutterwave_payment(trans_id, expected_amount, expected_currency):

                # Prepare the transaction data
                transaction_data = {
                    'id': trans_id,
                    'txRef': transaction_ref,
                    'amount': expected_amount,
                    'status': 'successful',
                    'createdAt': payload['payload']['createdAt']
                }
                # Get a Firestore client to interact with the database.
                firestore_client: google.cloud.firestore.Client = firestore.client()

                # Payment verification successful, update the user's document
                user_doc_ref = firestore_client.collection('calcutists').document(str(user_id))

                # Add the transaction data to the user's document
                user_doc_ref.update({
                    'transactions': firestore.ArrayUnion([transaction_data])
                })

                return https_fn.Response(f"Transaction Complete with ID {user_doc_ref.id} added.", status=200)
            
            else:
                # Payment verification failed, inform the customer
                # return jsonify({'error': 'Payment verification failed'}), 400
                return https_fn.Response("Payment verification failed", status=400)

        except Exception as e:
            print(f"Error processing webhook payload: {e}")
            # return jsonify({'error': 'Internal Server Error'}), 500
            return https_fn.Response("Internal Server Error", status=500)

    else:
        # return jsonify({'error': 'Bad Request'}), 400
        return https_fn.Response("Bad Request", status=400)