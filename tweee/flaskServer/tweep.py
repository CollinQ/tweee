import tweepy
import pandas as pd

# Initialize the Tweepy client
client = tweepy.Client(
    consumer_key="3hCyuZpdOq143mcs7lWclZMRz",
    consumer_secret="bONpuxARUFVRuFpiXYfp9zTTz5Yqu4b2fmLJh7v372jdVTWaZP",
    access_token="1765110121313755136-90P4qDrW7J5Vb6nVR5pvipBLkZStpz",
    access_token_secret="tcaf5BEMMWLKR7KYkr8yw6Hg1ZUxzeyeA9TxZJRH1GPmT",
    bearer_token="AAAAAAAAAAAAAAAAAAAAAAKpsgEAAAAAV60wxLYXlBESAW%2BBTrjxwXaH8m0%3DIDWZrab7sg3uuSFnsg6ptI5N6yGyOz4ec7I3gqYNwfIiJBIorO",
    wait_on_rate_limit=True
)

# Load tweet IDs from the file

# Store the tweet IDs
ids = [839264382865424384]

# Create an empty DataFrame to store the tweet data
tweets_df2 = pd.DataFrame()

# Retrieve each tweet using the Tweepy client
for tweet_id in ids:
    try:
        # Use the `get_tweet` method to fetch the tweet
        response = client.get_tweet(tweet_id, tweet_fields=['created_at', 'lang', 'public_metrics'], user_fields=['location', 'followers_count', 'friends_count', 'favourites_count', 'description', 'verified'])
        tweet_data = response.data

        # Extract user data (if available)
        user_data = tweet_data.author_id
        
        # Append the data to the DataFrame
        tweets_df2 = tweets_df2.append(pd.DataFrame({
            'ID': tweet_data.id,
            'Tweet': tweet_data.text,
            'Creado_tweet': tweet_data.created_at,
            'Locacion_usuario': user_data.location if user_data else None,
            'Seguidores_usuario': user_data.followers_count if user_data else None,
            'Amigos_usuario': user_data.friends_count if user_data else None,
            'Favoritos_usuario': user_data.favourites_count if user_data else None,
            'Descripcion_usuario': user_data.description if user_data else None,
            'Verificado_usuario': user_data.verified if user_data else None,
            'Idioma': tweet_data.lang
        }, index=[0]))
    except Exception as e:
        print(f"Error fetching tweet {tweet_id}: {e}")

# Reset the DataFrame index
tweets_df2 = tweets_df2.reset_index(drop=True)
