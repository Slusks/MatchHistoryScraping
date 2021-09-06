import requests
import re
import sys
import os
from requests.auth import HTTPBasicAuth
import time
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)
import pprint
from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
import csv
import json
import traceback
sys.path.insert(0, 'C:/Users/sam/Desktop/ScrapeTest')
from cookie_monster import COOKIE

###Basically, key = scraped value, value = table output value
full_headers_dict = {"gameVersion":"patch", "summonerName":"player", "championId": "champion", "magicDamageDealt":"totalmagicdamagedealt", "physicalDamageDealt":"totalphysicaldamagedealt", "physicalDamageTaken":"physicaldamagetaken", "kills":"kills","deaths":"deaths","assists":"assists", 'firstBloodKill': 'firstblood', 'totalDamageDealtToChampions': 'totaldamagetochampions', 'physicalDamageDealtToChampions': 'physicaldamagetochampions', 'magicDamageDealtToChampions': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'magicalDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBoughtInGame': 'controlwardspurchased', 'totalMinionsKilled': 'minionskilled', 'neutralMinionsKilledTeamJungle': "neutralminionskilledinteam'sjungle", 'neutralMinionsKilledEnemyJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'turretKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'doubleKills': 'doublekills', 'tripleKills': 'triplekills', 'quadraKills': 'quadrakills', 'pentaKills': 'pentakills', 'goldEarned':'goldearned', 'goldSpent': 'goldspent', "largestCriticalStrike":"largestcriticalstrike", "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill", "teamId":'side', 'gameId':'gameid'}
lpl_full_headers_dict = {"name": "player","hero":"champion","kill":"kills","death":"deaths","assist":"assists",'firstBlood': 'firstblood', 'totalDamageToChamp': 'totaldamagetochampions', 'pDamageToChamp': 'physicaldamagetochampions', 'mDamageDealtToChamp': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'mDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBought': 'controlwardspurchased', 'lasthit': 'minionskilled', 'neutralKilledTJungle': "neutralminionskilledinteam'sjungle", 'neutralKilledEJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'towerKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'firstInhibitorAssist': 'firstinhibassist', 'dKills': 'doublekills', 'tKills': 'triplekills', 'qKills': 'quadrakills', 'pKills': 'pentakills', 'side':'side', 'gold':'goldearned', 'GoldSpent': 'goldspent', "pDamageDealt":"totalphysicaldamagedealt", "pDamageTaken":"physicaldamagetaken", 'mDamageDealt':'totalmagicdamagedealt', 'largestCriticalStrike':'largestcriticalstrike',  "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill", 'gameId':'gameid'}
scrape_headers = full_headers_dict.keys()
lpl_scrape_headers = lpl_full_headers_dict.keys()
table_headers = full_headers_dict.values()
reg = r'^([\w]+.[\w]+)'

#Function that grabs the URL list from a csv
def get_urllist(csv):
    l = []
    #url_file = r"F:/LeagueStats/scraping/MatchHistoryScraping/data/URL.csv"
    url_file = csv
    file = pd.read_csv(url_file, header=0)
    l = list(file.url)
    single = list(set(l))
    for i in single:
        if type(i) != str:
            single.remove(i)
    print(len(single))
    return (single)

# coding: utf-8
#!/usr/bin/env python3
#Super basic. I'm importing the cookie from the already logged in 
# instance of my internet browser to requests. Then that let's me scrape the data I need.
#You should be able to use this as the basis for a script that lets you iterate over a 
# number of URLs for the json files, by replacing the get request with a for loop.

#Converts from Raw URL to URL for JSON formatted data###############################################
#Note: amateur matches are played on the normal server so they apparently have a different kind of url
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

