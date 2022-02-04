import os
import datetime
import unlzw3
from pathlib import Path
from requests import get  # to make GET request
year = [2022]
month = [x for x in range(1, 2)]

for y in year:
    for m in month:
        if m<10:
            mc = '0' + str(m)
        else:
            mc = str(m)
        date = str(y) + mc
        url = 'https://imecwww.imec.be/~aspinfo/ams/stats/ams_stats_%s.txt' % date

        lots = {}
        sys = {}
        nowi = []

        fromsite = get(url).content
        file = fromsite.decode('utf-8').split('\n')
        for i in file:
            a=i
            if i == '':
                break
            job = i.replace(',','').split()
            if len(job) == 16:
                job.append('placeholder')
            errflg = 0
            try:
                job[7] = datetime.datetime.strptime(job[7], '%d-%m-%y').date()
                job[8] = datetime.datetime.strptime(job[8], '%d-%m-%y').date()
            except:
                errflg = 1
            lotfinder = lots.get(job[3])

            if lotfinder == None and errflg == 0:
                lots[job[3]] = {job[5]:[job]}

            elif lotfinder != None and errflg == 0:
                syslist = lots[job[3]].keys()
                a  = job[5] in syslist
                if job[5] in syslist:
                    lots[job[3]][job[5]].append(job)
                else:
                    lots[job[3]][job[5]] = [job]
                    cc = lots[job[3]][job[5]]
            elif errflg == 1:
                if len(job) == 16:
                    job.append('placeholder')
                job.append('x')
                try:
                    job[7] = job[7].strftime('%d/%m/%Y')
                except:
                    pass
                try:
                    job[8] = job[8].strftime('%d/%m/%Y')
                except:
                    pass
                nowi.append(job)

        new = {}
        requestd = 0
        measurd = 0
        for i in lots:
            for j in lots[i]:
                lots[i][j] = sorted(lots[i][j], reverse=True, key=lambda d: d[0])
                lots[i][j] = sorted(lots[i][j], reverse=False, key=lambda d: d[8])
                lots[i][j][0].append(lots[i][j][0][9])
                a=len(lots[i][j][0])

                for k in range(len(lots[i][j])-1):
                    a = lots[i][j]
                    b= lots[i][j][k][8]
                    measurd = lots[i][j][k][8]
                    requestdnxt = lots[i][j][k+1][7]
                    if requestdnxt < measurd:
                        aa=1
                        td=(measurd - requestdnxt).days
                        lots[i][j][k + 1].append(str(int(lots[i][j][k + 1][9]) - td))

                    else:
                        lots[i][j][k + 1].append(lots[i][j][k + 1][9])

        corrected = []
        for i in lots:
            for j in lots[i]:
                for k in lots[i][j]:
                    k[7] = k[7].strftime('%d/%m/%Y')
                    k[8] = k[8].strftime('%d/%m/%Y')
                    corrected.append(k)
        for i in corrected:
            if len(i) == 18:
                delay = (float(i[17])*24 - float(i[11]))/24
                if delay < 0:
                    delay = 0
                i.append(str(delay))
        for i in nowi:
            # i[7] = i[7].strftime('%d/%m/%Y')
            # i[8] = i[8].strftime('%d/%m/%Y')
            corrected.append(i)

        with open(date + '.csv','w',encoding = 'utf-8') as f:
            for k in corrected:
                f.write(','.join(k)+'\n')
        f.close()

a=1