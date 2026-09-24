import csv

def get_player_stats(player_name, team_name, year):
    """
    Parse through nbaroster.csv and get all stats for a given person, team, and year.

    Args:
        player_name (str): Name of the player to search for
        team_name (str): Name of the team to search for
        year (int or str): Season year to search for

    Returns:
        dict or list of dicts: Player stats if found, None if not found
        Returns a list if multiple matches found, single dict if one match
    """
    matches = []

    with open('nbaroster.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check if all three conditions match
            if (row['Player'] == player_name and
                row['Team'] == team_name and
                row['Season'] == str(year)):
                matches.append(row)

    if not matches:
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        return matches

def get_player_stats_list(player_name, team_name, year):
    """
    Alternative version that always returns a list of matching player stats.

    Args:
        player_name (str): Name of the player to search for
        team_name (str): Name of the team to search for
        year (int or str): Season year to search for

    Returns:
        list: List of dictionaries containing player stats (empty if none found)
    """
    matches = []

    with open('nbaroster.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check if all three conditions match
            if (row['Player'] == player_name and
                row['Team'] == team_name and
                row['Season'] == str(year)):
                matches.append(row)

    return matches

# Example usage:
if __name__ == "__main__":
    # Example: Get stats for Michael Jordan with Chicago Bulls in 1996
    stats = get_player_stats("Michael Jordan", "Chicago Bulls", 1996)
    if stats:
        print(f"Found stats for {stats['Player']}:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    else:
        print("Player not found")

    # Or get all matches as a list
    all_matches = get_player_stats_list("Michael Jordan", "Chicago Bulls", 1996)
    print(f"\nFound {len(all_matches)} match(es)")
    for i, match in enumerate(all_matches):
        print(f"Match {i+1}: {match['Player']} - {match['Team']} {match['Season']}")