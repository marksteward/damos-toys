#!/usr/bin/env python3
import requests
import os
from datetime import datetime
from lxml import html
import re

ITEM_URL_FORMAT = 'https://www2.hf.uio.no/damos/Index/item/chosen_item_id/{}'


def writefile(filename, data):
    with open(os.path.join(outdir, filename), 'w') as f:
        f.write(data)

def scrape(outdir, start=1, end=10000):
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    for n in range(start, end):
        try:
            r = requests.get(ITEM_URL_FORMAT.format(n))
            tree = html.fromstring(r.text)
            h2s = tree.cssselect('h2')
            if not h2s:
                raise ValueError('No h2 elements found')

            title = h2s[0].text
            if title == 'Application error':
                # Missing tablet - first is 2893
                continue

            # First with changes is 468 (show up as <em>)
            tablet = tree.cssselect('pre')[0].text_content()
            meta = tree.cssselect('.meta_info')[0]
            bib = tree.cssselect('.bib_info')[0]
            meta = '\n'.join(meta.itertext())
            bib = '\n'.join(bib.itertext())
            meta = re.sub(r'^Metadata\n(\n|$)', '', meta)
            bib = re.sub(r'Basic Tablet Bibliography(\n|$)', '', bib)

            writefile('{}.tablet.txt'.format(n), tablet + '\n')
            writefile('{}.title.txt'.format(n), title + '\n')
            writefile('{}.meta.txt'.format(n), meta + '\n')
            writefile('{}.bib.txt'.format(n), bib + '\n')

        except Exception as e:
            import pdb;pdb.set_trace()
            raise


now = datetime.now()
outdir = 'scrape-' + now.strftime('%Y%m%d')

scrape(outdir, start=1, end=6000)
print('Scrape complete')

