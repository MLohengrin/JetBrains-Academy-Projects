# Coffee Machine

class CoffeeMachine:

    def __init__(self):
        self.water = 400
        self.milk = 540
        self.coffee_beans = 120
        self.disposable_cups = 9
        self.money = 550
        self.state = "main"

    def input(self, input):
        if self.state == "action":
            if input == "buy":
                self.state = "buying"
                print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")
            elif input == "fill":
                self.state = "fill_water"
            elif input == "take":
                self.take()
                print("Write action (buy, fill, take, remaining, exit)")
                self.state = "action"
            elif input == "remaining":
                self.status()
                print("Write action (buy, fill, take, remaining, exit)")
                self.state = "action"
            elif input == "exit":
                self.state = "exit"
        elif self.state == "buying":
            if input == "1":
                self.subtract(250, 0, 16, 4)
            elif input == "2":
                self.subtract(350, 75, 20, 7)
            elif input == "3":
                self.subtract(200, 100, 12, 6)
            # elif input == "back":
            # else:
            #     print("Ops")
            self.state = "main"
        elif self.state == "fill_water":
            print("Write how many ml of water do you want to add:")
            self.water += int(input)
            self.state = "fill_milk"
        elif self.state == "fill_milk":
            print("Write how many ml of milk do you want to add:")
            self.milk += int(input)
            self.state = "fill_coffee"
        elif self.state == "fill_coffee":
            print("Write how many grams of coffee beans do you want to add:")
            self.coffee_beans += int(input)
            self.state = "fill_cups"
        elif self.state == "fill_cups":
            print("Write how many disposable cups of coffee do you want to add:")
            self.disposable_cups += int(input)
            self.state = "main"

    # def fill(self):
    #     print("Write how many ml of water do you want to add:")
    #     water = int(input())
    #     self.water += water
    #     print("Write how many ml of milk do you want to add:")
    #     milk = int(input())
    #     self.milk += milk
    #     print("Write how many grams of coffee beans do you want to add:")
    #     coffee = int(input())
    #     self.coffee_beans += coffee
    #     print("Write how many disposable cups of coffee do you want to add:")
    #     cups = int(input())
    #     self.disposable_cups += cups

    # def buy(self):
    #     print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")
    #     if choice == "1":
    #         self.subtract(250, 0, 16, 4)
    #     elif choice == "2":
    #         self.subtract(350, 75, 20, 7)
    #     elif choice == "3":
    #         self.subtract(200, 100, 12, 6)
    #     elif choice == "back":
    #         return
    #     else:
    #         print("Ops")

    def subtract(self, water, milk, coffee, money):
        if self.water >= water:
            self.water -= water
        else:
            print("Sorry, not enough water")
            return
        if self.milk >= milk:
            self.milk -= milk
        else:
            print("Sorry, not enough milk")
            return
        if self.coffee_beans >= coffee:
            self.coffee_beans -= coffee
        else:
            print("Sorry, not enough coffee")
            return
        if self.disposable_cups >= 1:
            self.disposable_cups -= 1
        else:
            print("Sorry, not enough cups")
            return
        self.money += money

    def status(self):
        print("The coffe machine has:\n"
              "%d of water\n"
              "%d of milk\n"
              "%d of coffee beans\n"
              "%d of disposable cups\n"
              "%d of money\n"
              % (self.water, self.milk, self.coffee_beans, self.disposable_cups, self.money))

    # def action(self, action):
    #     print("Write action (buy, fill, take, remaining, exit)")
    #     if action == "buy":
    #         self.buy()
    #         return True
    #     elif action == "fill":
    #         self.fill()
    #         return True
    #     elif action == "take":
    #         self.take()
    #         return True
    #     elif action == "remaining":
    #         self.status()
    #         return True
    #     elif action == "exit":
    #         return False

    def take(self):
        print("I gave you $%d" % self.money)
        self.money = 0


coffee_machine = CoffeeMachine()

while coffee_machine.state != "exit":
    if coffee_machine.state == "main":
        print("Write action (buy, fill, take, remaining, exit)")
        coffee_machine.state = "action"
    coffee_machine.input(input())
