import sqlite3
import cmd
import queue
import random

from forms import MATCHING_FORMS

QUERY = '''
    select d.ROWID, c.form, c.verb, c.pos, c.conjugation, f.key from carddeck d 
    INNER JOIN cards c 
    ON d.ROWID = c.ROWID 
    INNER JOIN forms f
    ON f.form = c.form
    INNER JOIN appdb a
    ON a.verb = c.verb
    WHERE f.level IN ({levels})
    ORDER BY f.key, RANDOM()
    LIMIT {limit}
 '''


###########################
#
###########################

class AppSettings:
    def __init__(self, level):
        self.level = level
        self.db = '/Users/davidp/work/verbe-italiani/data/db/app.db'
        self.today = 1


class OneCard:
    def __lt__(self, other):
        return(self.key < other.key)

    def __init__(self, rowid, form, verb, pos, conjugation, key):
        self.rowid = rowid
        self.form = form
        self.verb = verb
        self.pos = pos
        self.conjugation = conjugation
        self.key = key

    def display_pos(self):
        pos_map = {
            0: "io",
            1: "tu",
            2: "lui",
            3: "lei",
            4: "noi",
            5: "voi",
            6: "loro(m)",
            7: "loro(f)",
        }
        if self.form in ['CONGIUNTIVO_PRESENTE', 'CONGIUNTIVO_IMPERFETTO', 'CONGIUNTIVO_PASSATO',
                         'CONGIUNTIVO_TRAPASSATO']:
            prefix = 'che '
        else:
            prefix = ''
        return(prefix + pos_map[self.pos])

    def generate_prompt(self, cursor, level):
        QUERY = '''
           SELECT f.display, c.conjugation FROM cards c INNER JOIN forms f ON c.form = f.form 
           WHERE c.verb = '{verb}' 
                AND pos = {pos} AND c.form IN ({forms}) 
                ORDER BY RANDOM() LIMIT 1
            '''
        forms = ','.join(MATCHING_FORMS[(level, self.form)])
        q = QUERY.format(verb=self.verb, pos=self.pos, forms=forms)
        rows = [row for row in cursor.execute(q)]
        form1, conjugation = rows[0]

        rows = [row for row in cursor.execute("select display from forms where form = '{form}'".format(form = self.form))]
        form2 = rows[0][0]
        return (form1, conjugation, form2, self.display_pos())

    def card_front(self, cursor, level):
        CARD_FRONT = '''
        +------------------------------------+
        |
        |    ({form1})
        |    
        |    {conjugation1}
        |    ---------------------
        |    ({form2})
        |    
        |    {prompt} _________?
        |    
        |    [space] 
        +------------------------------------+
        '''
        form1, conjugation, form2, prompt = self.generate_prompt(cursor, level)
        return (
            CARD_FRONT.format(level=level, form1=form1.lower(),
                              conjugation1=conjugation.upper(), form2=form2.lower(), prompt=prompt)
        )

    def card_back(self, cursor, level):
        CARD_BACK = '''
        +------------------------------------+
        |
        |    ({form1})
        |    
        |    {conjugation1}
        |    ---------------------
        |    ({form2})
        |    
        |    {conjugation2}
        |
        |    [x] [ ] [3] [4] [5]
        +------------------------------------+
        '''
        form1, conjugation, form2, _ = self.generate_prompt(cursor, level)
        return (
            CARD_BACK.format(level=level, form1=form1.lower(),
                              conjugation1=conjugation.upper(), form2=form2.lower(), conjugation2=self.conjugation)
        )


class FlashVerbItaliano(cmd.Cmd):

    def __init__(self, cursor, level):
        super(FlashVerbItaliano, self).__init__()
        self.cursor = cursor
        self.level = level
        self.todo = queue.SimpleQueue()
        self.redo = queue.SimpleQueue()
        self.card = None

    def load_cards(self):
        if self.level == 'A1':
            levels = "'A1'"
            limit = 25
        q = QUERY.format(limit=limit, levels=levels)
        rows = [row for row in self.cursor.execute(q)]
        for row in rows:
            self.todo.put(OneCard(*row))
        return(self)

    def do_start(self, line):
        self.card = self.todo.get()
        self.do_front(line)

    def do_front(self, line):
        print(self.card.card_front(self.cursor, self.level))

    def do_back(self, line):
        print(self.card.card_back(self.cursor, self.level))

    def do_5(self, line):
        self.card += 1
        self.do_front(line)

    def emptyline(self, line):
        pass


    def do_EOF(self, line):
        return True


def main():

    SETTINGS = AppSettings("A1")

    conn = sqlite3.connect(SETTINGS.db)
    cursor = conn.cursor()

    app = FlashVerbItaliano(cursor, SETTINGS.level).load_cards()
    app.cmdloop()


if __name__ == '__main__':
    main()
