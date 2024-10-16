import requests

token = 'google maps api token'
center_coordinate = ("51.128151", "71.430398")

path_to_df = 'path_where you save you dataframe'

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


