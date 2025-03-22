import pandas as pd 
import numpy as np 


def build_features_for_analytics(dataframe: pd.DataFrame)-> pd.DataFrame:
    """
    Function to build features from the dataset.

    Args:
        dataframe (pd.DataFrame): The dataframe to build features from.

    Returns:
        pd.DataFrame: The dataframe with the features added.
    """
    df = dataframe.copy()
    if 'arrival_date' in df.columns:
        df['arrival_day_of_week'] = df['arrival_date'].dt.day_name()
    if 'reservation_status_date' in df.columns:
        df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date']) # Convert to Datetime 
    # Revenue per booking 
    if 'total_nights' not in df.columns:
        df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
        df['revenue'] = df['adr'] * df['total_nights'] # Calculating the revenue generated from the booking
    # Room Mismatch
    if 'room_mismatch' not in df.columns:
        df['room_mismatch'] = df['reserved_room_type'] != df['assigned_room_type']
    return df
    

def build_features_for_rag(dataframe: pd.DataFrame, verbose: bool = False)-> pd.DataFrame:
    """
    Function to build features from the dataset.

    Args:
        dataframe (pd.DataFrame): The dataframe to build features from.
    
    Returns:
        pd.DataFrame: The dataframe with the features added.
    """
    df = dataframe.copy()

    ### We will build some features/columns as well as extract some global insights on the data 
    # common to multiple features which will be stored in a dictionary.

    global_metrics = {} # To store global metrics/insights


    ### ---- Revenue Trends ---- ###
    if verbose:
        print("Processing Revenue Trends...")
    df['total_revenue'] = df['adr'] * (df['adults'] + df['children'] + df['babies'])

    # Global metrics
    try:
        global_metrics['average_revenue_per_booking'] = df['total_revenue'].mean()  
        global_metrics['revenue_per_month'] = df.groupby(['year', 'month'])['total_revenue'].sum().reset_index() 
        global_metrics['revenue_per_market_segment'] = df.groupby('market_segment')['total_revenue'].sum().reset_index()
        global_metrics['revenue_per_meal_plan'] = df.groupby('meal')['total_revenue'].sum().reset_index()
    except Exception as e:
        print(f"Error: {e}")
    
    
    ### ---- Booking and Cancellations Trends ---- ###
    if verbose:
        print("Processing Booking and Cancellations Trends...")
    try: 
        global_metrics['cancellations_by_hotel'] = df.groupby('hotel')['is_canceled'].sum().reset_index()
        global_metrics['cancellations_by_country'] = df.groupby('country')['is_canceled'].sum().reset_index()
        global_metrics['cancellations_by_customer_type'] = df.groupby('customer_type')['is_canceled'].sum().reset_index()
        global_metrics['cancellations_by_season'] = df.groupby('is_holiday_season')['is_canceled'].sum().reset_index()
        global_metrics['overall_cancellation_rate'] = df['is_canceled'].mean()*100
    except Exception as e:
        print(f"Error: {e}")

    
    ### ---- Occupancy and Demand Trends ---- ###
    if verbose:
        print("Processing Occupancy and Demand Trends...")
    # Total stay duration per booking
    df['average_stay_duration'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']
    # Lead time classification (Short, Medium, Long)
    df['lead_time_bins'] = pd.cut(df['lead_time'], bins=[0, 30, 90, np.inf], labels=['Short', 'Medium', 'Long'])
    try:
        global_metrics['average_stay_duration'] = df['average_stay_duration'].mean()
        # Occupancy rate per hotel (aggregate)
        occupancy_rate_per_hotel = df.groupby('hotel')['is_canceled'].mean().reset_index()
        occupancy_rate_per_hotel['occupancy_rate'] = 1 - occupancy_rate_per_hotel['is_canceled']
        if 'is_canceled' in occupancy_rate_per_hotel.columns:
            occupancy_rate_per_hotel.drop(columns=['is_canceled'], inplace=True)
        global_metrics['occupancy_rate_per_hotel'] = occupancy_rate_per_hotel
        # Demand per market segment (total bookings per segment)
        demand_per_market_segment = df['market_segment'].value_counts().reset_index()
        demand_per_market_segment.columns = ['market_segment', 'booking_count']
        global_metrics['demand_per_market_segment'] = demand_per_market_segment
    except Exception as e:
        print(f"Error: {e}")
    

    ### ---- Customer and Demographic Features ---- ###
    if verbose: 
        print("Processing Customer and Demographic Features...")
    df['guests_per_booking'] = df['adults'] + df['children'] + df['babies']
    try: 
        global_metrics['percentage_families'] = (df[df['guests_per_booking'] > 2].shape[0] / df.shape[0]) * 100  
        global_metrics['percentage_repeated_guests'] = df['is_repeated_guest'].mean() * 100  
        global_metrics['special_requests_avg'] = df['total_of_special_requests'].mean()
    except Exception as e:
        print(f"Error: {e}")

    
    ### ---- Time Based Trends ---- ###
    if verbose:
        print("Processing Time Based Trends...")
    df['waiting_list_days'] = df['days_in_waiting_list'] 
    try:
        # Booking trend over time (total bookings per month)
        booking_trend_over_time = df.groupby(['year', 'month'])['hotel'].count().reset_index()
        booking_trend_over_time.columns = ['year', 'month', 'total_bookings']
        # Busiest weeks (total bookings per week number)
        busiest_weeks = df.groupby('arrival_date_week_number')['hotel'].count().reset_index()
        busiest_weeks.columns = ['week_number', 'total_bookings']
        # Effect of holiday season on bookings (total bookings during holiday vs. non-holiday)
        holiday_season_effect = df.groupby('is_holiday_season')['hotel'].count().reset_index()
        holiday_season_effect.columns = ['is_holiday_season', 'total_bookings']
        # Average waiting list days over time 
        waiting_list_trend = df.groupby(['year', 'month'])['days_in_waiting_list'].mean().reset_index()
        waiting_list_trend.columns = ['year', 'month', 'average_waiting_list_days']
        # Single global metric
        average_waiting_list_days = df['days_in_waiting_list'].mean() 

        # add to global metrics
        global_metrics['booking_trend_over_time'] = booking_trend_over_time
        global_metrics['busiest_weeks'] = busiest_weeks
        global_metrics['holiday_season_effect'] = holiday_season_effect
        global_metrics['waiting_list_trend'] = waiting_list_trend
        global_metrics['average_waiting_list_days'] = average_waiting_list_days
    except Exception as e:
        print(f"Error: {e}")


    return df, global_metrics
    





