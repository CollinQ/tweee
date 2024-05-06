import pandas as pd
from openai import OpenAI
import os

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_openai_embeddings(text_input):
    """Fetch embeddings for a given text input using OpenAI's API."""
    if pd.isna(text_input) or text_input.strip() == "":
        print("Skipping empty or NaN text input.")
        return None
    try:
        print(f"Sending text input to OpenAI: {text_input}")
        response = client.embeddings.create(input=text_input, model="text-embedding-3-small")
        embeddings = response.data[0].embedding
        return embeddings
    except Exception as e:
        print(f"An error occurred while fetching embeddings: {e}")
        return None

def create_sample_dataset(original_file, sample_file, n=1000):
    """Create a sample dataset from the original file."""
    df = pd.read_csv(original_file)
    df_sample = df.sample(n)
    df_sample.to_csv(sample_file, index=False)
    print(f"Sample of size {n} saved to {sample_file}")

def main():
    original_file = '2016_US_election_tweets_100k.csv'
    sample_file = 'sample_tweets.csv'
    
    create_sample_dataset(original_file, sample_file, n=1000)

    df = pd.read_csv(sample_file)
    print("Columns in the DataFrame:", df.columns)

    if 'tweet_text' in df.columns:
        df['Embeddings'] = df['tweet_text'].apply(lambda x: get_openai_embeddings(x))
        df['Embeddings'] = df['Embeddings'].apply(lambda x: str(x) if x is not None else None)
        print(df.head(10))
        df.to_csv(sample_file, index=False)
        print("Updated CSV file with embeddings has been saved.")
    else:
        print("Error: No 'tweet_text' column found in the CSV file.")
if __name__ == "__main__":
    main()
