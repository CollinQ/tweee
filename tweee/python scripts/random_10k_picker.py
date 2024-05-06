import json

def sample_every_fifth_tweet(input_file, output_file):
    try:
        # Load tweets from the original JSON file
        with open(input_file, 'r') as file:
            tweets = json.load(file)
        
        # Select every fifth tweet
        sampled_tweets = tweets[::5]  # This slices the list to take every 5th element

        # Save the sampled tweets to a new JSON file
        with open(output_file, 'w') as file:
            json.dump(sampled_tweets, file, indent=4)

        print(f"Sampled {len(sampled_tweets)} tweets and saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = '/Users/johnkim/Documents/GitHub/allergy/tweee/part1_half1.json'  # Path to your large JSON file
    output_file = '/Users/johnkim/Documents/GitHub/allergy/tweee/random_10k.json'  # Path to where you want to save the sampled JSON file
    sample_every_fifth_tweet(input_file, output_file)
