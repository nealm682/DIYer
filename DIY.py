# Testing multiple api calls to gpt and serpapi
from serpapi import GoogleSearch
import os
import ast
import streamlit as st
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

#NOTE TO SELF.  Past this command in the CLI to display UI: streamlit run DIY.py [ARGUMENTS]

#app framework with text input and title
st.title('DIY Planning with AI')
topic = st.text_input("**What are you trying to DIY?**")
searchPhrase = ""
acknowledgement = ""
list_of_tools = ""
arr = []
first_video_link = ""

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    serp_api_key = st.text_input("SerpApi API Key", key="serp_api_key", type="password")
    "[Get an Serpapi API key](https://serpapi.com/manage-api-key)"

# API Keys
llm = OpenAI(openai_api_key=openai_api_key)
llm2 = OpenAI(openai_api_key=openai_api_key)
llm3 = OpenAI(openai_api_key=openai_api_key)

# Wrangle the data by assigning the topicSummary to a variable and then calling OpenAI to summarize it
if topic:
    # Prompt Templates
    # Simplify the topic into a keyword
    summarize_youtube_template = """Summarize this topic into the most optimal Youtube search phrase. Context: {topic}  Youtube Search Phrase:"""

    prompt = PromptTemplate(
        input_variables = ['topic'],
        template=summarize_youtube_template
    )

    formatted_prompt = prompt.format(topic=topic)

    searchPhrase = llm.predict(formatted_prompt)


# Acknowledge the user's reason for visiting.  Let them know you will be helping them with the project as an assistant.
if searchPhrase:
 # Prompt Templates
    # Simplify the topic into a keyword
    summarize_youtube_template = """Acknowledge the user's {topic}.  Acknowledgement:"""

    prompt = PromptTemplate(
        input_variables = ['topic'],
        template=summarize_youtube_template
    )

    formatted_prompt = prompt.format(topic=topic)

    acknowledgement = llm2.predict(formatted_prompt)

    st.write(acknowledgement)
    #add a space between the acknowledgement and the youtube search results
    st.write("")

# Search Youtube for relevant videos based on the topic.  I'm selecting the first index of the array
if acknowledgement:
    # search youtube for the top video result based on main topic
    params = {
    "api_key": serp_api_key,
    "engine": "youtube",
    "search_query": searchPhrase
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    first_video_link = results['video_results'][0]['link']
    first_video_title = results['video_results'][0]['title']
    first_video_thumbnail = results['video_results'][0]['thumbnail']['static']
    second_video_link = results['video_results'][1]['link']
    second_video_title = results['video_results'][1]['title']
    second_video_thumbnail = results['video_results'][1]['thumbnail']['static']

    # Print the first video title and link
    st.write("\n\n**First, here are the top 2 video result on Youtube that could be helpful:**")
    st.write(first_video_title)
    st.markdown(f'<a href="{first_video_link}" target="_blank"><img src="{first_video_thumbnail}" alt="Thumbnail" style="width:200px;height:150px;"></a>', unsafe_allow_html=True)
    st.write(second_video_title)
    st.markdown(f'<a href="{second_video_link}" target="_blank"><img src="{second_video_thumbnail}" alt="Thumbnail" style="width:200px;height:150px;"></a>', unsafe_allow_html=True)


# Create a list of tools and supplies needed to complete the project
if first_video_link:
     # Prompt Templates
    # Simplify the topic into a keyword
    tools_template = """Generate a list of parts, supplies and necessary tools required to complete the following topic. Only reply with an array. No need to add titles or numbers. Limit it to a maximum list of 10. {topic}.  array:"""

    prompt = PromptTemplate(
        input_variables = ['topic'],
        template=tools_template
    )

    formatted_prompt = prompt.format(topic=topic)

    list_of_tools = llm3.predict(formatted_prompt)

    arr = [item.strip() for item in list_of_tools.split(',')]
    #print out a nice numbered list of tools and supplies
    st.write("\n\n**Here is a list of tools and supplies you will need to complete this project:**")
    # add a radio button to each output in the list to select the item
    for i in range(len(arr)):
        st.write(i+1, arr[i])

# Ask the user for their zip code so we can search for the best prices on the tools and supplies
if (arr):
    zipcode = st.text_input("\n\n**I can shop around for the best prices for these supplies.  What is your zip code?**")
