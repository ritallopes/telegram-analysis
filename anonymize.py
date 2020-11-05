#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
A program to anonymize telegram chat
"""
import argparse
import pandas as pd
from cryptography.fernet import Fernet



def main():

    parser = argparse.ArgumentParser(
            description="Extract all raw text from a specific Telegram chat")
    parser.add_argument('filepath', help='the json chatlog file to analyse')
    parser.add_argument('-f','--out-file', help='Descarrega em arquivo',
                        action='store_true')

    args=parser.parse_args()
    filepath = args.filepath

    chatdf=pd.read_json(filepath, encoding='mbcs')
    chatdf['from'] = chatdf['from'].apply(hash)
    chatdf.to_csv('chatdf.csv', sep ='\t')
if __name__ == "__main__":
    main()
