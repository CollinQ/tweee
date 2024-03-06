from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Assuming your BEARER_TOKEN environment variable is already set
bearer_token = os.environ.get("BEARER_TOKEN")

def create_url():
    tweet_fields = "tweet.fields=lang,author_id"
    ids = "ids=1278747501642657792,1255542774432063488" # Adjust as needed
    url = f"https://api.twitter.com/2/tweets?{ids}&{tweet_fields}"
    return url

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def connect_to_endpoint(url):
    response = requests.get(url, auth=bearer_oauth)
    if response.status_code != 200:
        return {
            "error": "Request returned an error: {} {}".format(response.status_code, response.text)
        }, response.status_code
    return response.json()

@app.route('/get-tweets', methods=['GET'])
def get_tweets():
    url = create_url()
    json_response = connect_to_endpoint(url)
    return jsonify(json_response)

if __name__ == "__main__":
    app.run(debug=True)
