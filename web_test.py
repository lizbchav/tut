import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
from openai import OpenAI
import os

def clean_unicode(text):
    return text.encode("utf-8", "ignore").decode("utf-8")
# Create a text input for the URL
url = st.text_input('Enter a URL')

def get_web_content(url):
    # Fetch the webpage
    web_content = ""
    response = requests.get(url)

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Display the title of the webpage
    st.write('Title of the webpage:')
    st.write(soup.title.string)

    # Display the text of the webpage
    st.write('Text of the webpage:')
    article_tags = soup.find_all('article')
    
    for article in article_tags:
        paragraphs = article.find_all('p')
        for p in paragraphs:
            web_content = web_content + str(p.get_text()) + '\n'

    return web_content

# Takes the transcription of the meeting and returns a summary of it via text completions
def abstract_summary_extraction(transcription):
    transcription_clean = clean_unicode(transcription)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are..."
            },
            {
                "role": "user",
                "content": transcription_clean
            }
        ]
    )
    return response.choices[0].message.content


openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

# Create a button to fetch the content
if st.button('Fetch Content'):
    display_content = get_web_content(url)
    st.write(abstract_summary_extraction(display_content))