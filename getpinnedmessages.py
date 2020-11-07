#!/usr/bin/env python3
from json import loads
import argparse
import pandas as pd
import re

parser = argparse.ArgumentParser(
        "Print all the pinned text messages from a Telegram chat log")
parser.add_argument(
        'file',
        help='path to the json file (chat log) to analyse')

args = parser.parse_args()

jsn = pd.read_json(args.file)

jsn['action'] = jsn['action'].fillna("no action")
pins = jsn['action'].str.contains(r'(\bpin|\bpinned)', flags = re.I)

#reply_id is the ID of the message that has been pinned.
pin_msgs = jsn.loc[jsn['id'].isin(jsn.loc[pins, 'message_id'])]
#ignore pins with no text
pin_msgs['text'].apply(print)