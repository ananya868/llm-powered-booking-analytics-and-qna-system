import io 
import base64 
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
from flask import Flask, request, jsonify


def build_analytics(dataframe: pd.DataFrame): 
    """
    Generate analytics plots from the given dataframe and return them as Base64 encoded strings.

    Args:
        dataframe (pd.DataFrame): The input dataframe containing the hotel booking data.

    Returns:
        dict: A dictionary containing the Base64 encoded strings of the generated plots.
    """
    df = dataframe.copy()

    ## Revenue Trends 
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])
    # Calculate Revenue per booking 
    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['revenue'] = df['adr'] * df['total_nights']
    revenue_trend = df.groupby(df['reservation_status_date'].dt.to_period('M'))['revenue'].sum()
    # Plot
    plt.figure(figsize=(12, 6))
    revenue_trend.plot(kind='line', marker='o', color='b')
    plt.title('Revenue Trends Over Time')
    plt.xlabel('Month-Year')
    plt.ylabel('Total Revenue')
    plt.grid(True)
    plt.xticks(rotation=45)
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot1 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Arrival Distribution by day of the week 
    plt.figure(figsize=(10, 5))
    sns.countplot(x=df['arrival_day_of_week'], order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], palette='viridis')
    plt.title('Arrival Distribution by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Arrivals')
    plt.xticks(rotation=45)
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot2 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Weekend vs Weekday Arrivals 
    plt.figure(figsize=(6, 4))
    sns.countplot(x=df['is_weekend_arrival'], palette='coolwarm')
    plt.xticks([0, 1], ['Weekday', 'Weekend'])
    plt.title('Weekend vs. Weekday Arrivals')
    plt.xlabel('Arrival Type')
    plt.ylabel('Number of Arrivals')
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot3 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Holiday vs Non-Holiday Season 
    plt.figure(figsize=(6, 4))
    sns.countplot(x=df['is_holiday_season'], palette='coolwarm')
    plt.xticks([0, 1], ['Non-Holiday', 'Holiday'])
    plt.title('Holiday Season vs. Non-Holiday Arrivals')
    plt.xlabel('Season Type')
    plt.ylabel('Number of Arrivals')
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot4 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Cancellation rate as percentage of total bookings 
    total_bookings = len(df)
    canceled_bookings = df['is_canceled'].sum()
    cancellation_rate = (canceled_bookings / total_bookings) * 100
    # plot these
    plt.figure(figsize=(6, 6))
    # Pie chart
    labels = ['Not Canceled', 'Canceled']
    sizes = [total_bookings - canceled_bookings, canceled_bookings]
    colors = ['skyblue', 'salmon']
    explode = (0, 0.1)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Title
    plt.title("Booking Cancellation Rate")
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot5 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Geographical Distribution of Bookings
    # Count of bookings per country
    country_bookings = df['country'].value_counts().head(10)  
    plt.figure(figsize=(12, 5))
    sns.barplot(x=country_bookings.index, y=country_bookings.values, palette='coolwarm')
    plt.title('Top 10 Countries Booking Hotels')
    plt.xlabel('Country')
    plt.ylabel('Number of Bookings')
    plt.xticks(rotation=45)
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot6 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Booking lead time distribution
    plt.figure(figsize=(12, 5))
    sns.histplot(df['lead_time'], bins=50, kde=True, color='purple')
    plt.title('Distribution of Booking Lead Time')
    plt.xlabel('Lead Time (Days)')
    plt.ylabel('Number of Bookings')
    plt.grid(True)
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot7 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Revenue by Distribution Channel
    channel_revenue = df.groupby('distribution_channel')['revenue'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=channel_revenue.index, y=channel_revenue.values, palette='Blues_r')
    plt.title('Revenue by Distribution Channel')
    plt.xlabel('Distribution Channel')
    plt.ylabel('Total Revenue')
    # save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot8 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Count of Reserved room types 
    room_counts = df['reserved_room_type'].value_counts()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=room_counts.index, y=room_counts.values, palette='magma')
    plt.title('Most Popular Reserved Room Types')
    plt.xlabel('Room Type')
    plt.ylabel('Number of Bookings')
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot9 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Special Requests vs Cancellation 
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=df['is_canceled'], y=df['total_of_special_requests'], palette='coolwarm')
    plt.title('Special Requests vs Cancellation')
    plt.xlabel('Is Canceled')
    plt.ylabel('Total Special Requests')
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot10 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Booking trends by month 
    plt.figure(figsize=(12, 5))
    sns.countplot(x=df['month'], order=[
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 
        'August', 'September', 'October', 'November', 'December'
    ], palette='viridis')
    plt.title('Monthly Hotel Booking Trends')
    plt.xlabel('Month')
    plt.ylabel('Number of Bookings')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # save plot to memory buffer 
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot11 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Cancellation Rate vs Lead time 
    plt.figure(figsize=(12, 5))
    sns.boxplot(x=df['is_canceled'], y=df['lead_time'], palette='coolwarm')

    plt.title('Cancellation Rate vs Lead Time')
    plt.xlabel('Canceled (1 = Yes, 0 = No)')
    plt.ylabel('Lead Time (Days)')
    plt.grid(True)
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot12 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Market Segment-wise Booking Distribution 
    plt.figure(figsize=(12, 5))
    sns.countplot(y=df['market_segment'], order=df['market_segment'].value_counts().index, palette='Set2')
    plt.title('Market Segment-wise Booking Distribution')
    plt.xlabel('Number of Bookings')
    plt.ylabel('Market Segment')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot13 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Cancelation Rate by Market Segment
    segment_cancellation = df.groupby('market_segment')['is_canceled'].mean() * 100
    plt.figure(figsize=(10, 5))
    sns.barplot(x=segment_cancellation.index, y=segment_cancellation.values, palette='Reds_r')
    plt.title('Cancellation Rate by Market Segment')
    plt.xlabel('Market Segment')
    plt.ylabel('Cancellation Rate (%)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot14 = base64.b64encode(img_buf.read()).decode("utf-8")

    ## Booking cancellation by Customer type 
    plt.figure(figsize=(10, 5))
    sns.countplot(x=df['customer_type'], hue=df['is_canceled'], palette='Set1')
    plt.title('Booking Cancellation by Customer Type')
    plt.xlabel('Customer Type')
    plt.ylabel('Number of Bookings')
    plt.legend(title="Canceled", labels=["No", "Yes"])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # Save plot to memory buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    img_buf.seek(0)
    # Encode image to Base64
    plot15 = base64.b64encode(img_buf.read()).decode("utf-8")

    
    return {
        "revenue_trends": plot1,
        "arrival_distribution": plot2,
        "weekend_vs_weekday": plot3,
        "holiday_vs_non_holiday": plot4,
        "cancellation_rate": plot5,
        "geographical_distribution": plot6,
        "booking_lead_time": plot7,
        "revenue_by_channel": plot8,
        "room_type_distribution": plot9,
        "special_requests_vs_cancellation": plot10,
        "booking_trends_by_month": plot11,
        "cancellation_rate_vs_lead_time": plot12,
        "market_segment_distribution": plot13,
        "cancellation_rate_by_segment": plot14,
        "cancellation_by_customer_type": plot15
    }
        


