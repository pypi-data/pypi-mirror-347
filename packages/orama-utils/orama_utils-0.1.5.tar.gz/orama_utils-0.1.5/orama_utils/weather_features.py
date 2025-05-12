import os
import json
import pandas as pd
import urllib.request
import csv
import codecs
from datetime import datetime, timedelta
from typing import List, Optional
import pathlib

def add_weather_features(
    df: pd.DataFrame,
    api_key: str,
    features: Optional[List[str]] = None,
    weather_db_path: str = "weather_db"
) -> pd.DataFrame:
    """
    Add weather features to a dataframe based on date and location columns.
    
    Args:
        df (pd.DataFrame): Input dataframe with 'date' and 'location' columns
        api_key (str): Visual Crossing Weather API key (you can get it from https://www.visualcrossing.com/weather-api)
        features (List[str], optional): List of weather features to include. If None, includes all available features.
            Available features: ['datetime', 'tempmax', 'tempmin', 'temp', 'feelslike', 
                               'precip', 'snow', 'windspeed', 'cloudcover']
        weather_db_path (str): Path to store weather data files
    
    Returns:
        pd.DataFrame: Original dataframe with added weather features
    Raises:
        ValueError: If the input dataframe is missing required columns or the API key is invalid
        NotImplementedError: If historical weather data fetching is not implemented
    """
    # Validate input dataframe
    required_columns = ['date', 'location']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"DataFrame must contain columns: {required_columns}")
    
    # Create weather_db directory if it doesn't exist
    pathlib.Path(weather_db_path).mkdir(parents=True, exist_ok=True)
    
    # Initialize or load last_update.json
    last_update_path = os.path.join(weather_db_path, "last_update.json")
    if os.path.exists(last_update_path):
        with open(last_update_path, 'r') as f:
            last_update = json.load(f)
    else:
        last_update = {}
    
    # Get date range from dataframe
    min_date = df['date'].min()
    max_date = df['date'].max()
    
    # Check if we need historical data
    if min_date.date() < datetime.now().date():
        raise NotImplementedError("Historical weather data fetching not implemented yet")
    
    # Get unique locations
    locations = df['location'].unique()
    
    # Process each location
    for location in locations:
        location_file = os.path.join(weather_db_path, f"{location.lower().replace(', ', '_')}.csv")
        needs_update = False
        
        # Check if we need to update the CSV
        if location in last_update:
            # Check if we have a valid last update time for this location
            # If not, we need to update the weather data
            if location in last_update and last_update[location]:
                try:
                    last_update_time = datetime.strptime(last_update[location], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    # Invalid date format in the last_update record
                    needs_update = True
            else:
                # No last update record for this location
                needs_update = True
            if (datetime.now() - last_update_time).total_seconds() > 18000:  # 5 hours
                needs_update = True
        else:
            needs_update = True
        
        # Check if CSV exists and contains required date range
        if os.path.exists(location_file):
            weather_df = pd.read_csv(location_file)
            weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
            if not (weather_df['datetime'].min() <= min_date and 
                   weather_df['datetime'].max() >= max_date):
                needs_update = True
        else:
            needs_update = True
        
        # Update weather data if needed
        if needs_update:
            start = min_date.strftime("%Y-%m-%d")
            end = max_date.strftime("%Y-%m-%d")
            
            url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start}/{end}?unitGroup=metric&elements=datetime%2Ctempmax%2Ctempmin%2Ctemp%2Cfeelslike%2Cprecip%2Csnow%2Cwindspeed%2Ccloudcover&include=days&key={api_key}&contentType=csv"
            
            try:
                result_bytes = urllib.request.urlopen(url)
                csv_data = list(csv.reader(codecs.iterdecode(result_bytes, 'utf-8')))
                
                if not csv_data:
                    raise ValueError(f"No weather data received for location: {location}. Please check the location name or API key validity.")
                
                # Save new data
                new_data = pd.DataFrame(csv_data[1:], columns=csv_data[0])
                new_data.to_csv(location_file, index=False)
                
                # Update last_update.json
                last_update[location] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(last_update_path, 'w') as f:
                    json.dump(last_update, f, indent=4)
                    
            except Exception as e:
                raise ValueError(f"Error fetching weather data for {location}: {str(e)} at location_file: {location_file}")
    
    # Merge weather data with input dataframe
    result_df = df.copy()
    
    for location in locations:
        location_file = os.path.join(weather_db_path, f"{location.lower().replace(', ', '_')}.csv")
        if os.path.exists(location_file):
            weather_df = pd.read_csv(location_file)
            weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
            
            # Filter features if specified
            if features:
                available_features = ['datetime'] + features
                weather_df = weather_df[available_features]
            
            # Merge weather data for this location
            location_mask = result_df['location'] == location
            location_dates = result_df.loc[location_mask, 'date']
            
            for date in location_dates:
                weather_row = weather_df[weather_df['datetime'] == date]
                if not weather_row.empty:
                    for col in weather_df.columns:
                        if col != 'datetime':
                            result_df.loc[(result_df['location'] == location) & 
                                        (result_df['date'] == date), f'weather_{col}'] = weather_row[col].iloc[0]
        else:
            raise ValueError(f"Weather data file not found for location: {location}. Please check the location name or API key validity.")
    
    return result_df
