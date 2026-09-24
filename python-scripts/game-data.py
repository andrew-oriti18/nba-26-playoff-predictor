import pandas as pd
import csv
import time
import re
import ast
import player_stats

def getGames():
    months = ['november','december', 'january', 'february', 'march']
    with open('game_history.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        url_base = 'https://www.basketball-reference.com/leagues/NBA_2026_games-'
        for i in range(0, 5):
            url = url_base + months[i] + '.html'
            df = pd.read_html(url)
            print(df[0])
            for ind, row in df[0].iterrows():
                data = []
                day = row['Date']
                away_score = row['PTS']
                away_team = row['Visitor/Neutral']
                home_score = row.iloc[5]
                home_team = row['Home/Neutral']
                data = [day, away_team, away_score, home_team, home_score]
                writer.writerow(data)

def getStats():
    season = 2026
    # Load roster data into memory first
    with open('nbaroster.csv', mode='r', newline='',encoding='utf-8') as roster:
        roster_reader = csv.reader(roster)
        roster_data = list(roster_reader)  # Read all roster data at once

    with open('game_history.csv', mode='r', newline='') as file:
        with open('game_stats.csv', mode='w', newline='', encoding='utf-8') as file2:
            reader = csv.reader(file)
            writer = csv.writer(file2)
            # Write header
            writer.writerow(['Season', 'Away', 'Home', 'Away Score', 'Home Score', 'Away Rosters', 'Home Rosters'])

            for row in reader:
                if row[0] != "Playoffs":
                    away = row[1]
                    home = row[3]
                    away_points = row[2]
                    home_points = row[4]
                    away_roster = []
                    home_roster = []

                    # Check each player in roster data
                    for team in roster_data:
                        # Skip header row and check season/team match
                        if len(team) >= 2 and team[0] != 'Season':  # Skip header
                            if team[0] == str(season) and team[1] == away:
                                away_roster.append(team[2])
                            if team[0] == str(season) and team[1] == home:
                                home_roster.append(team[2])

                    # Write game data with rosters
                    writer.writerow([season, away, home, away_points, home_points,
                                ';'.join(away_roster), ';'.join(home_roster)])

    print("Game stats written to game_stats.csv")

def gameData():
    #test = player_stats.get_player_stats('Kobe Bryant', 'Los Angeles Lakers', 2000)
    with open('team_stats.csv', mode='r', newline='', encoding='utf-8') as file3:
        with open('game_stats.csv', mode='r', newline='', encoding='utf-8') as file:
            with open('training_data.csv', mode='a', newline='', encoding='utf-8') as file2:
                header = ['Away Score', 'Away3P', 'Away3PA', 'Away2P', 'Away2PA', 'AwayFT', 'AwayFTA', 'AwayORB', 'AwayDRB', 'AwayAST', 'AwaySTL', 'AwayBLK', 'AwayTOV', 'AwayPF', 'AwayPTS', 'AwayOFE', 'AwayDFE','AwayPace','Away2P','Away0-3','Away3-10','Away10-16','Away16-3P','Away3P',
                        'Home Score', 'Home3P', 'Home3PA', 'Home2P', 'Home2PA', 'HomeFT', 'HomeFTA', 'HomeORB', 'HomeDRB', 'HomeAST', 'HomeSTL', 'HomeBLK', 'HomeTOV', 'HomePF', 'HomePTS', 'HomeOFE', 'HomeDFE','HomePace','Home2P','Home0-3','Home3-10','Home10-16','Home16-3P','Home3P',]

                season = 2026
                writer = csv.writer(file2)
                #writer.writerow(header)
                reader = csv.DictReader(file)
                reader2 = list(csv.DictReader(file3))
                current_game = list()
                tracker = 1
                for row in reader:
                    team = row['Away']
                    roster = row['Away Rosters'].split(';')
                    roster_stats = [0.0] * 16
                    team_stats = [0.0] * 7
                    points = row['Away Score']
                    current_game.append(float(points))
                    for player in roster:
                        #'MP', '3P', '3PA', '2P', '2PA', 'FT', 'FTA','ORB', 'DRB',
                        #  'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'OFE', 'DFE'
                        year = row['Season']   
                        team = row['Away']
                        stats = player_stats.get_player_stats(player, team, year)
                        minutes = stats['MP']
                        i = 0
                        for key, value in stats.items():
                            if i > 4:
                                roster_stats[i - 5] += (float(value) * float(minutes))
                            i += 1

                    for row2 in reader2:
                        if(row2['Season'] == str(season) and row2['Team'] == team):
                            team_stats = [float(row2['Pace']),float(row2['2P']),float(row2['0-3']),float(row2['3-10']),float(row2['10-16']),float(row2['16-3P']),float(row2['3P'])]

                    current_game += roster_stats
                    current_game += team_stats

                    #get home stats 
                    team = row['Home']
                    roster = row['Home Rosters'].split(';')
                    points = row['Home Score']
                    current_game.append(float(points))
                    roster_stats = [0.0] * 16
                    team_stats = [0.0] * 7
                    for player in roster:
                        year = row['Season']   
                        team = row['Home']
                        stats = player_stats.get_player_stats(player, team, year)
                        minutes = stats['MP']
                        i = 0
                        for key, value in stats.items():
                            if i > 4:
                                roster_stats[i - 5] += (float(value) * float(minutes))
                            i += 1
                            
                    for row2 in reader2:
                        if(row2['Season'] == str(season) and row2['Team'] == team):
                            team_stats = [float(row2['Pace']),float(row2['2P']),float(row2['0-3']),float(row2['3-10']),float(row2['10-16']),float(row2['16-3P']),float(row2['3P'])]

                    current_game += roster_stats
                    current_game += team_stats

                    print(current_game)
                    print(f'{tracker}')
                    writer.writerow(current_game)
                    current_game = []
                    tracker += 1
    print("Written data to training_data")



def testin():
    with open('game_stats.csv', mode='r',encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row['Away Rosters'])

#testin()
getGames()
getStats()
gameData()