# https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/1160644?gameHash=744c3e9779ad519c&amp;tab=overview,Unnamed:&tab=stats
#Aatrox Scoreline

#normal table headers
oracle_headers = ['kills', 'deaths', 'assists', 'largestkillingspree',
 'largestmultikill', 'firstblood', 'totaldamagetochampions',
  'physicaldamagetochampions', 'magicdamagetochampions', 'truedamagetochampions', 'totaldamagedealt', 
  'physicaldamagedealt', 'magicdamagedealt', 'truedamagedealt', 'largestcriticalstrike', 
  'totaldamagetoobjectives', 'totaldamagetoturrets', 'damagehealed', 'damagetaken', 'physicaldamagetaken', 
  'magicdamagetaken', 'truedamagetaken', 'wardsplaced', 'wardsdestroyed', 'stealthwardspurchased', 
  'controlwardspurchased', 'goldearned', 'goldspent', 'minionskilled', 'neutralminionskilled', 
  "neutralminionskilledinteam'sjungle", 'neutralminionskilledinenemyjungle', 'url', 'champion']


# format: scraped headers: oracle's elixer header
headers_to_convert = {'firstBloodKill': 'firstblood',
'totalDamageDealtToChampions':'totaldamagetochampions',
'physicalDamageDealtToChampions':'physicaldamagetochampions',
'magicDamageDealtToChampions':'magicdamagetochampions',
'trueDamageDealtToChampions':'truedamagetochampions', 
'damageDealtToObjectives':'totaldamagetoobjectives',
'damageDealtToTurrets':'totaldamagetoturrets',
'totalHeal': 'damagehealed',
'totalDamageTaken':'damagetaken', 
'magicalDamageTaken':'magicdamagetaken',
'wardsKilled': 'wardsdestroyed', 
'sightWardsBoughtInGame':'stealthwardspurchased', 
'visionWardsBoughtInGame':  'controlwardspurchased',
'totalMinionsKilled':  'minionskilled', 
'neutralMinionsKilledTeamJungle': "neutralminionskilledinteam'sjungle",
'neutralMinionsKilledEnemyJungle':'neutralminionskilledinenemyjungle',
}
#Scraped headers: headers to add to table
headers_to_add = {'killingSprees': 'killingsprees' ,
'longestTimeSpentLiving':'longesttimespentliving',
'damageSelfMitigated':'selfmitigateddamage',
'visionScore':'visionscore',
'timeCCingOthers': 'timeccingothers',
'turretKills':'totalTurretKills',
'inhibitorKills':'totalInhibitorKills',
'totalTimeCrowdControlDealt':'totaltimeapplyingcc',
'firstBloodAssist': 'firstbloodassist',
'firstTowerKill':'firsttowerkill',
'firstTowerAssist': 'firsttowerassist',
'firstInhibitorKill':'firstinhibkill',
'firstInhibitorAssist':'firstinhibassist',
'doubleKills': 'doublekills',
'tripleKills': 'triplekills',
'quadraKills':'quadrakills',
'pentaKills':'pentakills',

}


##########################################

###Gotta make a function that converts the headings or adds new ones.

def header_converter(heading_input):
    #combination of the headers to convert and the headers to add
    header_dict ={
      'killingSprees': 'killingsprees' ,
      'longestTimeSpentLiving':'longesttimespentliving',
      'damageSelfMitigated':'selfmitigateddamage',
      'visionScore':'visionscore',
      'timeCCingOthers': 'timeccingothers',
      'turretKills':'totalTurretKills',
      'inhibitorKills':'totalInhibitorKills',
      'totalTimeCrowdControlDealt':'totaltimeapplyingcc',
      'firstBloodAssist': 'firstbloodassist',
      'firstTowerKill':'firsttowerkill',
      'firstTowerAssist': 'firsttowerassist',
      'firstInhibitorKill':'firstinhibkill',
      'firstInhibitorAssist':'firstinhibassist',
      'doubleKills': 'doublekills',
      'tripleKills': 'triplekills',
      'quadraKills':'quadrakills',
      'pentaKills':'pentakills',
      'firstBloodKill': 'firstblood',
      'totalDamageDealtToChampions':'totaldamagetochampions',
      'physicalDamageDealtToChampions':'physicaldamagetochampions',
      'magicDamageDealtToChampions':'magicdamagetochampions',
      'trueDamageDealtToChampions':'truedamagetochampions', 
      'damageDealtToObjectives':'totaldamagetoobjectives',
      'damageDealtToTurrets':'totaldamagetoturrets',
      'totalHeal': 'damagehealed',
      'totalDamageTaken':'damagetaken', 
      'magicalDamageTaken':'magicdamagetaken',
      'wardsKilled': 'wardsdestroyed', 
      'sightWardsBoughtInGame':'stealthwardspurchased', 
      'visionWardsBoughtInGame':  'controlwardspurchased',
      'totalMinionsKilled':  'minionskilled', 
      'neutralMinionsKilledTeamJungle': "neutralminionskilledinteam'sjungle",
      'neutralMinionsKilledEnemyJungle':'neutralminionskilledinenemyjungle',
    }
    return header_dict[heading_input]
