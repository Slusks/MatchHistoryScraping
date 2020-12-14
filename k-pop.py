from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
import csv
from csv import reader

old_file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\match_database_characters_removed.csv")
new_file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\match_database_KDA_split.csv")

def kda_what(old_file, new_file):
    open_file = open(old_file, encoding='utf-8')
    read_file = csv.reader(open_file)
    with open(new_file, 'w', encoding='utf-8', newline='') as output_file:
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
                for j,i in enumerate(row):
                    if j == 0: #will need to split on the / probably
                        new_i = i.split('/')
                        for item in new_i:
                            new_row.append(item)
                    elif j > 29: #make sure we dont remove any K's from URL's or champion names which are always the last 2 row indices
                        #print('index over 29')
                        new_row.append(i)
                    else:
                        if 'k' in i: #removing the K's from the damage numbers and then multiplying the remaining value by 1000 to get a number
                            new_i = i.replace('k','')
                            try:
                                new_i = 1000*(float(new_i))
                                new_row.append(new_i)
                            except:
                                print(row)
                        elif 'mil' in i: #removing the mils from the portuguese entries
                            new_i = i.replace('mil','')
                            new_i = 1000*(float(new_i))
                            new_row.append(new_i)
                        elif 'тыс' in i: #removing the тыс from the LCL entries
                            new_i = i.replace(' тыс.','')
                            try:
                                new_i = 1000*(float(new_i))
                            except ValueError as e:
                                print(row)
                                print(e)
                            new_row.append(new_i)
                        elif '-' in i: # all locations where there is a '-' is just a 0 value to replacing that. 
                            new_i = 0
                            new_row.append(new_i)
                        else:
                            new_row.append(i)
            output.writerow(new_row)
    
kda_what(old_file, new_file)

# KDA,
# Largest Killing Spree,
# Largest Multi Kill,
# First Blood,
# Total Damage to Champions,
# Physical Damage to Champions,
# Magic Damage to Champions,
# True Damage to Champions,
# Total Damage Dealt,
# Physical Damage Dealt,
# Magic Damage Dealt,
# True Damage Dealt,
# Largest Critical Strike,
# Total Damage to Objectives,
# Total Damage to Turrets,
# Damage Healed,
# Damage Taken,
# Physical Damage Taken,
# Magic Damage Taken,
# True Damage Taken,
# Wards Placed,
# Wards Destroyed,
# Stealth Wards Purchased,
# Control Wards Purchased,
# Gold Earned,
# Gold Spent,
# Minions Killed,
# Neutral Minions Killed,
# Neutral Minions Killed in Team's Jungle,
# Neutral Minions Killed in Enemy Jungle,
# url,
# champion