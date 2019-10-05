import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import ftfy
import xlwt
from xlwt import Workbook

main_page_url = "https://www.subtorrents1.com/series-1/"
output_csv_path = "/Users/aleira/Desktop/series1.csv"
lectulandia_main_page_url = "https://www.lectulandia.co/book/#post-57669"


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
    # try:
    # var = 10
    """                   # Second Example
    while var > 0:
       print ("Current variable value :"+ var)
       var = var -1
       if var == 5:
          break
    """
    # print ("Good bye!")
    # Workbook is created
    wb = Workbook()
    excel_libros = Workbook()

    # add_sheet is used to create sheet.
    primer_hoja = excel_libros.add_sheet('Catalogo de libros')
    # write(fila, columna)
    # Applying multiple styles
    style = xlwt.easyxf('font: bold 1, color black;')

    # Writing on specified sheet
    # sheet.write(0, 0, 'SAMPLE', style)

    main_page = get_html_page(main_page_url)
    lectulandia_main_page = get_html_page(lectulandia_main_page_url)

    # get series
    # var_libros = 0
    # t=lectulandia_main_page.find("article",{"class":"card"})
    # print(t)
    # exit()
    primer_hoja.write(0, 0, 'Titulo', style)
    primer_hoja.write(0, 1, 'Autor', style)
    primer_hoja.write(0, 2, 'Genero', style)
    primer_hoja.write(0, 3, 'Sinopsis', style)

    for libros in lectulandia_main_page.find("main", {"id": "main"}):  # aca va un find_all
        #

        # test=lectulandia_main_page.find("article", {"class": "card"})
        # avoid series with invalid value. Comento....
        if libros is None or libros == "\n" or libros.name=="header":
           continue
        # for x in range(0,4):
        try:
            div_titulo = libros.find("div", {"class": "details"})
            titulo = div_titulo.find("a",{"class":"title"})
            titulo_href = "https://www.lectulandia.co" + titulo.attrs['href']
            libro_details = get_html_page(titulo_href)
            div_book_details = libro_details.find("div", {"id": "primary"})
            description = div_book_details.find("div", {"id": "sinopsis"})
            autor = div_book_details.find("div", {"id": "autor"})
            genero = div_book_details.find("div", {"id": "genero"})



            print(titulo.attrs['title'])
            #print(titulo_href)
            print(autor.get_text())
            print(description.get_text())
            print(genero.get_text())
            print("\n")
        except Exception:
            print("error")
        # print(lectulandia_main_page)
        # p1=lectulandia_main_page.find("div")
        # p2=p1.find("a",{"class":"title"})
        # print(p2.get_text())

        """
        var_libros = var_libros +1
        if var_libros > 5:
            print("Chau")
            #wb.save('/Users/aleira/Desktop/xlwt example11.xls') 
            break
        """
        # else: None
        # return None
        # exit()
        # get series url
        # libros_test=lectulandia_main_page.find("div",{"class":"details"})
        # libros_test = ftfy.fix_text(lectulandia_main_page.select("div.title")[0].text)
        # ftfy.fix_text(series_page.select("div.fichseriedescrip")[0].text)
        # print(libros_test.get_text())
    excel_libros.save('/Users/agustinleira/Desktop/xlwt example2.xls')
    exit()

    var = 0
    with open(output_csv_path, mode='w') as series_file:

        series_writer = csv.writer(series_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # write the headers.
        series_writer.writerow(["Series main_page_url", "Series name", "Ficha tecnica", "Resumen"])
        sheet1.write(0, 0, 'Series main_page_url', style)
        sheet1.write(0, 1, 'Series name', style)
        sheet1.write(0, 2, 'Ficha tecnica', style)
        sheet1.write(0, 3, 'Resumen', style)
        row = 1
        column = 0
        # wb.save('/Users/aleira/Desktop/xlwt example7.xls')

        # get series
        for series in main_page.find("select", {"id": "serie"}):
            #
            try:

                # avoid series with invalid value.
                if series is None or series == "\n" or series["value"] == "#":
                    continue
                # for x in range(0,4):
                # get series url
                series_url = ftfy.fix_text(series["value"])
                # print(series_url)
                # break
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
                # write new row in the Excel
                sheet1.write(row, 0, series_url.lstrip())
                sheet1.write(row, 1, series_name.lstrip())
                sheet1.write(row, 2, technical_series_detail.lstrip())
                sheet1.write(row, 3, description.lstrip())
                row = row + 1
                print("Serie: " + series_name, "URL de la serie: " + series_url)
                # print(technical_series_detail.strip())
                """
                var = var +1
                if var > 5:
                    print("Chau")
                    #wb.save('/Users/aleira/Desktop/xlwt example11.xls') 
                    break
                #else: None 
                    #return None
                """
            except Exception as ex:
                log_error(str(ex))
    wb.save('/Users/aleira/Desktop/xlwt example1.xls')


get_series_data()
