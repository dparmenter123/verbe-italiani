import re
import os
import sys
import urllib.request
import csv
import random
from bs4 import BeautifulSoup

####################
#
####################

ITALIAN_VERB = "https://conjugator.reverso.net/conjugation-italian-verb-%s.html"
IDATA = 'data/italian'
CSVDATA = 'data/csvs'

# create database if need be
try:
    os.makedirs(IDATA)
    os.makedirs(CSVDATA)
except FileExistsError:
    pass


# write out the csvs, take care about quoting and encoding
def write_full_csv(rows):
    with open('%s/full-verbs.csv' % (CSVDATA), encoding='utf-8', mode='w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in rows:
            w.writerow(row)

def write_mini_csv(rows):
    with open('%s/mini-verbs.csv' % (CSVDATA), encoding='utf-8', mode='w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in rows:
            w.writerow(row[-2:])

####################
#
####################

def download_verb_data(verb):
    url = ITALIAN_VERB % verb
    datapath = '%s/%s.html' % (IDATA, verb)

    try:
        with (open(datapath, 'r')) as f:
            contents = f.read()
    except FileNotFoundError:
        contents = urllib.request.urlopen(url).read()
        with open(datapath, 'w') as f:
            f.write(contents.decode(encoding="utf-8", errors="strict"))

    soup = BeautifulSoup(contents, 'html.parser')
    body = soup.html.body
    return (body)


def one_block(body, pos, verb, mobile_title, prompt):
    mood_tense = mobile_title.split(' ')
    mood = mood_tense[0]
    tense = ' '.join(mood_tense[1:])
    for block in body.find_all('div', attrs={"mobile-title": mobile_title}):
        forms = []
        for li in block.find_all('li'):
            conjugation = li.text.split(' ')
            if len(conjugation) == 1:
                subject = '... '
                form = conjugation[0]
            elif conjugation[0] == 'che':
                subject = ' '.join(conjugation[0:2])
                form = ' '.join(conjugation[2:])
            else:
                subject = conjugation[0]
                form = ' '.join(conjugation[1:])
            subject = random.choice(subject.split('/'))

            if mood == 'Condizionale':
                form = 'se (%s) %s' % (subject, form)
            else:
                form = '(%s) %s' % (subject, form)

            if mobile_title == 'Gerundio Passato':
                combined = ' '.join([prompt, verb.upper()])
            else:
                combined = ' '.join([prompt, subject, verb.upper()])

            combined = combined.strip()
            form = form.strip()

            forms += [[str(pos), ':'.join(mood_tense), subject, verb.upper(), combined, form]]
        return (forms)


####################
#
####################

def one_conjugation(body, pos, verb, mobile_title, prompt, mode):
    forms = one_block(body, pos, verb, mobile_title, prompt)
    if len(forms) == 0:
        return[]
    elif mode == 'random':
        return([random.choice(forms)])
    elif mode == 'first':
        return([forms[0]])
    elif mode == 'firstplus' and len(forms) > 1:
        return([forms[0], random.choice(forms[1:])])
    return(forms)

####################
#
####################

forms = [
#    ["Indicativo Presente",             '(adesso)',             'all'],
#    ["Indicativo Imperfetto",           '(ieri)',               'firstplus'],
    ["Indicativo Passato remoto",       '(molto tempo fa)',     'random'],
    ["Indicativo Futuro semplice",      '(domani)',             'random'],
#    ["Indicativo Passato prossimo",     '(perfetto)',           'random'],
#    ["Indicativo Trapassato prossimo",  '(perchè ieri)',        'random'],
    ["Congiuntivo Presente",            '(presente)',           'random'],
    ["Congiuntivo Imperfetto",          '(ieri)',               'random'],
#    ["Congiuntivo Passato",             '(perfetto)',           'firstplus'],
    ["Condizionale Presente",           'se (presente)',        'rendom'],
   # ["Gerundio Presente",               '(...ndo)',             'random'],
   # ["Gerundio Passato",                '(passato ...ndo)',     'random'],
   # ["Participio Presente",             '(aggetivo)',           'random'],
   # ["Imperativo Presente",             '(per favore)',         'first'],
   # ["Indicativo Futuro anteriore"",    '???",               'random'],
   # ["Congiuntivo Trapassato",          '???",               'random'],
     ]

def one_verb(pos, verb):
    sys.stderr.write('[%s]\n' % (verb))
    body = download_verb_data(verb)
    rows = []
    for mobile_title, prompt, mode in forms:
        rows +=  one_conjugation(body, pos, verb, mobile_title, prompt, mode)

    return (rows)

def one_verb2(pos, verb):
    sys.stderr.write('[%s]\n' % (verb))
    body = download_verb_data(verb)
    rows = []
    rows +=  one_conjugation(body, pos, verb, "Indicativo Presente", prompt='adesso,', mode='all')
    # rows +=  one_conjugation(body, pos, verb, "Indicativo Imperfetto")
    # rows +=  one_conjugation(body, pos, verb, "Indicativo Passato remoto", mode='firstplus')
    # rows +=  one_conjugation(body, pos, verb, "Indicativo Futuro semplice")
    # rows +=  one_conjugation(body, pos, verb, "Indicativo Passato prossimo")
    # rows +=  one_conjugation(body, pos, verb, "Indicativo Trapassato prossimo")
    # rows +=  one_conjugation(body, pos, verb, "Indicativo Futuro anteriore")
    # rows +=  one_conjugation(body, pos, verb, "Congiuntivo Presente")
    # rows +=  one_conjugation(body, pos, verb, "Congiuntivo Passato")
    # rows +=  one_conjugation(body, pos, verb, "Congiuntivo Trapassato")
    # rows +=  one_conjugation(body, pos, verb, "Congiuntivo Imperfetto")
    # rows +=  one_conjugation(body, pos, verb, "Condizionale Presente")
    # rows +=  one_conjugation(body, pos, verb, "Condizionale Passato")
    # rows +=  one_conjugation(body, pos, verb, "Gerundio Presente")
    # rows +=  one_conjugation(body, pos, verb, "Gerundio Passato")
    # rows +=  one_conjugation(body, pos, verb, "Participio Presente")
    # rows +=  one_conjugation(body, pos, verb, "Participio Passato")
    # rows +=  one_conjugation(body, pos, verb, "Imperativo Presente", mode='first')
    #######    rows +=  one_conjugation(body, pos, verb, "Infinito Presente")
    return(rows)

def main():
    rows = [['Position', 'Mood:Tense', 'Subject', 'Infinitive', 'Front', 'Back']]
    with open('top37.dat') as f:
        for pos, verb in enumerate(f.readlines()):
            rows += one_verb(pos, verb.strip())
    random.shuffle(rows)
    write_full_csv(rows)
    write_mini_csv(rows)

if __name__ == '__main__':
    main()



