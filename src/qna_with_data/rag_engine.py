import pandas as pd 
import numpy as np 
import os
from dotenv import load_dotenv
load_dotenv()
import json 

from sentence_transformers import SentenceTransformer
from pinecone import Pinecone 
from groq import Groq 


class RAGEngine:
    def __init__(self, 
        embedding_model = "sentence-transformers/all-MiniLM-L6-v2", 
        index_name = "hotelbookings", 
        vector_db_api=os.getenv("PINECONE_API_KEY"), 
        groq_api=os.getenv("GROQ_API_KEY")
    ):
        self.embedder = SentenceTransformer(embedding_model)
        self.pc = Pinecone(api_key=vector_db_api)
        self.index = self.pc.Index(index_name)
        self.groq_client = Groq(api_key=groq_api)


    def query_vector_db(self, query, topk):
        """
        Query the vector database for the most similar vectors to the query vector
        """
        query_vector = self.embedder.encode(query)

        # Query the vector database
        results = self.index.query(
            vector=query_vector.tolist(),
            top_k=topk, 
            include_metadata=True
        )
        context = []
        for i in results.matches: 
            context.append(i.metadata.get('text'))
            context.append(str(i.get('score')))
        # join into string 
        context = " ".join(context)
        return context
    

    def generate_response(self, user_query, context, model="llama3-70b-8192"):
        """
        Generate response using an open source llm 
        """     
        prompt = f"""
            You are an AI assistant with access to the following retrieved information from the hotel bookings data.
            {context}

            Using the provided context, answer the following question as accurately and concisely as possible:

            Question: {user_query}

            If the retrieved context is not relevant (score is very low) or does not contain the answer, say "I don't know" instead of making up information.
        """
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
        )

        response = chat_completion.choices[0].message.content
        return response
        




