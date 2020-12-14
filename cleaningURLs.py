import pandas as pd
from pathlib import Path
import time

#match data scraped from internet
file = Path(r"F:\LeagueStats\scraping\MatchHistoryScraping\match_database.csv")

df = pd.read_csv(file)


#urls from complete_league_stats from my sql and therefore oracles elixer
urlfile = Path(r"F:\LeagueStats\scraping\non_lpl_url.csv")

urldf = pd.read_csv(urlfile)
oe_urllist = urldf['url'].tolist() #list containing all of the urls from oracle's elixer


#urls from the scraped files
sc_urllist = df['url'].tolist() #list containing all of the urls that we scraped
leave = [108]
cut_10 = [108, 109, 110, 113, 114, 115, 116, 117, 118, 119, 120, 124, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 146, 150]

def check_URL_Matching(oracle_list, scraped_list):
    print("check URL Start")
    #url_lengths = []
    match_urls = []
    no_match_urls = []
    for i in scraped_list:
        #url_lengths.append(len(i))
        if i not in oracle_list:
            no_match_urls.append(i)
        else:
            match_urls.append(i)
    print("matches:", len(match_urls))
    print("weirdos:", len(no_match_urls))
    #print("url lengths:", sorted(set(url_lengths)))

#check_URL_Matching(oe_urllist, sc_urllist)
def url_trim_108(x):
    try:
        if len(x) != 108:
            return x[:-10]
        else:
            print('fine')
            return x
    except:
        return x

def url_fix_ta(x):
    try:
        if len(x) == 116:
            if x[-3:]==';ta':
                return x+'b=overview'
            else:
                return x
        else:
            print('also fine')
            return x
    except:
        return x




df2 = df
start_time = time.perf_counter()
count = 0
df2['url'] = df2['url'].apply(lambda x: url_trim_108(x))
df2['url'] = df2['url'].apply(lambda x: url_fix_ta(x))


sc_urllist2 = df2['url'].tolist()
end_time = time.perf_counter()
t_time = end_time - start_time
print('time:', t_time)



check_URL_Matching(oe_urllist, sc_urllist2)

