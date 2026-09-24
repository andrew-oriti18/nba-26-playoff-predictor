# NBA 2026 Playoff Predictor

## Purpose & Results
- The goal was to predict the winner and bracket of the 2026 NBA playoffs

- Succesfully predicted the New York Knicks to win the NBA 2026 Championship against the San Antonio Spurs

- Achieved a overeal 87% accuracy out of all series matchups. Need to improve the accuracy in determing the length of the series.

## Methodology
- Scraped the data using simple html scraping.
- Saved player data from each team, and some team statistics starting from the 2010 season all the way to the 2026 season.
- Also scraped the outcome of each game starting from the 2010 season through the 2026 season up to the playoffs.

- Combined all data into a single file where each entry contains the outcome of a game, the two teams who played, their team stats for that season, and combined player average stats for that season.

- Trained an XGBoost Regressor model using the dataset defined above to output the predicted score of a game between two teams.
- Used Monte Carlo Simulations to add randomness and determine which team would win in the series matchup in 2026.

## Improvements
- Want to add a player elo metric to include more statistics beyond just their box stats and also include their importance to the team.
- Hope to add some way to include injuries or news online to allow for better predicting.
- Improve the Monte Carlo simulations by changing the variance to be based on some team statistic rather than a flat rate for all teams.

- Want to automize the system to automatically predict the entire playoffs by simply giving the bracket rather than having to manual change the matchup for each series.