def amateur_url_for_request_scraping(raw_url):
    #print ("request scraping url:", raw_url)
    if "/NA1/" in raw_url:
        cut = raw_url.split("#match-details/")[1].split("/")[:-1]
        end = raw_url.split("/")[-1].split("?")[0]
        new_url = "https://acs.leagueoflegends.com/v1/stats/game/" + cut[0] + "/" +  cut[1] + "?visiblePlatformId=NA1&visibleAccountId=" + end
    elif "/EUW1/" in raw_url:
        cut = raw_url.split("#match-details/")[1].split("/")[:-1]
        end = raw_url.split("/")[-1].split("?")[0]
        new_url = "https://acs.leagueoflegends.com/v1/stats/game/" + cut[0] + "/" +  cut[1] + "?visiblePlatformId=EUW1&visibleAccountId=" + end
    return (new_url)
####################################################################################################

#Functions that only need to be run when script is initiated########################################

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


#Professional Non-LPL data #########################################################################
#returns json with full match data
def get_match_data(url, test):
    good_url = url_for_request_scraping(url)
    json_file = requests.get(good_url, cookies=user_cookie)
    assert json_file.status_code == 200
    json_content = json_file.json()
    if test == True:
        pprint.pprint(json_content)
    return(json_content)

#returns dataframe
def build_dataframe(input_match_data, test):
    json_content = input_match_data
    count = 0
    while count < 10:
        player = json_content["participantIdentities"][count]["player"]["summonerName"]
        champion_id = json_content["participants"][count]["championId"]
        champion_name = champ_key_dict[str(champion_id)]
        gameId = json_content["gameId"]
        try:
            patch = re.match(reg, json_content["gameVersion"]).group()
        except:
            patch = "Unrecorded"
        stats = json_content["participants"][count]["stats"]
        stats.update({"championId": champion_name , "gameId": gameId, "summonerName":player, "gameVersion":patch})
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

#Remove all of the columns that contain data we're not tracking
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

#Modifies pro and amateur dataframes so the data is the right type/format
def fix_dataframe(dataframe, amateur):
    if amateur == True:
        try:
            positions = {"TOP, SOLO":"top", "MIDDLE, SOLO":"mid", "JUNGLE, NONE":"jng", "BOTTOM, DUO_CARRY":"bot", "BOTTOM, DUO_SUPPORT":"sup"}#, 'MIDDLE, DUO': 'FLEX', 'BOTTOM, DUO': 'FLEX', 'MIDDLE, DUO_SUPPORT':'FLEX'}
            dataframe["player"] = dataframe["player"].apply(lambda x: positions[x] if x in positions else 'flex') #.apply(lambda x: positions[x]) #this probably needs to be more complex/robust
            #dataframe["win"] = dataframe["win"].apply(lambda x: 1 if x else 0)
        except Exception as e:
            error_logging(error_directory, url, "##" , "amateur_dataframe", False)
            bad_urllist.append(url)
            #print("fix_dataframe_error: Amateur")
            #print(url)
            #print(dataframe["player"])
    else:
        bool_list = ["firstbloodassist","firstblood","firstinhibkill","firsttowerassist","firsttowerkill"]
        for h in bool_list:
            dataframe[h] = dataframe[h].apply(lambda x: 1 if x else 0)
    return (dataframe)

#LPL Formatted Modules #############################################################################
def lpl_url_for_request_scraping(raw_url, test):
    base_url = "https://lpl.qq.com/web201612/data/LOL_MATCH_DETAIL_"
    match_num = raw_url.split('=')[1] #raw_url[-4:]
    new_url = base_url + match_num + ".js"
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

#AMATEUR DATA########################################################################################
#Check if url is amateur
def amateur_check(url):
    if "/NA1/" in url:
        return (True)
    elif "/EUW1/" in url:
        return (True)
    else:
        return (False)

def amateur_get_match_data(url, test):
    good_url = amateur_url_for_request_scraping(url)
    json_file = requests.get(good_url, cookies=user_cookie)
    assert json_file.status_code == 200
    json_content = json_file.json()
    if test == True:
        pprint.pprint(json_content)
    return(json_content)

