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
full_headers_dict = {"summonerName":"player", "championId": "champion", "magicDamageDealt":"totalmagicdamagedealt", "physicalDamageDealt":"totalphysicaldamagedealt", "physicalDamageTaken":"physicaldamagetaken", "kills":"kills","deaths":"deaths","assists":"assists", 'firstBloodKill': 'firstblood', 'totalDamageDealtToChampions': 'totaldamagetochampions', 'physicalDamageDealtToChampions': 'physicaldamagetochampions', 'magicDamageDealtToChampions': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'magicalDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBoughtInGame': 'controlwardspurchased', 'totalMinionsKilled': 'minionskilled', 'neutralMinionsKilledTeamJungle': "neutralminionskilledinteam'sjungle", 'neutralMinionsKilledEnemyJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'turretKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'doubleKills': 'doublekills', 'tripleKills': 'triplekills', 'quadraKills': 'quadrakills', 'pentaKills': 'pentakills', 'goldEarned':'goldearned', 'goldSpent': 'goldspent', "largestCriticalStrike":"largestcriticalstrike", "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill", "teamId":'side', 'gameId':'gameid'}
lpl_full_headers_dict = {"name": "player","hero":"champion","kill":"kills","death":"deaths","assist":"assists",'firstBlood': 'firstblood', 'totalDamageToChamp': 'totaldamagetochampions', 'pDamageToChamp': 'physicaldamagetochampions', 'mDamageDealtToChamp': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'mDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBought': 'controlwardspurchased', 'lasthit': 'minionskilled', 'neutralKilledTJungle': "neutralminionskilledinteam'sjungle", 'neutralKilledEJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'towerKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'firstInhibitorAssist': 'firstinhibassist', 'dKills': 'doublekills', 'tKills': 'triplekills', 'qKills': 'quadrakills', 'pKills': 'pentakills', 'side':'side', 'gold':'goldearned', 'GoldSpent': 'goldspent', "pDamageDealt":"totalphysicaldamagedealt", "pDamageTaken":"physicaldamagetaken", 'mDamageDealt':'totalmagicdamagedealt', 'largestCriticalStrike':'largestcriticalstrike',  "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill", 'gameId':'gameid'}
scrape_headers = full_headers_dict.keys()
lpl_scrape_headers = lpl_full_headers_dict.keys()
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
"https://lpl.qq.com/es/stats.shtml?bmid=7325",
"https://lpl.qq.com/es/stats.shtml?bmid=6909",
"http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT03/1632489?gameHash=8a0464cfacf2ff50",
"http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT03/1672030?gameHash=d0df39be673c8e95"]

#fixes URL to grab the data json. Needs to be fixed for new 2021 URL format
#This will only work for non-LPL matches at this time.
def url_for_request_scraping(raw_url):
    cut = raw_url.split("#match-details/")[1].split("&amp;tab=overview,Unnamed: 31False")[0]
    new_url = "https://acs.leagueoflegends.com/v1/stats/game/"+cut
    return (new_url)

def lpl_url_for_request_scraping(raw_url, test):
    base_url = "https://lpl.qq.com/web201612/data/LOL_MATCH_DETAIL_"
    js = ".js"
    match_num = raw_url[-4:]
    new_url = base_url + match_num + js
    if test == True:
        pprint.pprint(new_url)
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
#returns json with full match data
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
        player = json_content["participantIdentities"][count]["player"]["summonerName"]
        champion_id = json_content["participants"][count]["championId"]
        champion_name = champ_key_dict[str(champion_id)]
        gameId = json_content["gameId"]
        stats = json_content["participants"][count]["stats"]
        stats.update({"championId": champion_name , "gameId": gameId, "summonerName":player})
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

#Remove all of the columns that we're not tracking
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

#This function modifies Boolean values to 1's/0's
def fix_dataframe(dataframe):
    bool_list = ["firstbloodassist","firstblood","firstinhibassist","firstinhibkill","firsttowerassist","firsttowerkill"]
    for h in bool_list:
        dataframe[h] = dataframe[h].apply(lambda x: 1 if x else 0)
    return (dataframe)    

####LPL MODULES###
def lpl_url_for_request_scraping(raw_url, test):
    base_url = "https://lpl.qq.com/web201612/data/LOL_MATCH_DETAIL_"
    js = ".js"
    match_num = raw_url[-4:]
    new_url = base_url + match_num + js
    if test == True:
        pprint.pprint(new_url)
    return (new_url)

#Get the lpl json data. 
def lpl_get_match_data(url, test):
    good_url = lpl_url_for_request_scraping(url, False)
    json_file = requests.get(good_url)
    json_content = json.loads(json_file.text[12:-1]) # or demjson.decode(json_file.content[12:-1])
    #assert json_file.status_code == 200
    if test == True:
        pprint.pprint(json_content)
    return(json_content)

