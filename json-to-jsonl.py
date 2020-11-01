# -*- coding: utf-8 -*-

import jsonlines
import json


with open('result.json', 'r', encoding="utf-8") as f:
    json_data = json.load(f)

with jsonlines.open('in.jsonl', 'w') as writer:
    writer.write_all(json_data)