import requests
import re
from requests.auth import HTTPBasicAuth
import time
import pandas as pd
import pprint
from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
from cookie_monster import COOKIE
import csv



#Variables and Headers - wont need this until we're processing the text files
# format: scraped headers: oracle's elixer header
#Scraped headers: headers to add to table
###Basically, key = scraped value, value = desired value
    #So I honestly can't remember if this is just filling in holes from Oracle's Elixer tables or if this is supposed to be all information, so it definitely contains some gaps
    #in the information it contains.
full_headers_dict = {"magicDamageDealt":"totalmagicdamagedealt", "physicalDamageDealt":"totalphysicaldamagedealt", "physicalDamageTaken":"physicaldamagetaken", "kills":"kills","deaths":"deaths","assists":"assists", 'firstBloodKill': 'firstblood', 'totalDamageDealtToChampions': 'totaldamagetochampions', 'physicalDamageDealtToChampions': 'physicaldamagetochampions', 'magicDamageDealtToChampions': 'magicdamagetochampions', 'trueDamageDealtToChampions': 'truedamagetochampions', 'damageDealtToObjectives': 'totaldamagetoobjectives', 'damageDealtToTurrets': 'totaldamagetoturrets', 'totalHeal': 'damagehealed', 'totalDamageTaken': 'damagetaken', 'magicalDamageTaken': 'magicdamagetaken', 'wardsKilled': 'wardsdestroyed', 'sightWardsBoughtInGame': 'stealthwardspurchased', 'visionWardsBoughtInGame': 'controlwardspurchased', 'totalMinionsKilled': 'minionskilled', 'neutralMinionsKilledTeamJungle': "neutralminionskilledinteam'sjungle", 'neutralMinionsKilledEnemyJungle': 'neutralminionskilledinenemyjungle', 'killingSprees': 'killingsprees', 'longestTimeSpentLiving': 'longesttimespentliving', 'damageSelfMitigated': 'selfmitigateddamage', 'visionScore': 'visionscore', 'timeCCingOthers': 'timeccingothers', 'turretKills': 'totalTurretKills', 'inhibitorKills': 'totalInhibitorKills', 'totalTimeCrowdControlDealt': 'totaltimeapplyingcc', 'firstBloodAssist': 'firstbloodassist', 'firstTowerKill': 'firsttowerkill', 'firstTowerAssist': 'firsttowerassist', 'firstInhibitorKill': 'firstinhibkill', 'firstInhibitorAssist': 'firstinhibassist', 'doubleKills': 'doublekills', 'tripleKills': 'triplekills', 'quadraKills': 'quadrakills', 'pentaKills': 'pentakills', 'goldEarned':'goldearned', 'goldSpent': 'goldspent', "largestCriticalStrike":"largestcriticalstrike", "largestKillingSpree":"largestkillingspree", "largestMultiKill":"largestmultikill"}

#Function that grabs the URL list from a csv
def get_urllist():
    l = []
    url_file = r"F:/LeagueStats/scraping/MatchHistoryScraping/data/URL.csv"
    file = pd.read_csv(url_file, header=0)
    l = list(file.url)
    single = list(set(l))
    if len(single) > 5:
        return (single)

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
"https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/660033?gameHash=3ae31e7697461999&amp;tab=overview,False",
"https://lpl.qq.com/es/stats.shtml?bmid=7325",
"https://lpl.qq.com/es/stats.shtml?bmid=7325"
]

single_url = "https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/660033?gameHash=3ae31e7697461999&amp;tab=overview,False"

