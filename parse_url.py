import pandas as pd
def get_urllist():
    l = []
    url_file = r"F:/LeagueStats/scraping/MatchHistoryScraping/data/URL.csv"
    out_url_list = r'C:/Users/sam/Desktop/ScrapeTest/urllist.csv'
    file = pd.read_csv(url_file, header=0)
    l = list(file.url)
    single = list(set(l))
    print (len(single))
    return (single)


