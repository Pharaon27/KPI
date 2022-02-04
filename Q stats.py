import shutil

shutil.copy2('Z:\\Q.txt', 'Q_copy.txt')
with open('Q_copy.txt','r') as queue:
    jobs = queue.readlines()
job_lines = []
for job in jobs:
    job_line = job.split()
    job_lines.append(job_line)

a = 1