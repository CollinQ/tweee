from flask import Flask, jsonify, request
from openai import OpenAI
import os
from scipy.spatial import distance
from datetime import datetime, timedelta, timezone
import json
import numpy as np
import requests
import chardet
from io import TextIOWrapper

app = Flask(__name__)
# Set your OpenAI API key here
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def load_tweets_from_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        tweets = response.json()
        for tweet in tweets:
            tweet['embeddings'] = [float(x) for x in tweet['embeddings']]
            tweet['time'] = datetime.strptime(tweet['time'], "%Y-%m-%dT%H:%M:%S%z")
        return tweets
    else:
        raise Exception(f"Failed to load data: HTTP {response.status_code} - {response.reason}")

def cosine_similarity(vec1, vec2):
    return 1 - distance.cosine(np.array(vec1, dtype=float), np.array(vec2, dtype=float))

from datetime import datetime, timedelta, timezone

def filter_tweets_by_week(tweets, base_date, week_offset):
    # Ensure base_date is offset-aware; if not, set it to UTC for simplicity
    if base_date.tzinfo is None:
        base_date = base_date.replace(tzinfo=timezone.utc)

    target_date = base_date + timedelta(weeks=week_offset)
    start_week = target_date - timedelta(days=target_date.weekday())
    end_week = start_week + timedelta(days=6)

    return [tweet for tweet in tweets if start_week <= tweet['time'] <= end_week]


def find_similar_tweets(tweets, target_embedding):
    results = []
    for tweet in tweets:
        similarity = cosine_similarity(target_embedding, tweet.get('embeddings', []))
        results.append({
            'id': tweet['id'],
            'text': tweet['text'],
            'similarity': round(similarity, 3),
            'time': tweet['time'].isoformat()  # Ensure the time is in a string format suitable for JSON
        })
    return sorted(results, key=lambda x: x['similarity'], reverse=True)[:5]


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
    input_text = content['text']
    input_date_str = content['date']  # Expected in YYYY-MM-DD format
    input_date = datetime.strptime(input_date_str, "%Y-%m-%d")

    new_embedding = get_openai_embeddings(input_text)
    if new_embedding:
        weeks = [-1, 0, 1]
        results = {}
        for week in weeks:
            week_tweets = filter_tweets_by_week(all_tweets, input_date, week)
            top_similar_tweets = find_similar_tweets(week_tweets, new_embedding)
            results[f'week_{week}'] = top_similar_tweets
        
        return jsonify(results)
    else:
        return jsonify({'error': 'Failed to generate embedding'})

tweets_file = 'https://twee-tweets1.s3.us-east-2.amazonaws.com/random_10k.json'
all_tweets = load_tweets_from_json(tweets_file)

if __name__ == '__main__':
    app.run(debug=True)
