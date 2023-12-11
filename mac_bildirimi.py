import requests
from datetime import datetime
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

def check_games_for_team(fixtures, team_id):
    for fixture in fixtures:
        if fixture['HomeTeamId'] == team_id:
            home_team = fixture['HomeTeamName']
            away_team = fixture['AwayTeamName']
            venue_name = fixture['VenueName']

            if trigger_ifttt_webhook("mac_bildirimi", home_team, away_team, venue_name):
                print(f"IFTTT Webhook triggered successfully for the game between {home_team} and {away_team} at {venue_name}!")
            else:
                print("Failed to trigger IFTTT Webhook.")
            return
    print(f"No home game today for team ID {team_id}.")

def get_todays_games():
    date = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.sportsdata.io/v3/soccer/scores/json/GamesByDate/{date}"
    headers = {
        "Ocp-Apim-Subscription-Key": os.environ['SPORTSDATA_IO_API_KEY']
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Log the fixture data
        print(f"Fixture obtained: {response.json()}")
        return response.json()
    else:
        print(f"Error fetching data: {response.text}")
        return None  # Or appropriate error handling

# Main execution
fixtures = get_todays_games()

fenerbahce_id = 572  # SportsData.io ID for Fenerbahçe
besiktas_id = 728    # SportsData.io ID for Beşiktaş

check_games_for_team(fixtures, fenerbahce_id)
check_games_for_team(fixtures, besiktas_id)
