import pandasai as pai 
from dotenv import load_dotenv
import os

load_dotenv()

class QNAEngine:
    def __init__(self, query: str, dataframe_path: str):
        self.query = query
        self.dataframe_path = dataframe_path

    def chat_using_sql_chain(self): 
        """
        Chat with the SQL chain model
        """
        pass
    
    def chat_using_pandasai(self):
        """
        Chat with the pandas dataframe
        """
        pandas_api = os.getenv("PANDAS_API_KEY")
        # if its empty then raise error
        if not pandas_api:
            raise ValueError("Pandas API key is missing.")
        pai.api_key.set(pandas_api) # Set api key

        df = pai.read_csv(self.dataframe_path) # read DataFrame
        
        # Generate response
        try:
            response = df.chat(
                self.query
            )   
        except Exception as e:
            response = str(e)

        return response

    
