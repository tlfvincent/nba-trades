"""
Extract Data

This module contains functions to extract NBA trade data.
"""

import itertools
import logging
import math
import requests

import pandas as pd

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_nba_team_pairs(nba_teams):
    """
    Extract all unique (and non-redundant) pairs of NBA teams.

    Parameters
    ----------
    nba_teams : list
        Contains three-letter for all NBA teams.

    Returns
    -------
    nba_team_pairs : list
        Contains all unique (and non-redundant) pairs of NBA teams.
    """

    logger.info("Extract all unique pairs of NBA teams.")
    nba_team_pairs = [
        nba_team for nba_team in itertools.combinations(nba_teams, 2)
    ]

    return nba_team_pairs

def trader_crawler(nba_team_pairs):
    """

    Parameters
    ----------
    nba_team_pairs : list
        Contains all unique (and non-redundant) pairs of NBA teams.

    Returns
    -------
    trade_info
    """
    trade_info = {}
    for nba_pair in nba_team_pairs:
        team_1 = nba_pair[0]
        team_2 = nba_pair[1]

        url = f"http://www.basketball-reference.com/friv/trades.fcgi?f1={team_1}&f2={team_1}"
        trade_ws, trade_dates = get_page_content(url)

        nba_pair_trade_info = process_trades_data(trade_ws, trade_dates)

        nba_pair_trade_info["team_1"] = team_1
        nba_pair_trade_info["team_2"] = team_2

    trade_info[nba_pair] = nba_pair_trade_info

    return trade_info


def get_page_content(url):
    """
    Extract HTML content of URL.

    Parameters
    ----------
    url : string
        Full URL to extract HTML content from.

    Returns
    -------
    trade_ws : list
        Contains list of trades between teams, along with win shares traded.

    trade_dates : list
        Contains dates at which all trades between teams occurred.
    """

    logger.info(f"Extract HTML content of URL {url}")
    response = requests.get(url)
    page_source = response.text

    logger.info(f"Extract all trades available in {url}")
    soup = BeautifulSoup(page_source)

    trades = soup.findAll(class_="bullets")
    trade_ws = [info.findAll("li") for info in trades]

    trades_details = soup.findAll(class_="transaction")
    trade_dates = [td.find("strong").text for td in trades_details]

    return trade_ws, trade_dates


def process_trades_data(trade_ws, trade_dates):
    """

    Parameters
    ----------
    trade_ws : list
        Contains list of trades between teams, along with win shares traded.

    trade_dates : list
        Contains dates at which all trades between teams occurred.

    Returns
    -------
    nba_pair_trade_info : pandas.DataFrame
        Contains dates and win shared for all recorded trades between pair of
        NBA teams.
    """

    nba_pair_trade_info = []
    for i, win_shares in enumerate(trade_ws):
        for data in win_shares:
            data_details = data.text.split(" ")
            ws_past, ws_future = (
                data_details.index("past") - 1,
                data_details.index("future") - 1
            )

            nba_pair_trade_info.append([
                float(words[ws_past]),
                float(words[ws_future]),
                trade_dates[i]
            ])

    nba_pair_trade_info = pd.DataFrame(
        nba_pair_trade_info,
        columns=["ws_sent", "ws_received", "trade_date"]
    )

    return nba_pair_trade_info
