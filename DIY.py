from serpapi import GoogleSearch
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.topic = ""
    st.session_state.searchPhrase = ""
    st.session_state.acknowledgement = ""
    st.session_state.list_of_tools = ""
    st.session_state.arr = []
    st.session_state.first_video_link = ""
    st.session_state.zipcode = ""
    st.session_state.total = 0
    st.session_state.products_list = []

with st.sidebar:
    st.session_state.openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    st.session_state.serp_api_key = st.text_input("SerpApi API Key", key="serp_api_key", type="password")
    "[Get a Serpapi API key](https://serpapi.com/manage-api-key)"
    st.header('Helpful Links:')

st.title('Generative AI Planning Tool for DIYers')
st.session_state.topic = st.text_input("**What are you trying to DIY?**", st.session_state.topic)

if st.session_state.topic:
    llm = OpenAI(openai_api_key=st.session_state.openai_api_key)
    if not st.session_state.searchPhrase:
        prompt_template = PromptTemplate(input_variables=['topic'], template="Summarize this topic into a keyword phrase: {topic}")
        st.session_state.searchPhrase = llm.predict(prompt_template.format(topic=st.session_state.topic))
        
    if not st.session_state.acknowledgement:
        prompt_template = PromptTemplate(input_variables=['topic'], template="Acknowledge the user's {topic} with interest.")
        st.session_state.acknowledgement = llm.predict(prompt_template.format(topic=st.session_state.topic))
        st.write(st.session_state.acknowledgement)

    if not st.session_state.first_video_link:
        params = {"api_key": st.session_state.serp_api_key, "engine": "youtube", "search_query": st.session_state.searchPhrase}
        search = GoogleSearch(params)
        results = search.get_dict()
        st.session_state.first_video_link = results['video_results'][0]['link']
        # Display other video links here if needed

    if not st.session_state.arr:
        prompt_template = PromptTemplate(input_variables=['topic'], template="Generate a list of tools and supplies for {topic}")
        st.session_state.list_of_tools = llm.predict(prompt_template.format(topic=st.session_state.topic))
        st.session_state.arr = [item.strip() for item in st.session_state.list_of_tools.split(',')]
        
    for i, item in enumerate(st.session_state.arr, start=1):
        st.write(f"{i}. {item}")
        
    st.session_state.zipcode = st.text_input("What is your zip code?", st.session_state.zipcode)

    if st.session_state.zipcode:
        if not st.session_state.products_list:
            for item in st.session_state.arr:
                params = {"engine": "home_depot", "q": item, "api_key": st.session_state.serp_api_key, "country": "us", "delivery_zip": st.session_state.zipcode}
                search = GoogleSearch(params)
                results = search.get_dict()
                products = results.get("products", [])[0:1]
                for product in products:
                    st.session_state.total += round(product.get("price", 0))
                    st.session_state.products_list.append(product)
        
        for product in st.session_state.products_list:
            st.image(product.get("thumbnail"))
            st.markdown(f"[{product.get('title')}]({product.get('link')})")
            st.write(f"${product.get('price')}")
        st.write(f"Grand total for all the supplies and parts will cost: ${st.session_state.total}")
