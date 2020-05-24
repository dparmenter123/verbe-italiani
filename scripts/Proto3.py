import enum
import queue
from transitions import Machine
import random

TODAY = 1

class Card:
    def __init__(self, section, id, time, repetitions=0, interval=1, easiness=2.5, next_practice=0):
        self.section = section
        self.id = id
        self.time = time
        self.repetitions = repetitions
        self.interval = interval
        self.easiness = easiness
        self.next_practice = next_practice

    def update(self, quality, time):
        # SM-2
        assert quality >= 0 and quality <= 5
        self.easiness = max(1.3, self.easiness + 0.1 - (5.0 - quality) * (0.08 + (5.0 - quality) * 0.02))
        if quality < 3:
            self.repetitions = 0
        else:
            self.repetitions += 1
        if self.repetitions == 1:
            self.interval = 1
        elif self.repetitions == 2:
            self.interval = 6
        else:
            self.interval *= self.easiness
        self.time = time


    def __repr__(self):
        return('{section} / {id}  | [time:{time}] [rep:{repetitions}] [int:{interval}] [ease:{easiness}] [next:{next_practice}]'.format(
            section=self.section, id = self.id, time=self.time, repetitions=self.repetitions, interval=self.interval,
            easiness=self.easiness, next_practice=self.next_practice
        ))


CARD_DECK = [
    Card('AAA', 1, 0),
    Card('AAA', 2, 0),
    Card('BBB', 3, 0),
    Card('CCC', 4, 0),
    Card('DDD', 5, 0),
    Card('DDD', 6, 0),
    Card('DDD', 7, 0),
]


class Proto3Model(object):
    def __init__(self):
        self.todo = queue.SimpleQueue()
        self.redo = queue.SimpleQueue()
        self.done = queue.LifoQueue()

        for card in CARD_DECK:
            self.todo.put(card)

        assert self.todo.qsize() > 0
        self.card = self.todo.get()
        self.section = self.card.section

    def dump_state(self):
        state = '''
        ============
          TODO: {todo}
          REDO: {redo}
          DONE: {done}
          CURRENT: {section} / {card}
       ============ 
        '''
        print(state.format(
            todo=self.todo.qsize(), redo=self.redo.qsize(), done=self.done.qsize(),
            section=self.section, card=self.card))

    def on_enter_BUILD(self):
        print('building')
        self.homeview()

    def on_enter_HOME_VIEW(self):
        print('homeview...')
        view = '''
        +-------------
        | HOME
        |
        | * study
        | * settings
        +-------------
        '''
        print(view)
        self.dump_state()

    def on_enter_ANY_TO_STUDY(self):
        print('any to study?')
        print('  todo:', self.todo.qsize())
        print('  card[%s]' %  self.card)
        if self.todo.qsize() > 0 or self.card:
            print('  yes')
            self.any_to_study_yes()
        else:
            print('  no')
            self.any_to_study_no()

    def on_enter_DONE(self):
        print('done!')

    def on_enter_SECTION_VIEW(self):
        view = '''
        +--------
        | SECTION
        |
        |    {section}
        |
        |  * front
        |  * home
        +----------
        '''
        print(view.format(section=self.card.section))
        self.front()

    def on_enter_FRONT_VIEW(self):
        view = '''
         +--------
         | FRONT
         |
         |    {card}
         |
         |  * flip
         |  * home
         +----------
         '''
        print(view.format(card=self.card))
        self.flip()

    def on_enter_BACK_VIEW(self):
        view = '''
         +--------
         | BACK
         |
         |    {card}
         |
         |  * correct
         |  * wrong
         +----------
         '''
        print(view.format(card=self.card))
        if card.id % 2 == 0 or
        if random.random() < 0.33:
            self.correct()
        else:
            self.wrong()

    def on_enter_CORRECT(self):
        print('CORRECT!')
        self.card.update(3, TODAY)
        self.done.put(self.card)
        self.card = None
        self.correct2()

    def on_enter_WRONG(self):
        print('WRONG!')
        self.card.update(0, TODAY)
        self.redo.put(self.card)
        self.card = None
        self.wrong2()

    def on_enter_MORE_TODO(self):
        print('More to do?')
        self.dump_state()
        if self.todo.qsize() > 0:
            print('  yes')
            self.card = self.todo.get()
            self.more_todo_yes()
        else:
            print('  no')
            self.more_todo_no()

    def on_enter_ANY_TO_REDO(self):
        assert self.todo.qsize() == 0
        assert not self.card
        print('Any to redo?')

        if self.redo.qsize() > 0:
            while self.redo.qsize() > 0:
                card = self.redo.get()
                self.todo.put(card)
            self.card = self.todo.get()
            self.any_to_redo_yes()
        else:
            self.any_to_redo_no()

    def on_enter_NEW_SECTION(self):
        print('new section?')
        self.dump_state()
        if self.section != self.card.section:
            print('  yes')
            self.new_section_yes()
        else:
            print('  no')
            self.new_section_no()

# The states
class States(enum.Enum):
    ERROR = 0
    START = 1
    BUILD = 2
    HOME_VIEW = 3
    ANY_TO_STUDY = 4
    SECTION_VIEW = 5
    FRONT_VIEW = 6
    BACK_VIEW = 7
    CORRECT = 8
    WRONG = 9
    MORE_TODO = 10
    ANY_TO_REDO = 11
    NEW_SECTION = 12
    DONE = 99

transitions = [
    ['build', States.START, States.BUILD ],
    ['homeview', States.BUILD, States.HOME_VIEW ],
    ['study', States.HOME_VIEW, States.ANY_TO_STUDY ],
    ['any_to_study_no', States.ANY_TO_STUDY, States.DONE ],
    ['any_to_study_yes', States.ANY_TO_STUDY, States.SECTION_VIEW ],
    ['front', States.SECTION_VIEW, States.FRONT_VIEW ],
    ['flip', States.FRONT_VIEW, States.BACK_VIEW ],
    ['flip_back', States.BACK_VIEW, States.FRONT_VIEW ],
    ['home1', States.SECTION_VIEW, States.HOME_VIEW],
    ['home2', States.FRONT_VIEW, States.HOME_VIEW],
    ['wrong', States.BACK_VIEW, States.WRONG],
    ['correct', States.BACK_VIEW, States.CORRECT],
    ['correct2', States.CORRECT, States.MORE_TODO],
    ['wrong2', States.WRONG, States.MORE_TODO],
    ['more_todo_yes', States.MORE_TODO, States.NEW_SECTION],
    ['more_todo_no', States.MORE_TODO, States.ANY_TO_REDO],
    ['any_to_redo_yes', States.ANY_TO_REDO, States.NEW_SECTION],
    ['any_to_redo_no', States.ANY_TO_REDO, States.DONE],
    ['new_section_yes', States.NEW_SECTION, States.SECTION_VIEW],
    ['new_section_no', States.NEW_SECTION, States.FRONT_VIEW]
]

def main():
    model = Proto3Model()
    machine = Machine(model, states=States, transitions=transitions, initial=States.START)
    model.build()
    model.study()
    while(model.state != States.DONE):
        model.front()


if __name__ == '__main__':
    main()
