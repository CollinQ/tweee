import ijson
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Convert Decimal instances to string to preserve precision
        return json.JSONEncoder.default(self, obj)

def copy_first_10k_tweets(input_file, output_file):
    with open(input_file, 'rb') as file:  # Open the original large JSON file
        tweets = ijson.items(file, 'item')  # Parse the JSON file incrementally

        with open(output_file, 'w') as outfile:
            outfile.write('[')  # Start the JSON array in the new file
            first = True

            for i, tweet in enumerate(tweets):
                if i >= 10000:  # Stop after collecting 10,000 tweets
                    break
                if not first:
                    outfile.write(',')
                json.dump(tweet, outfile, cls=DecimalEncoder, indent=4)  # Serialize using custom encoder
                first = False

            outfile.write(']')  # Close the JSON array in the new file

    print("Copied the first 10,000 tweets to", output_file)

if __name__ == "__main__":
    input_file = 'modified_concatenated_tweets.json'  # Adjust the path to your large JSON file
    output_file = 'first_10k.json'  # The new file containing only the first 10,000 tweets
    copy_first_10k_tweets(input_file, output_file)
