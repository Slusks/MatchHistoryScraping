#MatchHistoryScraping

from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException 
import zipfile
import os
import time
import glob
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)
import shutil
import csv
from csv import reader
from bs4 import BeautifulSoup as bs #https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25




# Global variables and start Parameters
mainDirectory = Path(r"F:/LeagueStats/scraping/MatchHistoryScraping/")
pw_directory = Path(r"C:/Users/sam/Documents/riotpw.txt")
chrome_driver = "F:/LeagueStats/scraping/MatchHistoryScraping/chromedriver.exe" # location of chrome driver
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--headless")
# Selenium to load the page
#Launching browser using instructions -> https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test
#Downloaded chrome driver is version 86.0.4240.22
driver = webdriver.Chrome(chrome_driver, options=chrome_options) # open chrome

#fixes the urls so they default to the stat page which hopefully fixes DOM element issues but who knows at this point.
def fix_urls(urllist):
    urllist_fixed = []
    for url in urllist:
        url_fixed = url+'&tab=stats'
        urllist_fixed.append(url_fixed)
    #    if len(url) == 108:
    #    elif len(url) == 126:
    return urllist_fixed

urldf = pd.read_csv(r"F:/LeagueStats/scraping/MatchHistoryScraping/URL.csv") # this includes the URLS for all games that have regular, accessible, matchhistory URLs.
#urldf = pd.read_csv(r"F:/LeagueStats/scraping/MatchHistoryScraping/testURL.csv") # url file for testing fixed number of pages.
urllist = urldf['url'].astype(str).tolist()
urllist_fixed = fix_urls(urllist)

#This is a selenium variable created to wait 30 seconds until pages load.
#Ignore exceptions is to try and avoid the stale element reference exception per:
#https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
ignored_exceptions=(NoSuchElementException, StaleElementReferenceException)
wait = WebDriverWait(driver, 30, ignored_exceptions=ignored_exceptions)


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

# Selenium to grab the champion names and add them to a dictionary
def get_champions():
    print('get_champion running')
    champdict = {}
    champlist =[]
    count = 2
    while count < 12:
        index = str(count)
        my_element_XPATH = '/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div/div[2]/div[3]/div/div/div/table/tbody/tr[1]/td['+index+']/div/div[1]/div'
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, my_element_XPATH)))
        except:
            return(False)
        try:
            champion = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div/div[2]/div[3]/div/div/div/table/tbody/tr[1]/td['+index+']/div/div[1]/div').get_attribute("data-rg-id")
        except:
            return (False)                     
        champ_number = count-1
        champlist.append(champion)
        champdict.update({champ_number : champion})
        count = count + 1
    return (champlist)

# Grab the HTML table data and put it into a list
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

#use the table list to build a dataframe and format it correctly
def build_dataframe(raw_table, champlist, url):
    print('build_dataframe running')
    data_rows = []
    for i in raw_table:
        if len(i) > 1:
            data_rows.append(i)
        else:
            continue
    ###headings = ['headings']
    ###for i in champlist:
    ###    headings.append(i)
    # all of the headings for when we transpose the dataframe
    new_headings = ['KDA', 'Largest Killing Spree', 'Largest Multi Kill', 'First Blood', 'Total Damage to Champions', 'Physical Damage to Champions', 'Magic Damage to Champions', 'True Damage to Champions', 'Total Damage Dealt', 'Physical Damage Dealt', 'Magic Damage Dealt', 'True Damage Dealt', 'Largest Critical Strike', 'Total Damage to Objectives', 'Total Damage to Turrets', 'Damage Healed', 'Damage Taken', 'Physical Damage Taken', 'Magic Damage Taken', 'True Damage Taken', 'Wards Placed', 'Wards Destroyed', 'Stealth Wards Purchased', 'Control Wards Purchased', 'Gold Earned', 'Gold Spent', 'Minions Killed', 'Neutral Minions Killed', "Neutral Minions Killed in Team's Jungle", 'Neutral Minions Killed in Enemy Jungle']

    dataframe = pd.DataFrame(data_rows) #raw dataframe

    dataframe2 = dataframe.transpose() #transpose so it matches the normal Oracle's Elixer format
    print('transposed')
    dataframe2.columns = new_headings #add headings
    print('new headings')
    dataframe2 = dataframe2.drop(0) #drop the now redundant row 0 which held our headings
    print('drop redundant line')

    dataframe2['url'] = url #add a column for our game url for relational purposes
    print('add url')
    dataframe2['champion'] = champlist #add the champions, note we're using the list here which might be risky because lists are unordered
    print('added champions')

    #print(dataframe2) # check for anything funny
    return dataframe2

#drop the dataframe to temp csv file    
def write_to_csv(dataframe):
    print('write_to_csv running')
    dataframe.to_csv(r'F:/LeagueStats/scraping/MatchHistoryScraping/game_data.csv', index=False, header=True) # print to our csv

#add content of temp csv file to database csv.
def combine_csv(match_file, database_file):
    print('combining csv')
    skip_row=[0]
    match_data_container = pd.read_csv(match_file, header=0, skiprows=skip_row, delimiter=',',encoding="utf-8-sig")
    match_data_container.to_csv(database_file, mode="a", index=False)


###############################################################################################################################################################

#Actual function flow starts here
#iterate through url list
url_count = 4717 #this can be set in case there is an error in the code after some number of good iterations
urllist_mod = urllist_fixed[url_count:] #this is how we can start in the middle without resetting the whole thing.
for url in urllist_mod:
    if url_count == 4717:
        driver.get(url) # will redirect to login page
        riot_login() #Login
        print("title: ", driver.title) #grab page title to confirm the page loaded
    else:
        print('get new url: ', url)
        time.sleep(3)
        driver.get(url)

    try:    
        wait.until(EC.element_to_be_clickable((By.ID, 'stats')))
        print('page loaded')
    except:
        driver.get(url)
        wait.until(EC.element_to_be_clickable((By.ID, 'stats')))
        print('---RELOADED PAGE---')
        pass


    page_source = driver.page_source # I believe this is how you pass off control of the web page to BS below.
    #get a list of champion names for that match
    champlist = get_champions()
    if not champlist:
        driver.get(url)
        champlist = get_champions()
        print ('---RELOADED CHAMP---')



    time.sleep(1)

    #beautiful soup to pull the data
    soup = bs(page_source, 'lxml')
    table = soup.find_all('table')[0] # Grab the first table
    time.sleep(1)

    output_table = create_table(table)
    new_dataframe = build_dataframe(output_table, champlist, url)
    time.sleep(1)
    #print(new_dataframe)
    write_to_csv(new_dataframe)
    #making sure we dont get limited by accessing too many match histories per minute
    time.sleep(1)
    # adding the new match data into the total database
    match_data = r'F:/LeagueStats/scraping/MatchHistoryScraping/game_data.csv'
    database_file = r'F:/LeagueStats/scraping/MatchHistoryScraping/match_database.csv'
    combine_csv(match_data, database_file)

    url_count = url_count + 1
    if url_count % 10 != 0:
        print('sleeping 3')
        time.sleep(3)
    elif url_count % 10 == 0:
        print('sleeping 10')
        time.sleep(10)
    print('URL Count', url_count)
 


    

