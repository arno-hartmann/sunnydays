import weather_rating_utils 

cities = []
cities = weather_rating_utils.get_all_destinations_from_dynamodb()

#print(cities)

#print(weather_rating('Windhoek'))

for item in cities:
    print(item['city'])
    x = weather_rating_utils.weather_rating(item['city'])
    print(x)
    weather_rating_utils.write_scoring_to_dynamodb(item['city'],item['city_id'], x)
