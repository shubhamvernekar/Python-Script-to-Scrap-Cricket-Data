#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:18:01 2019

@author: shubham
@source website: http://stats.espncricinfo.com/
"""
import requests
import urllib.request
import time
import re
import csv
from bs4 import BeautifulSoup

url  = 'http://stats.espncricinfo.com/ci/engine/records/index.html'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
target = soup.find("div",{'id':"recteam"})
target = target.findAll('ul',{'class':'Record'})
target1 = target[0].findAll('a',href=True, text=True)
target2 = target[1].findAll('a',href=True, text=True)
teamid = []
start = '?'
end = ';'
for i in target1:
    teamid.append((i['href'].split(start))[1].split(end)[0])
for i in target2:
    teamid.append((i['href'].split(start))[1].split(end)[0])

print('Opreation In Process: It had to open >3000 links. So it might take a long')

playersListUrlstr = 'http://stats.espncricinfo.com/ci/engine/records/averages/batting.html?class=2;'
playersListUrlend = ';type=team'
players = []
pId = []
prun = []
pYandR = []
counr =0

#This for loop obtain player name & player Total runs in odi
for i in teamid:
    playerListUrl = playersListUrlstr + i + playersListUrlend
    response = requests.get(playerListUrl)
    soup = BeautifulSoup(response.text, 'lxml')
    mtable = soup.select_one("table:nth-of-type(1)")
    for row in mtable.findAll('tr',{'class','data1'}):
        columns = row.findAll('td')
        players.append(columns[0].text)
        pId.append((columns[0].find('a').get('href')).split('player/')[1].split('.html')[0])
        prun.append(columns[5].text)
    print('.')
print('50% of process is completed..')
#function to get players score each year   
def cummulify(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.findAll('table',{'class','engineTable'})
    flag = True
    tr = table[3].findAll('tbody')[4].findAll('tr')
    string = ""
    for i in tr[1:]:
        td = i.findAll('td')
        year = td[0].text
        run = td[5].text
        if(re.search("^year",year)):
            string = string + (year+": Run "+run+"\n")
        else:
            flag = False
            break
    
    if(flag == False):
        tr = table[3].findAll('tbody')[5].findAll('tr')
        for i in tr[1:]:
            td = i.findAll('td')
            year = td[0].text
            run = td[5].text
            string = string + (year+": Run "+run+"\n")
    pYandR.append(string)
        
linkStart = 'http://stats.espncricinfo.com/ci/engine/player/'
linkEnd = '.html?class=2;template=results;type=batting'

for i in pId:
    link = linkStart + i + linkEnd
    cummulify(link)
    print('.')
    

#Write Data to csv
print('Writing data to csv')

headers = ['Player Name ','ODI Year : Run','Total Carrier Runs']
with open('CricData.csv','w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers) 
    row = []
    for i in range(0,len(players)):
        row.append(players[i])
        row.append(pYandR[i])
        row.append(prun[i])
        csvwriter.writerow(row)
        row = []

print('Opreation Successfull: All data is present inside CricData.csv file inside this program dir')
        
    
    