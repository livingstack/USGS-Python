import requests
import json
import pygal
import datetime
from datetime import datetime
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask
url = "https://waterservices.usgs.gov/nwis/iv/?sites=10163000,10155200&format=json,1.1&period=P7D"

response = requests.get(url)

#filtered7dayswaterlist = response.Content
response_dict = response.json()



print ("water content:", response_dict.keys())



sevendayswaterlist = response_dict['value']


#print("water content:", response_dict['value'])
#.timeseries[0].values[0].value])
print(sevendayswaterlist.keys())

#gather data from index0 which contains USGS 10155200 PROVO RIV AT RIV ROAD BRIDGE NR HEBER CITY, UT
middletimeseriessevendayswaterlist = sevendayswaterlist['timeSeries'][0]

print(middletimeseriessevendayswaterlist.keys())

msevendayswaterlistvalues = middletimeseriessevendayswaterlist['values'][0]
middlesevendayswaterlistresults = msevendayswaterlistvalues['value']

#print (middlesevendayswaterlistresults)

#gather data from index2 which contains USGS 10163000 PROVO RIVER AT PROVO, UT
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

#print (mconvertedsevendayswaterlistresults[0])

#filter through all the sampling for the values at 6 am and store in middlestorevalues
for storedvalue in mconvertedsevendayswaterlistresults:
    stringvalue = storedvalue['dateTime']
    newvalue = stringvalue.split("T") #storedvalue.split("T")
    if newvalue[1] == "06:00:00.000-06:00":
        middlestoredvalues.append(storedvalue)

print(middlestoredvalues)

#print (lconvertedsevendayswaterlistresults[0])

#filter through all the sampling for the values at 6 am and store in lowerstorevalues
for storedvalue in lconvertedsevendayswaterlistresults:
    stringvalue = storedvalue['dateTime']
    newvalue = stringvalue.split("T") #storedvalue.split("T")
    if newvalue[1] == "06:00:00.000-06:00":
        lowerstoredvalues.append(storedvalue)

print(type(lowerstoredvalues))

#import pdb; pdb.set_trace()


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

mflow, mdate = [],[]
lflow, ldate = [],[]

formattedmdate = []
formattedldate = []



    
for sampling in middlestoredvalues:
    mflow.append(int(float(sampling['value'])))
    mdate.append(sampling['dateTime'])

for sampling in lowerstoredvalues:
    lflow.append(int(float(sampling['value'])))
    ldate.append(sampling['dateTime'])

for date in mdate:
    somedate = datetime.fromisoformat(date)
    middlesampledate = str(somedate.month) + "-" + str(somedate.day) + "-" + str(somedate.year)
    formattedmdate.append(middlesampledate)

for date in ldate:
    somedate = datetime.fromisoformat(date)
    lowersampledate = str(somedate.month) + "-" + str(somedate.day) + "-" + str(somedate.year)
    formattedldate.append(lowersampledate)

#print(mflow)
#print(lflow)
#make visualization


chart1 = pygal.Bar()
chart1.title = "Middle Provo flows from past week"
chart1.x_labels = formattedmdate

#chart1.add('', [535,523,548,528,516,535])
chart1.add('Flows', mflow)
#chart1.render()
#chart1.render_to_file('python_usgs_middle_repo.svg')

#style2 = LS('#333366', base_style=LCS)
#chart2 = pygal.Bar(style = style2, x_label_rotation=45, show_legend=true)
chart2 = pygal.Bar()
chart2.title = "Lower Provo flows from past week"
chart2.x_labels = formattedldate

chart2.add('Flows',lflow)
#chart2.render_to_file('python_usgs_lower_repo.svg')

chart3 = pygal.Bar()
chart3.title = "Lower and Middle Provo flows from past week"
chart3.x_labels = formattedldate
chart3.add('Lower Flows',lflow)
chart3.add('Middle Flows',mflow)
chart3.render_to_file('/opt/streamflows/static/images/Lower_and_Middle_Provo.svg')
lcurrentdate = formattedldate[-1]
lyesterday = formattedldate[-2]


