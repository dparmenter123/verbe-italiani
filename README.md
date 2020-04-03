# verbe-italiani

This site is a work in progress designed to help me (and maybe you!) learning the many, many conjugations of Italian verbs.

Key principles:
* Learning verbs is hard!
* Flashcards do work (for me)
* Take an easy form (indicativo) on the front, and learn to conjugate it into the specified form on the back

The system relies on the kindness of reverso.net to get the conjugated forms. I use BeautifulSoup to parse the output, and cache the html in _data/html/*.html_ so as to not hit reverso.net too much.

## ./scripts
* _filter.sh_ - takes an input CSV and filters it by verb type, picking one random element from each form
* _flashcards.py_ - takes a verb list, downloads each verb, and generates a CSV with all of the forms. The CSV can be tailored to your needs, and flashcard system. I use Anki and Notecards+.

## ./data/lists
* _top37.dat_ -- a somewhat random combination of common regular, irregular, and reflexive verbs
* _sorted.it.word.unigrams_ -- a massive list of italian words sorted by frequency. You need to filter it and cut it down based on your goals. Then it can be used as input to _flashcards.py_

## how to filter the big list of words
this will take the list, filter in verb like words, pick the top 500 and then pick the verb, and not the frequency.

cat sorted.it.word.unigrams | egrep '(ire|are|ere)$' | head -500 | cut -f2

## how to filter the output
cat top233.csv | egrep 'Passato prossimo' | cut -d ',' -f 4 -f 5 | gshuf > top233-perfetto.csv
cat top233.csv | egrep 'Congiuntivo (Presente|Imperfetto)' | cut -d ',' -f 4 -f 5 | gshuf > top233-congiuntivo.csv
