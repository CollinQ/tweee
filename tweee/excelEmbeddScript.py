import pandas as pd
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_openai_embeddings(text_input):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text_input,
            encoding_format="float"
        )
        embeddings = response.data[0].embedding
        return embeddings
    except Exception as e:
        print(f"An error occurred while fetching embeddings: {e}")
        return None

def main():
    file_path = 'tweets.xlsx'
    df = pd.read_excel(file_path)

    df['Embeddings'] = df['text'].apply(lambda x: get_openai_embeddings(x))
    
    df['Embeddings'] = df['Embeddings'].apply(lambda x: str(x) if x is not None else None)

    # Save the DataFrame back to the same Excel file
    df.to_excel(file_path, index=False)
    print("Updated Excel file with embeddings has been saved.")

if __name__ == "__main__":
    main()
