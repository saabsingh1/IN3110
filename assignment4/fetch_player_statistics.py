import os
import re
from operator import itemgetter
from sqlite3 import Row
from turtle import rt
from types import NoneType
from typing import Dict, List
from unicodedata import name
from urllib.parse import urljoin

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"


def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba. We check each team and their players and rank them
    based on points scored.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    assert len(teams) == 8

    # Gets the player for every team and stores in dict (get_players)
    all_players = {}

    for team in teams:
        name = team['name']
        players = get_players(team['url'])
        all_players[name] = players

    # gets player statistics for each player,
    # using get_player_stats
    for team, players in all_players.items():
        for player in players:
            statdict = (get_player_stats(player['url'], team))
            for key, val in statdict.items():
                player[key] = val

    # Select top 3 for each team by points:
    best = {}
    for team, players in all_players.items():
        # Sorting and extracting top 3 based on points
        top_3 = []
        point_list = []
        for player in players:
            # we get all the points from the players in the team
            point_list.append(player['points'])
        point_list = sorted(point_list)
        # we then check which players have the top 3 best points stats
        for player in players:
            if player['points'] == point_list[-1] or player['points'] == point_list[-2] or player['points'] == point_list[-3]:
                # if they are one of the top 3 we append them to the list
                top_3.append(player)
        top3 = sorted(top_3, key=itemgetter('points'), reverse=True)
        best[team] = top3

    # we plot the stats we want, for the top 3 players on each team
    stats_to_plot = ['points', 'assists', 'rebounds']
    for stat in stats_to_plot:
        plot_best(best, stat=stat)


def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team. Saves the plots as figures in corresponding files.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """

    color_table = {
        "Golden State": "yellow",
        "Boston": "black",
        "Dallas": "blue",
        "Memphis": "purple",
        "Miami": "red",
        "Philadelphia": "olive",
        "Milwaukee": "green",
        "Phoenix": "orange"
    }

    count_so_far = 0
    all_names = []

    # iterate through each team and then
    for team, players in best.items():
        # we pick the color for the team, from the table above
        color = color_table[team]
        # collects the stat and name of each player on the team
        plotstat = []
        names = []
        for player in players:
            names.append(player["name"])
            plotstat.append(player[stat])

        # saving the players name
        all_names.extend(names)
        # the position of bars is shifted by the number of players so far
        x = range(count_so_far, count_so_far + len(players))
        count_so_far += len(players)
        # making bars for this team's players stats,
        # with the team name as the label
        bars = plt.bar(x, plotstat, color=color, label=team)
        plt.bar_label(bars)

    # uses the names, rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    # add the legend with the colors  for each team
    plt.legend(loc=0)
    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title("top 3 players " + stat + " per game for each team ")
    # save the figure to a file
    plt.tight_layout()
    filename = stat + ".png"
    print(f"Creating {filename}")
    my_path = "NBA_player_statistics/"
    if not os.path.exists(my_path):
        os.mkdir(my_path)
    plt.savefig(my_path + filename)
    # clear so we can plot new stats when called next time
    plt.clf()


def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(
                base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    assert len(in_semifinal) == 8

    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals. Going trought roster
    with html parsing, and finding the players names and urls.
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    # Getting the html and parsing it to find the table we want
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Roster").find_next("table")

    players = []
    rows = table.find_all("tr")
    rows = rows[3:]
    # Looping over the rows to get the players we want from roster
    for row in rows:
        # finding columns
        cols = row.find_all("td")
        # finding name links (a tags)
        name_col = cols[2]
        a = name_col.find("a")
        # name is the text in the col
        name = a.text
        # putting together the players url
        url = base_url + a['href']
        # appending to dict of all players in team
        players.append({'name': name, 'url': url})
    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team. Going trought the table for their career statistics,
    we find their stats over points, assists and rebounds for the 2021. For those who are missing their stats for this season,
    we give them 0 for each stat.
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    # Getting the html and parsing it to find all the tables of the players
    # wikipage
    html = get_html(player_url)
    soup = BeautifulSoup(html, 'html.parser')
    # we have to this because the table we want doesnt have a consistent name
    # for alle the players wiki pages.
    all_table = soup.findAll('table', {"class": "wikitable sortable"})
    # but its always the first wikitable sortable
    table = all_table[0]

    stats = {}

    rows = table.findAll("tr")
    rows = rows[1:]
    # looping over the rows
    for row in rows:
        # year = re.findall(r'NBA season">(.*)</a>', str(row)) didnt work
        # finding all cols for row
        cols = row.find_all("td")
        # team and year col
        rteam = cols[1].text[:-1]
        year1 = cols[0].text[:-1]
        # winners this season have this char, so we have to remove it for the
        # check
        if '†' in year1:
            year1 = year1[:-1]
        # to not get out of range
        if len(year1) > 0:
            # checking that the player plays in the team, and that the stats
            # are for 2021-22
            if year1 == '2021–22' and team == rteam:
                # assigning stats
                points = cols[12].text.strip()
                assists = cols[9].text.strip()
                rebounds = cols[8].text.strip()
                # removing so that we can parse to float later
                if '*' in points:
                    points = points[:-1]
                elif '*' in assists:
                    assists = assists[:-1]
                elif '*' in rebounds:
                    rebounds = rebounds[:-1]
                # appending to players stat dict with stats as keys
                stats = {
                    "points": float(points),
                    "assists": float(assists),
                    "rebounds": float(rebounds)}
        # if they are missing stats
        if len(stats) == 0:
            stats = {
                "points": float(0),
                "assists": float(0),
                "rebounds": float(0)}
    return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
