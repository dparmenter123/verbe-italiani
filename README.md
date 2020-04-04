# verbe-italiani

This site is a work in progress designed to help me (and maybe you!) learning the many, many conjugations of Italian verbs.

Key principles:
* Learning verbs is hard!
* Flashcards do work (for me), in concert with all the other ways you need to study
* So I pick a random form of the present for the FRONT of the card, and on the BACK, showthe same person/number for each of the other moods/tenses

The system relies on the kindness of reverso.net to get the conjugated forms. I use BeautifulSoup to parse the output, and cache the html in _data/html/*.html_ so as to not hit reverso.net too much.

## system requirements

* Python 3.x
* Typical venv, as documented in requirements.txt
* I use homebrew for mac, and so should you
* Recommend installing 'brew install coreutils' to get some useful command line utilities, including the wonderful _gshuf_


## Flashcards Apps

I have tested this with Anki Desktop (OSX), and Notecards+ (iOS)

## Output
Output is a CSV, with these columns

~~~
    Position    POS       Verb        Form                  Front                                   Back
    --------    ---       ----        ----                  -----                                   ----
    "0",	4,        "finire",  "Imperfetto",          "noi finiamo -> Imperfetto",            "noi finivamo"
    "0",        6,        "finire",  "Passato remoto",      "loro(m) finiscono -> Passato Remoto",  "loro(m) finirono"
    "0",        7,        "finire",  "Futuro semplice",     "loro(f) finiscono -> Futuro",          "loro(f) finiranno"
    "0",        1,        "finire",  "Passato prossimo",    "tu finisci -> Perfetto",               "tu hai finito"
    "0",        0,      , "finire",  "Trapassato prossimo", "io finisco -> Trapassato Prossimo",    "io avevo finito"
    "0",        "random", "finire",  "Trapassato prossimo", "io finisco -> Trapassato Prossimo",    "io avevo finito"
~~~

With the following definitions:
* Position -- position from the input file. If your input is sorted by frequency, this gives you a way to prioritize / cut
* POS -- part of speech: 0 == IO, 1 == TU, 2 == LUI, 3 == LEI, ...
* POS -- random is a random choice from the previous 8, useful to filter down
* Verb -- e.g. 'pensare', 'svegliarsi'...
* Form -- Italian name of the form, useful for filtering
* Front -- front of the card
* Back -- back of the card

## Loading this in Excel

Works.

## ./scripts* _filter.sh_ - takes an input CSV and filters it by verb type, picking one random element from each form
* _flashcards.py_ - takes a verb list, downloads each verb, and generates a CSV with all of the forms. The CSV can be tailored to your needs, and flashcard system. I use Anki and Notecards+.

## Generating flashcards

~~~
    python ./scripts/flashcards.py data/lists/top233.dat data/csvs/top233.csv
~~~

## ./data/lists
* _top37.dat_ -- a somewhat random combination of common regular, irregular, and reflexive verbs
* _sorted.it.word.unigrams_ -- a massive list of italian words sorted by frequency. You need to filter it and cut it down based on your goals. Then it can be used as input to _flashcards.py_

## how to filter the big list of words
this will take the list, filter in verb like words, pick the top 500 and then pick the verb, and not the frequency.

cat sorted.it.word.unigrams | egrep '(ire|are|ere)$' | head -500 | cut -f2

## how to filter the output

Here are all the forms, note the spellings
* Indicativo Condizionale Presente
* Indicativo Condizionale Passato
* Indicativo Imperfetto
* Indicativo Passato remoto
* Indicativo Futuro semplice
* Indicativo Passato prossimo
* Indicativo Trapassato prossimo
* Indicativo Futuro anteriore
* Congiuntivo Presente
* Congiuntivo Passato
* Congiuntivo Trapassato
* Congiuntivo Imperfetto

~~~
    # gshuf is a super useful utility that randomizes the input records. Anki does not do that, stupidly.
    
    # to study a random set of the top 233 perfect (PP) forms
    $ cat top236.csv | egrep 'random' | egrep 'Passato prossimo' | cut -d ',' -f 5 -f 6 | gshuf > top236-perfetto.csv
    
    # to study both forms of the subjunctive
    $ cat top236.csv | egrep 'random' | egrep 'Congiuntivo (Presente|Imperfetto)' | cut -d ',' -f 5 -f 6 | gshuf > top236-congiuntivo.csv
~~~
