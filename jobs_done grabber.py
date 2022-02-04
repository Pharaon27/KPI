import datetime
import re
import string
import os
def job_reader(start_date, end_date):
    start_date_plus = start_date - datetime.timedelta(days=60)
    jobs = []
    jobd = {}
    jobds = {}
    job_lot = {}
    jobs_done_open = open('C:\\Users\\gavril74\\PycharmProjects\\KPI\\data\\jobs_done_extended', 'r')
    i = 0
    for line in jobs_done_open:
        job = re.split(', |,|  , ', line[:-1])
        try:
            job.index('-ADDED')
        except:
            date = datetime.datetime.strptime(job[9], '%d/%m/%y')
            time = (datetime.datetime.strptime(job[10], '%H:%M:%S')).time()
            date_time = datetime.datetime.combine(date, time)

            job.append(date_time)

            if start_date <= date_time <= end_date:
                link = fromlinuxstring(job[5])
                file_names, file_pathes = all_file_listing(link, 10)
                for path in file_pathes:
                    if path.find('.csv') != -1:
                        csv_path = path
                request_time = request_time_grabber(csv_path)
                jobd['job_number'] = job[0]
                jobd['lot'] = job[1]
                jobd['sys'] = job[2]
                jobd['probecard'] = job[3]
                jobd['link'] = link
                jobd['requestors'] = job[6]
                jobd['meas_date'] = date_time
                jobd['request_date'] = request_time
                job.append(request_time)
                jobds[i] = jobd.copy()
                jobs.append(job)
                job_lot[job[0]] = job[1].lower()
                i += 1
            elif start_date_plus <= date_time <= end_date:
                job_lot[job[0]] = job[1].lower()
            elif date_time < start_date:
                break
    return jobs, job_lot, jobds


def fromlinuxstring(address):
    address = address.replace('/imec/other/param', '\\\\unixbe\\param')
    address = address.replace('/', '\\')
    address = address.replace('\n', '')
    return address


def all_file_listing(path, depth):
    all_files = []
    all_files_path = []
    start_depth = 1

    def all_files_wrapped(path_r, depth_r, d):
        with os.scandir(path_r) as collector:
            for file_r in collector:
                if file_r.is_file():
                    all_files.append(file_r.name)
                    all_files_path.append(file_r.path)
                elif file_r.is_dir() and d <= depth_r:
                    d += 1
                    all_files_wrapped(file_r.path, depth_r, d)
                    d -= 1
        return all_files, all_files_path

    all_files, all_files_path = all_files_wrapped(path, depth, start_depth)
    return all_files, all_files_path


def request_time_grabber(path):
    request_time_line = -1
    request_time = -1
    if path != -1:
        csv_open = open(path, 'r')
        csv = csv_open.readlines()
        for line in range(len(csv)):
            if csv[line].find('Timestamp:') != -1:
                request_time_line = csv[line][csv[line].find('Timestamp:') + 11: -1]
                request_time = datetime.datetime.strptime(request_time_line, '%d%b%y:%H:%M:%S')

    return request_time


def wafers_in(start_date, end_date):
    commands = []
    start_date_plus = start_date - datetime.timedelta(days=60)
    wi_open = open('C:\\Users\\gavril74\\PycharmProjects\\KPI\\data\\wi_details.txt', 'r')
    for line in wi_open:
        wafer = line[:-2].split(' ')
        date_time = datetime.datetime.strptime(wafer[0] + ' ' + wafer[1], '%m/%d/%y %H:%M:%S')
        if start_date_plus <= date_time <= end_date:
            command = [wafer[3].lower(), date_time]
            commands.append(command)
        elif date_time > end_date:
            break
    return commands


def main():
    lot_in = []
    s_date = datetime.datetime(2021, 12, 14)
    e_date = datetime.datetime(2021, 12, 15)
    jobs, job_lot, jobds = job_reader(s_date, e_date)
    commands_in = wafers_in(s_date, e_date)
    sortedsd= sorted(commands_in)
    for command in commands_in:
        lot = job_lot.get(command[0], command[0])
        command.append(lot)
    srtd = sorted(job_lot)
    for key in jobds:
        jobd = jobds[key]
        timepack = []
        for command in commands_in:
            b = command
            if jobd['job_number'] == command[2]:
                timepack.append(command[1])
            elif jobd['lot'] == command[2]:
                timepack.append(command[1])

        jobd['wafers_in'] = timepack


    a = 1


if __name__ == '__main__':
    main()
b = 2
