import json
from scipy.spatial import distance

def load_tweets_from_json(file_path):
    with open(file_path, 'r') as file:
        tweets = json.load(file)
    return tweets

def cosine_similarity(vec1, vec2):
    if vec1 is None or vec2 is None:
        return 0  # Returning 0 similarity if any vector is None
    return 1 - distance.cosine(vec1, vec2)

def find_similar_embeddings_sorted(target_embedding, tweets):
    for tweet in tweets:
        tweet['similarity'] = cosine_similarity(target_embedding, tweet.get('embeddings', []))

    # Sort tweets based on similarity and return top 5
    sorted_tweets = sorted(tweets, key=lambda x: x.get('similarity', 0), reverse=True)
    return sorted_tweets[:5]

def main():
    json_file = 'modified_sample_tweets.json'  # Path to your JSON file
    tweets = load_tweets_from_json(json_file)

    if not tweets:
        print("No tweets found in the file.")
        return

    if 'embeddings' not in tweets[0]:
        print("The first tweet does not have 'embeddings'.")
        return

    target_embedding = tweets[0]['embeddings']

    if not target_embedding:
        print("Embeddings for the first tweet are empty or invalid.")
        return

    top_similar_embeddings = find_similar_embeddings_sorted(target_embedding, tweets)
    print("Top 5 most similar embeddings:")
    for tweet in top_similar_embeddings:
        print(tweet['text'][:50], "...", tweet['similarity'])

if __name__ == "__main__":
    main()
