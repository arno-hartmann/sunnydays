import boto3

dynamodb = boto3.resource('dynamodb')

def score_weather(weather_state_abbr):
    scoring = {
        "c" : 3,
        "lc": 1,
        "sn": -9,
        "sl" : -9,
        "h" : -9,
        "t" : -9,
        "hr" : -9,
        "lr" : -9,
        "s" : -9,
        "hc" : -9,
        }
    weather_score = scoring[weather_state_abbr]   
    return weather_score 


def modus(list):
    dict={}
    for item in list:
        if item in dict: 
            dict[item]+=1
        else: 
            dict[item]=1

    max = 0
    max_item = None
    for item in dict:
        if dict[item] > max:
            max = dict[item]
            max_item = item
    return max_item

def make_list_of_forecasts_one_day(city, min, max):
    table_sunny = dynamodb.Table('weather')
    response = table_sunny.query(

        KeyConditionExpression='city=:city AND #date between :min AND :max',

        ExpressionAttributeValues={
            ':city': city,
            ':min': min,
            ':max': max
                },
        ExpressionAttributeNames={
            '#date': 'date'
        }
        )['Items']
    weather_list = []

    for item in response:
        weather_list.append(item['weather_state_abbr'])
    return(weather_list)


def make_list_of_forecasts(city):
    forecastlist = []
    for x in range (1, 4):
        min = x*100
        max = min+100

        forecastlist.append(make_list_of_forecasts_one_day(city,min,max))
    return forecastlist


def weather_rating(city):
    days = make_list_of_forecasts(city)
    weather_indicator = []
    weather_score = 0

    for y in range (0, 3):
        weather_indicator.append(modus(days[y]))
        weather_score += score_weather(weather_indicator[y])
    return weather_score
   

def get_all_destinations_from_dynamodb():
    table_destination = dynamodb.Table('destination')
    response = table_destination.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table_destination.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items']) 

    return data

def write_scoring_to_dynamodb(city, city_id, scoring):
    table_destination = dynamodb.Table('destination')
    table_destination.update_item(
        Key={
            'city': city,
            'city_id': city_id,
        },
        UpdateExpression='SET weather_score = :val1',
        ExpressionAttributeValues={
            ':val1': scoring
        }
    )
