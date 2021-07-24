import requests
import re
from requests.auth import HTTPBasicAuth
import time
import pandas as pd
import pprint
from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
from cookie_monster import COOKIE
import json
import os


#Variables and Headers - wont need this until we're processing the text files
# format: scraped headers: oracle's elixer header
#Scraped headers: headers to add to table
###Basically, key = scraped value, value = desired value
    #So I honestly can't remember if this is just filling in holes from Oracle's Elixer tables or if this is supposed to be all information, so it definitely contains some gaps
    #in the information it contains.
#####

#Original:
#full_headers_dict = {"magicDamageDealt":"totalmagicdamagedealt", "physicalDamageDealt":"totalphysicaldamagedealt", "physicalDamageTaken":"physicaldamagetaken", "kills":"kills","deaths":"deaths","assists":"assists", 'firstBloodKill': 'firstblood', 'totalDamageDealtToChampions': 'totaldamagetochampions', 'physicalDamageDealtToChampions': 'physicaldamagetochampions', 'magicDamageDealtToChampions': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'magicalDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBoughtInGame': 'controlwardspurchased', 'totalMinionsKilled': 'minionskilled', 'neutralMinionsKilledTeamJungle': "neutralminionskilledinteam'sjungle", 'neutralMinionsKilledEnemyJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'turretKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'firstInhibitorAssist': 'firstinhibassist', 'doubleKills': 'doublekills', 'tripleKills': 'triplekills', 'quadraKills': 'quadrakills', 'pentaKills': 'pentakills', 'goldEarned':'goldearned', 'goldSpent': 'goldspent', "largestCriticalStrike":"largestcriticalstrike", "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill", "teamId":'side'}
#full_headers_dict_lpl = {"name": "player","hero":"champion","kill":"kills","death":"deaths","assist":"assists",'firstBlood': 'firstblood', 'totalDamageToChamp': 'totaldamagetochampions', 'pDamageToChamp': 'physicaldamagetochampions', 'mDamageDealtToChamp': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'mDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBought': 'controlwardspurchased', 'lasthit': 'minionskilled', 'neutralKilledTJungle': "neutralminionskilledinteam'sjungle", 'neutralKilledEJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'towerKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'firstInhibitorAssist': 'firstinhibassist', 'dKills': 'doublekills', 'tKills': 'triplekills', 'qKills': 'quadrakills', 'pKills': 'pentakills', 'side':'side', 'gold':'goldearned', 'GoldSpent': 'goldspent', "physicalDamageDealt":"totalphysicaldamagedealt", "pDamageTaken":"physicaldamagetaken", 'mDamageDealt':'totalmagicdamagedealt', 'largestCriticalStrike':'largestcriticalstrike',  "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill", 'game-id':'gameId'}

#New Headers dictionaries without added player/champion/gameId function below.
raw_headers_dict = {"summonerName":"player", "championId": "champion", "magicDamageDealt":"totalmagicdamagedealt", "physicalDamageDealt":"totalphysicaldamagedealt", "physicalDamageTaken":"physicaldamagetaken", "kills":"kills","deaths":"deaths","assists":"assists", 'firstBloodKill': 'firstblood', 'totalDamageDealtToChampions': 'totaldamagetochampions', 'physicalDamageDealtToChampions': 'physicaldamagetochampions', 'magicDamageDealtToChampions': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'magicalDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBoughtInGame': 'controlwardspurchased', 'totalMinionsKilled': 'minionskilled', 'neutralMinionsKilledTeamJungle': "neutralminionskilledinteam'sjungle", 'neutralMinionsKilledEnemyJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'turretKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'firstInhibitorAssist': 'firstinhibassist', 'doubleKills': 'doublekills', 'tripleKills': 'triplekills', 'quadraKills': 'quadrakills', 'pentaKills': 'pentakills', 'goldEarned':'goldearned', 'goldSpent': 'goldspent', "largestCriticalStrike":"largestcriticalstrike", "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill", "teamId":'side', 'gameId':'gameId'}
raw_headers_dict_lpl = {"name": "player","hero":"champion","kill":"kills","death":"deaths","assist":"assists",'firstBlood': 'firstblood', 'totalDamageToChamp': 'totaldamagetochampions', 'pDamageToChamp': 'physicaldamagetochampions', 'mDamageDealtToChamp': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'mDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBought': 'controlwardspurchased', 'lasthit': 'minionskilled', 'neutralKilledTJungle': "neutralminionskilledinteam'sjungle", 'neutralKilledEJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'towerKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'firstInhibitorAssist': 'firstinhibassist', 'dKills': 'doublekills', 'tKills': 'triplekills', 'qKills': 'quadrakills', 'pKills': 'pentakills', 'side':'side', 'gold':'goldearned', 'GoldSpent': 'goldspent', "pDamageDealt":"totalphysicaldamagedealt", "pDamageTaken":"physicaldamagetaken", 'mDamageDealt':'totalmagicdamagedealt', 'largestCriticalStrike':'largestcriticalstrike',  "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill", 'game-id':'gameId'}
#### I dont know if I want gameId or matchId in the lpl headers dict
# 
#Alphabetizing the raw dictionaries of headers to make sure everything is always in the same order for output. 
#This is apparently not very Pythonic
#def get_key(dic, val):
#    for key, value in dic.items():
#        if val == value:
#             return key

