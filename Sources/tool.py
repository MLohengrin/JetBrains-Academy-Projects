# Memorization Tool

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

MENUS = {'main':
             ['Add flashcards',
              'Practice flashcards',
              'Exit'],
         'add flashcards':
             ['Add a new flashcard',
              'Exit']
         }

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)


def print_menu(menu):
    for n, text in enumerate(MENUS[menu]):
        print(f'{n + 1}. {text}')


def flashcard_to_db(question, answer):
    Session = sessionmaker(bind=engine)
    session = Session()
    flashcard = Flashcard(question=question, answer=answer, box=1)
    session.add(flashcard)
    session.commit()


def add_new_flashcard():
    while True:
        print('Question:')
        question = input()
        if question == '' or question == " ":
            continue
        else:
            break
    while True:
        print('Answer:')
        answer = input()
        if answer == '' or answer == " ":
            continue
        flashcard_to_db(question, answer)
        # flashcards.append([question, answer])
        break


def add_flashcards():
    while True:
        print_menu('add flashcards')
        choice = input()
        if choice == '1':
            add_new_flashcard()
        elif choice == '2':
            break
        else:
            print(choice, 'is not an option')


def get_flashcards():
    Session = sessionmaker(bind=engine)
    session = Session()
    result_list = session.query(Flashcard).all()
    flashcards = []
    for flashcard in result_list:
        flashcards.append([flashcard.question, flashcard.answer, flashcard.box])
    return flashcards


def delete_flashcard(pair):
    Session = sessionmaker(bind=engine)
    session = Session()
    flashcards = session.query(Flashcard).filter(Flashcard.question == pair[0])
    session.delete(flashcards[0])
    session.commit()


def edit_flashcard(pair):
    print(f'current question: {pair[0]}')
    print('please write a new question:')
    new_question = input()
    if new_question == '' or new_question == ' ':
        new_question = pair[0]
    print(f'current answer: {pair[1]}')
    print('please write a new answer:')
    new_answer = input()
    if new_answer == '' or new_answer == ' ':
        new_answer = pair[1]
    Session = sessionmaker(bind=engine)
    session = Session()
    flashcards = session.query(Flashcard).filter(Flashcard.question == pair[0])
    flashcard = flashcards[0]
    flashcard.question = new_question
    flashcard.answer = new_answer
    flashcard.box = 1
    session.commit()


def update_flashcard(pair):
    while True:
        print('press "d" to delete the flashcard:\n'
              'press "e" to edit the flashcard:')
        choice = input()
        if choice == 'd':
            delete_flashcard(pair)
            break
        elif choice == 'e':
            edit_flashcard(pair)
            break
        else:
            print(choice, 'is not an option')


def new_rank_flashcard(pair, correctness):
    Session = sessionmaker(bind=engine)
    session = Session()
    flashcards = session.query(Flashcard).filter(Flashcard.question == pair[0])
    flashcard = flashcards[0]
    flashcard.box = flashcard.box + 1 if correctness == 'y' else 1
    session.commit()
    if flashcard.box == 3:
        delete_flashcard(pair)


def check_answer(pair):
    while True:
        print('press "y" if your answer is correct:\n'
              'press "n" if your answer is wrong:')
        choice = input()
        if choice == 'y':
            new_rank_flashcard(pair, 'y')
            break
        elif choice == 'n':
            new_rank_flashcard(pair, 'n')
            break
        else:
            print(choice, 'is not an option')


def practice_flashcards():
    flashcards = get_flashcards()
    if len(flashcards) == 0:
        print('There is no flashcard to practice!')
        return
    for pair in flashcards:
        print('Question:', pair[0])
        while True:
            print('press "y" to see the answer:\n'
                  'press "n" to skip:\n'
                  'press "u" to update:')
            choice = input()
            if choice == 'y':
                print('Answer:', pair[1])
                check_answer(pair)
                break
            elif choice == 'n':
                break
            elif choice == 'u':
                update_flashcard(pair)
                break
            else:
                print(choice, 'is not an option')


def connect_db():
    engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    return engine


def main():
    while True:
        print_menu('main')
        choice = input()
        if choice == '1':
            add_flashcards()
        elif choice == '2':
            practice_flashcards()
        elif choice == '3':
            print('Bye!')
            break
        else:
            print(choice, 'is not an option')


engine = connect_db()
main()
