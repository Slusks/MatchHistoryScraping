# MatchHistoryScraping
 Version 1: Scraping League match history with selenium and Bs4
    - Slow
    - Unreliable
    - required significant data cleaning
    - Would time out and then needed to be restarted at last record
    - Runtime anecdotes
        - 12.5 seconds per record
        - 4 or 5 days to run

 Version 2: Scraping only the english URLs using Requests and pandas
    - Fast
    - Reliable
    - required some data cleaning
    - not robust
    - Runtime facts (6/9/2021)
        20459 records
        897 errors
        Runtime: 5 hours 24 minutes
        Avg time per record: 1.05 seconds
        Success rate: 95.6%

Version 3: Same as above but for all match types with additional error handling
    - Medium speed
    - Reliable
    - Integrated some of the data cleaning. Will probably finish most of the cleaning in SQL
    - Robust and easier to trouble shoot
    - Runtime facts (9/6/2021):
        42212 records
        892 errors
        Runtime: 7 hours 52 minutes
        Avg time per record: 1.47 seconds.
        Success rate: 97.89%

Version 4 TBD:
    - Will have to find new place to pull non-lpl data from if this is going to be continued.


