# Fantasy Football Trade Evaluator

A Python script to help fantasy football managers evaluate trades by analyzing player projections, past performance, bye weeks, and injury risks. The tool provides trade value comparisons and roster feedback to optimize team composition.

## Features
- Evaluates trades based on:
  - Projected fantasy points for the current season.
  - Previous season's fantasy points.
  - Bye week scheduling.
  - User-defined injury risk (1-10 scale).
- Tracks roster composition and compares it to an ideal roster (e.g., 2 QBs, 4 RBs).
- Provides feedback on roster balance after a trade.
- Supports all positions: QB, RB, WR, TE, K, DST.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
Install Dependencies: Ensure you have Python 3.6+ installed. Install the required library:
bash

Copy
pip install pandas
Set Up Data Files: Download the required CSV files (see ) and place them in the same directory as the script.
Usage
Run the script:
bash

Copy
python trade_evaluator.py
Follow the prompts:
Enter the current week (1-17).
Input the number of players you currently have for each position (QB, RB, WR, TE, K, DST).
Enter the players you're trading for (up to 5), including their full names and injury risk (1-10).
Enter the players you're trading away, with the same details.
View the output:
The script calculates the trade value for both sides.
It provides roster feedback, highlighting over- or under-stocked positions.
A recommendation is given based on whether the trade is beneficial.
Example:

text

Copy
Enter the current week (1-17): 5
How many QB players do you currently have? 2
...
Enter the players you are trading for:
How many players do you want to input? (Max 5) 2
Enter player's full name (First Last): Patrick Mahomes
How likely do you think Patrick Mahomes will get injured? (1-10): 3
...
Value of players you're getting: 325.6
Value of players you're giving away: 280.4
Based off of projected points for this year, points scored last year, bye weeks, and injury risk this trade may be beneficial for you!
Data Requirements
The script requires two sets of CSV files from FantasyPros:

Projection Files (season-long fantasy point projections):
FantasyPros_Fantasy_Football_Projections_QB.csv
FantasyPros_Fantasy_Football_Projections_RB.csv
FantasyPros_Fantasy_Football_Projections_WR.csv
FantasyPros_Fantasy_Football_Projections_TE.csv
FantasyPros_Fantasy_Football_Projections_K.csv
FantasyPros_Fantasy_Football_Projections_DST.csv
Statistics Files (previous season's performance):
FantasyPros_Fantasy_Football_Statistics_QB.csv
FantasyPros_Fantasy_Football_Statistics_RB.csv
FantasyPros_Fantasy_Football_Statistics_WR.csv
FantasyPros_Fantasy_Football_Statistics_TE.csv
FantasyPros_Fantasy_Football_Statistics_K.csv
FantasyPros_Fantasy_Football_Statistics_DST.csv
Notes:

Ensure the files are in the same directory as trade_evaluator.py.
The CSVs must include columns like Player, FPTS, and Team (for projections).
Download these files from FantasyPros or similar sources, ensuring they match the expected format.
