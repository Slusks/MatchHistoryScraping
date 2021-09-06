from pathlib import Path 
import csv
from csv import reader
import pandas as pd
import re
from datetime import datetime
import os
import shutil
now = datetime.now()

####################################################################################################################
## Files and Procedure ##

#0. Scrape the match history taken from SQL/Oracles Elixer
#MatchHistoryScraping.py

#1. Scraped file:
scraped_file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\data\delinquent_match_database.csv") 

#2. Remove First Blood Dot
first_blood_fixed = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\cleaning files\match_database_FB_Fixed.csv") 

#3. Remove unwanted characters and langauges via regex
characters_removed = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\cleaning files\match_database_characters_removed.csv")

#4. convert KDA and clean out the bad characters
kda_fixed = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\cleaning files\match_database_KDA_split.csv")

#5. Trim the urls so they match the oracle's elixer urls
fixed_url_for_sql = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\cleaning files\match_database_for_sql.csv")

#6. Remove rows with a bad champion reference
champ_list = ['Jayce', 'JarvanIV', 'Orianna', 'MissFortune', 'Nautilus', 'Aatrox', 'Elise', 'Qiyana', 'Varus', 'TahmKench', 'Renekton', 'RekSai', 'Mordekaiser', 'Xayah', 'Rakan', 'Sejuani', 'Azir', 'Pantheon', 'Quinn', 'Olaf', 'Leona', 'Ryze', 'Velkoz', 'Braum', 'Kennen', 'Ornn', 'Vladimir', 'LeeSin', 'Rumble', 'Thresh', 'Camille', 'Fizz', 'Syndra', 'Senna', 'Irelia', 'Ekko', 'Hecarim', 'Sivir', 'Cassiopeia', 'Gragas', 'Lucian', 'Aphelios', 'Zoe', 'Sylas', 'Bard', 'Gangplank', 'Leblanc', 'Yasuo', 'Malphite', 'DrMundo', 'Diana', 'Swain', 'Urgot', 'Ezreal', 'Kaisa', 'Taliyah', 'Zac', 'Karthus', 'Nocturne', 'Nidalee', 'Kassadin', 'Veigar', 'Viktor', 'Ashe', 'Trundle', 'Riven', 'Blitzcrank', 'Zilean', 'Tristana', 'Sett', 'Alistar', 'Galio', 'Annie', 'Fiora', 'Akali', 'Kindred', 'Shyvana', 'Soraka', 'Lulu', 'XinZhao', 'Poppy', 'Maokai', 'Morgana', 'Lissandra', 'Rengar', 'Kayle', 'Karma', 'Sona', 'Kled', 'Ziggs', 'Skarner', 'Jhin', 'Gnar', 'Xerath', 'Chogath', 'Kalista', 'Taric', 'Yuumi', 'Illaoi', 'Yorick', 'Zyra', 'Shen', 'Vayne', 'Heimerdinger', 'Nami', 'Draven', 'Pyke', 'Ahri', 'Malzahar', 'Darius', 'Caitlyn', 'AurelionSol', 'Tryndamere', 'MasterYi', 'Ivern', 'Graves', 'Twitch', 'Singed', 'Jinx', 'Corki', 'Neeko', 'Sion', 'Lux', 'Khazix', 'Volibear', 'Shaco', 'Anivia', 'Warwick', 'Janna', 'Amumu', 'Zed', 'KogMaw', 'Jax', 'MonkeyKing', 'Teemo', 'Brand', 'Nunu', 'Talon', 'Fiddlesticks', 'Evelynn', 'TwistedFate', 'Kayn', 'Katarina', 'Vi', 'Rammus', 'Lillia', 'Garen', 'Nasus', 'Udyr', 'Yone', 'Rell', 'Wukong']
rows_missing_champs_removed = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\cleaning files\match_database_fixed_missing_champs_removed.csv")
rows_missing_champs_stored = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\cleaning files\match_database_fixed_missing_champs_stored.csv")


#7. Remove all the duplicate lines
duplicate_lines_removed = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\cleaning files\match_database_duplicates_removed.csv")

#8. take completely clean file and store with a name that says when it was cleaned




########################################################################################################################
## FUNCTIONS ##

#checks for duplicates and rows that are missing a champion
def check_file(file):
    print('Check File Running')
    df = pd.read_csv(file)
    duplicate = df[df.duplicated()]
    bad = df[df['champion']=='False']['url'].values
    #bad_list = bad.tolist()
    blank = df[df['champion']=='']['url'].values
    print('Info:', df.info() )
    print("Duplicate Rows:")
    print(duplicate)
    print(len(duplicate))
    print("Bad Rows:")
    print(bad)
    print(len(bad))
    print("Awful Rows:")
    print(blank)
    print(len(blank))
    return df

#takes the data file and trades out the dot for a 0 or 1 in the first blood column - from dot.py
def dot_to_binary(old_file, fixed_file):
    print('dot to binary running')
    open_file = open(old_file, encoding='utf-8')
    read_file = csv.reader(open_file)
    next(read_file)
    data = ""
    with open(old_file, encoding='utf-8') as file:
        data = file.read().replace('●','1').replace('○','0')
    with open(fixed_file, 'w', encoding='utf-8') as file:
        file.write(data)

