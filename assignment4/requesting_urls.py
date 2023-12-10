from typing import Dict, Optional

import requests

## -- Task 1 -- ##


def get_html(
        url: str,
        params: Optional[Dict] = None,
        output: Optional[str] = None):
    """Gets an HTML page from an url and return its contents as a string using requests.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """
    # passing the optional parameters argument to the get function
    response = requests.get(url, params=params)
    html_str = response.text

    # if output is specified, the response txt and url get printed to a
    # txt file with the name in `output`
    if output:
        output = open(output, "w")
        output.write(response.url)
        output.write("\n")
        output.write(html_str)

    return html_str
