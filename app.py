from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def display_standings():
    # API URL
    url = "https://api-web.nhle.com/v1/standings/now"

    # Send an HTTP GET request to the API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Extract the relevant data from the response
        standings = data.get('standings', [])
        
        # Create a nested dictionary to group the teams by conference and division
        team_data = {}
        
        for team in standings:
            conference_name = team.get('conferenceName', 'N/A')
            division_name = team.get('divisionName', 'N/A')
            team_name = team.get('teamName', {}).get('default', 'N/A')
            games_played = team.get('gamesPlayed', 'N/A')
            wins = team.get('wins', 'N/A')
            losses = team.get('losses', 'N/A')
            ot_losses = team.get('otLosses', 'N/A')
            points = team.get('points', 'N/A')
            point_percentage = round(team.get('points')/(team.get('gamesPlayed')*2),3)
            win_percentage = round(team.get('winPctg'),3)
            pythag = round((team.get('goalFor')**2.19)/((team.get('goalFor')**2.19)+(team.get('goalAgainst')**2.19)),3)
            xP = round((team.get('gamesPlayed')*2)*pythag,2)
            xW = round(team.get('gamesPlayed')*pythag,2)
            xvrP = round(team.get('points') - xP,2)
            xvrW = round(team.get('wins') - xW,2)
            pace = int(point_percentage*164)
            xTP = int(pythag*164)
            
            if conference_name not in team_data:
                team_data[conference_name] = {}
            
            if division_name not in team_data[conference_name]:
                team_data[conference_name][division_name] = []
            
            team_data[conference_name][division_name].append({
                'Team Name': team_name,
                'Games Played': games_played,
                'Wins': wins,
                'Losses': losses,
                'OT Losses': ot_losses,
                'Points': points,
                'Points Percentage': point_percentage,
                'Win Percentage': win_percentage,
                'Pythag': pythag,
                'xP': xP,
                'xW': xW,
                'xvrP': '+' + str(xvrP) if xvrP > 0 else str(xvrP),
                'xvrW': '+' + str(xvrW) if xvrW > 0 else str(xvrW),
                'Pace': pace,
                'xTP': xTP
            })

        return render_template('nhl_standings.html', team_data=team_data)
    else:
        return f"Failed to fetch data. Status code: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=False)
