#!/usr/bin/python3
import os
import re
import csv

cols = ['run', 'scload', 'read', 'filter', 'filled', 'training', 'model', 'runtime']
dir = './logs'

sparkload_time = []
read_time = []
filter_time = []
filled_time = []
training_time = []
model_time = []
run_time = []

for run in os.listdir(dir):
    infile = open(os.path.join(dir, run), 'r')
    for line in infile:
        if re.search('PerfMeasure: Total Run Time', line):
            run_time.append(float(line.split()[6]))
        elif re.search('PerfMeasure: Spark', line):
            sparkload_time.append(float(line.split()[6]))
        elif re.search('PerfMeasure: result saved in', line):
            model_time.append(float(line.split()[5]))
        elif re.search('PerfMeasure: filled_data ', line):
            filled_time.append(float(line.split()[4]))
        elif re.search('PerfMeasure: training data in', line):
            training_time.append(float(line.split()[5]))
        elif re.search('PerfMeasure: read data in', line):
            read_time.append(float(line.split()[5]))
        elif re.search('PerfMeasure: filtered data in', line):
            filter_time.append(float(line.split()[5]))
        else:
            continue

size = range(len(sparkload_time))
with open(os.path.join(dir, 'result.csv'), 'w') as outfile:
    csv_out = csv.writer(outfile)
    csv_out.writerow(cols)
    for x in zip(size, sparkload_time, read_time, filter_time, filled_time, training_time, model_time, run_time):
        csv_out.writerow(x)