# def sort_dictionary(in_dict):
#     y = list(in_dict.values())
#     new_d = {}
#     y_sorted = sorted(y)
#     for i in y_sorted:
#         key = get_key(in_dict,i)
#         new_d[key] = i
#     return(new_d)

# full_headers_dict = sort_dictionary(raw_headers_dict)
# full_headers_dict_lpl = sort_dictionary(raw_headers_dict_lpl)

# coding: utf-8
#!/usr/bin/env python3
#Super basic. I'm importing the cookie from the already logged in 
# instance of my internet browser to requests. Then that let's me scrape the data I need.
#You should be able to use this as the basis for a script that lets you iterate over a 
# number of URLs for the json files, by replacing the get request with a for loop.


test_raw_urllist = [
"https://matchhistory.br.leagueoflegends.com/pt/#match-details/ESPORTSTMNT03/570139?gameHash=ba727c1db6d1cfbb&amp;tab=overview",
"https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT05/1540037?gameHash=df189f4cefd8bfea&amp;tab=overview",
"http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/1160644?gameHash=744c3e9779ad519c&amp;tab=overview,Unnamed: 31",
"https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/660033?gameHash=3ae31e7697461999&amp;tab=overview,False"#,
"https://lpl.qq.com/es/stats.shtml?bmid=7325",
"https://lpl.qq.com/es/stats.shtml?bmid=6909"
]

single_url = "https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/660033?gameHash=3ae31e7697461999&amp;tab=overview,False"

