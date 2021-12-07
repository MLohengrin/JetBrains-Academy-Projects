# Flashcards

import argparse
import builtins
import io
import json
import random

watcher = io.StringIO()
export_file = None


def print(*args, sep=' ', end='\n', file=None):
    builtins.print(*args, sep, end, file)
    builtins.print(*args, sep, end, file=watcher)


def input(*args, **kwargs):
    temp = builtins.input(*args, **kwargs)
    watcher.write(temp + '\n')
    return temp


class Card:
    cards = []

    def __init__(self, term, definition, mistakes=0):
        self.term = term
        self.definition = definition
        self.mistakes = mistakes
        Card.cards.append(self)

    @staticmethod
    def find_term(term):
        for card in Card.cards:
            if card.term == term:
                return card

    @staticmethod
    def find_definition(definition):
        for card in Card.cards:
            if card.definition == definition:
                return card

    @staticmethod
    def get_random_card():
        return random.choice(Card.cards)

    @staticmethod
    def reset_stats():
        for card in Card.cards:
            card.mistakes = 0

    @staticmethod
    def get_hardests():
        top_mistakes = 0
        for card in Card.cards:
            if card.mistakes > top_mistakes:
                top_mistakes = card.mistakes
        hardests = []
        if top_mistakes == 0:
            return hardests
        for card in Card.cards:
            if card.mistakes == top_mistakes:
                hardests.append(card)
        return hardests


# obsolete
def get_options():
    print('Input the number of cards:')
    tot_cards = int(input())
    return tot_cards


def add_card():
    print(f'The card')
    while True:
        term = input()
        if Card.find_term(term):
            print(f'The card "{term}" already exists. Try again:')
        else:
            break
    print(f'The definition of the card:')
    while True:
        definition = input()
        if Card.find_definition(definition):
            print(f'The definition "{definition}" already exists. Try again:')
        else:
            break
    Card(term, definition)
    print(f'The pair ("{term}":"{definition}") has been added.')


def remove_card():
    print('Which card?')
    to_remove = input()
    card = Card.find_term(to_remove)
    if card:
        Card.cards.remove(card)
        print('The card has been removed.')
    else:
        print(f'Can\'t remove "{to_remove}": there is no such card.')


def update_cards(json_dict):
    for term, attributes in json_dict.items():
        old_card = Card.find_term(term)
        if old_card:
            old_card.definition = attributes[0]
            old_card.mistakes = attributes[1]
        else:
            Card(term, attributes[0], attributes[1])


def import_cards(file_name=None):
    if not file_name:
        print('File name:')
        file_name = input()
    try:
        with open(file_name, 'r') as json_file:
            json_dict = json.load(json_file)
    except FileNotFoundError:
        print('File not found.')
        return
    update_cards(json_dict)
    print(f'{len(json_dict)} cards have been loaded.')
    return


def cards_to_dict():
    ext_dict = dict()
    for card in Card.cards:
        ext_dict[card.term] = [card.definition, card.mistakes]
    return ext_dict


def export_cards(file_name=None):
    json_dict = cards_to_dict()
    if not file_name:
        print('File name:')
        file_name = input()
    with open(file_name, 'w') as json_file:
        json.dump(json_dict, json_file)
    print(f'{len(json_dict)} cards have been saved.')


def ask_card():
    print('How many times to ask?')
    n_cards = int(input())
    for _ in range(n_cards):
        card = Card.get_random_card()
        print(f'Print the definition of "{card.term}"')
        answer = input()
        if answer == card.definition:
            print('Correct!')
        else:
            alt_card = Card.find_definition(answer)
            if alt_card:
                print(
                    f'Wrong. The right answer is "{card.definition}", but your definition is correct for "{alt_card.term}".')
            else:
                print(f'Wrong. The right answer is "{card.definition}"')
            card.mistakes += 1


# TODO
def activate_log():
    print('File name:')
    log_name = input()
    with open(log_name, 'w') as f:
        f.write(watcher.getvalue())
    print('The log has been saved.')


def hardest_card():
    hardests = Card.get_hardests()
    if len(hardests) == 0:
        print('There are no cards with errors.')
    elif len(hardests) == 1:
        print(f'The hardest card is "{hardests[0].term}". You have {hardests[0].mistakes} errors answering it')
    else:
        p_cards = ', '.join(['\"' + c.term + '\"' for c in hardests])
        print(f'The hardest cards are {p_cards}. You have {hardests[0].mistakes} errors answering it.')


def reset_stats():
    Card.reset_stats()
    print('Card statistics have been reset.')


def select_option():
    print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
    choice = input()
    if choice == 'add':
        add_card()
    elif choice == 'remove':
        remove_card()
    elif choice == 'import':
        import_cards()
    elif choice == 'export':
        export_cards()
    elif choice == 'ask':
        ask_card()
    elif choice == 'log':
        activate_log()
    elif choice == 'hardest card':
        hardest_card()
    elif choice == 'reset stats':
        reset_stats()
    elif choice == 'exit':
        print('Bye bye!')
        if export_file:
            export_cards(export_file)
        watcher.close()
        exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--import_from')
    parser.add_argument('--export_to')
    args = parser.parse_args()
    if args.import_from:
        import_cards(args.import_from)
    if args.export_to:
        global export_file
        export_file = args.export_to
    while True:
        select_option()


if __name__ == "__main__":
    main()