#removes unwanted characters via regex
def character_cleanup(input_file, output_file):
    print('character cleanup running')
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

#remove KDA column and replace with 3 columns for k, d, and a, also fixes numerical values. 
def kda_what(old_file, new_file):
    print('kda what running')
    open_file = open(old_file, encoding='utf-8')
    read_file = csv.reader(open_file)
    with open(new_file, 'w', encoding='utf-8') as output_file:
        output = csv.writer(output_file)
        count = 0
        for row in read_file:
            new_row = []
            if count == 0: #splitting the KDA header into a k, d, and a header.
                kda_row = ['kills', 'deaths', 'assists']
                new_head_row = row[1:]
                for i in new_head_row:
                    kda_row.append(i)
                output.writerow(kda_row)
                count = count+1
                print('head added')
            else:
                for i in row:
                    if row.index(i) == 0: #will need to split on the / probably
                        new_i = i.split('/')
                        for item in new_i:
                            new_row.append(item)
                    elif row.index(i) > 29: #make sure we dont remove any K's from URL's or champion names which are always the last 2 row indices
                        #print('index over 29')
                        new_row.append(i)
                    else:
                        if 'k' in i: #removing the K's from the damage numbers and then multiplying the remaining value by 1000 to get a number
                            try:
                                new_i = i.replace('k','')
                                new_i = 1000*(float(new_i))
                                new_row.append(new_i)
                            except:
                                print('bad row:', row)
                        elif '-' in i: # all locations where there is a '-' is just a 0 value to replacing that. 
                            new_i = 0
                            new_row.append(new_i)
                        else:
                            new_row.append(i)
            output.writerow(new_row)

#fixes urls that have had the stat endpoint added - from cleaningURLs.py
def url_trim_108(x):
    try:
        if len(x) != 108:
            return x[:-10]
        else:
            #print('fine')
            return x
    except:
        return x

#fixes urls that dont have the full tab endpoint removed - from cleaningURLs.pyt
def url_fix_ta(x):
    try:
        if len(x) == 116:
            if x[-3:]==';ta':
                return x+'b=overview'
            else:
                return x
        else:
            #print('also fine')
            return x
    except:
        return x

#replaces MonkeyKing with Wukong
def long_live_the_king(x):
    try:
        if x=='MonkeyKing':
            return 'Wukong'
        else:
            return x
    except:
        return x 

#drops rows that dont have a champion in them, or have a bad champ reference like unnamed: 31
def drop_False_champ(old, new_good, store_bad):
    print('drop False champ running')
    df = pd.read_csv(old)
    new_df = df[df.champion.isin(champ_list)]
    bad_rows = df[~df.champion.isin(champ_list)]
    new_df.to_csv(new_good, index=False, header=True)
    bad_rows.to_csv(store_bad, index=False, header=True)

#drops duplicate rows
def drop_dup(old_file, new_file):
    print('drop dup running')
    df = pd.read_csv(old_file)
    no_dup = df.drop_duplicates()
    no_dup.to_csv(new_file, index=False, header=True)

#write whatever we ended up with to a master database.
def write_to_master(input_file):
    today = now.strftime("%m-%d-%Y_%H-%M")
    master_file_name = r"\master_file_dtd_" + today + ".csv"
    target_directory = r"F:\LeagueStats\scraping\MatchHistoryScraping\cleaning files"
    full_master_file_name = Path(target_directory + master_file_name)
    shutil.copy(input_file, full_master_file_name)
    print("New file created:", today)

#####################################################################################################################
## RUN FUNCTIONS ##

#Start
#Fixing first blood dot
dot_to_binary(scraped_file, first_blood_fixed)

#regex cleanup of languages and trailing '.#'s
character_cleanup(first_blood_fixed, characters_removed)

#takes the scraped file and cleans all the characters that shouldn't be there
#also seperates out the KDA column
kda_what(characters_removed, kda_fixed)



#fixes the urls in the dataframe to match what's in oracle's elixer
df2 = pd.read_csv(kda_fixed)
df2['url'] = df2['url'].apply(lambda x: url_trim_108(x))
print('url trim running')
df2['url'] = df2['url'].apply(lambda x: url_fix_ta(x))
print('fix ta running')
df2['champion'] = df2['champion'].apply(lambda x: long_live_the_king(x))
print("Long Live The King")
df2.to_csv(fixed_url_for_sql, index = False, header = True)

data_frame_trimmed_url = pd.read_csv(fixed_url_for_sql)

######
## INTERLUDE ##
# at this point we have a file that is sql usable all the way until the last row, which is going to have either a champion or not a champion
# we now need to figure out what rows are good and what rows dont have a champion.
######

#takes out the rows with a bad champion reference and puts them in another file
drop_False_champ(fixed_url_for_sql, rows_missing_champs_removed, rows_missing_champs_stored)


#drops duplicate rows that are left in the working file
drop_dup(rows_missing_champs_removed, duplicate_lines_removed)


#This writes the final file without the duplicates in it to a seperate file and adds a time stamp
write_to_master(duplicate_lines_removed)


#checks what's left after rows missing champions are removed
#df = check_file(rows_missing_champs_removed)








