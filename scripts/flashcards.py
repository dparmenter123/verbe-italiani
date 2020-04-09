import csv
from collections import defaultdict
import random
import os
import sys

url1 = '/Users/davidp/work/verbe-italiani/data/csvs/top236.csv'

forms = [
    'Condizionale Passato',
    'Condizionale Presente',
    'Congiuntivo Imperfetto',
    'Congiuntivo Perfetto',
    'Congiuntivo Presente',
    'Congiuntivo Trapassato',
    'Futuro',
    'Futuro Anteriore',
    'Imperfetto',
    'Passato Remoto',
    'Perfetto',
#    'Presente',
    'Trapassato Prossimo'
]

def write_full_csv(url, cards):
    with open(url, encoding='utf-8', mode='w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for card in cards:
            w.writerow(card)

def read_full_csv(url):
    db = defaultdict(dict)
    with open(url, encoding='utf-8', mode='r') as f:
        r = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for i, row in enumerate(r):
            if i == 0:
                continue
            _, pos, root, form, front, back = row
            if not form in db[root].keys():
                db[root][form] = ['' for i in range(8)]
            db[root][form][int(pos)] = back
    return(db)


def one_form(db, form):
    keys = list(db.keys())
    random.shuffle(keys)

    cards = []
    for root in keys:
        presente = db[root]['Presente']
        i = random.choice(range(8))
        front = '%s --> %s' % (presente[i], form)
        back = db[root][form][i]
        cards += [[front, back]]
    return (cards)


def main(url):
    db = read_full_csv(url1)
    for form in forms:
        cards = one_form(db, form)
        base, ext = os.path.splitext(url)
        suffix = '-'.join(form.lower().split(' '))
        output = '%s-%s%s' % (base, suffix, ext)
        write_full_csv(output, cards)

if __name__ == '__main__':
    main(sys.argv[1])
