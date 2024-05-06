from flask import Flask, jsonify, request
import tweepy
import os

app = Flask(__name__)

CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_KEY_SECRET = os.environ.get('TWITTER_CONSUMER_KEY_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

def authenticate_twitter_app():
	auth=tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api=tweepy.API(auth)
	return api

api = authenticate_twitter_app()

@app.route('/user-lookup', methods=['GET'])
def user_lookup():
    username = request.args.get('username', default='elonmusk', type=str) 

    user_response = api.get_user(screen_name=username)

    if user_response:
        user_data = {
            "id": user_response.id_str,
            "name": user_response.name,
            "username": user_response.screen_name,
            "followers_count": user_response.followers_count,
            "following_count": user_response.friends_count,
            "tweet_count": user_response.statuses_count
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "User not found or unable to fetch user details"}), 404

if __name__ == '__main__':
    app.run(debug=True)
