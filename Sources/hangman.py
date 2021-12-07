# Hangman

import random

answer_list = ['python', 'java', 'kotlin', 'javascript']
print("H A N G M A N")

while True:
    choice = input('Type "play" to play the game, "exit" to quit: ')
    if choice == "exit":
        break
    elif choice == "play":
        lives = 8
        correct_answer = answer_list[random.randint(0, len(answer_list) - 1)]
        letters_available = set(correct_answer)
        answer_showed = "-" * len(correct_answer)
        answer_showed = list(answer_showed)
        guessed = set()
        while lives > 0 and "-" in answer_showed:

            print()
            print("".join(answer_showed))
            letter = input("Input a letter: ")
            if len(letter) != 1:
                print("You should input a single letter")
            elif not letter.islower():
                print("Please enter a lowercase English letter")
            elif letter in guessed:
                print("You've already guessed this letter")
            else:
                if letter in letters_available:
                    letters_available.discard(letter)
                    for char in range(len(answer_showed)):
                        if correct_answer[char] == letter:
                            answer_showed[char] = letter
                else:
                    if letter not in correct_answer:
                        print("That letter doesn't appear in the word")
                    else:
                        print("No improvements")
                    lives -= 1
                guessed.add(letter)

        if lives > 0:
            print("You guessed the word!\nYou survived!")
        else:
            print("You lost!")
