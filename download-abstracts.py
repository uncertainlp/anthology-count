
import bibtexparser
import gzip
import urllib.request
from collections import defaultdict
import numpy as np
from datetime import datetime

print("Downloading https://aclanthology.org/anthology+abstracts.bib.gz")
urllib.request.urlretrieve("https://aclanthology.org/anthology+abstracts.bib.gz", "anthology+abstracts.bib.gz")

print("Parsing bibtex (may take minutes)...")
with gzip.open('anthology+abstracts.bib.gz', 'rb') as f:
    data = bibtexparser.load(f)

from_year = 2010 # not enough abstracts before then
current_year = datetime.now().year
print(f"Collecting abstracts from {from_year} to {current_year}...")

years = set(str(x) for x in np.arange(from_year, current_year))

by_year_abstract = defaultdict(list)
by_year_title = defaultdict(list)

for d in data.entries:
    if d['year'] in years:
        if 'title' in d:
            by_year_title[d['year']].append(d['title'])
        if 'abstract' in d:
            by_year_abstract[d['year']].append(d['abstract'])

print("Here is what I found:\n\nYear\tPapers\tAbstracts")
for year in sorted(years):
    print(f"{year}\t{len(by_year_title[year])}\t{len(by_year_abstract[year])}")

to_save = {'title': by_year_title, 'abstract': by_year_abstract}

import json
with open(f'abstracts-{from_year}-{current_year}.json', 'w') as f:
    json.dump(to_save, f)


