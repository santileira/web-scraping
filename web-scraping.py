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
#lectulandia_main_page_url = "https://www.lectulandia.co/book/#post-57669"
lectulandia_main_page_url = "https://www.lectulandia.co/book/"

#numero_de_pagina = 1


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

    wb = Workbook()
    excel_libros = Workbook()
    primer_hoja = excel_libros.add_sheet('Catalogo de libros')
    style = xlwt.easyxf('font: bold 1, color black;')
    main_page = get_html_page(main_page_url)
    lectulandia_main_page = get_html_page(lectulandia_main_page_url)
    primer_hoja.write(0, 0, 'Autor', style)
    primer_hoja.write(0, 1, 'Titulo', style)
    primer_hoja.write(0, 2, 'Genero', style)
    primer_hoja.write(0, 3, 'Sinopsis', style)
    row = 1
    cantidad_de_libros = 0
    numero_de_pagina = 1

    for paginas in range(1563):
        for libros in lectulandia_main_page.find("main", {"id": "main"}):  # aca va un find_all

            if libros is None or libros == "\n" or libros.name=="header":
               continue

            try:
                div_titulo = libros.find("div", {"class": "details"})
                titulo = div_titulo.find("a",{"class":"title"})
                titulo_href = "https://www.lectulandia.co" + titulo.attrs['href']
                libro_details = get_html_page(titulo_href)
                div_book_details = libro_details.find("div", {"id": "primary"})
                description = div_book_details.find("div", {"id": "sinopsis"})
                autor = div_book_details.find("div", {"id": "autor"})
                autor_imp = autor.get_text()
                autor_imp_2 = autor_imp.split(' ',1)[1]
                genero = div_book_details.find("div", {"id": "genero"})
                genero_imp = genero.get_text()
                genero_imp_2 = genero_imp.split(' ',1)[1]
                primer_hoja.write(row, 0, autor_imp_2)
                primer_hoja.write(row, 1, titulo.attrs['title'])
                primer_hoja.write(row, 2, genero_imp_2)
                primer_hoja.write(row, 3, description.get_text())
                row = row + 1
                cantidad_de_libros = cantidad_de_libros + 1

                print(titulo.attrs['title'])
                print(autor_imp_2)
                print(description.get_text())
                print(genero_imp_2)
                print("\n")

                if cantidad_de_libros == 24:
                    numero_de_pagina = numero_de_pagina + 1

                    pagina_siguiente = "https://www.lectulandia.co/book/page/"+str(numero_de_pagina)+"/" #"https://www.lectulandia.co/book/page/2/"
                    lectulandia_main_page = get_html_page(pagina_siguiente)
                    print(pagina_siguiente)
                    cantidad_de_libros = 0
                    break
                # else: None
                # return None
            except Exception:
                print("error")

    excel_libros.save('/Users/aleira/Desktop/xlwt example61.xls')
    print(cantidad_de_libros)
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
