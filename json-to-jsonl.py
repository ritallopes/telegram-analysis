# -*- coding: utf-8 -*-
import jsonlines
import json
import argparse




def main():
    parser = argparse.ArgumentParser(
            description="Extract all raw text from a specific Telegram chat")
    parser.add_argument('filepath', help='the json chatlog file to analyse')

    args=parser.parse_args()
    filepath = args.filepath

    with open(filepath, 'r', encoding="utf-8") as f:
        json_data = json.load(f)

    with jsonlines.open(filepath+'l', 'w') as writer:
        writer.write_all(json_data)


if __name__ == "__main__":
    main()
