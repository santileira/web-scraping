import asyncio
import csv
import time

import aiohttp
import ftfy
import os

from html_page.html_page import get

main_page_url = "https://www.subtorrents1.com/series-1/"
output_csv_path = "/Users/sleira/Personal/series.csv"


async def process_series(session: aiohttp.ClientSession, series, series_writer):
    series_name = ""
    series_url = ""
    try:
        # avoid series with invalid value.
        if series is None or series == "\n" or series["value"] == "#":
            return

        # get series url
        series_url = ftfy.fix_text(series["value"])

        # get series name
        series_name = ftfy.fix_text(series.text)

        # get with series detail
        series_page = await get(session=session, url=series_url)

        # get technical series detail in div with id fichserietecnica
        technical_series_detail = ftfy.fix_text(series_page.select("div.fichserietecnica")[0].text)

        # get description in div with id fichseriedescrip
        description = ftfy.fix_text(series_page.select("div.fichseriedescrip")[0].text)

        # write new row in the csv
        series_writer.writerow([series_url, series_name, technical_series_detail, description])

        print(series_name)
    except Exception as ex:
        print(f'Error processing series {series_name} with url {series_url}, ex: {str(ex)}')


async def main():
    async with aiohttp.ClientSession() as session:
        main_page = await get(session=session, url=main_page_url)
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/series.csv"
        with open(dir_path, mode='w') as series_file:

            series_writer = csv.writer(series_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # write the headers.
            series_writer.writerow(["Series main_page_url", "Series name", "Ficha tecnica", "Resumen"])

            tasks = [asyncio.create_task(process_series(session=session, series_writer=series_writer, series=series))
                     for series in main_page.find("select", {"id": "serie"})]

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
#Program completed in 47.14327 seconds.