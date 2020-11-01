#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
A program to extract raw text from Telegram chat log
"""
import argparse
from json import loads
import pandas as pd

def search_event(df, usernames, no_newlines):
    if no_newlines:
        df['text'] = df['text'].str.replace(r'\n+','')
    if usernames:
        df[['text', 'from']].apply(lambda line: print('@'+line['from']+': '+line['text']), axis=1)
    else:
        df['text'].str.encode('mbcs').str.decode('utf-8').apply(print)



def main():

    parser = argparse.ArgumentParser(
            description="Extract all raw text from a specific Telegram chat")
    parser.add_argument('filepath', help='the json chatlog file to analyse')
    parser.add_argument('-u','--usernames', help='Show usernames before messages. '
                        'If someone doesn\'t have a username, the line will start with "@: ".'
                        'Useful when output will be read back as a chatlog.',
                        action='store_true')
    parser.add_argument('-n','--no-newlines', help='Remove all newlines from messages. Useful when '
                        'output will be piped into analysis expecting newline separated messages. ',
                        action='store_true')

    args=parser.parse_args()
    filepath = args.filepath
    

    chatdf = pd.read_json(filepath, encoding="mbcs")
    
    search_event(chatdf[["from", "from_id", "text"]], usernames=args.usernames, no_newlines=args.no_newlines)



if __name__ == "__main__":
    main()
