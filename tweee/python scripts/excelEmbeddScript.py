import pandas as pd
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_openai_embeddings(text_input):

    if pd.isna(text_input) or text_input.strip() == "":
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


def main():
    file_path = '2016_US_election_tweets_100k.csv'
    df = pd.read_csv(file_path)

    print("Columns in the DataFrame:", df.columns)

    if 'tweet_text' in df.columns:
        df['Embeddings'] = df['tweet_text'].apply(lambda x: get_openai_embeddings(x))
        df['Embeddings'] = df['Embeddings'].apply(lambda x: str(x) if x is not None else None)

        print(df.head(10))

        # Save the DataFrame back to the same CSV file
        df.to_csv(file_path, index=False)
        print("Updated CSV file with embeddings has been saved.")
    else:
        print("Error: No 'tweet_text' column found in the CSV file.")

if __name__ == "__main__":
    main()
