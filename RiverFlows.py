import requests
import json
url = "https://waterservices.usgs.gov/nwis/iv/?sites=10163000,10155200&format=json,1.1&period=P7D"

response = requests.get(url)

#filtered7dayswaterlist = response.Content
response_dict = response.json()

print ("water content:", response_dict.keys())

sevendayswaterlist = response_dict['value']


#print("water content:", response_dict['value'])
#.timeseries[0].values[0].value])
print(sevendayswaterlist.keys())

middletimeseriessevendayswaterlist = sevendayswaterlist['timeSeries'][0]

print(middletimeseriessevendayswaterlist.keys())

msevendayswaterlistvalues = middletimeseriessevendayswaterlist['values'][0]
middlesevendayswaterlistresults = msevendayswaterlistvalues['value']

#print (middlesevendayswaterlistresults)


lowertimeseriessevendayswaterlist = sevendayswaterlist['timeSeries'][2]

#print(lowertimeseriessevendayswaterlist.keys())

lsevendayswaterlistvalues = lowertimeseriessevendayswaterlist['values'][0]
lowersevendayswaterlistresults = lsevendayswaterlistvalues['value']
#print (lowersevendayswaterlistresults)


lconvertedsevendayswaterlistresults = []
mconvertedsevendayswaterlistresults = []


lowerstoredvalues = []
middlestoredvalues = []
storedvalues = []

for sampling in lowersevendayswaterlistresults:
 lconvertedsevendayswaterlistresults.append(sampling)

for sampling in middlesevendayswaterlistresults:
 mconvertedsevendayswaterlistresults.append(sampling)

print (mconvertedsevendayswaterlistresults[0])


for storedvalue in mconvertedsevendayswaterlistresults:
    stringvalue = storedvalue['dateTime']
    newvalue = stringvalue.split("T") #storedvalue.split("T")
    if newvalue[1] == "06:00:00.000-06:00":
        middlestoredvalues.append(storedvalue)

print(middlestoredvalues)

print (lconvertedsevendayswaterlistresults[0])


for storedvalue in lconvertedsevendayswaterlistresults:
    stringvalue = storedvalue['dateTime']
    newvalue = stringvalue.split("T") #storedvalue.split("T")
    if newvalue[1] == "06:00:00.000-06:00":
        lowerstoredvalues.append(storedvalue)

print(lowerstoredvalues)

import pdb; pdb.set_trace()

#convertedlstoredvalues = []

#for jsonobject in lowerstoredvalues:
#   print (jsonobject)
#   jsonstring = str(jsonobject)
#   doublejsonstring = jsonstring.replace("\'","\"")
#   print (doublejsonstring)
#   convertedlstoredvalues.append(json.loads(doublejsonstring))
#print (convertedlstoredvalues[0])
#convertedmstoredvalues = json.loads(middlestoredvalues)

#print (type(convertedlstoredvalues))
#print(type(middlestoredvalues))
