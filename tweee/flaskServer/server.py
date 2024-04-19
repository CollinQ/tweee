from flask import Flask, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Set your OpenAI API key here
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_openai_embeddings(text_input):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",  # or any other suitable model
            input=text_input,
            encoding_format="float"  # You can choose "base64" depending on your needs
        )
        # Extracting the embeddings from the response
        embeddings = response.data[0].embedding  # Adjusted based on actual accessible attributes
        return embeddings
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}  # Return or log the error for debugging


@app.route('/get-embedding', methods=['GET'])
def get_embedding():
    # Hardcoded string for testing
    test_string = "test string"
    embeddings = get_openai_embeddings(test_string)
    return jsonify(embeddings)  # Returning the embeddings as JSON response

if __name__ == '__main__':
    app.run(debug=True)
