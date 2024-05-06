import ijson

def load_and_print_last_tweet(json_file):
    with open(json_file, 'rb') as file:  # open the file in binary mode
        # Directly parse items under the root array
        tweets = ijson.items(file, 'item')
        last_tweet = None
        for tweet in tweets:
            last_tweet = tweet  # Continue assigning till the last one

        if last_tweet:
            print("Last Tweet:")
            print(f"ID: {last_tweet.get('id')}")
            print(f"Screen Name: {last_tweet.get('screen_name')}")
            print(f"User ID: {last_tweet.get('user_id')}")
            print(f"Time: {last_tweet.get('time')}")
            print(f"Link: {last_tweet.get('link')}")
            print(f"Text: {last_tweet.get('text')}")
            print(f"Source: {last_tweet.get('source')}")
            print(f"Embeddings: {last_tweet.get('embeddings')}")
        else:
            print("No tweets found in the file.")

if __name__ == "__main__":
    json_file = 'part1.json'  # Adjust the file path if needed
    load_and_print_last_tweet(json_file)
