import pandas as pd
from scipy.spatial import distance
import ast

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['created_at'] = pd.to_datetime(df['created_at'])
    return df

def calculate_similarities(df, target_embedding):
    df['Embeddings'] = df['Embeddings'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    df['similarity'] = df['Embeddings'].apply(lambda emb: 1 - distance.cosine(target_embedding, emb) if emb is not None else 0)
    return df

def filter_and_sort_by_week(df, target_date, entries_per_week=5):
    week_info = target_date.isocalendar()
    target_week = week_info.week
    target_year = week_info.year
    
    results = {}
    for week_shift in [-1, 0, 1]:  # Weeks before, target, and after
        week = target_week + week_shift
        week_df = df[(df['created_at'].dt.isocalendar().week == week) & 
                     (df['created_at'].dt.year == target_year)]
        sorted_df = week_df.sort_values(by='similarity', ascending=False).head(entries_per_week)
        results[f"week_{week_shift}"] = sorted_df

    return results

def main():
    file_path = 'sample_tweets.csv'
    df = load_data(file_path)
    target_tweet = df.iloc[500]  # Example: Select a specific tweet
    target_embedding = ast.literal_eval(target_tweet['Embeddings'])
    similar_tweets = calculate_similarities(df, target_embedding)
    results = filter_and_sort_by_week(similar_tweets, target_tweet['created_at'])
    
    # Print results for each week
    for key, week_tweets in results.items():
        print(f"Results for {key}:")
        print(week_tweets[['tweet_text', 'created_at', 'similarity']], '\n')

if __name__ == "__main__":
    main()
