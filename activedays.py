#!/usr/bin/env python3
"""
A program to plot the activity of a chat over 24 hours
"""
import argparse
from json import loads
from datetime import date,timedelta,datetime
from os import path
from collections import defaultdict
import matplotlib.pyplot as plt
from sys import maxsize
import pandas as pd

def extract_info(event):
    return event['date'], event['date'].isoweekday(), len(event['text'])
def make_ddict_in_range(events,start,end):
    """
    return a defaultdict(int) of dates with activity on those dates in a date range
    """
    #generator, so whole file is not put in mem
    msg_infos = (events.apply(extract_info, axis=1))
    msg_infos = ((date,weekday,length) for (date,weekday,length) in msg_infos if date >= start and date <= end)
    counter = defaultdict(int)
    #a dict with days as keys and frequency as values
    day_freqs = defaultdict(int)
    for date_text,day_text,length in msg_infos:
       counter[day_text] += length
       day_freqs[day_text] += 1
    for k,v in counter.items():
        counter[k] = v/day_freqs[k]
    #divide each day's activity by the number of times the day appeared.
    #this makes the bar height = average chars sent on that day
    #and makes the graph a more accurate representation, especially with small date ranges

    return counter

def parse_args():
    parser = argparse.ArgumentParser(
            description="Visualise the most active days of week in a Telegram chat")
    required = parser.add_argument_group('required arguments')
    #https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments
    required.add_argument(
            '-f', '--file',
            help='paths to the json file (chat log) to analyse.',
            required = True
            )
    parser.add_argument(
            '-o', '--output-folder',
            help='the folder to save the activity graph image in.'
            'Using this option will make the graph not display on screen.')
    #parser.add_argument(
    #        '-b', '--bin-size',
    #        help='the number of days to group together as one datapoint. '
    #        'Higher number is more smooth graph, lower number is more spiky. '
    #        'Default 3.',
    #        type=int,default=3)
    #        #and negative bin sizes are = 1
    parser.add_argument(
            '-s','--figure-size',
            help='the size of the figure shown or saved (X and Y size).'
            'Choose an appropriate value for your screen size. Default 14 8.',
            nargs=2,type=int,default=[14,8]
            )
    parser.add_argument(
            '-d','--date-range',
            help='the range of dates you want to look at data between. '
            'Must be in format YYYY-MM-DD YYYY-MM-DD with the first date '
            'the start of the range, and the second the end. Example: '
            "-d '2017-11-20 2017-05-15'. Make sure you don't put a day "
            'that is too high for the month eg 30th February.',
            default="1000-01-01 4017-01-01"
            #hopefully no chatlogs contain these dates :p
    )

    return parser.parse_args()

def save_figure(folder,filename):

    if len(filename) > 200:
    #file name likely to be so long as to cause issues
        figname = input(
            "This graph is going to have a very long file name. Please enter a custom name(no need to add an extension): ")
    else:
        figname = "Active days in {}".format(filename)

    plt.savefig("{}/{}.png".format(folder, figname))

def annotate_figure(filename,start,end):
    if start == date(1000,1,1) and end == date(4017,1,1):
        datestr = "entire chat history"
        plt.title("Active days in {} in {}".format(filename,datestr))
    else:
        datestr = "between {} and {}".format(start,end)
        plt.title("Active days in {}, {}".format(filename,datestr))
    plt.ylabel("Activity level (avg. chars sent on day)", size=14)
    plt.xlabel("Day of the week", size=14)
    plt.gca().set_xlim([1,8])
    plt.xticks(([x+0.5 for x in range(8)]),['','Mon','Tue','Wed','Thu','Fri','Sat','Sun'])

    #if binsize > 1:
    #    plt.ylabel("Activity level (chars per {} days)".format(binsize), size=14)
    #else:
    #    plt.ylabel("Activity level (chars per day)", size=14)

def get_dates(arg_dates):
    if " " not in arg_dates:
        print("You must put a space between start and end dates")
        exit()
    daterange = arg_dates.split()
    start_date = datetime.strptime(daterange[0], "%Y-%m-%d").date()
    end_date = datetime.strptime(daterange[1], "%Y-%m-%d").date()
    return (start_date,end_date)

def main():
    """
    main function
    """

    args = parse_args()

    filepath = args.file
    savefolder = args.output_folder
    figure_size = args.figure_size
    start_date,end_date = get_dates(args.date_range)

    filename = path.splitext(path.split(filepath)[-1])[0]


    chat= pd.read_json(filepath)
    chat_counter = make_ddict_in_range(chat,start_date,end_date)
    
    plt.figure(figsize=figure_size)
    plt.bar(*zip(*chat_counter.items()))
    annotate_figure(filename,start_date,end_date)
    if savefolder is not None:
    #if there is a given folder to save the figure in, save it there
        save_figure(savefolder,filename)
    else:
        #if a save folder was not specified, just open a window to display graph
        plt.show()

if __name__ == "__main__":
    main()