def amateur_build_dataframe(input_match_data, test):
    json_content = input_match_data
    count = 0
    while count < 10:
        role = json_content['participants'][count]['timeline']['role']
        lane = json_content['participants'][count]['timeline']['lane']
        if role:
            player = lane +", " + role
        else:
            player =  lane
        champion_id = json_content["participants"][count]["championId"]
        champion_name = champ_key_dict[str(champion_id)]
        gameId = json_content["gameId"]
        try:
            patch = re.match(reg, json_content["gameVersion"]).group()
        except:
            patch = "Unrecorded"
        stats = json_content["participants"][count]["stats"]
        stats.update({"championId": champion_name , "gameId": gameId, "summonerName":player, "gameVersion":patch})
        if count == 0:
            df = pd.DataFrame([stats])
            count = count + 1
        else:
            new_df = pd.DataFrame([stats])
            count = count + 1
            try:
                df = df.append(new_df) #guessing this is where the summonerName error is coming
            except Exception as e:
                print ("amateur build dataframe error:", e) 
    if test == True:
        pprint.pprint(df)
    return(df)

# Amateur should otherwise reuse the other pro functions
#prune_dataframe
#fix_dataframe
####################################################################################################
#Writing Data to file ############################################################################## 
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

def error_logging(error_directory, url, count, function, test):
    log_file = error_directory + str(count) +"_"+ function + ".csv"
    var = traceback.format_exc()
    if test == True:
        print("var:", var)
    log = open(log_file, 'a')
    log.write(url+" \n")
    log.write(var)
    log.close()
    #newline=''
    if type(count) != str:
        count = count + 1
    return (var)

#Run Script #########################################################################################
on_Laptop = os.path.exists(r'C:/Users/samsl/') #Checks if we're on my laptop or Desktop
testing = False
#These are all of the Desktop Files
if on_Laptop == False:
    if testing == True:
        desktop_url_file = r"C:/Users/sam/Desktop/ScrapeTest/test/test_url_file.csv"
        urllist = get_urllist(desktop_url_file)
        match_file = r'C:/Users/sam/Desktop/ScrapeTest/test/test_match_file_V3.csv'
        database_file = r'C:/Users/sam/Desktop/ScrapeTest/test/test_database_V3.csv'
        amateur_match_file = r'C:/Users/sam/Desktop/ScrapeTest/test/test_amateur_match_file_V3.csv'
        amateur_database_file = r'C:/Users/sam/Desktop/ScrapeTest/test/test_amateur_database_V3.csv'
        lpl_match_file = r'C:/Users/sam/Desktop/ScrapeTest/test/lpl_test_match_file_V3.csv'
        lpl_database_file = r'C:/Users/sam/Desktop/ScrapeTest/test/lpl_test_database_V3.csv'
        lpl_2016_database_file = r'C:/Users/sam/Desktop/ScrapeTest/test/lpl_2016_test_database_V3.csv'
    elif testing == False:
        desktop_url_file = r"F:/LeagueStats/scraping/MatchHistoryScraping/Version3/all_url.csv"
        urllist = get_urllist(desktop_url_file)
        match_file = r'C:/Users/sam/Desktop/ScrapeTest/prod/prod_match_file_V3.csv'
        amateur_database_file = r'C:/Users/sam/Desktop/ScrapeTest/prod/prod_amateur_database_V3.csv'
        amateur_match_file = r'C:/Users/sam/Desktop/ScrapeTest/prod/prod_amateur_match_file_V3.csv'
        database_file = r'C:/Users/sam/Desktop/ScrapeTest/prod/prod_database_V3.csv'
        lpl_match_file = r'C:/Users/sam/Desktop/ScrapeTest/prod/lpl_prod_match_file_V3.csv'
        lpl_database_file = r'C:/Users/sam/Desktop/ScrapeTest/prod/lpl_prod_database_V3.csv'
        lpl_2016_database_file = r'C:/Users/sam/Desktop/ScrapeTest/prod/lpl_2016_prod_database_V3.csv'
    error_file = r'C:/Users/sam/Desktop/ScrapeTest/test/ErrorLog/error_urls.csv'#Note that this is still in the test folder
    error_directory = r'C:/Users/sam/Desktop/ScrapeTest/test/ErrorLog/' #Note that this is still in the test folder
