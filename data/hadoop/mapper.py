#!/usr/bin/env python3
import sys
import os

input_file = os.environ.get('map_input_file', '')

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if line.startswith("id") or line.startswith("imdb_id"):
        continue

    if 'imdb_list' in input_file:
        parts = line.split(',')
        if len(parts) < 3:
            continue
        imdb_id = parts[1]
        title = parts[2]
        print(f"{imdb_id}\tL\t{title}")

    elif 'imdb_reviews' in input_file:
        parts = line.split(',')
        if len(parts) < 4:
            continue
        imdb_id = parts[0]
        review_rating = parts[2]
        review_text = ','.join(parts[3:])
        print(f"{imdb_id}\tR\t{review_rating}\t{review_text}")
