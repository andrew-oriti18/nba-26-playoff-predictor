import pandas as pd
import csv
import time
import re
import ast

urlBase_league = 'https://www.basketball-reference.com/leagues/NBA_'
urlBase_teams = 'https://www.basketball-reference.com/teams/'
year = 2025
#league_list = pd.io.html.read_html(urlBase_league)
#teams = dframe_list[0]["Eastern Conference"]
def getTeams():
    with open('nbateams.csv', mode='w', newline='', encoding='utf-8') as file:
        league_writer = csv.writer(file)
        #create the header
        league_header = ['Season', 'Teams']
        league_writer.writerow(league_header)

        for year in range(2000,2027):
            url = urlBase_league + str(year) + '.html'

            dframe = pd.read_html(url)
            east = list(dframe[0]["Eastern Conference"])
            west = dframe[1]["Western Conference"]
            teams = list()
            for e in east:
                t = re.sub(r'\s*\(\d+\)\s*$', '', e)
                t = t.removesuffix('*')
                if 'Division' not in e:
                    teams.append(t)
            for w in west:
                t = re.sub(r'\s*\(\d+\)\s*$', '', w)
                t = t.removesuffix('*')
                if 'Division' not in w:
                    teams.append(t)
            data = [str(year), teams]
            league_writer.writerow(data)
            print(teams)
            time.sleep(2.5)

def getRoster():
    #Turns the abbreviations csv into a dictionary
    with open('nbateams-abbrs.csv', mode = 'r', newline='') as f:
        reader = csv.DictReader(f)
        teams_abbr = {row['Team']: row['Abbr'] for row in reader}

    #Gets the stats for each player in the league during specified seasons
    year = 2010
    with open('nbaroster.csv', mode='w', newline='', encoding='utf-8') as file:
        header = ['Season', 'Team', 'Player', 'Position', 'MP', '3P', '3PA', '2P', '2PA', 'FT', 'FTA',
         'ORB', 'DRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'OFE', 'DFE']
        df = pd.read_csv('nbateams.csv')
        writer = csv.writer(file)
        writer.writerow(header)
        for season in df.itertuples(index=False):
            if year < 2027:
                league = ast.literal_eval(season.Teams)
                print(f'Seasons - {season.Season}')
                for team in league:
                    print(team)
                    abbr = teams_abbr[team]
                    print(abbr)
                    url = urlBase_teams + abbr + '/' + str(year) + '.html'
                    print(url)
                    dframe = pd.read_html(url)
                    time.sleep(2.0)
                    team_data = [year, team]
                    table = dframe[1]
                    #table.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in table.columns]

                    for idx, row in table.iterrows():
                        if idx != 0:
                            if row['MP'] == 0:
                                minutes = 1
                            else:
                                minutes = row['MP']
                            stats_dat = [ row['Player'], row['Pos'], row['MP'], row['3P'], row['3PA'],
                             row['2P'], row['2PA'], row['FT'], row['FTA'], row['ORB'], row['DRB'],
                             row['AST'], row['STL'], row['BLK'], row['TOV'], row['PF'], row['PTS']]
                                
                            oE = ((3 * row['3P'] - row['3PA'] + 2 * row['2P'] - row['2PA'] + row['FT'] - 0.5 * row['FTA']
                             + 0.5 * row['ORB'] + 1.5 * row['AST'] - 1.5 * row['TOV'] + row['PTS']) * 4) / minutes
                            stats_dat.append(oE)

                            dE = ((row['DRB'] + 2 * row['BLK'] + 1.5  * row['STL'] - 1.25 * row['PF']) * 4) / minutes
                            stats_dat.append(dE)

                            if row.Player != 'Team Totals':
                                data = team_data + stats_dat
                                writer.writerow(data) 

                year += 1
            else:
                return

"""
with open("nbaroster.csv", mode='w', newline='', encoding='utf-8') as file:
    writer2 = csv.writer(file)
    # Write all rows at once
    header = ["Team", "Abr", "Season", "Roster"]
    writer2.writerow(header)
    for (abr, teamname) in NBA_TEAMS:
        url = urlBase + abr + "/" + str(year) + ".html"
        team_frame = pd.read_html(url)
        roster = list(team_frame[0]["Player"])
        data = [teamname, abr, year, roster]
        writer2.writerow(data)
        print(teamname + str(year))
        time.sleep(5)
"""

def testing():
    with open('nbateams-abbrs.csv', mode = 'r', newline='') as f:
       reader = csv.DictReader(f)
       teams_abbr = {row['Team']: row['Abbr'] for row in reader}
    
    df = pd.read_csv('nbateams.csv')
    teams = df.iloc[10]
    year = teams['Season']
    league = ast.literal_eval(teams['Teams'])
    print(league)
    for team in league:
        print(team)
        abbr = teams_abbr[team]
        print(abbr)
        url = urlBase_teams + abbr + '/' + str(year) + '.html'
        print(url)
        time.sleep(2)

def teamStats():
    year = 2016
    with open('team_stats.csv', mode='a', newline='', encoding='utf-8') as file:
        #header = ['Season', 'Team', 'Pace','2P','0-3','3-10','10-16','16-3P','3P']
        df = pd.read_csv('nbateams.csv')
        writer = csv.writer(file)
        #writer.writerow(header)
        while year < 2027:
            url = urlBase_league + str(year) + '.html'
            df = pd.read_html(url)
            stats = df[11]
            play = df[10]
            for idx, row in stats.iterrows():
                data = []
                season = year
                playstyle = play.iloc[idx]
                shooting = stats.iloc[idx]['FG% by Distance']
                name = stats.iloc[idx]['Unnamed: 1_level_0']['Team']
                new_name = re.sub(r'\s*\(\d+\)\s*$', '', name)
                new_name = new_name.removesuffix('*')
                if(name != 'League Average'):
                    shooting_stats = [shooting['2P'], shooting['0-3'], shooting['3-10'], shooting['10-16'],
                    shooting['16-3P'], shooting['3P']]
                    pace = playstyle['Unnamed: 13_level_0']['Pace']
                    data += [str(season), new_name, pace] + shooting_stats
                    print(data)
                    writer.writerow(data)
            year += 1
            time.sleep(2)

    

def test2():
    url = 'https://www.basketball-reference.com/leagues/NBA_2016.html'
    df = pd.read_html(url)
    stats = df[10].iloc[0]
    print(stats)
    print(stats['Pace'])
    #print(stats["FG% by Distance"])
    #print(df[10].iloc[0]['Unnamed: 1_level_0']['Team'])
    #print(stats['FG% by Distance']['2P'])

getRoster()
#testing()
#test2()