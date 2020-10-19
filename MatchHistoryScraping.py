#MatchHistoryScraping

from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
import zipfile
import os
import time
import glob
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)
import shutil
import csv
from bs4 import BeautifulSoup as bs #https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25




# Global variables and start Parameters
chrome_driver = "F:/LeagueStats/scraping/LeagueMatchDataScraping/chromedriver.exe" # location of chrome driver
driver = webdriver.Chrome(chrome_driver) # open chrome


urldf = pd.read_csv(r"F:/LeagueStats/scraping/LeagueMatchDataScraping/URL.csv") # this includes the URLS for all games that have regular, accessible, matchhistory URLs.
urllist = 'https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT05/1390263?gameHash=11c29bbfef59b453&amp;tab=overview' #urldf['url'].astype(str).tolist()
destinationFolder = Path(r"F:/LeagueStats/scraping/LeagueMatchDataScraping/downloads") #this will be used in later production
riot_login_url = ''

#This is a selenium variable created to wait 20 seconds until pages load.
wait = WebDriverWait(driver, 20)



###
mainDirectory = Path(r"F:/LeagueStats/scraping/LeagueMatchDataScraping/")
pw_directory = Path(r"C:/Users/sam/Documents/riotpw.txt")
###

print(mainDirectory)

#login to riot games account
def riot_login():
    print('Running Login')
    username = 'thanatos0512'
    pw = open(pw_directory, 'r')
    password = pw.read()
    #https://stackoverflow.com/questions/56380889/wait-for-element-to-be-clickable-using-python-and-selenium
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
    wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.XPATH , "/html/body/div/div/div/div[2]/div[1]/div/button"))).click()

#function to send the URL to the search bar
def go_to_match_history(url):
    print('go_to_match_history running')
    driver.get(url)
    print(url)
    time.sleep(10)

# Selenium to grab the champion names and add them to a dictionary
def get_champions():
    print('get_champion running')
    champdict = {}
    champlist =[]
    count = 2
    while count < 12:
        index = str(count)
        champion = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div/div[2]/div[3]/div/div/div/table/tbody/tr[1]/td['+index+']/div/div[1]/div').get_attribute("data-rg-id")
        champ_number = count-1
        champlist.append(champion)
        champdict.update({champ_number : champion})
        count = count + 1
    return (champlist)


def create_table(table):
    print('create_table running')
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_columns = []
        for column in columns:
            divs = column.find_all('div')
            for div in divs:
                if div.get_text():
                    text = div.get_text()
                    #print('div text', div.get_text())
                elif div.get_text() == '-':
                    text = '0'
                else:
                    continue
                output_columns.append(text)
        output_rows.append(output_columns) #this is where we make the list of rows
    return output_rows

#output_rows now contains a list of rows, where each row is either a heading, or an 11 element list where 
# element[0] is the title 
# element[1]-[10] are the statistics of interest.
# https://www.geeksforgeeks.org/creating-pandas-dataframe-using-list-of-lists/


def build_dataframe(raw_table, champlist):
    print('build_dataframe running')
    data_rows = []
    for i in raw_table:
        if len(i) > 1:
            data_rows.append(i)
        else:
            continue
    headings = ['headings']
    for i in champlist:
        headings.append(i)
    # all of the headings for when we transpose the dataframe
    new_headings = ['KDA', 'Largest Killing Spree', 'Largest Multi Kill', 'First Blood', 'Total Damage to Champions', 'Physical Damage to Champions', 'Magic Damage to Champions', 'True Damage to Champions', 'Total Damage Dealt', 'Physical Damage Dealt', 'Magic Damage Dealt', 'True Damage Dealt', 'Largest Critical Strike', 'Total Damage to Objectives', 'Total Damage to Turrets', 'Damage Healed', 'Damage Taken', 'Physical Damage Taken', 'Magic Damage Taken', 'True Damage Taken', 'Wards Placed', 'Wards Destroyed', 'Stealth Wards Purchased', 'Control Wards Purchased', 'Gold Earned', 'Gold Spent', 'Minions Killed', 'Neutral Minions Killed', "Neutral Minions Killed in Team's Jungle", 'Neutral Minions Killed in Enemy Jungle']

    dataframe = pd.DataFrame(data_rows) #raw dataframe

    dataframe2 = dataframe.transpose() #transpose so it matches the normal Oracle's Elixer format
    print('transposed')
    dataframe2.columns = new_headings #add headings
    print('new headings')
    dataframe2 = dataframe2.drop(0) #drop the now redundant row 0 which held our headings
    print('drop redundant line')

    dataframe2['url'] = urllist[0] #add a column for our game url for relational purposes
    print('add url')
    dataframe2['champion'] = champlist #add the champions, note we're using the list here which might be risky because lists are unordered
    print('added champions')

    #print(dataframe2) # check for anything funny
    return dataframe2
    
def write_to_csv(dataframe):
    print('write_to_csv running')
    dataframe.to_csv(r'F:/LeagueStats/scraping/game_data.csv', index=False, header=True) # print to our csv


#TO DO LIST
# - take CSV generated here and add it to a master CSV
# - Build in iteration so this can run across all of the urls
# - run

# Selenium to load the page
#Launchring browser using instructions -> https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test
#Downloaded crhome driver is version 86.0.4240.22
###############################################################################################################################################################

#Actual function flow starts here
#iterate through url list
url_count = 1
for url in urllist:
    if url_count == 1:
        driver.get(urllist) # will redirect to login page
        riot_login() #Login
        print("title: ", driver.title) #grab page title to confirm the page loaded
    else:
        driver.get(url)
    
    #go_to_match_history(urllist)

    wait.until(EC.element_to_be_clickable((By.ID, "tab-695"))).click() #Go to the statistics section of the page
    page_source = driver.page_source # I believe this is how you pass off control of the web page to BS below.

    #get a list of champion names for that match
    champlist = get_champions()

    #beautiful soup to pull the data
    soup = bs(page_source, 'lxml')
    table = soup.find_all('table')[0] # Grab the first table

    output_table = create_table(table)
    new_dataframe = build_dataframe(output_table, champlist)

    write_to_csv(new_dataframe)
    
    #making sure we dont get limited by accessing too many match histories per minute
    print('sleeping')
    url_count = url_count + 1
    time.sleep(10)

