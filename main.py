import sqlite3 
import streamlit as st
import pandas as pd
import praw 
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import sqlite3


#streamlit run main.py

reddit = praw.Reddit(
    user_agent="myApp",
    client_id = "",
    client_secret = ""
)

st.sidebar.title("Navigation Bar")
options = st.sidebar.selectbox("",("wallstreetbets","Chart","3"))

connection = sqlite3.connect('table.db')
cursor = connection.cursor()

st.title(options)

if options == "wallstreetbets":
    subred = reddit.subreddit("wallstreetbets")
    #symbol = st.sidebar.text_input("Symbol",value="AAPL",max_chars=5)
    #use subread.search or .rising or .top or .hot('insert here the stock name',limit=1000)
    subm = [[s.url,s.title,s.upvote_ratio,s.score,s.author]for s in subred.new(limit=10)]
    #data = pd.DataFrame(subm, columns=['id','url','title','comments','score','author','time','content'])
    #json format works
    st.write(subm)
    num_days = st.sidebar.slider('Number of days',1,30,3)

    cursor.execute("""
        SELECT COUNT(*) AS num_mentions, symbol
        FROM mention JOIN stock ON stock.id = mention.stock_id
        WHERE date(dt) > current_date - interval '%s day'
        GROUP BY stock_id, symbol
        HAVING COUNT (symbol) > 10
        ORDER BY num_mentions DESC
    """, (num_days,))

    counts = cursor.fetchall()
    for c in counts:
        st.write(c)
    
    cursor.execute(""""
        SELECT symbol, message, url, dt, username
        FROM mention JOIN stock ON stock.id = mention.stock_id
        ORDER BY dt DESC
        LIMIT 10
    """)

    mentions = cursor.fetchall()
    for m in mentions:
        st.text(m['dt'])
        st.text(m['symbol'])
        st.text(m['message'])
        st.text(m['url'])
        st.text(m['username'])
    
    rows = cursor.fetchall()
    st.write(rows)


if options == "Chart":
    name = st.text_input("Insert ticker")
    #x = name.upper()
    if name:
        ticker = yf.download(name.upper(),period='ytd')
        #close_tick = ticker.Close
        #st.write(ticker.columns)
        fig = px.line(ticker.Close,x=ticker.index,y="Close", title=name.upper()+" Price")
        fig.update_xaxes(rangeslider_visible=True)

        st.write(fig)

