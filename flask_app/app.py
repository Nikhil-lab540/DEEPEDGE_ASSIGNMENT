
from flask import Flask, request, jsonify
import os
from utils import search_articles,fetch_article_content,concatenate_content,generate_answer


# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Load API keys from environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


print("SERPER_API_KEY:", SERPER_API_KEY)

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    try:
        """
        Handles the POST request to '/query'. Extracts the query from the request,
        processes it through the search, concatenate, and generate functions,
        and returns the generated answer.
        """
        # get the data/query from streamlit app
        data =request.json
        user_query =data.get("user_query")

        print("Received query: ")
        
        # Step 1: Search and scrape articles based on the query
        
        articles = search_articles(user_query)
        print("Step 1: Articles retrieved: ")

        if not articles:
            return jsonify({"answer": "No relevant articles found for the query."}), 200


        # Step 2: Concatenate content from the scraped articles
        content = concatenate_content(articles)
        print("Step 2: concatenating content")
        if not content:
            return jsonify({"answer": "No relevant content found to generate an answer."}), 200

        # Step 3: Generate an answer using the LLM
        answer = generate_answer(content, user_query)
        print("Step 3: generating answer")

        # return the jsonified text back to streamlit
        return jsonify({"answer": answer}), 200
    except Exception as e:
        # Log the error and return a 500 error response
        print(f"Error occurred: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
