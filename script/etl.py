import pandas as pd
import constants
import coordinates_converter as cc
import requests
import random
from datetime import datetime, timedelta

def extract(path=constants.path_to_df):
    df = pd.read_csv(path)
    return df


def get_coordinates(address, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Geocoding error: {data['status']}")
            return None
    else:
        print(f"HTTP error: {response.status_code}")
        return None

def generate_random_dates(start_date, end_date, num_dates):
    def random_date(start, end):
        delta = end - start
        random_days = random.randint(0, delta.days)
        return start + timedelta(days=random_days)
    
    return [random_date(start_date, end_date).strftime('%Y-%m-%d') for _ in range(num_dates)]




def transform(df):
    #get_coordinates
    df['coordinates'] = [get_coordinates(address, token) for address in df['address']]
    df['coordinates'] = df['coordinates'].apply(lambda x: (51.1256348, 71.5114112) if pd.isna(x) else x)
    #calculating km_to_center
    df['km_to_center'] = [haversine_distance(i) for i in df['coordinates'] ]
    #clean_data, transform, feature engineering
    df['gen_area'] = [str(df.iloc[i]['gen_area'])[:2] for i in range(200)]
    df.gen_area.replace('na',30, inplace=True)
    df['gen_area'] = df['gen_area'].astype('int64')
    df['gen_area'] = [int(i) + 20 if i < 20 else i for i in df['gen_area']]
    df['live_area']=[i*0.2 for i in df['gen_area']]
    df['stage'] = [random.randint(1, 25) for _ in range(200)]
    df.WC=[random.randint(1, 3) for _ in range(200)]
    df.kitchen_studio = [random.randint(0, 1) for _ in range(200)]
    df.kitchen_studio = list(map(lambda x: True if x == 1 else False, df.kitchen_studio))
    df.date_arenda = generate_random_dates(datetime(2024, 1, 1), datetime(2024, 12, 31), 200)
    df['tg_for_m'] = round(df['price'] / df['gen_area'])
    df['sootn_area'] = df['gen_area'].astype(str) + "/" + round(df['live_area']).astype(int).astype(str)
    
    return df

df = pd.read_csv(r'C:\Users\arlan\Desktop\Programming BIG DATA\assignment 2\data\data_new.csv')