#These are all of the Laptop files
else: 
    laptop_url_file = r'C:/Users/samsl/Desktop/ScrapeTest/test/test_url_file.csv'
    urllist = get_urllist(laptop_url_file)
    match_file = r'C:/Users/samsl/Desktop/ScrapeTest/test/test_match_file_V3.csv'
    database_file = r'C:/Users/samsl/Desktop/ScrapeTest/test/test_database_V3.csv'
    lpl_match_file = r'C:/Users/samsl/Desktop/ScrapeTest/test/lpl_test_match_file_V3.csv'
    lpl_database_file = r'C:/Users/samsl/Desktop/ScrapeTest/test/lpl_test_database_V3.csv'
    lpl_2016_database_file = r'C:/Users/samsl/Desktop/ScrapeTest/test/lpl_2016_test_database_V3.csv'
    error_file = r'C:/Users/samsl/Desktop/ScrapeTest/test/error_log/error_urls.csv' 
    error_directory = r'C:/Users/samsl/Desktop/ScrapeTest/test/error_log/'
iteration_count = 0
lpl_iteration_count = 0
bad_urllist = []
start_time = time.time()
for url in urllist:
    if not lpl_check(url):
        try:
            amateur = amateur_check(url)
            if amateur:
                full_match_data = amateur_get_match_data(url, False)
                long_match_dataframe = amateur_build_dataframe(full_match_data, False) #builds the data with a different value in player
                short_match_dataframe = prune_dataframe(long_match_dataframe, False)
                short_match_dataframe = short_match_dataframe.rename(columns = full_headers_dict) 
                short_match_dataframe = fix_dataframe(short_match_dataframe, amateur)
                short_match_dataframe['url'] = url
                write_to_csv(short_match_dataframe, amateur_match_file) #does this need to exist or can we just drop the panda dataframes into the CSV?
                combine_csv(amateur_match_file, amateur_database_file, iteration_count, False)
            else:
                full_match_data = get_match_data(url, False)
                long_match_dataframe = build_dataframe(full_match_data, False)
                short_match_dataframe = prune_dataframe(long_match_dataframe, False)
                short_match_dataframe = short_match_dataframe.rename(columns = full_headers_dict) 
                short_match_dataframe = fix_dataframe(short_match_dataframe, amateur)
                short_match_dataframe['url'] = url
                write_to_csv(short_match_dataframe, match_file) #does this need to exist or can we just drop the panda dataframes into the CSV?
                combine_csv(match_file, database_file, iteration_count, False)
        except Exception as e:
            print("main exception")
            error_logging(error_directory, url, iteration_count, "main", True)
            bad_urllist.append(url)
        iteration_count = iteration_count + 1
        if iteration_count != 0 and iteration_count % 50 == 0:
            print ('iteration_count', iteration_count)
        else:
            pass
    elif lpl_check(url):
        try:
            lpl_full_match_data = lpl_get_match_data(url, False)
            lpl_long_match_dataframe = lpl_build_dataframe(lpl_full_match_data, False)
            lpl_short_match_dataframe = lpl_prune_dataframe(lpl_long_match_dataframe, False)
            lpl_short_match_dataframe = lpl_short_match_dataframe.rename(columns = lpl_full_headers_dict)
            lpl_short_match_dataframe['url'] = url
            if len(lpl_short_match_dataframe.columns) == 26:
                write_to_csv(lpl_short_match_dataframe, lpl_match_file)
                combine_csv(lpl_match_file, lpl_2016_database_file, lpl_iteration_count, False)
            else:
                write_to_csv(lpl_short_match_dataframe, lpl_match_file)
                combine_csv(lpl_match_file, lpl_database_file, lpl_iteration_count, False)
        except Exception as e:
            error_logging(error_directory, url, lpl_iteration_count, "lpl_main", True)
            bad_urllist.append(url)
        lpl_iteration_count = lpl_iteration_count + 1
        if iteration_count % 50 == 0:
            print ('lpl_iteration_count', lpl_iteration_count)
        else:
            pass

with open(error_file, 'w', newline='') as f:
    for i in bad_urllist:
        f.write(i+"\n")

print("Run time:", time.time() - start_time )
print("records:", lpl_iteration_count + iteration_count)

