"""
Created on Sat Jul 10 15:32:33 2021

@author: Shireesha Govindu
"""

import streamlit as st
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import tweepy
from tweepy import OAuthHandler
import re
import textblob
from textblob import TextBlob
import time
import tqdm

#To ignore Warnings
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns


STYLE = """ 
<style>
img {
     max-width : 100%
   }
</style>"""

def main():
    html_temp = """ 
        <div style = "background-color : #F06296;">
            <p style = "color:white; font-size :40px; padding :9px">
                Live Twitter Sentiment Analysis </p> </div> """
                
    st.markdown(html_temp, unsafe_allow_html = True)        
     ###########Image#########
    from PIL import Image
    image = Image.open('picture.png')
    st.image(image, caption = 'Twitter for Sentiment Analysis',use_column_width = True)
                
    
    st.subheader("Select a topic which you'd like to get the sentiment analysis on : ")
    
    #Twitter API Connection
    
    consumer_key = "Enter Consumer key"
    consumer_secret = "Enter Consumer secret key"
    access_token = "Enter access token key"
    access_token_secret = "Enter access token secret key"
    
    #We have use the about credentials to authenticate the API
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    ##To get the tweets in a proper format, first we create a dataframe to store the extracted data.

    df = pd.DataFrame(columns =["Date","User","IsVerified","Tweet","Likes","RT","User_location"])
    
    #Function to extract tweets

    def get_tweets(Topic, Count):
        i=0
        for tweet in tweepy.Cursor(api.search, q =Topic, count =100, lang ="en", exclude = 'retweets').items():
            print(i, end = '\r')
            df.loc[i,"Date"] =tweet.created_at
            df.loc[i,"User"] = tweet.user.name
            df.loc[i,"IsVerified"] = tweet.user.verified
            df.loc[i,"Tweet"] = tweet.text
            df.loc[i, "Likes"] = tweet.favorite_count
            df.loc[i,"RT"] = tweet.retweet_count
            df.loc[i,"User_location"] = tweet.user.location
            
            #Save as csv
            #df.to_csv("TweetDataset.csv",index =False)
            #Save as excel
            #df.to_excel('{}.xlsx'.format("TweetDataset"),index =False)
            
            i =i+1
            if i>Count :
                break
            else:
                pass

    
    #Function to clean the Tweet

    def clean_tweet(tweet):
        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(w+:\/\/\s+)|([RT])', ' ',str(tweet).lower()).split())

   
    #Function to analyze the sentiment
    def analyze_sentiment(tweet):
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity >0 :
            return 'Positive'
        elif analysis.sentiment.polarity ==0 :
            return 'Neutral'
        else :
            return 'Negative'
    
   
    
    ##Collecting Input from the user
    Topic = str()
    Topic = str(st.text_input("Enter the topic you are interested in (Press enter once done)"))
    
    if len(Topic) >0:
        #Call the function to extract the data
        with st.spinner("Please wait, Tweets are being extracted"):
            get_tweets(Topic, Count =199)
        st.success('Tweets have been extracted!!')

    #Call function to get clean tweets
    df['clean_tweet'] = df['Tweet'].apply(lambda x : clean_tweet(x))

    #Call function to get sentiments
    df["Sentiment"] = df["Tweet"].apply(lambda x : analyze_sentiment(x))
    
    # Summary of the tweets
    
    st.write("Total Tweets extracted for Topic {} are : {}".format(Topic,len(df.Tweet)))
    st.write("Total Positive Tweets are : {}".format(len(df[df["Sentiment"]=="Positive"])))
    st.write("Total Negative Tweets are : {}".format(len(df[df["Sentiment"]=="Negative"])))
    st.write("Total Neutral Tweets are : {}".format(len(df[df["Sentiment"]=="Neutral"])))
    
    # See the extracted Data
    if st.button("See the Extracted Tweets"):
        #st.markdown(html_temp, unsafe_allow_html =True)
        st.success("Below are the extracted Tweets : ")
        st.write(df.head(50))
        
    
    #To get the count plot
    if st.button("Get the count plot for different sentiments"):
        st.success("Generating a Count Plot")
        st.subheader("Count Plot for Different Sentiments")
        st.write(sns.countplot(df["Sentiment"]))
        st.pyplot()
        
        
    #Pie Chart
    if st.button("Get Pie chart for different Sentiments"):
        st.success("Generating Pie Chart")
        a=len(df[df["Sentiment"]=="Positive"])
        b =len(df[df["Sentiment"]=="Negative"])
        c = len(df[df["Sentiment"] == "Neutral"])
        d= np.array([a,b,c])
        explode = (0.1,0.0,0.1)
        st.write(plt.pie(d,shadow =True, explode = explode, labels = ["Positive","Negative", "Neutral"],autopct = '%1.2f%%'))
        st.pyplot()
        
        
    #Get the countplot based on verified and unverified users
    if st.button("Get the count plot based on verified and unverified users"):
        st.success("Generating a Count Plot(Verified and Unverified Users)")
        st.subheader("Count Plot for Different Sentiments of verified and unverified users")
        st.write(sns.countplot(df["Sentiment"],hue =df.IsVerified))
        st.pyplot()
        
        
    
    
    st.sidebar.header("About Twitter Sentiment Analysis App")
    st.sidebar.info("This is a Twitter sentiment analysis Project built for analysing the sentiments of the tweets extracted from a particular topic given by the user. The different visualizations will help us to view the sentiments like positive, negative or neutral of the tweets extracted ")
    st.sidebar.text("Built with Streamlit library, Python")
    st.sidebar.header("For any Queries/Suggestions Please reach out at :")
    st.sidebar.info("shireesha.govindu@gmail.com")
    
    
    if st.button("Exit"):
        st.balloons()
        
        
if __name__ == '__main__' :
    main()

