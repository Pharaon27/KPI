import os
import datetime
import unlzw3
from pathlib import Path
path = 'C:\\Users\\gavril74\\PycharmProjects\\KPI\\planning_files'
files = os.listdir(path)
year = [2022]
month = [1]
planning_files = []
for y in year:
    for m in month:
        if m<10:
            mc = '0' + str(m)
        else:
            mc = str(m)
        date = str(y) + mc
        for file in files:
            if file[9:15] == date:
                planning_files.append(file)

queue = []
q_base = {}
q_sorter = {}
for plan in planning_files:
    date = datetime.datetime.strptime(plan[9:17], '%Y%m%d')
    planning_file = open(path + '\\' + plan, 'r', encoding='utf-8')
    starter = 0
    stopper = 0
    for line in planning_file:
        if line == 'QUEUE\n':
            starter += 1
        elif line == 'HOLD\n':
            starter = 0
            stopper += 1
        elif starter != 0 and line != '\n' and line.find('====') == -1:
            line_list = []
            separator = line.replace('  ',',').split(',')
            for sign in separator:
                if sign != '':
                    line_list.append(sign)
            queue.append(line_list)
        elif stopper != 0:
            stopper = 0
            break

    q_base[date] = queue
    queue = []
for day in q_base:
    wafers_not_in = []
    wafers_in = []
    for session in q_base[day]:
        if session[8].find('??') != -1:
            wafers_not_in.append(session)
        else:
            wafers_in.append(session)
    q_sorter[day] = {'wafers_in': wafers_in, 'wafers_not_in': wafers_not_in}
in_list, out_list = [], []
evolution = {'wafers_in':[], 'wafers_not_in':[]}
for day in q_sorter:
    evolution['wafers_in'].append(len(q_sorter[day]['wafers_in']))
    evolution['wafers_not_in'].append(len(q_sorter[day]['wafers_not_in']))
a=1