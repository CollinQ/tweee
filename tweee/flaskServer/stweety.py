import stweet as st


def try_search():
    search_tweets_task = st.SearchTweetsTask(all_words='#covid19')
    output_jl_tweets = st.JsonLineFileRawOutput('output_raw_search_tweets.jl')
    output_jl_users = st.JsonLineFileRawOutput('output_raw_search_users.jl')
    output_print = st.PrintRawOutput()
    st.TweetSearchRunner(search_tweets_task=search_tweets_task,
                         tweet_raw_data_outputs=[output_print, output_jl_tweets],
                         user_raw_data_outputs=[output_print, output_jl_users]).run()


def try_user_scrap():
    user_task = st.GetUsersTask(['iga_swiatek'])
    output_json = st.JsonLineFileRawOutput('output_raw_user.jl')
    output_print = st.PrintRawOutput()
    st.GetUsersRunner(get_user_task=user_task, raw_data_outputs=[output_print, output_json]).run()


def try_tweet_by_id_scrap():
    id_task = st.TweetsByIdTask('839264382865424384')
    output_json = st.JsonLineFileRawOutput('output_raw_id.jl')
    output_print = st.PrintRawOutput()
    st.TweetsByIdRunner(tweets_by_id_task=id_task,
                        raw_data_outputs=[output_print, output_json]).run()


if __name__ == '__main__':
    #try_search()
    #try_user_scrap()
    try_tweet_by_id_scrap()