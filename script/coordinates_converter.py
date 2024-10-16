import math
center_coordinate = ("51.128151", "71.430398")


def haversine_distance( coord2):
    R = 6371.0
    
    lat1, lon1 = center_coordinate
    lat2, lon2 = coord2
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return round(distance, 2)



def dms_to_decimal(dms_str):
    dms_str = dms_str.replace('°', ' ').replace("'", ' ').replace('"', ' ')
    dms_list = dms_str.split()
    
    if len(dms_list) < 4:
        raise ValueError("DMS string is not properly formatted")
    
    degrees = float(dms_list[0])
    minutes = float(dms_list[1])
    seconds = float(dms_list[2])
    direction = dms_list[3]
    
    decimal_degrees = degrees + minutes / 60 + seconds / 3600
    
    if direction in ['S', 'W']:
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def convert_coords_to_decimal(coords):

    if ',' in coords:
        lat_str, lon_str = coords.split(',')
        return float(lat_str.strip()), float(lon_str.strip())
    
    lat_str, lon_str = coords.split() 
    lat_decimal = dms_to_decimal(lat_str)
    lon_decimal = dms_to_decimal(lon_str)
    
    return lat_decimal, lon_decimal



