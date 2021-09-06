# This file fixes the dots that are used to indicate first blood by changing them to 1's and 0's.


from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
import pathlib
import csv
from csv import reader
import os



old_file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\match_database.csv")
old_file_delinquent = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\delinquent_match_database.csv")
fixed_file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\match_database_FB_Fixed.csv")

def dot_to_binary(old_file, fixed_file):
    open_file = open(old_file, encoding='utf-8')
    read_file = csv.reader(open_file)
    next(read_file)

    data = ""
    with open(old_file, encoding='utf-8') as file:
        data = file.read().replace('●','1').replace('○','0')
    with open(fixed_file, 'w', encoding='utf-8') as file:
        file.write(data)

dot_to_binary(old_file_delinquent, fixed_file)

    
    

    








