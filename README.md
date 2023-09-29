# DIYer
# Generative AI Planning Tool for DIYers

This project is a Streamlit app aimed at assisting DIY enthusiasts in planning their projects by leveraging the capabilities of OpenAI and SerpAPI. The app helps users gather the best resources, find how-to videos from YouTube, and build a list of necessary tools and supplies along with their best prices.  Demo: https://pf9yhoje3dv3cmtsskdry6.streamlit.app/


## Features

- **Keyword Phrase Generation:** The app summarizes the user's project topic into an optimal YouTube search phrase.
- **Acknowledgement Generation:** It acknowledges the user's intent and explains the resources being gathered.
- **YouTube Search:** It utilizes SerpAPI to fetch relevant YouTube videos based on the topic.
- **List of Tools and Supplies:** The app generates a concise list of necessary parts, supplies, and tools required for the project.
- **Price Comparison:** It searches for the best prices for the listed tools and supplies based on the user’s zip code.

## Prerequisites

- Python 3.9 or later
- OpenAI API Key
- SerpAPI API Key

## Installation

1. Clone this repository:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory and install the required packages:
    ```sh
    cd <project-directory>
    pip install -r requirements.txt
    ```
3. Run the Streamlit app:
    ```sh
    streamlit run DIY.py
    ```

## Usage

1. Input your OpenAI and SerpAPI keys in the sidebar.
   - [Get an OpenAI API key](https://platform.openai.com/account/api-keys)
   - [Get a SerpAPI API key](https://serpapi.com/manage-api-key)
2. Enter your DIY project topic in the main input box.
3. The app will process the input and provide a summary, YouTube video links, a list of necessary tools and supplies, and their best prices based on the provided zip code.

## Notes

- API keys are required for accessing OpenAI and SerpAPI services. You can get free API keys by following the provided links in the sidebar.
- The app will ask for the API keys, and they are necessary for the functionalities provided by the respective APIs.

## Contributing

If you would like to contribute to this project, please fork this repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
 
