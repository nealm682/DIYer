# Testing multiple api calls to gpt and serpapi
from serpapi import GoogleSearch
import os
import ast
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

#NOTE TO SELF.  Past this command in the CLI to display UI: streamlit run DIY.py [ARGUMENTS]

searchPhrase = ""
acknowledgement = ""
list_of_tools = ""
arr = []
first_video_link = ""
zipcode = ""
topicComplete = False
searchPhraseComplete = False
acknowledgementComplete = False
first_video_linkComplete = False

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", placeholder="Enter your API key here")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    serp_api_key = st.text_input("SerpApi API Key", key="serp_api_key", type="password")
    "[Get an Serpapi API key](https://serpapi.com/manage-api-key)"
    st.header('Helpful Links:')

#app framework with text input and title
st.title('DIY Planning tool enhanced with Artificial Intelligence')
topic = st.text_input("**What are you trying to DIY?**")

# API Keys
llm = OpenAI(openai_api_key=openai_api_key)
llm2 = OpenAI(openai_api_key=openai_api_key)
llm3 = OpenAI(openai_api_key=openai_api_key)

# Wrangle the data by assigning the topicSummary to a variable and then calling OpenAI to summarize it
if topic and topicComplete == False:
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
if searchPhrase and searchPhraseComplete == False:
 # Prompt Templates
    # Simplify the topic into a keyword
    summarize_youtube_template = """Acknowledge the user's {topic}. Briefly explain that you are gathering resources that will help the user with their project. This will include a couple of how to videos from youtube.  And also building a short list of supplies they will need for their task. Acknowledgement:"""

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
if acknowledgement and acknowledgementComplete == False:
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
    with st.sidebar:
        st.write("")
        st.write("Here are the top 2 video results on Youtube that could be helpful:")
        st.write(first_video_title)
        st.markdown(f'<a href="{first_video_link}" target="_blank"><img src="{first_video_thumbnail}" alt="Thumbnail" style="width:200px;height:150px;"></a>', unsafe_allow_html=True)
        st.write(second_video_title)
        st.markdown(f'<a href="{second_video_link}" target="_blank"><img src="{second_video_thumbnail}" alt="Thumbnail" style="width:200px;height:150px;"></a>', unsafe_allow_html=True)



# Create a list of tools and supplies needed to complete the project
if first_video_link and first_video_linkComplete == False:
     # Prompt Templates
    # Simplify the topic into a keyword
    tools_template = """Generate a list of parts, supplies and necessary tools required to complete the following topic. Only reply with an array. No need to add titles or numbers. Limit it to a maximum list of 3. List them highest priority.  Meaning, if they are installing equipment list the equipment as top of the list. People are more likely to have a screw driver, so list that at the bottom. {topic}.  array:"""

    prompt = PromptTemplate(
        input_variables = ['topic'],
        template=tools_template
    )

    formatted_prompt = prompt.format(topic=topic)

    list_of_tools = llm3.predict(formatted_prompt)

    arr = [item.strip() for item in list_of_tools.split(',')]
    st.write("")
    #print out a nice numbered list of tools and supplies
    st.write("**Here is a list of tools and supplies you will need to complete this project:**")
    # add a radio button to each output in the list to select the item
    for i in range(len(arr)):
        st.write(i+1, arr[i])
st.write("")
# Ask the user for their zip code so we can search for the best prices on the tools and supplies
if (arr):
    zipcode = st.text_input("**I can shop around for the best prices for these supplies.  What is your zip code?**")


# Search for the best prices on the tools and supplies

             
if zipcode:
    # Set an array variable that will hold the sum of the array product values
    total = 0
    products_list = []

    # Create a loop that will iterate through the array and call the serpapi API for each item in the array
    for item in arr:
        params = {
            "engine": "home_depot",
            "q": item,  # Search each item in the array
            "api_key": serp_api_key,  # Replace with your actual SerpAPI key
            "country": "us",
            "delivery_zip": zipcode  # Adjust as needed
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        products = results.get("products", [])[0:1]  # This will give an empty list if "products" does not exist

        for product in products:
            thumbnail = product.get("thumbnails", [[]])[0][0]  # Get the first thumbnail
            title = product.get("title", "No title available")
            price = product.get("price", 0)
            link = product.get("link", "")
            
            total += round(price)
            products_list.append({"thumbnail": thumbnail, "title": title, "price": price, "link": link})

    # Display the products in a 3x3 grid
    for i in range(0, len(products_list), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(products_list):
                product = products_list[i + j]
                # Get the highest resolution thumbnail available
                thumbnail = product.get("thumbnails", [[]])[-1][-1]  # Get the last thumbnail
                
                with cols[j]:
                    # Adjust width if necessary, remove if you want to use the original width of the thumbnail
                    st.image(thumbnail)
                    st.markdown(f"[{product['title']}]({product['link']})")
                    st.write(f"${product['price']}")

                    
    st.write(f"Grand total for all the supplies and parts will cost: ${total}")
