"""
Main

This is the main entrypoint to the application
"""

import logging
import sys

import pandas as pd

from src import extract_data

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# NBA_TEAMS = [
#     "ATL", "BOS", "CHA", "CHI", "CLE",
#     "DAL", "DEN", "DET", "GSW", "HOU",
#     "IND", "LAC", "LAL", "MEM", "MIA",
#     "MIL", "MIN", "NJN", "NOH", "NYK",
#     "OKC", "ORL", "PHI", "PHO", "POR",
#     "SAC", "SAS", "TOR", "UTA", "WAS"
# ]
NBA_TEAMS = [
    "ATL", "BOS", "CHA", "CHI", "CLE",
]


def main():
    """
    This function executes the pipeline to extract historical trade data_data
    in the NBA.
    """
    nba_team_pairs = extract_data.get_nba_team_pairs(NBA_TEAMS)

    trade_info = extract_data.trader_crawler(nba_team_pairs)

    df = pd.concat(trade_info)
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df["trade_date"].dt.strftime('%Y-%m')

    df.to_csv("trade_win_shares.csv", index=False)


if __name__ == "__main__":

    main()
