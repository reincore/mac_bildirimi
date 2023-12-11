import requests
from datetime import datetime
import os

def trigger_ifttt_webhook(event, home_team, away_team, venue_name):
    url = f"https://maker.ifttt.com/trigger/{event}/with/key/{os.environ['IFTTT_API_KEY']}"
    payload = {"value1": home_team, "value2": away_team, "value3": venue_name}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 200

def check_games_for_team(fixtures, team_info):
    team_id, team_name, venue_name = team_info
    for fixture in fixtures:
        if fixture['HomeTeamId'] == team_id:
            home_team = fixture.get('HomeTeamName', 'Unknown Home Team')
            away_team = fixture.get('AwayTeamName', 'Unknown Away Team')

            if trigger_ifttt_webhook("mac_bildirimi", home_team, away_team, venue_name):
                print(f"IFTTT Webhook triggered successfully for the game between {home_team} and {away_team} at {venue_name}.")
            else:
                print(f"Failed to trigger IFTTT Webhook for {team_name}.")
            return
    print(f"No home game today for {team_name}.")

def get_todays_games():
    date = datetime.now().strftime('%Y-%m-%d')  # For testing: '2023-12-17'
    url = f"https://api.sportsdata.io/v3/soccer/scores/json/GamesByDate/{date}"
    headers = {"Ocp-Apim-Subscription-Key": os.environ['SPORTSDATA_IO_API_KEY']}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.text}")
        return None

def main():
    # Team ID, Name, and Venue mapping
    teams = {
        572: ("Fenerbahçe", "Fenerhabçe Şükrü Saraçoğlu Stadyumu"),
        728: ("Beşiktaş", "Beşiktaş İnönü Stadyumu")
    }

    fixtures = get_todays_games()
    if fixtures:
        for team_id, team_data in teams.items():
            team_name, venue_name = team_data
            check_games_for_team(fixtures, (team_id, team_name, venue_name))
    else:
        print("No fixtures data available.")

if __name__ == "__main__":
    main()