longer_raw_urllist =['http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/80532?gameHash=ebf3b1a721dc6fde&amp;tab=overview', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/TRLH1/1002210083?gameHash=9ed4c4cb1c26a1ec&amp;tab=overview', 'https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/1384397?gameHash=2c834113f5dc5d1a&amp;tab=overview', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/1180492?gameHash=861f480faed92b0a', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/TREU/1001490197?gameHash=c1d99cbca313dd17&amp;tab=overview', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT01/1310941?gameHash=d9ada7733493c79c', 'https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT01/1321280?gameHash=294b476f65218cfe&amp;tab=overview', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/1300358?gameHash=20b575528c3d1ab9', 'https://matchhistory.na.leagueoflegends.com/en/#match-details/TRLH1/1002520246?gameHash=175bf6e0da0ff375', 'http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/170093?gameHash=47e0556f123b2106&amp;tab=overview'] 

#table_headers = ["kills","deaths","assists","Largest Killing Spree","Largest Multi Kill","First Blood","Total Damage to Champions","Physical Damage to Champions","Magic Damage to Champions","True Damage to Champions","Total Damage Dealt","Physical Damage Dealt","Magic Damage Dealt","True Damage Dealt","Largest Critical Strike","Total Damage to Objectives","Total Damage to Turrets","Damage Healed","Damage Taken","Physical Damage Taken","Magic Damage Taken","True Damage Taken","Wards Placed","Wards Destroyed","Stealth Wards Purchased","Control Wards Purchased","Gold Earned","Gold Spent","Minions Killed","Neutral Minions Killed","Neutral Minions Killed in Team's Jungle","Neutral Minions Killed in Enemy Jungle","url","champion"]



#fixes URL into the form that it needs to be for scraping
#This will only work for non-LPL matches at this time.
def url_for_request_scraping(raw_url):
    cut = raw_url.split("#match-details/")[1].split("&amp;tab=overview,Unnamed: 31False")[0]
    new_url = "https://acs.leagueoflegends.com/v1/stats/game/"+cut
    return (new_url)

def url_for_lpl_scraping(raw_url):
    base_url = "https://lpl.qq.com/web201612/data/LOL_MATCH_DETAIL_"
    js = ".js"
    match_num = raw_url[-4:]
    new_url = base_url + match_num + js
    return (new_url)

# Starting in your browser, select the "cookie" content from your network request AFTER you've logged in. It should
# look similar to the following:


# Format your cookie into a dictionary form
user_cookie = dict()

for item in COOKIE.split("; "):
    k, v = item.split("=")
    user_cookie[k] = v

#Functions that only run once
#This is pulling the champion data.
champ_dd = requests.get("https://ddragon.leagueoflegends.com/cdn/11.8.1/data/en_US/champion.json", cookies=user_cookie)
champ_json = champ_dd.json()
champ_name = champ_json["data"] #this creates a list of all the champions
champ_key_dict = {}
for i in champ_name:
    champ_key_dict.update({champ_json["data"][i]["key"]:i})
#pprint.pprint(champ_dd.json())

### Creating the headers
x = ["player", "champion"]
headers_list = list(full_headers_dict.keys())
z = ["gameId"]
table_headings = x+headers_list+z

#get request that needs to be looped
def get_match_data(url, test, lpl):
    if lpl:
        good_url = url_for_lpl_scraping(url)
    else:
        good_url = url_for_request_scraping(url)
    json_file = requests.get(good_url, cookies=user_cookie)
    assert json_file.status_code == 200
    json_content = json_file.json()
    if test == True:
        pprint.pprint(json_content)
    return(json_content)

 
# Take the json data, combine it into a list of lists
################################## THIS FUNCTION IS NOT WORKING
def get_data(json_content, test):
    count = 0
    list_list = []
    while count < 10:
        outputlist = []
        player = json_content["participantIdentities"][count]["player"]["summonerName"]
        champion_id = json_content["participants"][count]["championId"]
        gameId = json_content["gameId"]
        outputlist.append(player)
        outputlist.append(champ_key_dict[str(champion_id)])
        for i in  full_headers_dict: #This is an issue. Didn't actually capture all the possible headers
            if i in headers_list:
                outputlist.append(json_content["participants"][count]["stats"][i]) #this line doesn't work
        outputlist.append(gameId)
        list_list.append(outputlist)
        count += 1
        print('count:', count)
    return (list_list)

#this has to be way worked on with data from LPL decoding
def get_data_lpl(json_content):
    print('get_data')
    count = 0
    list_list = []
    while count < 10:
        outputlist = []
        player = json_content["participantIdentities"][count]["player"]["summonerName"]
        champion_id = json_content["participants"][count]["championId"]
        gameId = json_content["gameId"]
        outputlist.append(player)
        outputlist.append(champ_key_dict[str(champion_id)])
        for i in  full_headers_dict: #This is an issue. Didn't actually capture all the possible headers
            if i in headers_list:
                outputlist.append(json_content["participants"][count]["stats"][i])
        outputlist.append(gameId)
        list_list.append(outputlist)
        count +=1
    return (list_list)

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



###Running Function
database_file = r'C:/Users/sam/Desktop/ScrapeTest/databaseV3.csv'
test_database_file = r'C:/Users/sam/Desktop/ScrapeTest/test_databaseV3.csv'
temp_file = r'C:/Users/sam/Desktop/ScrapeTest/scrapeV2.csv'
error_url_file = r'C:/Users/sam/Desktop/ScrapeTest/error_url_list.csv'
raw_urllist = test_raw_urllist #get_urllist() #
print("got URLs")
iteration_count = 0
start_time = time.time()
error_url_index =[]
error_urls =[]
test = 0
for url in raw_urllist:
    try:
        content = get_match_data(url, False, False) #url, test, lpl content
        data_list = get_data(content, True)
        print('data_list')
        write_to_csv(data_list)
        combine_csv(temp_file, test_database_file)
        iteration_count = iteration_count + 1
        print("completed:", iteration_count)
        time.sleep(0.5)
    except:
        #print('error url:',raw_urllist.index(url))
        error_url_index.append(raw_urllist.index(url))
        error_urls.append(url)
        continue
    #collecting all the urls that failed
    write_to_csv(error_urls, error_url_file )
    #runstats
    print('output_file:', test_database_file)
    print("Run time:", time.time() - start_time )
    print("records:", iteration_count)