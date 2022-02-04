import os
import datetime
import unlzw3
from pathlib import Path
from requests import get  # to make GET request



date = '2021' + '12'
url = 'https://imecwww.imec.be/~aspinfo/ams/stats/ams_stats_%s.txt' % date

lots = {}
nowi = []

fromsite = get(url).content
file = fromsite.decode('utf-8').split('\n')

for i in file:
    a=i
    if i == '':
        break
    job = i.replace(',','').split()
    lotfinder = lots.get(job[3])
    if lotfinder == None and job[7].find('?') == -1:
        # if len(job[8])>8:
        #     job[8] = job[8][1:]
        lots[job[3]] = [job]
    elif lotfinder != None and job[7].find('?') == -1:
        # if len(job[8])>8:
        #     job[8] = job[8][1:]
        lots[job[3]].append(job)
    elif job[7].find('?') != -1:
        nowi.append(job)


# ConfigList = {'a':'01-02-2014', 'b':'01-03-2014', 'c':'01-08-2013', 'd':'01-09-2013', 'e':'01-10-2013'}
# a= sorted(ConfigList, key=lambda d: datetime.datetime.strptime(ConfigList[d], '%d-%m-%Y'))
new = {}
requestd = 0
measurd = 0
for i in lots:
    lots[i] = sorted(lots[i], reverse = True, key=lambda d: int(d[0]))
    lots[i][0].append(lots[i][0][9])
    for j in range(len(lots[i])-1):
        a = lots[i]
        b= lots[i][j][8]
        c= len(b)

        try:
            requestd = datetime.datetime.strptime(lots[i][j][7], '%d-%m-%y')
            measurd = datetime.datetime.strptime(lots[i][j][8], '%d-%m-%y')
        except:
            pass
        try:
            requestdnxt = datetime.datetime.strptime(lots[i][j+1][7], '%d-%m-%y')
            measurdnxt = datetime.datetime.strptime(lots[i][j+1][8], '%d-%m-%y')
            if requestdnxt < measurd:
                aa=1
                td=(measurd - requestdnxt).days
                lots[i][j + 1].append(str(int(lots[i][j + 1][9]) - td))
            else:
                lots[i][j + 1].append('0')
        except:
            lots[i][j + 1].append('0')
corrected = []
for i in lots:
    for j in lots[i]:
        b=j
        corrected.append(j)
for i in nowi:
    corrected.append(i)

with open(date + 'old.csv','w',encoding = 'utf-8') as f:
    for k in corrected:
        f.write(','.join(k)+'\n')
f.close()
a=1