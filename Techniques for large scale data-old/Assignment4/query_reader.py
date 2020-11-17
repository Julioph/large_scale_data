import requests
import pandas as pd
from collections import OrderedDict

url = 'https://query.wikidata.org/sparql'
# ======Swed universities
query = """\
SELECT ?uni  ?uniLabel ?yearFounded ?placeLabel
WHERE
{
  ?uni wdt:P31 wd:Q3918 .
  ?uni wdt:P17 wd:Q34 .
  ?uni wdt:P571 ?yearFounded .
  OPTIONAL {?uni wdt:P276 ?place .}
  OPTIONAL {?uni wdt:P131 ?place .}

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()

universities = []
for item in data['results']['bindings']:
    universities.append(OrderedDict({
        'wdhandle': item['uni']['value'],
        'University': item['uniLabel']['value'],
        'countryName': "Sweden",
        'placeName': item['placeLabel']['value'],
        'yearFounded': item['yearFounded']['value'].split("-", 1)[0]}))

df = pd.DataFrame(universities)
df.set_index('University', inplace=True)
# df = df.astype({'yearFounded': float, 'area': float, 'medianIncome': float, 'age': float})
print(df)

#====== all alumni of swed universities
# query = """\
# SELECT DISTINCT ?alu ?aluLabel ?bornPlaceLabel ?bornCountryLabel ?uniLabel
# WHERE
# {
#   ?alu wdt:P19 ?bornPlace ;
#        wdt:P69 ?uni .
#   ?bornPlace wdt:P17 ?bornCountry.
#   ?uni wdt:P17 wd:Q34 ;
#        wdt:P31 wd:Q3918 .
#
#
#   SERVICE wikibase:label {bd:serviceParam wikibase:language "en" .}
# }
# """
#
# r = requests.get(url, params={"format":"json", "query":query})
# data = r.json()
#
# alumni = []
# for item in data['results']['bindings']:
#     alumni.append(
#     OrderedDict({
#         'wdhandle': item['alu']['value'],
#         'Person': item['aluLabel']['value'],
#         'placeName': item['bornPlaceLabel']['value'],
#         'countryName': item['bornCountryLabel']['value'],
#         'University': item['uniLabel']['value']
#         })
#         )
#
# df = pd.DataFrame(alumni)
# df.set_index('Person', inplace=True)
# # df = df.astype({'yearFounded': float, 'area': float, 'medianIncome': float, 'age': float})
# print(df.tail(10))
