#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A program to extract all text sent by a particular user from a Telegram chat log
"""
import argparse
from json import loads
import pandas as pd
import re

def main():

    parser = argparse.ArgumentParser(
        description="Extract all raw text sent by a specific user in a specific Telegram chat")
    parser.add_argument(
        'filepath', help='the jsonl chatlog file to analyse')
    parser.add_argument(
        'username', help='a username of the person whose text you want (without @ sign), case insensitive')

    args=parser.parse_args()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    filepath = args.filepath
    username_or_id = args.username

    chat = pd.read_json(filepath)
    chat[['from', 'text']] = chat[['from', 'text']].fillna(" ")
    chat.loc[(chat['from'].str.contains(username_or_id, flags=re.I)) | (chat['from_id'].apply(str).str.contains(username_or_id, flags=re.I)),['text']].apply(print)
    
if __name__ == "__main__":
    main()
