import boto3

dynamodb = boto3.resource('dynamodb')


table_destination = dynamodb.Table('destination')

cities = [
    {'city': 'London', 'city_id': '44418', 'airport' : 'LOND'}, 
    {'city': 'Athen', 'city_id': '946738', 'airport' : 'ATH'}, 
    {'city': 'Lissabon', 'city_id': '742676', 'airport' : 'LIS'},
    {'city': 'Barcelona', 'city_id': '753692', 'airport' : 'BCN'},
    {'city': 'Marseille', 'city_id': '610264', 'airport' : 'MRS'},
    {'city': 'Windhoek', 'city_id': '1466719', 'airport' : 'WDH'}
    ]

for item in cities:
    dict = {
        'city' : item['city'],
        'city_id' : item['city_id'],
        'airport' : item['airport']
    }
    table_destination.put_item(Item=dict)