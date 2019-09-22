import csv

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import ftfy
import datetime
main_page_url = "https://www.subtorrents1.com/series-1/"
output_csv_path = "/Users/sleira/Personal/series.csv"


def get_html_page(url: str) -> BeautifulSoup:
    """
    Attempts to get the content at `main_page_url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML and status code is 200, convert the content to `Beautiful Soap` object, otherwise return None.
    """
    try:

        # The closing() function ensures that any network resources are freed when they go out of scope in that with block.
        # Using closing() like that is good practice and helps to prevent fatal errors and network timeouts.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }
        with closing(get(url, headers=headers)) as response:
            if response.status_code == 200 and is_html_response(response):
                return BeautifulSoup(response.content, "html.parser")
            else:
                return None

    except RequestException as r_ex:
        log_error('Error during requests to {} : {}'.format(url, str(r_ex)))
        return None


def is_html_response(response) -> bool:
    """
    Returns true if the content type seems be HTML else false.
    """
    content_type = response.headers['Content-Type'].lower()
    return (content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


def get_series_data():
    print(datetime.datetime.utcnow())
    main_page = get_html_page(main_page_url)
    with open(output_csv_path, mode='w') as series_file:

        series_writer = csv.writer(series_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # write the headers.
        series_writer.writerow(["Series main_page_url", "Series name", "Ficha tecnica", "Resumen"])

        # get series
        for series in main_page.find("select", {"id": "serie"}):
            try:

                # avoid series with invalid value.
                if series is None or series == "\n" or series["value"] == "#":
                    continue

                # get series url
                series_url = ftfy.fix_text(series["value"])
                # get series name
                series_name = ftfy.fix_text(series.text)

                # get with series detail
                series_page = get_html_page(series_url)

                # get technical series detail in div with id fichserietecnica
                technical_series_detail = ftfy.fix_text(series_page.select("div.fichserietecnica")[0].text)

                # get description in div with id fichseriedescrip
                description = ftfy.fix_text(series_page.select("div.fichseriedescrip")[0].text)

                # write new row in the csv
                series_writer.writerow([series_url, series_name, technical_series_detail, description])

                print(series_name)
            except Exception as ex:
                log_error(str(ex))


get_series_data()
