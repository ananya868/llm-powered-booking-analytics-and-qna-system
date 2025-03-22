# LLM-Powered Booking Analytics and Q&A System

## Overview

A system that processes hotel booking data, extracts insights, and enables
retrieval-augmented question answering (RAG). 

LLM Used - Llama-3-70b 

## Features

- **Booking Analytics**: Analyze booking data to extract meaningful insights, trends, and patterns through plots.
- **Q&A System**: Interact with the booking dataset using natural language queries, receiving accurate and context-aware responses

**Example Response**
```bash
Query: What was the overall cancellation rate?
Answer: The overall cancellation rate for hotel bookings was 37.04%.

Query: which country has more than 200 cancellations?
Answer: According to the provided data, the country AGO has a total of 205 cancellations, which is more than 200.

Query: What was the average stay duration?
Answer: The average stay duration for hotel bookings was 3.43 days.
```
Analytics - 
<table>
  <tr>
    <td><img src=tests/analytics_plots/market_segment_distribution.png width="300"></td>
    <td><img src=tests/analytics_plots/revenue_trends.png width="300"></td>
    <td><img src=tests/analytics_plots/revenue_by_channel.png width="300"></td>
  </tr>
</table>

## **NOTE**

> The file 'test.ipynb' contains test runs for api endpoints

## **How to Setup** 

1. Clone repo -
```bash
git clone https://github.com/ananya868/llm-powered-booking-analytics-and-qna-system.git
cd llm-powered-booking-analytics-and-qna-system
```
2. Install dependencies (You may create new virutal env if req) -
```bash
pip install -r requirements.txt
```
3. Set up Environment Variables
   - Create an .env file inside the main dir
   - put your groq api key along with **already given pinecone api key** into .env file:
      - Your Groq AI api key (free to use at https://groq.com/)
      - Pinecone API key (Already filled)
      - ```
        GROQ_API_KEY = "### Your key here ###"
        PINECONE_API_KEY = "pcsk_7PfeFx_5f1ZpvFYhnW5Yeqw3zTwA3YXTB1E21MNE7fivTC5YGM8TiVNgKzBz4rAzGyroRf"
        ```

## **Usage**

1. **To run, simply run the cmd** -
```bash
python main.py
```
Wait for server and dependant clients to load completely. You will see something like this after successful loading -
   
![A](data/misc/run.png)

3. **Interact with the QnA System**:
   - Access the interactive interface at http://127.0.0.1:5000 (or the specified port).

4. **API endpoints**:
   - analytics/ - returns base64 encoded plots for various insights, trends, and patterns.
   - ask/  (requires parameter: query) - returns response using RAG engine based on pinecone vector db.


### Once flask app is running, you can test endpoints using the following python code:

```python
import requests
import time
import os
import base64

# Analytics
response = requests.post("http://127.0.0.1:5000/analytics")
data = response.json()

# Save plots to save_path dir
def save_plot(save_path: str = "analytics_plots/"):
    os.mkdir(save_path)
    for key, value in data.items():
        with open(f"{save_path}/{key}.png", "wb") as f:
            f.write(base64.b64decode(value))
        print(f"Saved {key}.png")

save_plot()

# QNA 
q1 = "What was the overall cancellation rate?"
answer = requests.post("http://127.0.0.1:5000/ask", json={"query": q1})
res = answer.json()

print(
  f"Query: {q1}\nAnswer: {res.get('response')}\n"
)
```

## **Project Structure**

```
data
  - raw : Raw data
  - misc : Misc data
  - structured : Processed data storage
notebooks : All jupyter notebooks
src : Main python scripts
  - analytics 
    - get_analytics.py : Generate analytics for dataframe
  - pre_processing
    - data_transformation.py : Transforms data to text for RAG
    - feature_engineering.py : Builds Features over dataframe
    - pre_process.py : Basic pre processing and data cleaning
  - qna_with_data
    - chat_with_csv.py (misc)
    - rag_engine.py : Main RAG script (pinecone)
tests : Saved plots from api endpoint 
README.md 
main.py : Flask app
requirements.txt
test.ipynb : Testing API Endpoints
```

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.






















