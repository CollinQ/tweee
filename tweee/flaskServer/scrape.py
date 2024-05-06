import stweet as st

if __name__ == '__main__':
    web_client = st.DefaultTwitterWebClientProvider.get_web_client_preconfigured_for_tor_proxy(
        socks_proxy_url='socks5://localhost:9050',
        control_host='localhost',
        control_port=9051,
        control_password='test1234'
    )

    search_tweets_task = st.SearchTweetsTask(all_words='#covid19')
    output_jl_tweets = st.JsonLineFileRawOutput('output_raw_search_tweets.jl')
    output_jl_users = st.JsonLineFileRawOutput('output_raw_search_users.jl')
    output_print = st.PrintRawOutput()
    st.TweetSearchRunner(search_tweets_task=search_tweets_task,
                         tweet_raw_data_outputs=[output_print, output_jl_tweets],
                         user_raw_data_outputs=[output_print, output_jl_users],
                         web_client=web_client).run()
    
    print(search_tweets_task)
    print(output_jl_tweets)
    print(output_jl_users)
    print(output_print)