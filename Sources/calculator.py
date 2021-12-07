# Smart Calculator

from collections import deque


class Calculator:
    def __init__(self) -> None:
        self.variables = dict()
        self.main()

    def main(self):
        while True:
            usr_inp = self.splitter(input())
            if len(usr_inp) == 0:
                pass
            elif len(usr_inp) == 1:
                inp = usr_inp[0]
                if inp.startswith("/"):
                    if inp == "/exit":
                        print("Bye!")
                        break
                    elif inp == "/help":
                        self.help()
                    else:
                        print("Unknown command")
                else:
                    if inp.isnumeric():
                        print(int(inp))
                    else:
                        if '=' in inp:
                            self.assignment(usr_inp)
                        elif self.is_valid_name(inp):
                            if inp in self.variables:
                                print(self.variables[inp])
                            else:
                                print("Unknown variable")
                        else:
                            print("Invalid identifier")
            else:
                if "=" in "".join(usr_inp):
                    self.assignment(usr_inp)
                else:
                    self.calculate(usr_inp)

    def splitter(self, args):
        out = list()
        temp = list()
        if args.startswith("/"):
            out.append(args)
            return out
        for char in args:
            if char.isnumeric():
                if temp and not temp[-1].isnumeric():
                    out.append("".join(temp))
                    temp.clear()
                temp.append(char)
            elif char.isalpha():
                if temp and not temp[-1].isalpha():
                    out.append("".join(temp))
                    temp.clear()
                temp.append(char)
            elif char == '+':
                if temp and not temp[-1] == '+':
                    out.append("".join(temp))
                    temp.clear()
                temp.append(char)
            elif char == '-':
                if temp and not temp[-1] == '-':
                    out.append("".join(temp))
                    temp.clear()
                temp.append(char)
            elif char == ' ':
                continue
            else:
                out.append("".join(temp))
                temp.clear()
                temp.append(char)
        if temp:
            out.append("".join(temp))
        return out

    def is_valid_name(self, var):
        return var.isalpha()

    def help(self):
        print("The program calculates the sum of number")

    def calculate(self, args):
        operators = deque()
        result = deque()
        total = deque()
        # Looping on the input arguments
        for arg in args:
            if arg.startswith('+'):
                arg = '+'
            if not arg.isnumeric() and arg.startswith('-'):
                if arg.count('-') % 2:
                    arg = '-'
                else:
                    arg = '+'
            # Add operands (numbers and variables) to the result (postfix notation) as they arrive.
            if arg.isnumeric() or (self.is_valid_name(arg) and arg in self.variables):
                result.append(arg)
            # If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
            elif len(operators) == 0 or operators[-1] == '(':
                operators.append(arg)
            # If the incoming operator has higher precedence than the top of the stack, push it on the stack.
            elif (arg == '*' or arg == '/') and (operators[-1] == '+' or operators[-1] == '-'):
                operators.append(arg)
            # If the precedence of the incoming operator is lower than or equal to that of the top of the stack, pop the stack and add operators to the result until you see an operator that has smaller precedence or a left parenthesis on the top of the stack; then add the incoming operator to the stack.
            elif arg == '+' or arg == '-':  # and (operators[-1] == '*' or operators[-1] == '/'):
                while len(operators) != 0 and operators[-1] != '(':
                    result.append(operators.pop())
                operators.append(arg)
            elif (arg == '*' or arg == '/') and (operators[-1] == '*' or operators[-1] == '/'):
                while len(operators) != 0 and operators[-1] != '+' and operators[-1] != '-' and operators[-1] != '(':
                    result.append(operators.pop())
                operators.append(arg)
            # If the incoming element is a left parenthesis, push it on the stack.
            elif arg == '(':
                operators.append(arg)
            # If the incoming element is a right parenthesis, pop the stack and add operators to the result until you see a left parenthesis. Discard the pair of parentheses.
            elif arg == ')':
                while operators and operators[-1] != '(':
                    result.append(operators.pop())
                if operators:
                    operators.pop()
                else:
                    print("Invalid expression")
                    return
            else:
                print("Invalid expression")
                return
        # Flush every operator left in result
        while len(operators) != 0:
            if operators[-1] != '(':
                result.append(operators.pop())
            else:
                break
        # Check for unbalanced brackets
        if len(operators) != 0:
            print("Invalid expression")
            return
        # Time to calculate the result
        while len(result) != 0:
            # If the incoming element is a number, push it into the stack (the whole number, not a single digit!).
            if result[0].isnumeric():
                total.append(int(result.popleft()))
            # If the incoming element is the name of a variable, push its value into the stack.
            elif self.is_valid_name(result[0]):
                total.append(self.variables[result.popleft()])
            else:
                try:
                    op, n2, n1 = result.popleft(), int(total.pop()), int(total.pop())
                    if op == '+':
                        total.append(n1 + n2)
                    elif op == '-':
                        total.append(n1 - n2)
                    elif op == '*':
                        total.append(n1 * n2)
                    elif op == '/':
                        total.append(n1 // n2)
                except IndexError:
                    print("Invalid expression")
                    return
        print(total.pop())

    def calculate_old(self, args):
        if len(args) % 2:
            minus = False
            tot = 0
            for arg in enumerate(args):
                value = arg[1]
                if self.is_valid_name(arg[1]) and arg[1] in self.variables:
                    value = self.variables[arg[1]]
                try:
                    if not arg[0] % 2:
                        tot += int(value) * (-1 if minus else 1)
                        minus = False
                    else:
                        if arg[1][0] == "-":
                            if len(arg[1]) % 2:
                                minus = True
                except (ValueError, TypeError):
                    print("Invalid expression")
            print(tot)
        else:
            print("Invalid expression")

    def assignment(self, inp):
        new_inp = "".join(inp).replace(" ", "").split('=')
        if len(new_inp) != 2:
            print("Invalid assignment")
        else:
            sx, dx = new_inp[0], new_inp[1]
            if not self.is_valid_name(sx):
                print("Invalid identifier")
                return
            if not self.is_valid_name(dx) and not dx.isnumeric():
                print("Invalid assignment")
                return
            if dx.isnumeric():
                self.variables[sx] = dx
            elif dx in self.variables:
                self.variables[sx] = self.variables[dx]
            else:
                print("Unknown variable")
                return


Calculator()
