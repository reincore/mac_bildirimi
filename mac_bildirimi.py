import requests
from datetime import datetime
import json
import os

def trigger_ifttt_webhook(event, value1, value2, value3):
    url = f"https://maker.ifttt.com/trigger/{event}/with/key/{os.environ['IFTTT_API_KEY']}"

    payload = {
        "value1": value1,
        "value2": value2,
        "value3": value3
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    return response.status_code == 200

def check_game(venue_id, date):
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?venue={venue_id}&date={date}"

    headers = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": os.environ['RAPID_API_KEY']
    }

    response = requests.request("GET", url, headers=headers)

    fixtures = response.json()
    print("Fixtures: ", fixtures)

    if fixtures['results']:
        fixture = fixtures['response'][0]
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        venue_name = fixture['fixture']['venue']['name']


        if trigger_ifttt_webhook("mac_bildirimi", home_team, away_team, venue_name):
            print(f"IFTTT Webhook triggered successfully for the game between {home_team} and {away_team} at {venue_name}!")
        else:
            print("Failed to trigger IFTTT Webhook.")
    else:
        print("No game today.")

fenerbahce_venue_id = 1581
besiktas_venue_id = 20301
date = datetime.now().strftime('%Y-%m-%d')


check_game(fenerbahce_venue_id, date)
check_game(besiktas_venue_id, date)