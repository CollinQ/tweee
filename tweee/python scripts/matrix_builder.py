import json
from scipy.spatial import distance
import numpy as np
from datetime import datetime, timedelta

def load_tweets_from_json(file_path):
    with open(file_path, 'r') as file:
        tweets = json.load(file)

    for tweet in tweets:
        if 'embeddings' in tweet and isinstance(tweet['embeddings'][0], str):
            tweet['embeddings'] = [float(x) for x in tweet['embeddings']]
        tweet['time'] = datetime.strptime(tweet['time'], "%Y-%m-%dT%H:%M:%S%z")  # Parse time

    return tweets

def cosine_similarity(vec1, vec2):
    if not vec1 or not vec2:
        return 0
    return 1 - distance.cosine(np.array(vec1, dtype=float), np.array(vec2, dtype=float))

def filter_tweets_by_week(tweets, base_date, week_offset):
    target_date = base_date + timedelta(weeks=week_offset)
    start_week = target_date - timedelta(days=target_date.weekday())
    end_week = start_week + timedelta(days=6)
    return [tweet for tweet in tweets if start_week <= tweet['time'] <= end_week]

def find_similar_tweets(tweets, target_tweet):
    target_embedding = target_tweet['embeddings']
    for tweet in tweets:
        tweet['similarity'] = cosine_similarity(target_embedding, tweet.get('embeddings', []))
    return sorted(tweets, key=lambda x: x.get('similarity', 0), reverse=True)[:5]

def main():
    json_file = '/Users/johnkim/Documents/GitHub/allergy/tweee/random_10k.json'
    tweets = load_tweets_from_json(json_file)
    target_index = len(tweets) // 4  # Choose the middle tweet as the target
    target_tweet = tweets[target_index]

    weeks = [-1, 0, 1]
    results = {}
    for week in weeks:
        week_tweets = filter_tweets_by_week(tweets, target_tweet['time'], week)
        top_similar_tweets = find_similar_tweets(week_tweets, target_tweet)
        results[f'week_{week}'] = top_similar_tweets

    for key, value in results.items():
        print(f"Results for {key}:")
        for tweet in value:
            print(f"{tweet['text'][:50]}... {tweet['similarity']}")

if __name__ == "__main__":
    main()
