import snscrape.modules.telegram as sntele
import pandas as pd
import re
from textblob import TextBlob
import streamlit as st
import numpy as np
import plotly.express as px


class telegram_scrapper:
    def __init__(self):
        return None

    def cleanText(self, text):

        """
       Clean the input text by removing @mentions, hashtags, URLs, and newlines.
       
       Parameters:
       - text (str): The input text to be cleaned.
       
       Returns:
       - str: The cleaned text after removing the specified patterns.
        """
       
        if isinstance(text, str):
            text = re.sub('@[A-Za-z0-9_]+', '', text)  # removes @mentions
            text = re.sub('#', '', text)  # removes hastag '#' symbol
            text = re.sub('RT[\s]+', '', text)
            text = re.sub('https?:\/\/\S+', '', text)  # removes URLs
            text = re.sub('\n', ' ', text)
            return text
        else:
            return ''

    def getSubjectivity(self, text):
        """
                
        Calculate and return the subjectivity of the given text using TextBlob sentiment analysis.
        
        Parameters:
            text (str): The text for which subjectivity needs to be determined.
            
        Returns:
            float: The subjectivity score of the text.
        
        """
        return TextBlob(text).sentiment.subjectivity

    def getPolarity(self, text):
        """
        Calculate the polarity of the given text using TextBlob's sentiment analysis.
        
        Parameters:
            self: The instance of the class.
            text: The input text for which polarity needs to be calculated.
        
        Returns:
            The polarity of the input text.
        """
        return TextBlob(text).sentiment.polarity

    def getAnalysis(self, score):
        """
        Determines the sentiment analysis based on the given score.

        Parameters:
            score (int): The score to analyze.

        Returns:
            str: The sentiment analysis result. Possible values are 'Negative', 'Neutral', or 'Positive'.
        """

        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    def create_wordcloud(self, text):
        """
        Creates a word cloud from the input text.

        Args:
            self: The class instance.
            text: The input text to generate the word cloud from.

        Returns:
            A string containing all the words from the input text.
        """
        allWords = ' '.join([tweets for tweets in text])
        return allWords

    def most_mentioned(self, df_series):
        """
        Returns the names and counts of the most mentioned words in the given DataFrame series.
        
        Parameters:
            df_series (DataFrame series): The input DataFrame series.
        
        Returns:
            tuple: A tuple containing two lists - the names of the most mentioned words and their respective counts.
        """
        t = re.findall('\$[A-Za-z]+', self.create_wordcloud(df_series))
        name = []
        counts = []
        for i in set(t):
            name.append(i)
            counts.append(t.count(i))
        return name, counts
    
    def sentiment_pie_chart(self, df):
        """
    	Generates a pie chart based on the sentiment analysis results in the input DataFrame.

    	:param df: The DataFrame containing the sentiment analysis results.
    	:return: The generated pie chart.
    	"""

        df_grouped = df['Analysis'].value_counts(ascending=False).reset_index(name='counts')
        fig = px.pie(df_grouped, values='counts', names='Analysis', title='Sentiment Analysis')


        return fig


    def scrapping_context(self, channels, max_limit):

        """
        Scrapes context from the given channels up to the specified maximum limit.

        Parameters:
            channels (list): The list of channels to scrape context from.
            max_limit (int): The maximum number of items to scrape from each channel.

        Returns:
            DataFrame: A DataFrame containing the scraped context along with additional analysis columns.
        """

        date_repo = []
        outlinks_repo = []
        context_repo = []
        for channel in channels:
            for i, context in enumerate(sntele.TelegramChannelScraper(name=channel).get_items()):
                date_repo.append(context.date)
                outlinks_repo.append(context.outlinks)
                context_repo.append(context.content)
                if i > max_limit:
                    break

        dict_file = {
            'date': date_repo,
            'context': context_repo,
            'outlinks_repo': outlinks_repo
        }

        df = pd.DataFrame(dict_file)
        df['clean_context'] = df['context'].apply(self.cleanText)

        df['Subjectivity'] = df['clean_context'].apply(self.getSubjectivity)

        df['Polarity'] = df['clean_context'].apply(self.getPolarity)

        df['Analysis'] = df['Polarity'].apply(self.getAnalysis)

        df.drop('context', axis=1, inplace=True)

        return df
    

######## App Code ######
st.set_page_config(page_title="Telegram Channel Data Scraper", page_icon=":🤖:", layout="wide")

col1, col2, col3 = st.columns([1,3,1])

with col2:
# Create a Streamlit app
   

    st.write("check out this [link](https://github.com/harshdabhi/Social-Sentiment-and-Scrapper):👨‍💼:")

    st.title("Telegram Channel Data Scraper")
    st.write("Enter the list of Telegram channels and the limit of scraping data.")

    channels = st.text_input('Enter the list of Telegram channel names separated by comma (e.g. Channel1, Channel2, Channel3)')
    max_limit = st.number_input('Enter the maximum number of posts to scrape per channel',step=10, min_value=10)

    if st.button('Scrape Data'):
        if channels:
            channel_list = [channel.strip() for channel in channels.split(',')]
            scrapper = telegram_scrapper()
            df = scrapper.scrapping_context(channel_list, max_limit)

            if len(df) > 0:
                st.subheader("Most Mentioned Words")
                names, counts = scrapper.most_mentioned(df['clean_context'])
                df_temp=pd.DataFrame({'names': names, 'counts': counts})
                st.bar_chart(df_temp,x='names',y='counts')

                st.subheader("Sentiment Analysis")

                sentiment_chart = scrapper.sentiment_pie_chart(df)
                st.plotly_chart(sentiment_chart, use_container_width=True)

                st.dataframe(df[['clean_context', 'Subjectivity', 'Polarity', 'Analysis']].head(50))
                

               

                # You can add more visualizations and data manipulation here as needed

            else:
                st.write('No data found for the provided channels and limit.')
        else:
            st.write('Please enter the list of channels and limit to scrape data.')


