# Rock-Paper-Scissors

# Write your code here
import random


def match(user_choice, computer_choice):
    result = ""

    if user_choice == computer_choice:
        result = "draw"
    else:
        # if user_choice == "paper":
        #     if computer_choice == "rock":
        #         result = "win"
        #     else:
        #         result = "lose"
        user_index = choices.index(user_choice)
        computer_index = choices.index(computer_choice)
        gap = (len(choices) // 2) - user_index
        computer_index_gapped = (computer_index + gap) % len(choices)
        if computer_index_gapped > len(choices) / 2:
            result = "lose"
        else:
            result = "win"
    return result


def read_score(name):
    f = open("rating.txt", "a+")
    for line in f:
        player, rating = line.split()
        if player == name:
            f.close()
            return int(rating)
    f.close()
    return 0


name = input("Enter your name: ")
print("Hello, %s" % name)
score = read_score(name)
choices = input()
if choices == "":
    choices = ["rock", "paper", "scissors"]
else:
    choices = choices.split(",")
print("Okay, let's start")

while True:
    user_choice = input()
    if user_choice in choices:
        computer_choice = choices[random.randint(0, len(choices) - 1)]
        result = match(user_choice, computer_choice)

        if result == "lose":
            print("Sorry, but the computer chose %s" % computer_choice)
        elif result == "draw":
            print("There is a draw (%s)" % computer_choice)
            score += 50
        elif result == "win":
            print("Well done. The computer chose %s and failed" % computer_choice)
            score += 100
    elif user_choice == "!exit":
        print("Bye!")
        break
    elif user_choice == "!rating":
        print("Your rating: %s" % score)
    else:
        print("Invalid input")
