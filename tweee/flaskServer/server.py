from flask import Flask, jsonify, request
from openai import OpenAI
import os
import pandas as pd
import ast
from scipy.spatial import distance
from io import BytesIO
import requests
import chardet
from io import TextIOWrapper

app = Flask(__name__)
# Set your OpenAI API key here
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def load_embeddings_from_json(url):
    try:
        # Step 1: Download JSON data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for unsuccessful requests

        # Step 2: Parse JSON data into a Python object
        json_data = response.json()

        # Step 3: Convert the JSON data to a DataFrame
        df = pd.DataFrame(json_data)
        df['embeddings'] = df['embeddings'].apply(ast.literal_eval)

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error downloading JSON data: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON data: {e}")
        return None


def cosine_similarity(vec1, vec2):
    return 1 - distance.cosine(vec1, vec2)

def find_most_similar_embedding(target_embedding, embeddings_df):
    highest_similarity = -1
    most_similar_index = None
    for index, row in embeddings_df.iterrows():
        similarity = cosine_similarity(target_embedding, row['Embeddings'])
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_index = index
    return most_similar_index, highest_similarity

def get_openai_embeddings(text_input):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",  # Adjust model as needed
            input=text_input,
            encoding_format="float"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
@app.route('/poop', methods=['GET'])
def test():
    text = request.args.get('text')
    date = request.args.get('date')
    return [text, date]

@app.route('/find-similar', methods=['GET'])
def find_similar():
    content = request.json
    input_text = content.get('text', '')
    new_embedding = get_openai_embeddings(input_text)
    if new_embedding:
        index, similarity = find_most_similar_embedding(new_embedding, embeddings_df)
        return jsonify({'most_similar_index': index, 'similarity': similarity})
    else:
        return jsonify({'error': 'Failed to generate embedding'})

# Load embeddings DataFrame on server start
url = 'https://twee-tweets1.s3.us-east-2.amazonaws.com/random_10k.json'
embeddings_df = load_embeddings_from_json(url)

if __name__ == '__main__':
    app.run(debug=True)