print(formattedmdate)
print(formattedldate)

lcfsflowdifference = lflow[-1] - lflow[-2]
mcfsflowdifference = mflow[-1] - mflow[-2]

print (lcfsflowdifference)
print (mcfsflowdifference)

cfsflowthresholdreached = 0
cfsflowthresholdbreached = False

if lcfsflowdifference >= 200 or lcfsflowdifference <= -200:
    cfsflowthresholdreached +=1    
    cfsflowthresholdbreached = True
    
if mcfsflowdifference >= 200 or mcfsflowdifference <= -200:
    cfsflowthresholdreached += 1
    cfsflowthresholdbreached = True


lprovothreshold = "null"
mprovothreshold = "null"

#lcfsflowdifference = -301
#mcfsflowdifference = 300

if lcfsflowdifference <= -1:
    lprovothreshold = "negative"
if lcfsflowdifference >= 1:
    lprovothreshold = "positive"
    
if mcfsflowdifference <= -1:
    mprovothreshold = "negative"
if mcfsflowdifference >= 1:
    mprovothreshold = "positive"

emaildecreaseflowsmessage = "There has been at least a 200 cfs flow decrease"
emailincreaseflowsmessage = "There has been at least a 200 cfs flow increase"



recipientemail = "dyeman20@gmail.com"

server = smtplib.SMTP(host="smtp.gmail.com",port = 587)
server.starttls()
server.login("dyeman20", "icnikxypnoqpzgcb")
msg = MIMEMultipart()
msg['From']="dyeman20@gmail.com"
msg['To']="dyeman20@gmail.com"
#msg['subject']=""


#import pdb; pdb.set_trace()

if cfsflowthresholdbreached == True:
    while cfsflowthresholdreached >=1 :

        if lcfsflowdifference >= 200 or lcfsflowdifference <= -200:
                    
            print("lthreshold:",lprovothreshold)
            if lprovothreshold == "positive":
                msg['subject']="Lower Provo Flows change"
                msg.attach(MIMEText(emailincreaseflowsmessage, 'plain'))
                server.send_message(msg)
                del msg['subject']
                cfsflowthresholdreached -= 1
            
            if lprovothreshold == "negative":
                msg['subject']="Lower Provo Flows change"
                msg.attach(MIMEText(emaildecreaseflowsmessage, 'plain'))
                server.send_message(msg)
                del msg['subject']
                cfsflowthresholdreached -= 1

        if mcfsflowdifference >= 200 or mcfsflowdifference <= -200:
            
            print ("Entered middle provo flows difference")
            print ("mthreshold:",mprovothreshold)

            

            if mprovothreshold == "positive":
                print ("Entered middle provo p threshold")
                msg['subject']="Middle Provo Flows change"
                msg.attach(MIMEText(emailincreaseflowsmessage, 'plain'))
                server.send_message(msg)
                del msg['subject']
                cfsflowthresholdreached -= 1
                
            if mprovothreshold == "negative":
                print ("Entered middle provo n threshold")
                msg['subject']="Middle Provo Flows change"
                msg.attach(MIMEText(emaildecreaseflowsmessage, 'plain'))
                server.send_message(msg)
                del msg['subject']
                cfsflowthresholdreachedd -= 1
print (msg)
#import pdb; pdb.set_trace()
app = Flask(__name__)

@app.route('/usgs')

def application(environ,start_response):
    status = '200 OK'
        #response_header = [('Content-type','text/html')]
    html = '<html>\n' \
        '<body>\n' \
        '<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">\n' \
        'Provo River CFS Flows:\n' \
        '</div>\n' \
        '<img src="/static/images/Lower_and_Middle_Provo.svg" alt="Lower and Middle provo flows for past 7 days"/>\n' \
	'</body>\n' \
        '</html>\n'
    html = bytes(html,encoding = 'utf-8')
    response_header = [('Content-type','text/html')]
    start_response(status,response_header)
    return [html]
