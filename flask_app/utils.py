import os,requests,json
from bs4 import BeautifulSoup
from langchain_community.llms import Ollama


from dotenv import load_dotenv
load_dotenv()

# Load API keys from environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

print("SERPER_API_KEY:", SERPER_API_KEY)


def search_articles(query):
    """
    Searches for articles related to the query using the Serper API.
    Returns a list of dictionaries containing article URLs and titles.
    """
        
    url = "https://google.serper.dev/search"
    print(query)

    payload = json.dumps({
    "q": query
    })
    headers = {
    'X-API-KEY': SERPER_API_KEY,
    'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json()
            articles = []

            for item in data.get('organic', []):
                article = {
                    'url': item.get('link'),
                    
                }
                articles.append(article)
            
            print("Articles retrieved: ", articles)
            return articles
        else:
            print("Error fetching articles: ", response.status_code, response.text)
            return []
    except requests.RequestException as e:
        print("Exception occurred: ", str(e))
        return []



def fetch_article_content(url):
    """
    Fetches the article content, extracting headings and text.
    """
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract headings and paragraphs
        headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        
        # Combine headings and paragraphs
        content = "\n".join(headings + paragraphs)
        return content.strip()
    else:
        print(f"Error fetching article content from {url}: {response.status_code}")
        return ""

    # content = ""
    # # implementation of fetching headings and content from the articles

    # return content.strip()


def concatenate_content(articles):
    """
    Concatenates the content of the provided articles into a single string.
    """
    full_text = ""
    # formatting + concatenation of the string is implemented here
    for article in articles:
        content = fetch_article_content(article['url'])
        print(f"Content fetched from {article['url']}: ", content)
        full_text += content + "\n\n"  # Add extra newlines between articles for separation
    
    
    

    return full_text


def generate_answer(content, query):
    """
    Generates an answer from the concatenated content using GPT-4.
    The content and the user's query are used to generate a contextual answer.
    """
    # Create the prompt based on the content and the query
    try:
        # Create the prompt based on the content and the query
        prompt = f"Based on the following content, answer the question:\n\nContent:\n{content}\n\nQuestion: {query}"

        # Assuming ollama is correctly imported and initialized
        llm = Ollama(model="llama3")
        
        # Generate the response
        response = llm.invoke(prompt)
        
        # Extract the answer from the response
        answer = response
        
        return answer
    
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "An error occurred while generating the answer."
    

    
