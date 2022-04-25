import get_flight_url_utils 

def lambda_handler(event, context):  
    get_flight_url_utils.get_sunny_destinations(3)