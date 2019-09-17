import csv

import pandas as pd
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from w3lib.html import replace_entities


def simple_get(url: str):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        """
        The closing() function ensures that any network resources are freed when they go out of scope in that with block. 
        Using closing() like that is good practice and helps to prevent fatal errors and network timeouts.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }
        with closing(get(url, headers=headers)) as response:
            if is_good_response(response):
                return response.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp) -> bool:
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.

    html.find_all("select", {"id": "serie"})[0].contents[3]["value"]
    """
    print(e)


url = "https://www.subtorrents1.com/series-1/"
path_csv = "/Users/sleira/Personal/series.csv"
raw_html = simple_get(url)

html = BeautifulSoup(raw_html, "html.parser")
with open(path_csv, mode='w') as series_file:
    series_writer = csv.writer(series_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    series_writer.writerow(["Series url", "Series name", "Ficha tecnica"])
    for series in html.find("select", {"id": "serie"}):
        try:
            if series == "\n" or series["value"] == "#":
                continue
            series_url = series["value"]
            series_name = series.text
            technical_series_detail = ""
          #  raw_html = simple_get(series_url)
          #  html_series = BeautifulSoup(raw_html, "html.parser")
          #  technical_series_detail = html_series.select("div.fichserietecnica")[0].text
            series_writer.writerow([series_url, series_name, technical_series_detail])
        except Exception as e:
            print(str(e))

