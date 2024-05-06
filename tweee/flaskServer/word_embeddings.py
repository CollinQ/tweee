import json
import os
from openai import OpenAI

# Setup the OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_openai_embeddings(text_input):
    """Fetch embeddings for given text input using OpenAI API."""
    if text_input.strip() == "":
        print("Skipping empty or NaN text input.")
        return None
    try:
        print(f"Sending text input to OpenAI: {text_input}")
        response = client.embeddings.create(
            input=text_input,
            model="text-embedding-3-small"
        )
        embeddings = response.data[0].embedding
        return embeddings
    except Exception as e:
        print(f"An error occurred while fetching embeddings: {e}")
        return None

def append_embeddings_to_tweets(json_file):
    """Load JSON data, append embeddings to each tweet, and save the modified JSON."""
    with open(json_file, 'r') as f:
        tweets = json.load(f)

    for tweet in tweets:
        tweet_text = tweet.get('text', '')
        embeddings = get_openai_embeddings(tweet_text)
        tweet['embeddings'] = embeddings if embeddings is not None else "No embeddings"

    with open('modified_' + json_file, 'w') as f:
        json.dump(tweets, f, indent=4)
    print("Updated JSON file with embeddings has been saved.")

def main():
    json_file = "concatenated_tweets.json"  # Specify the path to the original full JSON file

    # Process the original JSON file to append embeddings
    append_embeddings_to_tweets(json_file)

if __name__ == "__main__":
    main()