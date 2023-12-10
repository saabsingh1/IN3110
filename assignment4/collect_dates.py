import re
from typing import Tuple

## -- Task 4 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year only accepts a 4-digit number between at least 1000-2029
    year = r"(?:100\d|10[1-9]\d|1[1-9]\d{2}|20[0-2]\d)"
    # month accepts month names or month numbers
    month = r"(?:(?:0?\d|1[0-2])|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Sept|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))"
    # day can be a number, which may or may not be zero-padded
    day = r"(?:\d{1,2})"

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'. Checks the strings position in the month array
    to determine the corresponding month numberized, have to + 1 because array index starts at 0.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return s

    # Convert to number as string
    if s in month_names:
        # if month is the 10th upwards we dont have to zero pad it
        if month_names.index(s) + 1 < 10:
            # zero pad and find index in array
            s = "0" + str(month_names.index(s) + 1)
        else:
            s = str(month_names.index(s) + 1)
    return s


def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'. Excpect for numbers that dont need zero-pad (10 and upwards)

    You don't need to use this function,
    but you may find it useful.
    """
    # if len of n is == 1 we know that n is < 10 and need padding
    if len(n) == 1:
        n = '0' + n
        return n
    return n


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex. Dates can be in different formats such as ISO, MDY, DMY or YMD. Because of this we have
    different regex patterns for each format. When parsing trough the text, we wil check for all the formats with different regex patterns.

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # regex for iso months
    iso_month_format = r"\b(?:0\d|1[0-2])\b"

    # Date on format YYYY/MM/DD - ISO

    # When there is special chars in between dates we add these as well
    ISO = year + '-' + iso_month_format + '-' + day

    # Date on format DD/MM/YYYY
    # this is the 'prettiest' use of it
    DMY = rf"{day} {month} {year}"

    # Date on format MM/DD/YYYY
    # When there is special chars in between dates we add these as well
    MDY = month + ' ' + day + ', ' + year

    # Date on format YYYY/MM/DD
    YMD = rf"{year} {month} {day}"

    # list with all supported formats
    formats = [ISO, DMY, MDY, YMD]
    dates = []

    # finding all dates in any format in text
    for format in formats:
        for match in re.findall(rf"{format}", text, flags=re.I):
            if match:
                # here we change format to the desired one, for each format
                if format == DMY:
                    m = match.split(" ")
                    day = zero_pad(m[0])
                    mon = convert_month(m[1])
                    year = m[2]
                    match = year + '/' + mon + '/' + day
                    dates.append(match)
                elif format == ISO:
                    m = match.split("-")
                    year = m[0]
                    mon = convert_month(m[1])
                    day = zero_pad(m[2])
                    match = year + '/' + mon + '/' + day
                    dates.append(match)
                elif format == MDY:
                    m = match.split(" ")
                    day = zero_pad(m[1])
                    day = day[:-1]
                    day = zero_pad(day)
                    mon = convert_month(m[0])
                    year = m[2]
                    match = year + '/' + mon + '/' + day
                    dates.append(match)
                elif format == YMD:
                    m = match.split(" ")
                    print(m[1])
                    year = m[0]
                    mon = convert_month(m[1])
                    day = zero_pad(m[2])
                    match = year + '/' + mon + '/' + day
                    dates.append(match)

    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        output = open(output, "w")
        output.write("DATES: ")
        output.write("\n")
        for date in dates:
            output.write(date)
            output.write("\n")
    return dates
