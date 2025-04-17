import pandas as pd
import re

class PlayerDatabase:
    csv_files = {
        "QB": "FantasyPros_Fantasy_Football_Projections_QB.csv",
        "RB": "FantasyPros_Fantasy_Football_Projections_RB.csv",
        "WR": "FantasyPros_Fantasy_Football_Projections_WR.csv",
        "TE": "FantasyPros_Fantasy_Football_Projections_TE.csv",
        "K": "FantasyPros_Fantasy_Football_Projections_K.csv",
        "DST": "FantasyPros_Fantasy_Football_Projections_DST.csv"
    }

    stats_files = {
        "QB": "FantasyPros_Fantasy_Football_Statistics_QB.csv",
        "RB": "FantasyPros_Fantasy_Football_Statistics_RB.csv",
        "WR": "FantasyPros_Fantasy_Football_Statistics_WR.csv",
        "TE": "FantasyPros_Fantasy_Football_Statistics_TE.csv",
        "K": "FantasyPros_Fantasy_Football_Statistics_K.csv",
        "DST": "FantasyPros_Fantasy_Football_Statistics_DST.csv"
    }

    def __init__(self, bye_weeks):
        dataframes = []
        stats_dataframes = []
        for pos, file_path in self.csv_files.items():
            df = pd.read_csv(file_path)
            df["Pos"] = pos 
            df["Bye Week"] = df["Team"].map(bye_weeks)  
            dataframes.append(df)

        for pos, file_path in self.stats_files.items():
            df = pd.read_csv(file_path)
            df["Pos"] = pos  
            df["Player"] = df["Player"].apply(self.clean_player_name)
            stats_dataframes.append(df)

        self.all_players_df = pd.concat(dataframes).reset_index(drop=True)
        self.stats_players_df = pd.concat(stats_dataframes).reset_index(drop=True)
    
    def clean_player_name(self, player_name):
        if isinstance(player_name, str):
            return re.sub(r'\s\([A-Z]+\)$', '', player_name)
        return player_name
    
    def get_player_data(self, player_name):
        result = self.all_players_df[self.all_players_df["Player"] == player_name]
        if result.empty:
            raise ValueError(f"Player '{player_name}' not found in projections.")
        return result.iloc[0]

    def get_player_stats(self, player_name):
        result = self.stats_players_df[self.stats_players_df["Player"] == player_name]
        if result.empty:
            raise ValueError(f"Player '{player_name}' not found in statistics.")
        return result.iloc[0]
    


class Roster:
    IDEAL_ROSTER = {
        "QB": 2,
        "RB": 4,
        "WR": 6,
        "TE": 1,
        "DST": 2,
        "K": 1
    }

    def __init__(self):
        self.players = {pos: 0 for pos in self.IDEAL_ROSTER}

    def adjust_for_trade(self, trading_for, trading_away, player_db):
        for player in trading_for:
            pos = player_db.get_player_data(player)["Pos"]
            self.players[pos] += 1
        for player in trading_away:
            pos = player_db.get_player_data(player)["Pos"]
            self.players[pos] -= 1

    def provide_feedback(self):
        print("\nNew Roster Configuration:")
        for pos, count in self.players.items():
            print(f"{pos}: {count}")
            if count > self.IDEAL_ROSTER[pos]:
                diff = count - self.IDEAL_ROSTER[pos]
                print(f"You will have {diff} more {pos} than ideal.")
            elif count < self.IDEAL_ROSTER[pos]:
                diff = self.IDEAL_ROSTER[pos] - count
                print(f"You will have {diff} less {pos} than ideal.")

