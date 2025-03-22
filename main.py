from src.analytics.get_analytics import build_analytics
from src.qna_with_data.rag_engine import RAGEngine

import pandas as pd 
import os 

import io 
import base64

from flask import Flask, request, jsonify


# Create Flask app
app = Flask(__name__)

# Load DataFrame
print("🕗 Loading DataFrame...")
dataframe = pd.read_csv("data/structured/data_for_analytics.csv")
print("✅ DataFrame loaded!")

# Load RAG Engine
print("🕗 Loading RAG Engine...")
rag_engine = RAGEngine()
print("✅ RAG client initiated!")


@app.route("/analytics", methods=["POST"])
def analytics():
    """
        API endpoint to generate analytics and return them as Base64-encoded images.
    """
    # get analytics from dataframe 
    analytics = build_analytics(dataframe) 
    return analytics


@app.route("/ask", methods=["POST"])
def ask():
    """
        API endpoint to generate a response to a given query using RAG for hotel bookings data.
    """
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # get response from RAG engine
    context = rag_engine.query_vector_db(query, 2)
    response = rag_engine.generate_response(query, context)
    
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)