from weather_rating_utils import get_all_destinations_from_dynamodb 
from weather_rating_utils import write_scoring_to_dynamodb
from weather_rating_utils import weather_rating


def weather_rating_to_dynamo():
    cities = get_all_destinations_from_dynamodb()

    for item in cities:
        city_weather_rating = weather_rating(item['city'])
        write_scoring_to_dynamodb(item['city'],item['city_id'], city_weather_rating)
