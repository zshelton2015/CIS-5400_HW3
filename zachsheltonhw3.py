###
# This code is written by Dr. Fitz and provided to students taking CIS5400
# at Florida Institute of Technology.
# Do not copy or reproduce without permission
###

import json
import dateparser
import requests
from lxml import html
from datetime import datetime as date


def get_html(url):
    """
    This function extracts the html code from a url
    :param url: 
    :return: html code from the web page referenced by url
    """
    response = requests.get(url)  # get page data from server, block redirects
    source_code = response.content  # get string of source code from response
    return source_code


def get_data_table(source_code):
    """
    This function creates a 2-D list of the following fields:
    [president_name, tenure, speech_link, speech_date, speech]
    The speech_date and speech are currently left blank.
    :param source_code: the html source code extracted from a url
    :return: a 2-D Python list or table
    """
    data_table = []
    speech_table = None
    trs = None
    html_elem = html.document_fromstring(source_code)  # make HTML element object
    tables = html_elem.cssselect("table")  # select the table element on the page

    # if you find a table, initialize the speech table to the first table
    if len(tables) > 0:
        speech_table = tables[0]

    # if you find the speech table, select its rows
    if speech_table is not None:
        trs = speech_table.cssselect("tr")

    # If you find rows in the table, go through each row
    # and process the data. Skip the header row (start at row 1)
    if trs is not None:
        for i in range(1, len(trs)):
            tr = trs[i]
            tds = tr.cssselect("td")
            president_name = ""

            # simple check to make sure the row has president name and speech url
            if len(tds) == 12:
                first_cell_data = tds[0].text_content().strip()
                tenure = tds[1].text_content().strip()
                # get the link element for the link to the speech
                speech_link_elmnt = tds[2].cssselect("a")
                speech_link = ""
                speech_date = ""
                speech = ""

                if len(first_cell_data) > 0:
                    president_name = first_cell_data

                if len(speech_link_elmnt) > 0:
                    speech_link = speech_link_elmnt[0].get("href")

                if len(president_name) > 0 and len(speech_link) > 0:
                    data_table.append([president_name, tenure, speech_link, speech_date, speech])
    return data_table


def scrape_data(url):
    """
    :param url: the url to 
    :return: 
    """
    return get_data_table(get_html(url))


def find_speech_date(data_table):
    """
    :param data_table
    :return: Nothing
    This function finds the date and speech content via the webpage in data[4] and a datetime string in
    data[3](data = each row of data_table)
    """
    for data in data_table:
        url = data[2]
        html_elem = html.document_fromstring(get_html(url))
        date_r = html_elem.cssselect('[class="field-docs-start-date-time"]')
        print(date_r[0].text_content())
        date_obj = dateparser.parse(date_r[0].text_content())
        val = html_elem.cssselect('[class="field-docs-content"]')
        speech = val[0].text_content()
        data[3] = date_obj.strftime('%')
        data[4] = speech.strip("  ")
    return 0
#Commit me1

def clean_speech(data_table):
    for data in data_table:
        speech = data[4]
        lines = speech.splitlines()
        n_speech = ""
        for line in lines:
            n_speech = n_speech + line
        data[4] = ""
        data[4] = n_speech
    return data_table


def write_txt(data_table):
    f = open("SOU_data.txt", 'w+')
    json.dump(data_table, f)
    f.close()
    return 0


def main():
    """
    The main driver of the program.
    It uses the base link to The American Presidency Project
    at UC Santa Barbara to extract SOU addresses
    """
    url = "https://www.presidency.ucsb.edu/" \
          "documents/presidential-documents-archive-guidebook/" \
          "annual-messages-congress-the-state-the-union"
    data_table = scrape_data(url)
    find_speech(data_table)
    clean_speech(data_table)
    """
    Two for loops writes values to .c
    """
    write_txt(data_table)


# call the main function to run the program
main()
