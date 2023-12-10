from email.mime import base
from gettext import find
import re
from urllib.parse import urljoin

## -- Task 2 and 3-- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex. By creating two expressions we can check trough the anchor tags,
    to see if we can find the href tags within those anchor tags. Can write urls to file if requested.
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # Compiling regex for use later
    atag_pat = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)
    href_pat = re.compile(r'href="([^">#]+)', flags=re.IGNORECASE)
    urls = set()
    # Finding all <a> tags in the html
    for a_tag in atag_pat.findall(html):
        # Checking if there is a href tag in the a tags
        match = href_pat.search(a_tag)
        if match:
            # if there is a match we only want the href
            tmp = match.group(1)
            # checking som special cases
            if tmp[0] == '/' and tmp[1] != '/':
                tmp = base_url + tmp
            elif tmp[0] == '/' and tmp[1] == '/':
                tmp = 'https:' + tmp
            urls.add(tmp)

    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        output = open(output, "w")
        for url in urls:
            output.write(url)
            output.write("\n")
    return urls


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Makes call to find urls, and filters with regex. Can write article urls to file
    if specified.
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    # finding all urls
    urls = find_urls(html)
    # regex that finds wiki articels
    pattern = re.compile(
        r'https:\/\/[a-z]{2}\.wikipedia\.org\/wiki([^:,]+)',
        flags=re.IGNORECASE)
    articles = set()
    # searching trought the urls too se if we can match with regex expression
    for url in urls:
        match = pattern.search(url)
        if match:
            articles.add(url)

    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        output = open(output, "w")
        for wiki in articles:
            output.write(wiki)
            output.write("\n")

    return articles


# Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
