#Cleans some artifacts out of the database.
    # for some reason there were locations where .#'s were appended to random row items.
    # Regex courtesy of Brendan

import re
from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
import pathlib

input_file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\match_database_FB_Fixed.csv")
output_file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\match_database_characters_removed.csv")

def character_cleanup(input_file, output_file):
    toZero = re.compile(r",-\.\d{1},")
    toValhalla = re.compile(r"k\.\d{1},")
    toMordor = re.compile(r"mil\.\d{1},")
    toSiberia = re.compile(r"тыс\.\.\d{1},")

    with open(input_file, "r", encoding='utf-8') as inputfile:
        data = inputfile.read()

    output = re.sub(toZero, ",0,", data)
    output = re.sub(toValhalla, "k,", output)
    output = re.sub(toMordor, "mil,", output)
    output = re.sub(toSiberia, "тыс.,", output)
    
    with open(output_file, "w", encoding='utf-8') as outputfile:
        outputfile.write(output)


character_cleanup(input_file, output_file)