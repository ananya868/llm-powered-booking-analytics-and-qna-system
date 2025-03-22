# Required Libraries 
import pandas as pd 
import numpy as np


def pre_process_data(dataframe: pd.DataFrame, save_dir: str = None) -> pd.DataFrame:
    """
    Function to pre-process the data before performing any analytics on it.

    Args:
        dataframe (pd.DataFrame): The dataframe to pre-process.
        save_dir (str): The directory to save the pre-processed data.

    Returns:
        pd.DataFrame: The pre-processed dataframe.
    """
    data = dataframe.copy() 

    ## Data Pre-Processing 
    # Handling Missing Values
    if 'children' in data.columns:
        data['children'] = data['children'].fillna(0) # Since, a missing value indicate there were no children checking-in 
    if 'country' in data.columns: 
        data['country'] = data['country'].fillna(data['country'].mode()[0]) # Considering the mode of the country column to fill the missing values
    if 'agent' in data.columns:
        data['agent'] = data.groupby('market_segment')['agent'].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 0))
        # Since, agents are specific to certain market segments, we can fill the missing values with the mode of the agent column within the market segment
    if 'company' in data.columns:
        data = data.drop('company', axis=1) # Dropping the company column as it has more than 90% missing values

    # Check if all null values are dropped 
    if data.isnull().sum().sum() > 0: 
        raise ValueError("Missing Values are still present in the dataset")

    # Data Transformation
    if all(col in data.columns for col in ['arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month']):        
        data = data.rename(columns={'arrival_date_year': 'year', 'arrival_date_month': 'month', 'arrival_date_day_of_month': 'day'})
        # Combine to one column 
        data['month'] = pd.to_datetime(data['month'], format='%B').dt.month # Convert month to numeric value
        data['arrival_date'] = pd.to_datetime(data[['year', 'month', 'day']])
        data['is_holiday_season'] = data['month'].isin([12, 1, 7, 8])  # holiday trends in the data
    if 'arrival_date' in data.columns: 
        data['arrival_day_of_week'] = data['arrival_date'].dt.day_name() # Extracting the day of the week from the arrival date
    if 'arrival_date' in data.columns:
        data['is_weekend_arrival'] = data['arrival_date'].dt.weekday >= 5  # 5 = Saturday, 6 = Sunday

    # Save 
    if save_dir is not None:
        data.to_csv(save_dir, index=False)

    return data 
    
    
    

