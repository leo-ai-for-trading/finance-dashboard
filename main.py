import streamlit as st
import pandas as pd
import praw 

#streamlit run main.py

reddit = praw.Reddit(
    user_agent="myApp",
    client_id = "DVH0cAZkUVU1k5pIZRxr_Q",
    client_secret = "9WJETN76viVWjoDjlPP75g66jfk6MQ"
)

st.sidebar.title("Navigation Bar")
options = st.sidebar.selectbox("",("wallstreetbets","twitter","3"))

st.title(options)

if options == "wallstreetbets":
    subred = reddit.subreddit("wallstreetbets")
    #symbol = st.sidebar.text_input("Symbol",value="AAPL",max_chars=5)
    #use subread.search or .rising or .top or .hot('insert here the stock name',limit=1000)
    subm = [[s.url,s.title,s.upvote_ratio,s.score,s.author]for s in subred.new(limit=10)]
    #data = pd.DataFrame(subm, columns=['id','url','title','comments','score','author','time','content'])
    #json format works
    st.write(subm)
