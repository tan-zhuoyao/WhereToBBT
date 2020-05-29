from math import sin, cos, sqrt, atan2, radians

def getDistance(lat1, lon1, lat2, lon2):    
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


# ownLat, ownLon: Lat and Lon values obtained from Telegram
# df: BBTLocation(Geocoded).csv

# return a list of addresses of top k closest stores around
def getTopKClosest(ownLat, ownLon, df, k_closest):
    output_dict = {}
    dist_lst = []
    for index, row in df.iterrows():
        lat1 = row['lat']
        lon1 = row['lon']
        distance = getDistance(lat1, lon1, ownLat, ownLon)
        dist_lst.append(distance)
        
        output_dict[str(distance)] = row['Brand']  + ' that is ' + str("%.2f" % distance) + 'km away, at ' + row['Address']   
    
    dist_lst.sort()
    output = []
    for i in range(k_closest):
        output.append(output_dict[str(dist_lst[i])])
    return output