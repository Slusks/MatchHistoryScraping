import json

#https://hackersandslackers.com/extract-data-from-complex-json-python/

file = "C:/Users/40001073/Python/MatchHistoryScraping/json_raw_matchHistory.json"
head = ["Largest Killing Spree","Largest Multi Kill","First Blood","Total Damage to Champions","Physical Damage to Champions","Magic Damage to Champions","True Damage to Champions","Total Damage Dealt","Physical Damage Dealt","Magic Damage Dealt","True Damage Dealt","Largest Critical Strike","Total Damage to Objectives","Total Damage to Turrets","Damage Healed","Damage Taken","Physical Damage Taken","Magic Damage Taken","True Damage Taken","Wards Placed","Wards Destroyed","Stealth Wards Purchased","Control Wards Purchased","Gold Earned","Gold Spent","Minions Killed","Neutral Minions Killed","Neutral Minions Killed in Team's Jungle","Neutral Minions Killed in Enemy Jungle","url","champion"]

f = open(file)

data = json.load(f)


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


players = json_extract(data,"summonerName")

#print(data['participants'])
KS = json_extract(data, "largestKillingSpree")
P = set(json_extract(data, "participantId"))
print(players)
print(P, KS)

#print("len", len(out))