def lpl_build_dataframe(input_match_data, test):
    jd = json.loads(input_match_data["sMatchInfo"][0]['battleInfo']['BattleData'])
    #'bMatchId' is what matches the URL
    side = 'left'
    count = 0
    records = 0
    while records < 10:
        if count == 5:
            count = 0
            side = 'right'
        else:
            player_info = jd[side]['players'][count]
            champion_name = champ_key_dict[str(player_info['hero'])]
            gameId = json.loads(input_match_data['bMatchId'])
            player_info.update({"hero": champion_name , "gameid": gameId})
            if count == 0 and records == 0:
                df = pd.DataFrame([player_info])
                records = records + 1
                count = count + 1
            else:
                new_df = pd.DataFrame([player_info])
                count = count + 1
                records = records + 1
                df = df.append(new_df)
    if test == True:
        pprint.pprint(df) 
    return (df)

def lpl_prune_dataframe(input_raw_dataframe, test):
    bad_df = input_raw_dataframe
    all_columns = bad_df.columns.values.tolist()
    bad_keys = []
    for i in all_columns:
        if i not in lpl_scrape_headers:
            bad_keys.append(i)
    good_df = bad_df.drop(bad_keys, axis=1)
    good_df['firstBlood'] = good_df['firstBlood'].apply(lambda x: 1 if x else 0)
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
    if iteration_count == 0:
        with open(database_file, 'w+') as database_file:
            match_data_container = pd.read_csv(match_data, header=0, delimiter=',', encoding="utf-8-sig")
            match_data_container.to_csv(database_file, mode="a", index=False)
    else:
        match_data_container = pd.read_csv(match_data, header=0, skiprows=[0], delimiter=',',encoding="utf-8-sig")
        match_data_container.to_csv(database_file, mode="a", index=False)
    if test == True:
            print('combining csv')
            print(iteration_count)

#check if URL is lpl
def lpl_check(url):
    if "https://lpl.qq.com" in url:
        return(True)
    else:
        return(False)

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
urllist = get_urllist() #raw_urllist #setting this as a variable so i can switch between this and other urllists      
test_match_file = r'C:/Users/sam/Desktop/ScrapeTest/test_match_file_V3.csv'
test_database_file = r'C:/Users/sam/Desktop/ScrapeTest/test_database_V3.csv'
lpl_test_match_file = r'C:/Users/sam/Desktop/ScrapeTest/lpl_test_match_file_V3.csv'
lpl_test_database_file = r'C:/Users/sam/Desktop/ScrapeTest/lpl_test_database_V3.csv'
error_file = r'C:/Users/sam/Desktop/ScrapeTest/error_urls.csv'
iteration_count = 0
lpl_iteration_count = 0
total_iteration = lpl_iteration_count + iteration_count
bad_urllist = []
start_time = time.time()
for url in urllist:
    if not lpl_check(url):
        try: #this currently works for Pre-2020, non-lpl urls and match data
            full_match_data = get_match_data(url, False)
            long_match_dataframe = build_dataframe(full_match_data, False)
            short_match_dataframe = prune_dataframe(long_match_dataframe, False)
            short_match_dataframe = short_match_dataframe.rename(columns = full_headers_dict) #this is returning a dataframe, might need to combine dataframes before dropping to csv for lpl
            short_match_dataframe = fix_dataframe(short_match_dataframe)
            write_to_csv(short_match_dataframe, test_match_file) #does this need to exist or can we just drop the panda dataframes into the CSV?
            combine_csv(test_match_file, test_database_file, iteration_count, False)
            iteration_count = iteration_count + 1
        except Exception as e:
            bad_urllist.append(url)
            print("non-lpl, pre-2021", e)
        if iteration_count % 50 == 0:
            print ('iteration_count', iteration_count)
        else:
            pass
    elif lpl_check(url):
        try: #this currently works for Pre-2020, non-lpl urls and match data
            full_match_data = lpl_get_match_data(url, False)
            long_match_dataframe = lpl_build_dataframe(full_match_data, False)
            short_match_dataframe = lpl_prune_dataframe(long_match_dataframe, False)
            short_match_dataframe = short_match_dataframe.rename(columns = lpl_full_headers_dict) #this is returning a dataframe, might need to combine dataframes before dropping to csv for lpl
            write_to_csv(short_match_dataframe, lpl_test_match_file)
            combine_csv(lpl_test_match_file, lpl_test_database_file, lpl_iteration_count, False)
            lpl_iteration_count = lpl_iteration_count + 1
        except Exception as e:
            print("lpl", e)
        if iteration_count % 50 == 0:
            print ('lpl_iteration_count', lpl_iteration_count)
        else:
            pass
        
with open(error_file, 'w+', newline='') as f:
    write = csv.writer(f)
    write.writerows(bad_urllist)

print("Run time:", time.time() - start_time )
print("records:", iteration_count + lpl_iteration_count)

