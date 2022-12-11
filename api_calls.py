import requests

api_key = "25KmFzF7mqAiSsReISZphGQ9S843SseGbfiQnzQH5hLc4qj6iK"
api_secret = "uhdeONDWDcqiWmU1sR9aNk5DVCQhVY8BKOe0pIut"

data = {
    'grant_type': 'client_credentials',
    'client_id': '25KmFzF7mqAiSsReISZphGQ9S843SseGbfiQnzQH5hLc4qj6iK',
    'client_secret': 'uhdeONDWDcqiWmU1sR9aNk5DVCQhVY8BKOe0pIut',
}

response = requests.post('https://api.petfinder.com/v2/oauth2/token', data=data)
print(response.json())


"""

"""