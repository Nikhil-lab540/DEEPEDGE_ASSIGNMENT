
import streamlit as st
import requests



st.title("LLM-based RAG Search")

# Input for user query
query = st.text_input("Enter your query:")

if st.button("Search"):
    if query:
        # Debugging: Print query and URL
        print(f"Accessing Flask API with query: {query}")
        
        # Make a POST request to the Flask API
        try:
            response = requests.post(url="http://localhost:5001/query", json={"user_query": query})
            
            if response.status_code == 200:
                # Display the generated answer
                answer = response.json().get('answer', "No answer received.")
                st.write("Answer:", answer)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a query before searching.")