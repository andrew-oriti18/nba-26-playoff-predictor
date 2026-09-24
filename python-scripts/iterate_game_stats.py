import csv

def iterate_game_stats_basic(filepath='game_stats.csv'):
    """
    Basic iteration through game_stats.csv - prints each row as a dictionary
    """
    print("=== Basic Iteration (each row as dict) ===")
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)  # Read all rows to know total count
        total_games = len(rows)

        for i, row in enumerate(rows[:5]):  # Show first 5 rows
            print(f"Game {i+1}: {row['Away']} @ {row['Home']} - {row['Away Score']}-{row['Home Score']}")
            print(f"  Combined Rosters: {len(row['Combined Rosters'].split(';')) if row['Combined Rosters'] else 0} players")

        if total_games > 5:
            print(f"... and {total_games - 5} more games")

def iterate_game_stats_with_parsing(filepath='game_stats.csv'):
    """
    Iteration with parsing of roster data into lists
    """
    print("\n=== Iteration with Parsed Rosters ===")
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        total_away_pts = 0
        total_home_pts = 0
        game_count = 0

        for row in reader:
            away_score = int(row['Away Score'])
            home_score = int(row['Home Score'])
            total_away_pts += away_score
            total_home_pts += home_score
            game_count += 1

            # Parse rosters - note: Combined Rosters contains BOTH teams' players
            all_players = row['Combined Rosters'].split(';') if row['Combined Rosters'] else []

            # Example: Show first 3 games details
            if game_count <= 3:
                print(f"Game {game_count}: {row['Away']} vs {row['Home']}")
                print(f"  Score: {away_score}-{home_score}")
                print(f"  Total players listed: {len(all_players)}")
                print(f"  First 5 players: {all_players[:5] if len(all_players) >= 5 else all_players}")

        print(f"\nAverages over {game_count} games:")
        print(f"  Away points per game: {total_away_pts/game_count:.1f}")
        print(f"  Home points per game: {total_home_pts/game_count:.1f}")

def iterate_game_stats_search(filepath='game_stats.csv', team_name=None):
    """
    Iteration to find games involving a specific team
    """
    print(f"\n=== Searching for games involving {team_name or 'Team'} ===")
    found_games = []

    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if team_name is None or row['Away'] == team_name or row['Home'] == team_name:
                found_games.append(row)
                if len(found_games) <= 5:  # Show first 5 matches
                    print(f"  {row['Away']} @ {row['Home']}: {row['Away Score']}-{row['Home Score']}")

        print(f"Found {len(found_games)} games")
        return found_games

def iterate_game_stats_aggregated(filepath='game_stats.csv'):
    """
    Iteration to compute aggregated statistics
    """
    print("\n=== Aggregated Statistics ===")
    team_stats = {}  # team -> {games_played, points_for, points_against}

    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            away_team = row['Away']
            home_team = row['Home']
            away_score = int(row['Away Score'])
            home_score = int(row['Home Score'])

            # Initialize teams if not seen before
            for team in [away_team, home_team]:
                if team not in team_stats:
                    team_stats[team] = {'games_played': 0, 'points_for': 0, 'points_against': 0}

            # Update stats
            team_stats[away_team]['games_played'] += 1
            team_stats[away_team]['points_for'] += away_score
            team_stats[away_team]['points_against'] += home_score

            team_stats[home_team]['games_played'] += 1
            team_stats[home_team]['points_for'] += home_score
            team_stats[home_team]['points_against'] += away_score

    # Calculate and display results
    print(f"{'Team':<20} {'Games':<6} {'PF':<6} {'PA':<6} {'Diff':<6}")
    print("-" * 50)
    for team, stats in team_stats.items():
        if stats['games_played'] > 0:
            avg_pf = stats['points_for'] / stats['games_played']
            avg_pa = stats['points_against'] / stats['games_played']
            diff = avg_pf - avg_pa
            print(f"{team:<20} {stats['games_played']:<6} {avg_pf:<6.1f} {avg_pa:<6.1f} {diff:<6.1f}")

def iterate_game_stats_with_rosters_split(filepath='game_stats.csv'):
    """
    Demonstrate how to work with the roster data since both teams are combined
    """
    print("\n=== Working with Combined Rosters ===")
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Process first few games to show roster structure
        for i, row in enumerate(reader):
            if i >= 3:  # Just first 3 games
                break

            print(f"\nGame {i+1}: {row['Away']} vs {row['Home']}")
            print(f"Score: {row['Away Score']}-{row['Home Score']}")

            if row['Combined Rosters']:
                players = row['Combined Rosters'].split(';')
                print(f"Total players from both teams: {len(players)}")
                print(f"Sample players: {players[:10]}")  # First 10 players

                # Note: To separate by team, you'd need additional logic or data
                # For now, we know it's combined data from both teams

if __name__ == "__main__":
    # Run all iteration examples
    iterate_game_stats_basic()
    iterate_game_stats_with_parsing()
    iterate_game_stats_search("Los Angeles Lakers")
    iterate_game_stats_search("New York Knicks")  # Team that might not exist in 2000 data
    iterate_game_stats_aggregated()
    iterate_game_stats_with_rosters_split()