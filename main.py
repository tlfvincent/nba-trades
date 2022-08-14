"""
Main

This is the main entrypoint to the application
"""
from src import extract_data

import pandas as pd

NBA_TEAMS = [
    "ATL", "BOS", "CHA", "CHI", "CLE",
    "DAL", "DEN", "DET", "GSW", "HOU",
    "IND", "LAC", "LAL", "MEM", "MIA",
    "MIL", "MIN", "NJN", "NOH", "NYK",
    "OKC", "ORL", "PHI", "PHO", "POR",
    "SAC", "SAS", "TOR", "UTA", "WAS"
]


def main():
    """
    This function executes the pipeline to extract historical trade data_data
    in the NBA.
    """
    nba_team_pairs = extract_data.get_nba_team_pairs(NBA_TEAMS)

    trade_info = extract_data.trader_crawler(nba_team_pairs)

    df = pd.DataFrame(
        trade_info,
        columns=["team1", "team2", "win_shares_sent", "win_shares_received", "trade_date"]
    )

    df.to_csv("trade_win_shares.csv", index=False)


if __name__ == "__main__":

    main()
