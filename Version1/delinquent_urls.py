#this function goes through a database of match history data and grabs all of the URLS

from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
import csv
from csv import reader
import pandas as pd

old_url_file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\no_champ_urls.csv")
new_url_file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\no_champ_urls2.csv")


open_file = open(old_url_file, encoding='utf-8')
read_file = csv.reader(open_file, skipinitialspace=True,delimiter=',')


df = pd.read_csv(old_url_file)
header = ['url']
df.to_csv(new_url_file, columns= header, index=False)



   
    
        


