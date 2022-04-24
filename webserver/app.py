from flask import Flask, render_template, request
import boto3

dynamodb = boto3.resource('dynamodb')

app = Flask(__name__)

@app.route('/')
def index():
    table_destination = dynamodb.Table('destination')
    response = table_destination.scan()
    data = response['Items']

    return render_template('index.html', data=data)

app.run(host="0.0.0.0", port=80)