longer_raw_urllist =['http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/80532?gameHash=ebf3b1a721dc6fde&amp;tab=overview', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/TRLH1/1002210083?gameHash=9ed4c4cb1c26a1ec&amp;tab=overview', 'https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/1384397?gameHash=2c834113f5dc5d1a&amp;tab=overview', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/1180492?gameHash=861f480faed92b0a', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/TREU/1001490197?gameHash=c1d99cbca313dd17&amp;tab=overview', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT01/1310941?gameHash=d9ada7733493c79c', 'https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT01/1321280?gameHash=294b476f65218cfe&amp;tab=overview', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/1300358?gameHash=20b575528c3d1ab9', 'https://matchhistory.na.leagueoflegends.com/en/#match-details/TRLH1/1002520246?gameHash=175bf6e0da0ff375', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/170093?gameHash=47e0556f123b2106&amp;tab=overview'] 

#table_headers = ["kills","deaths","assists","Largest Killing Spree","Largest Multi Kill","First Blood","Total Damage to Champions","Physical Damage to Champions","Magic Damage to Champions","True Damage to Champions","Total Damage Dealt","Physical Damage Dealt","Magic Damage Dealt","True Damage Dealt","Largest Critical Strike","Total Damage to Objectives","Total Damage to Turrets","Damage Healed","Damage Taken","Physical Damage Taken","Magic Damage Taken","True Damage Taken","Wards Placed","Wards Destroyed","Stealth Wards Purchased","Control Wards Purchased","Gold Earned","Gold Spent","Minions Killed","Neutral Minions Killed","Neutral Minions Killed in Team's Jungle","Neutral Minions Killed in Enemy Jungle","url","champion"]


######################################Functions that only run once############################################################################################
# Format your cookie into a dictionary form
def get_urllist():
    l = []
    url_file = r"F:/LeagueStats/scraping/MatchHistoryScraping/data/URL.csv"
    file = pd.read_csv(url_file, header=0)
    l = list(file.url)
    single = list(set(l))
    if len(single) > 5:
        return (single)

#gotta run this on both header dicts prior to running anything else so they end up in the same order
# orders them by value because all of the values are the same
def get_key(dic, val):
    for key, value in dic.items():
         if val == value:
             return key
def sort_dictionary(in_dict):
    x = list(in_dict.keys())
    y = list(in_dict.values())
    new_d = {}
    y_sorted = sorted(y)
    for i in y_sorted:
        key = get_key(in_dict,i)
        new_d[key] = i
    return(new_d)

#get alphabetized headers dictionary
a_full_headers_dict_lpl = sort_dictionary(raw_headers_dict_lpl)
a_keys = a_full_headers_dict_lpl.keys()

#alphabetized non-lpl headers
a_full_headers_dict = sort_dictionary(raw_headers_dict)
b_keys = a_full_headers_dict.keys()

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

### Creating the headers for non lpl
#I'm not sure why I'm doing this so I am removing it and hoping nothing breaks
# x = ["player", "champion"]
# headers_list = list(full_headers_dict.keys())
# z = ["gameId"]
# table_headings = x+headers_list+z

headers_list = list(a_full_headers_dict.keys())
headers_list_lpl = list(a_full_headers_dict_lpl.keys())

###############################################################################################################################################################
######################################  Gen Functions #########################################################################################################
#fixes URL into the form that it needs to be for scraping
def url_for_request_scraping(raw_url, test):
    cut = raw_url.split("#match-details/")[1].split("&amp;tab=overview,Unnamed: 31,False")[0]
    cut_cut = cut.replace('Unnamed: 31', "") #this and the line below might have a better pythoni method to complete
    cut_cut = cut_cut.replace("False","")
    new_url = "https://acs.leagueoflegends.com/v1/stats/game/"+cut_cut
    if test == True:
        pprint.pprint(new_url)
    return (new_url)

def url_for_request_scraping_lpl(raw_url, test):
    base_url = "https://lpl.qq.com/web201612/data/LOL_MATCH_DETAIL_"
    js = ".js"
    match_num = raw_url[-4:]
    new_url = base_url + match_num + js
    if test == True:
        pprint.pprint(new_url)
    return (new_url)


#get request that needs to be looped
def get_match_data(url, test):
    good_url = url_for_request_scraping(url, False)
    json_file = requests.get(good_url, cookies=user_cookie)
    assert json_file.status_code == 200
    json_content = json_file.json()
    if test == True:
        pprint.pprint(json_content)
    return(json_content)

def get_match_data_lpl(url, test):
    good_url = url_for_request_scraping_lpl(url, False)
    json_file = requests.get(good_url, cookies=user_cookie)
    assert json_file.status_code == 200
    json_content = json_file.json()
    if test == True:
        pprint.pprint(json_content)
    return(json_content)

 
# Take the json data, combine it into a list of lists
def get_data(json_content, test):
    count = 0
    list_list = []
    while count < 10:
        outputlist = []
        player = json_content["participantIdentities"][count]["player"]["summonerName"] #str
        champion_id = json_content["participants"][count]["championId"] #str
        gameId = json_content["gameId"] #str
        teamId = json_content["participants"][count]["teamId"]#str
        for i in  a_full_headers_dict.keys():
            if i =='championId':
                outputlist.append(champ_key_dict[str(champion_id)])
            elif i == 'gameId':
                outputlist.append(gameId)
            elif i == 'summonerName':
                 outputlist.append(player)
            elif i =='teamId':
                outputlist.append(teamId)
            elif i in headers_list:
                outputlist.append(json_content["participants"][count]["stats"][i])
            else:
                outputlist.append("None")
        list_list.append(outputlist)
        count += 1
        print('count:', count)
    if test == True:
        pprint.pprint(list_list)
    return (list_list)

#this has to be way worked on with data from LPL decoding
def get_data_lpl(json_content, test):
    list_list = []
    jd = json.loads(json_content["sMatchInfo"][0]['battleInfo']['BattleData']) #this returns a json
    keys = jd.keys()
    control = {'side':'left', 'count':0, 'records':0}
    gameId= json_content['bMatchId']
    #this subsection is to move between the 'right' and 'left' team lists because that's how this info is nested.
    while control['records'] < 10: #set this to 1 to get it to run for only one player
        output_list = []
        if control['count'] == 5:
            control['side'] = 'right'
            control['count'] = 0
        else: #I think the champion id -> champion modifier goes in here.
            side = control['side']
            count = control['count']
            data = jd[side]['players'][count] #dicts
        for i in a_keys:
            try:
                if i == 'hero': #this statement worked
                    output_list.append(str(champ_key_dict[jd[side]['players'][count][i]]))
                elif data[i]:
                    #print('yes')
                    output_list.append(data[i]) #list of all of the player info, which is currently fucking up
                elif i == 'firstBlood': #have to have this statement in here because apparently if the player didn't FB they just leave the line empty and python picks it up as False
                        if not data[i]:
                            data[i] = '0'
                            output_list.append(data[i])
                        else:
                            data[i] = '1'
                            output_list.append(data[i])
                elif i == 'game-id':
                    output_list.append(gameId)
                elif i == 'side':
                    output_list.append(control['side'])
                else:
                    print (i, 'not in lpl headers')
            except Exception as e: # probably dont need this full line because I'm doing something with the exception
                if i in b_keys:
                    print (i, "in non-lpl headers")
                    pass
                elif i == 'game-id' or 'side':
                    continue
                else:
                    print ("exception", i)
        list_list.append(output_list)
        control['count'] = control['count'] + 1
        control['records'] = control['records'] + 1
        print('done')
    if test == True:
        pprint.pprint(list_list)
    return(list_list)

#write lists to temp CSV
def write_to_csv(data_list, temp_output_file):
    print('write_to_csv running')
    dataframe = pd.DataFrame(data_list)
    dataframe.to_csv(temp_output_file, index=False, header=True) # print to our csv

#add content of temp csv file to database csv.
def combine_csv(match_data, database_file):
    print('combining csv')
    skip_row=[0]
    match_data_container = pd.read_csv(match_data, header=0, skiprows=skip_row, delimiter=',',encoding="utf-8-sig")
    match_data_container.to_csv(database_file, mode="a", index=False)
#####################################################################################################################################################

#check if URL is lpl
def not_lpl(url):
    if "https://lpl.qq.com" in url:
        return(False)
    else:
        return(True)

###Variables and Functions to run. #####################################################################################################################################3
on_Laptop = True

if on_Laptop:
    database_file = r'C:/Users/samsl/Desktop/ScrapeTest/databaseV3.csv'
    test_database_file = r'C:/Users/samsl/Desktop/ScrapeTest/test_databaseV3.csv'
    temp_file = r'C:/Users/samsl/Desktop/ScrapeTest/scrapeV2.csv'

    database_file_lpl = r'C:/Users/samsl/Desktop/ScrapeTest/databaseV3_lpl.csv'
    test_database_file_lpl = r'C:/Users/samsl/Desktop/ScrapeTest/test_databaseV3_lpl.csv'
    temp_file_lpl = r'C:/Users/samsl/Desktop/ScrapeTest/scrapeV2_lpl.csv'

    master_file = r'C:/Users/samsl/Desktop/ScrapeTest/master_combined_database.csv'

    error_url_file = r'C:/Users/samsl/Desktop/ScrapeTest/error_url_list.csv'    
elif not on_Laptop:
    database_file = r'C:/Users/sam/Desktop/ScrapeTest/databaseV3.csv'
    test_database_file = r'C:/Users/sam/Desktop/ScrapeTest/test_databaseV3.csv'
    temp_file = r'C:/Users/sam/Desktop/ScrapeTest/scrapeV2.csv'

    database_file_lpl = r'C:/Users/sam/Desktop/ScrapeTest/databaseV3_lpl.csv'
    test_database_file_lpl = r'C:/Users/samsl/Desktop/ScrapeTest/test_databaseV3_lpl.csv'
    temp_file_lpl = r'C:/Users/sam/Desktop/ScrapeTest/scrapeV2_lpl.csv'

    master_file = r'C:/Users/sam/Desktop/ScrapeTest/master_combined_database.csv'

    error_url_file = r'C:/Users/sam/Desktop/ScrapeTest/error_url_list.csv'

 ########################################################################################################################################################################   
raw_urllist = test_raw_urllist #get_urllist() #
print("got URLs")
iteration_count = 0
start_time = time.time()
error_url_index =[]
error_urls =[]
e_list = []
for url in raw_urllist:
    if not_lpl(url):
        try: #this is only working for one match at the moment. 
            content = get_match_data(url, False) #url, test
            data_list = get_data(content, True)
            print('data_list')
            write_to_csv(data_list, temp_file)
            combine_csv(temp_file, test_database_file)
            iteration_count = iteration_count + 1
            print("completed:", iteration_count)
            time.sleep(0.5)
        except Exception as e:
            print('e',e)
            error_url_index.append(raw_urllist.index(url))
            error_urls.append(url)
            e_list.append(e)
            continue
    else:
        try:
            content = get_match_data_lpl(url, False) #url, test, lpl content
            data_list = get_data_lpl(content, True)
            write_to_csv(data_list, temp_file_lpl)
            combine_csv(temp_file_lpl, test_database_file_lpl)
            iteration_count = iteration_count + 1
            print("completed:", iteration_count)
            time.sleep(0.5)
        except Exception as e:
            print('e', e)
            error_url_index.append(raw_urllist.index(url))
            error_urls.append(url)
            e_list.append(e)
            continue

    #combine into master file
    combine_csv(test_database_file_lpl, test_database_file)
    print ('renaming file')
    os.rename(test_database_file, master_file)

    #collecting all the urls that failed
    write_to_csv(error_urls, error_url_file, e_list )

    #runstats
    print('output_file:', test_database_file)
    print("Run time:", time.time() - start_time )
    print("records:", iteration_count)