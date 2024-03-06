from flask import Flask, jsonify, request
import tweepy
import os

app = Flask(__name__)

consumer_key = "placeholder"
consumer_secret = "placeholder"
access_token = "placeholder"
access_token_secret = "placeholder"

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

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
