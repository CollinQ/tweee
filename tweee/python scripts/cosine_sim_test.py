import json
from scipy.spatial import distance
import numpy as np

def load_tweets_from_json(file_path):
    with open(file_path, 'r') as file:
        tweets = json.load(file)

    # Ensure all embeddings are lists of floats
    for tweet in tweets:
        if 'embeddings' in tweet:
            try:
                # Convert strings or other formats to floats
                if isinstance(tweet['embeddings'][0], str):
                    tweet['embeddings'] = [float(x) for x in tweet['embeddings']]
            except Exception as e:
                print(f"Error converting embeddings: {e}")
                tweet['embeddings'] = []

    return tweets

def cosine_similarity(vec1, vec2):
    if vec1 is None or vec2 is None or not vec1 or not vec2:
        return 0  # Handling empty or invalid vectors
    # Convert lists to numpy arrays for cosine calculation
    vec1 = np.array(vec1, dtype=float)
    vec2 = np.array(vec2, dtype=float)
    try:
        return 1 - distance.cosine(vec1, vec2)
    except Exception as e:
        print(f"Error calculating cosine similarity: {e}")
        return 0

def find_similar_embeddings_sorted(target_embedding, tweets):
    for tweet in tweets:
        tweet['similarity'] = cosine_similarity(target_embedding, tweet.get('embeddings', []))

    # Sort tweets based on similarity
    sorted_tweets = sorted(tweets, key=lambda x: x.get('similarity', 0), reverse=True)
    return sorted_tweets[:5]

def main():
    json_file = '/Users/johnkim/Documents/GitHub/allergy/tweee/first_10k.json'
    tweets = load_tweets_from_json(json_file)

    if not tweets or 'embeddings' not in tweets[0]:
        print("No suitable tweets found or embeddings are missing.")
        return

    target_embedding = tweets[0]['embeddings']
    top_similar_embeddings = find_similar_embeddings_sorted(target_embedding, tweets)
    print("Top 5 most similar embeddings:")
    for tweet in top_similar_embeddings:
        print(tweet['text'][:50], "...", tweet['similarity'])

if __name__ == "__main__":
    main()
