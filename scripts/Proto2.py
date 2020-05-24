from statemachine import StateMachine, State
import queue

TODAY = 0
class Card:
    def __init__(self, section, id, repetitions=0, interval=1, easiness=2.5, next_practice=0):
        self.section = section
        self.id = id
        self.repetitions = repetitions
        self.interval = interval
        self.easiness = easiness
        self.next_practice = next_practice

CARD_DECK = [
    Card('section 1', 1),
    Card('section 1', 2),
    Card('section 2', 3),
    Card('section 3', 4),
    Card('section 4', 5),
    Card('section 4', 6),
    Card('section 4', 7),
]

class AppStateMachine(StateMachine):
    initialize = State('initialize', initial=True)
    build = State('build')
    doneview = State('done view')
    homeview = State('home view')
    settingsview = State('settings view')
    any_to_study_p = State('any to study?')
    sectionview = State('section view')
    frontview = State('front view')
    backview = State('back view')
    correct = State('correct')
    wrong = State('wrong')
    more_todo_p = State('more to do?')
    any_to_redo_p = State('any to redo?')
    new_section_p = State('new section?')
    
    initialize_to_build = initialize.to(build)

    build_to_home_view = build.to(homeview)

    homeview_to_settings = homeview.to(settingsview)
    homeview_to_any_to_study = homeview.to(any_to_study_p)

    settings_to_build = settingsview.to(build)

    any_to_study_yes = any_to_study_p.to(sectionview)
    any_to_study_no = any_to_study_p.to(doneview)

    sectionview_to_homeview = sectionview.to(homeview)
    sectionview_to_frontview = sectionview.to(frontview)

    frontview_to_homeview = frontview.to(homeview)
    frontview_to_backview = frontview.to(backview)

    backview_to_frontview = backview.to(frontview)
    backview_to_homeview = backview.to(homeview)
    backview_to_wrong = backview.to(wrong)
    backview_to_correct = backview.to(correct)

    correct_to_more_todo = correct.to(more_todo_p)
    wrong_to_more_todo = wrong.to(more_todo_p)

    more_todo_yes = more_todo_p.to(new_section_p)
    more_todo_no = more_todo_p.to(any_to_redo_p)

    any_to_redo_yes = any_to_redo_p.to(new_section_p)
    any_to_redo_no = any_to_redo_p.to(doneview)

    def __init__(self):
        super(AppStateMachine, self).__init__(self)
        self.todo = queue.SimpleQueue()
        self.redo = queue.LifoQueue()
        self.sections = []
        self.current_card = None

    def on_enter_done(self):
        print('done')

    def on_enter_initialize(self):
        print('initialize', initial=True)
        self.initialize_to_build()

    def on_enter_build(self):
        print('entering build')
        for card in CARD_DECK:
            if card.next_practice <= TODAY:
                if card.section not in self.sections: self.sections += [card.section]
                self.todo.put((card))
        if self.todo.qsize() > 0:
            self.current_card = self.todo.get()
        self.build_to_home_view()

    def on_enter_homeview(self):
        print('entering home')
        view = '''
        +----------------
        | HOME
        |
        | * settings?
        | * study
        +----------------
        '''
        print(view)
        self.homeview_to_any_to_study()

    def on_enter_settingsview(self):
        print('settings view')

    def on_enter_any_to_study_p(self):
        print('entering any to study?')
        if self.current_card:
            print('yes')

    def on_enter_sectionview(self):
        print('section view')

    def on_enter_frontview(self):
        print('front view')

    def on_enter_backview(self):
        print('back view')

    def on_enter_correct(self):
        print('correct')

    def on_enter_wrong(self):
        print('wrong')

    def on_enter_more_todo_p(self):
        print('more todo?')

    def on_enter_any_to_redo_p(self):
        print('any to redo?')

    def on_enter_new_section_p(self):
        print('new section?')



    # def on_enter_home(self):
    #     prompt = '''
    #     +----------------
    #     | HOME:
    #     |
    #     | DUE: {todo} / {redo}
    #     |
    #     | menu:
    #     |  * start
    #     +-----------------
    #     '''
    #     print(prompt.format(todo=self.todo.qsize() + 1,
    #                         redo=self.redo.qsize()))
    #
    # def on_enter_section(self):
    #     prompt = '''
    #     +----------------
    #     | SECTION:
    #     |
    #     |    {section}
    #     |
    #     | menu:
    #     |  * forward
    #     |  * back
    #     +-----------------
    #     '''
    #     print(prompt.format(section=self.current_card[0]))
    #
    # def on_enter_front(self):
    #     prompt = '''
    #     +----------------
    #     | FRONT:
    #     |
    #     |    {card}
    #     |
    #     | menu:
    #     |  * flip
    #     +-----------------
    #     '''
    #     print(prompt.format(card=self.current_card[1]))
    #
    # def on_enter_back(self):
    #     prompt = '''
    #     +----------------
    #     | BACK:
    #     |
    #     |    {card}
    #     |
    #     | menu:
    #     |  * wrong
    #     |  * right_3
    #     |  * right_4
    #     |  * right_5
    #     +-----------------
    #     '''
    #     print(prompt.format(card=self.current_card[1]))
    #
    # def on_enter_wrong(self):
    #     print('wrong')

def main():
    app = AppStateMachine()
    app.initialize_to_build()

if __name__ == '__main__':
    main()
