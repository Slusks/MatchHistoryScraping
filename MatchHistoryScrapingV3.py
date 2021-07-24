import requests
import re
import sys
from requests.auth import HTTPBasicAuth
import time
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)
import pprint
from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
import csv
import json
sys.path.insert(0, 'C:/Users/sam/Desktop/ScrapeTest')
from cookie_monster import COOKIE

###Basically, key = scraped value, value = table output value
full_headers_dict = {"summonerName":"player", "championId": "champion", "magicDamageDealt":"totalmagicdamagedealt", "physicalDamageDealt":"totalphysicaldamagedealt", "physicalDamageTaken":"physicaldamagetaken", "kills":"kills","deaths":"deaths","assists":"assists", 'firstBloodKill': 'firstblood', 'totalDamageDealtToChampions': 'totaldamagetochampions', 'physicalDamageDealtToChampions': 'physicaldamagetochampions', 'magicDamageDealtToChampions': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'magicalDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBoughtInGame': 'controlwardspurchased', 'totalMinionsKilled': 'minionskilled', 'neutralMinionsKilledTeamJungle': "neutralminionskilledinteam'sjungle", 'neutralMinionsKilledEnemyJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'turretKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'firstInhibitorAssist': 'firstinhibassist', 'doubleKills': 'doublekills', 'tripleKills': 'triplekills', 'quadraKills': 'quadrakills', 'pentaKills': 'pentakills', 'goldEarned':'goldearned', 'goldSpent': 'goldspent', "largestCriticalStrike":"largestcriticalstrike", "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill", "teamId":'side', 'gameId':'gameId'}

scrape_headers = full_headers_dict.keys()
table_headers = full_headers_dict.values()

#Function that grabs the URL list from a csv
def get_urllist():
    l = []
    url_file = r"F:/LeagueStats/scraping/MatchHistoryScraping/data/URL.csv"
    file = pd.read_csv(url_file, header=0)
    l = list(file.url)
    single = list(set(l))
    print(len(single))
    return (single)

# coding: utf-8
#!/usr/bin/env python3
#Super basic. I'm importing the cookie from the already logged in 
# instance of my internet browser to requests. Then that let's me scrape the data I need.
#You should be able to use this as the basis for a script that lets you iterate over a 
# number of URLs for the json files, by replacing the get request with a for loop.


raw_urllist = [
"https://matchhistory.br.leagueoflegends.com/pt/#match-details/ESPORTSTMNT03/570139?gameHash=ba727c1db6d1cfbb&amp;tab=overview",
"https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT05/1540037?gameHash=df189f4cefd8bfea&amp;tab=overview",
"http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/1160644?gameHash=744c3e9779ad519c&amp;tab=overview,Unnamed: 31",
"https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/660033?gameHash=3ae31e7697461999&amp;tab=overview,False",
"https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3695017432/246666621?tab=overview",
"https://matchhistory.euw.leagueoflegends.com/en/#match-details/EUW1/4702645805/219539932?tab=overview"]

#fixes URL to grab the data json. Needs to be fixed for new 2021 URL format
#This will only work for non-LPL matches at this time.
def url_for_request_scraping(raw_url):
    cut = raw_url.split("#match-details/")[1].split("&amp;tab=overview,Unnamed: 31False")[0]
    new_url = "https://acs.leagueoflegends.com/v1/stats/game/"+cut
    return (new_url)

#2021 URL is going to need to look like this: https://acs.leagueoflegends.com/v1/stats/game/EUW1/4702645805?visiblePlatformId=EUW1&visibleAccountId=219539932
# Parsing 2021 JSON is also probably going to be new.

# Format your cookie into a dictionary form
user_cookie = dict()

for item in COOKIE.split("; "):
    k, v = item.split("=")
    user_cookie[k] = v

#This is pulling the champion data.
champ_dd = requests.get("https://ddragon.leagueoflegends.com/cdn/11.8.1/data/en_US/champion.json", cookies=user_cookie)
champ_json = champ_dd.json()
champ_name = champ_json["data"] #this creates a list of all the champions
champ_key_dict = {}
for i in champ_name:
    champ_key_dict.update({champ_json["data"][i]["key"]:i})
#pprint.pprint(champ_dd.json())

##PULLING DATA###
####### Pre 2021, Non-LPL data ######
def get_match_data(url, test):
    good_url = url_for_request_scraping(url)
    json_file = requests.get(good_url, cookies=user_cookie)
    assert json_file.status_code == 200
    json_content = json_file.json()
    if test == True:
        pprint.pprint(json_content)
    return(json_content)

