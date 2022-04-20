
def make_flight_url(origin, destination, departure, arrival):

    url = ("https://www.skyscanner.de/transport/fluge/"+ origin+"/"+ destination+"/"+departure+"/"+arrival+"/")
    print(url)
    return url





#make_flight_url("lond", "fra","220421","220424")
