
def make_flight_url(origin, destination, departure, arrival):

    url = ("https://www.skyscanner.de/transport/fluge/"+ origin+"/"+ destination+"/"+departure+"/"+arrival+"/")
    print(url)
    return url
