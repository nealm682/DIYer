import streamlit as st
from serpapi import GoogleSearch
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Initialize session state variables
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.topic = ""
    st.session_state.zipcode = ""
    st.session_state.products_list = []
    st.session_state.total = 0
    st.session_state.arr = []
    st.session_state.searchPhrase = ""
    st.session_state.acknowledgement = ""
    st.session_state.first_video_link = ""

# Sidebar for API keys
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", placeholder="Enter your API key here")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    serp_api_key = st.text_input("SerpApi API Key", key="serp_api_key", type="password")
    "[Get an Serpapi API key](https://serpapi.com/manage-api-key)"

# Main Page
st.title('Generative AI Planning Tool for DIYers')
st.session_state.topic = st.text_input("**What are you trying to DIY?**", st.session_state.topic)

if st.session_state.topic:
    # Once the topic is input, a button appears to allow the user to start the process
    if st.button("Start"):
        llm = OpenAI(openai_api_key=openai_api_key)
        # Additional API calls and processing here
        st.session_state.searchPhrase = "Example Search Phrase"  # Example
        st.session_state.acknowledgement = "Acknowledgement Message"  # Example
        st.session_state.first_video_link = "Example Video Link"  # Example
        st.session_state.arr = ['tool1', 'tool2', 'tool3']  # Example

    if st.session_state.acknowledgement:
        st.write(st.session_state.acknowledgement)

    if st.session_state.arr:
        st.write("**Here is a list of tools and supplies you will need to complete this project:**")
        for i, item in enumerate(st.session_state.arr, start=1):
            st.write(f"{i}. {item}")
        st.session_state.zipcode = st.text_input("**I can shop around for the best prices for these supplies. What is your zip code?**", st.session_state.zipcode)
        
        if st.session_state.zipcode and st.button("Find Prices"):
            # Call the API for each item in the arr and update the products_list and total
            for item in st.session_state.arr:
                # API call example, please replace with actual call
                st.session_state.products_list.append({"thumbnail": 'url', "title": 'title', "price": 10, "link": 'link'})
                st.session_state.total += 10  # Example

    if st.session_state.products_list:
        for product in st.session_state.products_list:
            st.image(product['thumbnail'])
            st.markdown(f"[{product['title']}]({product['link']})")
            st.write(f"${product['price']}")
        st.write(f"Grand total for all the supplies and parts will cost: ${st.session_state.total}")
