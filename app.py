import requests
import pandas as pd
from flask import Flask, render_template
import numpy as np

app = Flask(__name__)

# Function to fetch and process NHL standings data
def fetch_and_process_standings():
    # Send a GET request to the NHL standings API
    url = 'https://statsapi.web.nhl.com/api/v1/standings'
    response = requests.get(url)
    data = response.json()

    # Extract the relevant data for each division
    divisions = data['records']

    division_data = {}

    xvrP_values = []
    xvrW_values = []

    for division in divisions:
        division_name = division['division']['name']

        table_data = []

        for team in division['teamRecords']:
            xvrP = round(team['points'] - ((team['gamesPlayed']) * 2) * (team['goalsScored'] ** 2.19) / ((team['goalsScored'] ** 2.19) + (team['goalsAgainst'] ** 2.19)), 2)
            xvrW = round(team['leagueRecord']['wins'] - (team['gamesPlayed']) * (team['goalsScored'] ** 2.19) / ((team['goalsScored'] ** 2.19) + (team['goalsAgainst'] ** 2.19)), 2)
            xvrP_values.append(xvrP)
            xvrW_values.append(xvrW)

            team_info = {
                'Name': team['team']['name'],
                'Games Played': team['gamesPlayed'],
                'Wins': team['leagueRecord']['wins'],
                'Losses': team['leagueRecord']['losses'],
                'Overtime': team['leagueRecord']['ot'],
                'Points': team['points'],
                'Point Percentage': round(team['points'] / ((team['leagueRecord']['wins'] + team['leagueRecord']['losses'] + team['leagueRecord']['ot']) * 2), 3),
                'Win Percentage': round(team['leagueRecord']['wins'] / (team['leagueRecord']['wins'] + team['leagueRecord']['losses'] + team['leagueRecord']['ot']), 3),
                'Pythag': round((team['goalsScored'] ** 2.19) / ((team['goalsScored'] ** 2.19) + (team['goalsAgainst'] ** 2.19)), 3),
                'xP': round(((team['gamesPlayed']) * 2) * (team['goalsScored'] ** 2.19) / ((team['goalsScored'] ** 2.19) + (team['goalsAgainst'] ** 2.19)), 2),
                'xW': round((team['gamesPlayed']) * (team['goalsScored'] ** 2.19) / ((team['goalsScored'] ** 2.19) + (team['goalsAgainst'] ** 2.19)), 2),
                'xvrP': '+' + str(xvrP) if xvrP > 0 else str(xvrP),
                'xvrW': '+' + str(xvrW) if xvrW > 0 else str(xvrW),
                'Pace': int(164*(team['points'] / ((team['leagueRecord']['wins'] + team['leagueRecord']['losses'] + team['leagueRecord']['ot']) * 2))),
                'xTP': int(164*(team['goalsScored'] ** 2.19) / ((team['goalsScored'] ** 2.19) + (team['goalsAgainst'] ** 2.19)))
            }
            table_data.append(team_info)

        division_df = pd.DataFrame(table_data)
        # Set index=False to remove the index column
        division_data[division_name] = division_df.to_html(classes='table table-striped', escape=False, index=False)

    max_xvrP = max(xvrP_values)
    min_xvrP = min(xvrP_values)
    max_xvrW = max(xvrW_values)
    min_xvrW = min(xvrW_values)

    return division_data, max_xvrP, min_xvrP, max_xvrW, min_xvrW

# Route to display NHL standings
@app.route('/')
def display_standings():
    division_data, max_xvrP, min_xvrP, max_xvrW, min_xvrW = fetch_and_process_standings()
    return render_template('nhl_standings.html', division_data=division_data, max_value=max(max_xvrP, max_xvrW), min_value=min(min_xvrP, min_xvrW))

if __name__ == '__main__':
    app.run(debug=False)
