
import re
from copy import copy
from dataclasses import dataclass
from turtle import heading

import bs4
import pandas as pd
from bs4 import BeautifulSoup
from requests import request
import requests
from requesting_urls import get_html

## --- Task 5, 6, and 7 ---- ##


# Dict over all types of events
event_types = {
    "DH": "Downhill",
    "SL": "Slalom",
    "GS": "Giant Slalom",
    "SG": "Super Giant slalom",
    "AC": "Alpine Combined",
    "PG": "Parallel Giant Slalom",
}


def time_plan(url: str) -> str:
    """Parses table from html text and extract desired information
    and saves in betting slip markdown file.

    arguments:
        url (str) : URL for page with calendar table
    return:
        markdown (str) : string containing the markdown schedule
    """
    # Loading page as html str
    html = get_html(url)
    # Using Beautiful soup to parse
    soup = BeautifulSoup(html, "html.parser")
    # Locating the table we want
    calendar = soup.find(id="Calendar")
    soup_table = calendar.find_next("table", {"class": "wikitable"})
    # extracting the events into pandas data frame
    df = extract_events(soup_table)

    # Writing the schedule markdown
    return render_schedule(df)


@dataclass
class TableEntry:
    """Data class representing a single entry in a table

    Records text content, rowspan, and colspan attributes
    """

    text: str
    rowspan: int
    colspan: int


def extract_events(table: bs4.element.Tag) -> pd.DataFrame:
    """Gets the events from the table by looping trough rows and columns for desired data and then appending
    this as tableentries in our data list. After this we filter away the data we dont want and store it as a Pandas DataFrame.
    arguments:
        table (bs4.element.Tag) : Table containing data
    return:
        df (DataFrame) : DataFrame containing filtered and parsed data
    """
    # Retrivieng the table headers and saving their labels in `keys`
    headings = table.find_all("th")

    # Finding the labels in the table
    labels = [th.text.strip() for th in headings]
    data = []

    # Extracts the data in table, keeping track of colspan and rowspan
    rows = table.find_all("tr")
    rows = rows[1:]

    # Looping trough the rows
    for tr in rows:
        # Finding the elements in the table
        cells = tr.find_all(["th", "td"])
        row = []
        # Looping trough the elements
        for cell in cells:
            rowspan = 1
            colspan = 1
            # Check to see if rowspan or colspan is shared between elements.
            if 'rowspan' in cell.attrs:
                rowspan = int(cell.attrs['rowspan'])
            if "colspan" in cell.attrs:
                colspan = int(cell.attrs['colspan'])
            text = strip_text(cell.text)
            # appending table entries
            row.append(
                TableEntry(
                    text=text,
                    rowspan=rowspan,
                    colspan=colspan,
                )
            )
        data.append(row)

    # expanding TableEntries into a dense table
    all_data = expand_row_col_span(data)
    print(all_data)
    # list of desired columns
    wanted = ["Date", "Venue", "Type"]
    # filtering data and returning pandas dataframe (this is done in
    # filter_data)
    filtered_data = filter_data(labels, all_data, wanted)
    df = filtered_data
    return df


def render_schedule(data: pd.DataFrame) -> str:
    """Render the schedule data to markdown

    arguments:
        data (DataFrame) : DataFrame containing table to write
    return:
        markdown (str): the rendered schedule as markdown
    """
    def expand_event_type(type_key):
        """Expand event type key (SL) to full name (Slalom)

        Useful with pandas Series.apply
        """
        # Returns the values from event_types
        return event_types.get(type_key[:2], type_key)

    # Changeing the type values to full names instead of abbreviations
    for t in data['Type']:
        d = expand_event_type(t)
        data['Type'] = data['Type'].replace([t], d)

    # had to pip install tabulate when using to_markdown()
    return data.to_markdown()


def strip_text(text: str) -> str:
    """Gets rid of cruft from table cells, footnotes and setting limit to 20 chars

    It is not required to use this function,
    but it may be useful.

    arguments:
        text (str) : string to fix
    return:
        text (str) : the string fixed
    """
    text = text[:20]  # 20 char limit
    text = re.sub(r"\[.*\]", "", text)
    return text


def filter_data(keys: list, data: list, wanted: list):
    """Filters away the columns not specified in wanted argument by comparing the keys(columns)
    in the dataframe to the ones in the list over wanted(columns). Drops those we dont want.

    It is not required to use this function,
    but it may be useful.

    arguments:
        keys (list of strings) : list of all column names
        data (list of lists) : data with rows and columns
        wanted (list of strings) : list of wanted columns
    return:
        filtered_data (newdf: DataFrame) : the filtered data
            This is the subset of data in `data`,
            after discarding the columns not in `wanted`.
    """
    # creating new dataframe
    newdf = pd.DataFrame(data, columns=keys)
    inWanted = False
    for key in keys:
        for want in wanted:
            # we want to keep this keep
            if key == want:
                inWanted = True
                # break out
                break
            inWanted = False
        # if our check is still false
        if not inWanted:
            # we drop the key, this is not in our wanted list
            newdf.drop(key, axis=1, inplace=True)
    # returning the dataframe after discarding unwanted columns
    return newdf


def expand_row_col_span(data):
    """Applies row/colspan to tabular data

    It is not required to use this function,
    but it may be useful.

    - Copies cells with colspan to columns to the right
    - Copies cells with rowspan to rows below
    - Returns raw data (removing TableEntry wrapper)

    arguments:
        data_table (list) : data with rows and cols
            Table of the form:

            [
                [ # row
                    TableEntry(text='text', rowspan=2, colspan=1),
                ]
            ]
    return:
        new_data_table (list): list of lists of strings
            [
                [
                    "text",
                    "text",
                    ...
                ]
            ]

            This should be a dense matrix (list of lists) of data,
            where all rows have the same length,
            and all values are `str`.
    """

    # first, apply colspan by duplicating across the column(s)
    new_data = []
    for row in data:
        new_row = []
        new_data.append(new_row)
        for entry in row:
            for _ in range(entry.colspan):
                new_entry = copy(entry)
                new_entry.colspan = 1
                new_row.append(new_entry)

    # apply row span by inserting copies in subsequent rows
    # in the same column
    for row_idx, row in enumerate(new_data):
        for col_idx, entry in enumerate(row):
            for offset in range(1, entry.rowspan):
                # copy to row(s) below
                target_row = new_data[row_idx + offset]
                new_entry = copy(entry)
                new_entry.rowspan = 1
                target_row.insert(col_idx, new_entry)
            entry.rowspan = 1

    # now that we've applied col/row span,
    # replace the table with the raw entries,
    # instead of the TableEntry objects
    return [[entry.text for entry in row] for row in new_data]


if __name__ == "__main__":
    # test the script on the past few years by running it:
    for year in range(20, 23):
        url = (
            f"https://en.wikipedia.org/wiki/20{year}–{year+1}_FIS_Alpine_Ski_World_Cup"
        )
        print(url)
        md = time_plan(url)
        print(md)