class TradeEvaluator:
    def __init__(self, player_db, current_week):
        self.player_db = player_db
        self.current_week = current_week
        self.weights = {
            'points_scored_last_year': 0.8,
            'projected_points': 1.0,
            'bye_week': -15,
            'injury_risk': -50 
        }

    def evaluate_player(self, player_name, injury_risks):
        player_data = self.player_db.get_player_data(player_name)
        player_stats = self.player_db.get_player_stats(player_name)
        value = 0
        value += player_stats['FPTS'] * self.weights['points_scored_last_year']
        rookie_points_multiplier = 2.0 if player_stats['FPTS'] == 0 else 1.0
        value += player_data['FPTS'] * self.weights['projected_points'] * rookie_points_multiplier
        
        if self.current_week < player_data['Bye Week']:
            value += self.weights['bye_week']
        value += injury_risks.get(player_name, 0) * self.weights['injury_risk']
        return value

    def evaluate_trade(self, trading_for, trading_away, trading_for_risks, trading_away_risks):
        trade_for_value = sum([self.evaluate_player(player, trading_for_risks) for player in trading_for])
        trade_away_value = sum([self.evaluate_player(player, trading_away_risks) for player in trading_away])
        return trade_for_value, trade_away_value

def is_valid_player_name(name):
    pattern = r"^[A-Z][a-z]+( [A-Z][a-z]+)*$"
    return bool(re.match(pattern, name))

def get_injury_risk(player_name):
    while True:
        try:
            injury_likelihood = int(input(f"How likely do you think {player_name} will get injured? (1-10, where 10 means currently injured): "))
            if 1 <= injury_likelihood <= 10:
                return injury_likelihood
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")

def input_players(player_db):
    players = []
    injury_risks = {}
    
    while True:
        try:
            number_of_players = int(input("How many players do you want to input? (Max 5) "))
            if 1 <= number_of_players <= 5:
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

    for _ in range(number_of_players):
        while True:
            player_name = input("Enter player's full name (First Last): ").title()
            if player_name not in player_db.all_players_df["Player"].values:
                print(f"{player_name} not found in the database.")
                continue
            if is_valid_player_name(player_name):
                injury_likelihood = get_injury_risk(player_name)
                players.append(player_name)
                injury_risks[player_name] = injury_likelihood / 10 
                break
            else:
                print("Invalid player name format. Please use 'First Last' format.")

    return players, injury_risks

def main():
    bye_weeks2024 = {
        'DET': 5, 'LAC': 5, 'PHI': 5, 'TEN': 5,
        'KC': 6, 'LAR': 6, 'MIA': 6, 'MIN': 6,
        'CHI': 7, 'DAL': 7,
        'PIT': 9, 'SF': 9,
        'CLE': 10, 'GB': 10, 'LV': 10, 'SEA': 10,
        'ARI': 11, 'CAR': 11, 'NYG': 11, 'TB': 11,
        'ATL': 12, 'BUF': 12, 'CIN': 12, 'JAC': 12,
        'NO': 12, 'NYJ': 12,
        'BAL': 14, 'DEN': 14, 'HOU': 14, 'IND': 14,
        'NE': 14, 'WAS': 14
    }

    player_db = PlayerDatabase(bye_weeks2024)
    roster = Roster()
    while True:
        try:
            current_week = int(input("Enter the current week (1-17): "))
            if 1 <= current_week <= 17:
                break
            else:
                print("Invalid input. Please enter a week number between 1 and 17.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for the week.")
    evaluator = TradeEvaluator(player_db, current_week)

    for pos, count in roster.IDEAL_ROSTER.items():
        while True:
            try:
                count = int(input(f"How many {pos} players do you currently have? "))
                if count >= 0:
                    roster.players[pos] = count
                    break
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")

    print("\nEnter the players you are trading for:")
    trading_for, trading_for_risks = input_players(player_db)

    print("\nEnter the players you are trading away: ")
    trading_away, trading_away_risks = input_players(player_db)

    trade_for_value, trade_away_value = evaluator.evaluate_trade(trading_for, trading_away, trading_for_risks, trading_away_risks)

    roster.adjust_for_trade(trading_for, trading_away, player_db)
    roster.provide_feedback()

    print(f"\nValue of players you're getting: {trade_for_value}")
    print(f"Value of players you're giving away: {trade_away_value}")

    if trade_for_value > trade_away_value:
        print("Based off of projected points for this year, points scored last year, bye weeks, and injury risk this trade may be beneficial for you!")
    else:
        print("Based off of projected points for this year, points scored last year, bye weeks, and injury risk you may want to reconsider this trade.")

if __name__ == "__main__":
    main()