def build_dataframe(input_match_data, test):
    json_content = input_match_data
    count = 0
    while count < 10:
        champion_id = json_content["participants"][count]["championId"]
        champion_name = champ_key_dict[str(champion_id)]
        gameId = json_content["gameId"]
        stats = json_content["participants"][count]["stats"]
        stats.update({"championId": champion_name , "gameId": gameId})
        if count == 0:
            df = pd.DataFrame([stats])
            count = count + 1
        else:
            new_df = pd.DataFrame([stats])
            count = count + 1
            df = df.append(new_df) 
    if test == True:
        pprint.pprint(df)
    return(df)

def prune_dataframe(input_raw_dataframe, test):
    bad_df = input_raw_dataframe
    all_columns = bad_df.columns.values.tolist()
    bad_keys = []
    for i in all_columns:
        if i not in scrape_headers:
            bad_keys.append(i)
    good_df = bad_df.drop(bad_keys, axis=1)
    if test == True:
        pprint.pprint(good_df)    
    return (good_df)
#######################################

### Writing Data 
#write lists to temp CSV
def write_to_csv(data_list, output_file):
    dataframe = pd.DataFrame(data_list)
    dataframe.to_csv(output_file, index=False, header=True) # print to our csv

#add content of temp csv file to database csv.
def combine_csv(match_data, database_file, iteration_count, test):
    print('combining csv')
    print(iteration_count)
    if iteration_count == 0:
        with open(database_file, 'w+') as database_file:
            match_data_container = pd.read_csv(match_data, header=0, delimiter=',', encoding="utf-8-sig")
            match_data_container.to_csv(database_file, mode="a", index=False)
    else:
        match_data_container = pd.read_csv(match_data, header=0, skiprows=[0], delimiter=',',encoding="utf-8-sig")
        match_data_container.to_csv(database_file, mode="a", index=False)


on_Laptop = False

# if on_Laptop:
#     database_file = r'C:/Users/samsl/Desktop/ScrapeTest/databaseV3.csv'
#     test_database_file = r'C:/Users/samsl/Desktop/ScrapeTest/test_databaseV3.csv'
#     temp_file = r'C:/Users/samsl/Desktop/ScrapeTest/scrapeV2.csv'

#     database_file_lpl = r'C:/Users/samsl/Desktop/ScrapeTest/databaseV3_lpl.csv'
#     test_database_file_lpl = r'C:/Users/samsl/Desktop/ScrapeTest/test_databaseV3_lpl.csv'
#     temp_file_lpl = r'C:/Users/samsl/Desktop/ScrapeTest/scrapeV2_lpl.csv'

#     master_file = r'C:/Users/samsl/Desktop/ScrapeTest/master_combined_database.csv'

#     error_url_file = r'C:/Users/samsl/Desktop/ScrapeTest/error_url_list.csv'    
# elif not on_Laptop:
#     database_file = r'C:/Users/sam/Desktop/ScrapeTest/databaseV3.csv'
#     test_database_file = r'C:/Users/sam/Desktop/ScrapeTest/test_databaseV3.csv'
#     temp_file = r'C:/Users/sam/Desktop/ScrapeTest/scrapeV2.csv'

#     database_file_lpl = r'C:/Users/sam/Desktop/ScrapeTest/databaseV3_lpl.csv'
#     test_database_file_lpl = r'C:/Users/samsl/Desktop/ScrapeTest/test_databaseV3_lpl.csv'
#     temp_file_lpl = r'C:/Users/sam/Desktop/ScrapeTest/scrapeV2_lpl.csv'

#     master_file = r'C:/Users/sam/Desktop/ScrapeTest/master_combined_database.csv'

#     error_url_file = r'C:/Users/sam/Desktop/ScrapeTest/error_url_list.csv'


#### RUNNING FILES ##########
urllist = raw_urllist #setting this as a variable so i can switch between this and other urllists      
test_match_file = r'C:/Users/sam/Desktop/ScrapeTest/test_match_file_V3.csv'
test_database_file = r'C:/Users/sam/Desktop/ScrapeTest/test_database_V3.csv'
iteration_count = 0
start_time = time.time()
for url in urllist:
    try: #this currently works for Pre-2020, non-lpl urls and match data
        full_match_data = get_match_data(url, False)
        long_match_dataframe = build_dataframe(full_match_data, True)
        short_match_dataframe = prune_dataframe(long_match_dataframe, False)
        short_match_dataframe.rename(columns = full_headers_dict)
        write_to_csv(short_match_dataframe, test_match_file)
        combine_csv(test_match_file, test_database_file, iteration_count, False)
        iteration_count = iteration_count + 1
    except Exception as e:
        print(e) 
    
 
print("Run time:", time.time() - start_time )
print("records:", iteration_count)
