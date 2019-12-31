from datetime import timedelta
from datetime import datetime
import os
from parse import parse

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# folder_name = input("what do you want directory to be?") + '/'     # commment in if want to customize folder
folder_name = 'BB3/'        # comment out if want to costumize folder
ensure_dir(folder_name)

dt_fmt = "%m/%d/%y  %H:%M:%S"
dt_prev = ""
#will edit out when wanting to put site in at same time
site = 0
file_name = ''
line_fmt = (
    '{:2d}/{:2d}/{:2d}	{:2d}:{:2d}:{:2d}	'
    '{:3d}	{:4d}	{:3d}	{:4d}	{:3d}	{:4d}	{:3d}'
)
# edit in if want to choose file name with extension
# sample_file_name = input('Whats the file name?')
# can edit out before running anything if want to type as an input
sample_file_name = 'WS19028_BB3.raw'
f = open(sample_file_name,"r")

# use readline() to read the first line
line_of_text = f.readline()

while line_of_text:
        parsed_line = parse(line_fmt, line_of_text)
        # print(parsed_line)
        # this checks if the date is in correct format, assumes data will be correct if date is
        try:
            time_of_sample = "{}/{}/{} {}:{}:{}".format(
                parsed_line[0], parsed_line[1], parsed_line[2],
                parsed_line[3], parsed_line[4], parsed_line[5]
            )
            dt = datetime.strptime(time_of_sample, dt_fmt)
        except Exception:  # the errors involves looping the error 46 times, then continuing
            print(time_of_sample)
            # puts error lines into a file
            error_file = open('files_with_errors.txt', "a")
            error_file.write(line_of_text)
            line_of_text = f.readline()
            continue

        # if open dt_prev, will take current dt and subtract 1 sec
        if dt_prev == "":
            dt_prev = dt - timedelta(seconds=1)
        dt_current = dt

        # checks to make sure time is not negative, would mean error
        if dt_current - dt_prev < timedelta(milliseconds=0):
            print(dt_current, dt_prev)
            error_file = open('files_with_errors.txt', "a")
            error_file.write(line_of_text)
            line_of_text = f.readline()
        elif dt_current - dt_prev < timedelta(minutes=5):
            # for the next iteration, sets current to prev
            dt_prev = dt_current
            if file_name == "":
                i = dt_current.strftime("%d_%m_%yT%H%M%S")
                # this is so can look up timestamp on spreadsheet and label site
                print('Old time: ' + str(dt_current))
                # edit in later, to name site during run
                #site = input("What is the site ID?")
                file_name = 'MBON_{}_site_{}.txt'.format(i, site)
                newfile = open(folder_name + file_name, "a")
                newfile.write(line_of_text)
            else:
                newfile = open(folder_name + file_name, "a")
                newfile.write(line_of_text)
        else:
            dt_prev = dt_current
            i = dt_current.strftime("%d_%m_%yT%H%M%S")
            # this is so can look up timestamp on spreadsheet and label site
            print('Old time: ' + str(dt_current))
            # edit in later, to name site during run
            # site = input("What is the site ID?")
            site = site + 1         #edit out later
            file_name = 'MBON_{}_site_{}.txt'.format(i,site)
            newfile = open(folder_name + file_name, "a")
            newfile.write(line_of_text)
        line_of_text = f.readline()
f.close()
