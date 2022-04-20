import weather_rating_utils 

cities = []
cities = weather_rating_utils.get_all_destinations_from_dynamodb()


for item in cities:
    city_weather_rating = weather_rating_utils.weather_rating(item['city'])
    weather_rating_utils.write_scoring_to_dynamodb(item['city'],item['city_id'], city_weather_rating)
