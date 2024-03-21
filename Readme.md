Telegram Channel Data Scrape

This project is a Telegram channel data scraper with sentiment analysis, created using Streamlit.


Getting Started

These are the steps to get this Telegram Channel Data Scraper up and running.

    Create a Conda Environment

    cmd: conda create -n env python==3.10



Activate the Environment

    cmd: conda activate env

Install Dependencies

    pip install -r requirements.txt

Run the Telegram Channel Data Scraper

    streamlit run streamlit.py

The Streamlit app will open in your browser.

Features

    🤖 Scrape public Telegram channels for context, links, and sentiment analysis.
    📊 View a bar chart for most mentioned words.
    📊 View a pie chart for the sentiment analysis of the scraped data.
    💻 Interactive table view with filtering and sorting capabilities.

Usage

    Enter the list of Telegram channel names, separated by commas, in the provided input box.
    Enter the maximum limit of posts to scrape in the provided input box.
    Click the "Scrape Data" button to start scraping data and view the most mentioned words and sentiment analysis.

License

This project is distributed under the [MIT License](https://github.com/harshdabhi)