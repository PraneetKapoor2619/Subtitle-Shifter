#SUBTITLE SHIFTER
#VERSION: 0.1
#Description: To be used to shift the time interval in which a particular subtitle is to be displayed
#
#Date: 30.07.2021
#Author: Praneet Kapoor

import os
import re
import sys

def printProgressBar(i, max, message):
	bar = 50
	percentage = i/max
	sys.stdout.write("\r")
	sys.stdout.write(f"[{'=' * int(bar * percentage):{bar}s}] {int(100 * percentage)} % {message}")
	sys.stdout.flush()
	return 0

def time_array(line):
	array = re.findall("[0-9.,]+", line)
	s_char = re.findall("[^0-9.,: ]+", line)
	print(s_char)
	for i in range(len(array)):
		if(array[i].find(',') != -1):
			array[i] = array[i].replace(',', '.')
		else: continue
	return array, s_char[0]

def time_dilation(array, delay_string):

#array[0] -> hh_1	delay_string[0] -> hours
#array[1] -> mm_1	delay_string[1] -> minutes
#array[2] -> ss_1	delay_string[2] -> seconds
#array[3] -> hh_2
#array[4] -> mm_2
#array[5] -> ss_2
	flag = None
	for i in range(len(array)):
		array[i] = round(float(array[i]), 3)
	for i in reversed(range(len(array))):
		if(i >= 3): j = i - 3
		else: j = i
		array[i] = array[i] + float(delay_string[j])
		if((array[i] >= 60) & ((i != 0) | (i != 3))):
			array[i] -= 60
			if(delay_string[j] == 0):
				array[i - 1] += 1
		if((i == 2) | (i == 5)):
			array[i] = str(round(array[i], 3))
		else: 
			array[i] = str(int(array[i]))
	return array
	
filename = input("Enter the name of subtitle file with extension: ")
try:
	fhandle = open(filename, "r", encoding = 'utf-8')
except: 
	print("\aIncorrect filename!")
	exit(0)

delay_string = input("Enter the gap in hh:mm:ss format -> ")
delay_string = re.findall("[0-9.,]+", delay_string)
delay_h = int(delay_string[0])
delay_m = int(delay_string[1])
if(delay_string[2].find(',') != -1):
	delay_string[2] = delay_string[2].replace(',', '.')
delay_s = float(delay_string[2])

new_file = "default" + filename[filename.find('.'):]
f2 = open(new_file, "w+")
print("\nNew file opened")
total_line_count = 0
for line in fhandle:
	total_line_count += 1
print(total_line_count, "lines detected")
if(total_line_count == 0): exit(0)

fhandle.seek(0)
counter = 1
dialogue_flag = False
for line in fhandle:
	if(dialogue_flag == False):
		f2.write(line)
		line.strip("\r\n\t ")
		print(line, end = ' ')
		try: 
			isnum = int(line)
		except:
			isnum = False
		if(isnum):
			print('Number detected')
			if(int(line) == counter):
				print("Here")
				counter += 1
				dialogue_flag = True
				continue
	else:
		print("fixing")
		dialogue_flag = False
		array, s_char = time_array(line)
		array = time_dilation(array, delay_string)
		s_char = " " + s_char + " "
		string = array[0] + ':' + array[1] + ':' + array[2] + s_char + array[3] + ':' + array[4] + ':' + array[5] + "\n"
		print(string)
		f2.write(string)
fhandle.close()
f2.close()
#os.system("rm " + filename)
#os.system("mv " + new_file + " filename")
