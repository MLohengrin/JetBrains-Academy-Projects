class Matrix:
    TRANSPOSITIONS = ("main", "side", "vertical", "horizontal")

    def __init__(self, sizes, empty=False):
        self.body = self.generate(sizes) if not empty else list()
        self.sizes = [int(sizes[0]), int(sizes[1])]

    def __str__(self):
        matrix = ""
        for row in self.body:
            for n in row:
                matrix += str(n) + " "
            matrix = matrix.rstrip(" ")
            matrix += "\n"
        return matrix.rstrip("\n")

    @staticmethod
    def generate(sizes):
        matrix_string = ""
        for _ in range(int(sizes[0])):
            matrix_string += input() + "\n"
        lines = matrix_string.splitlines()
        body = []
        for line in lines:
            body.append(list())
            nums = line.split()
            for n in nums:
                body[-1].append(int(n) if "." not in n else float(n))
        return body

    def add(self, matrix_2):
        matrix_sum = Matrix([str(self.sizes[0]), str(self.sizes[1])], True)
        for row in range(self.sizes[0]):
            matrix_sum.body.append(list())
            for col in range(self.sizes[1]):
                matrix_sum.body[-1].append(self.body[row][col] + matrix_2.body[row][col])
        return matrix_sum

    def mconst(self, constant):
        matrix_mul = Matrix([str(self.sizes[0]), str(self.sizes[1])], True)
        for row in range(self.sizes[0]):
            matrix_mul.body.append(list())
            for col in range(self.sizes[1]):
                matrix_mul.body[-1].append(self.body[row][col] * constant)
        return matrix_mul

    def mul(self, matrix_2):
        matrix_mul = Matrix([str(self.sizes[0]), str(self.sizes[1])], True)
        for row in range(self.sizes[0]):
            matrix_mul.body.append(list())
            for col in range(matrix_2.sizes[1]):
                val = 0
                for x in range(self.sizes[1]):
                    val += self.body[row][x] * matrix_2.body[x][col]
                matrix_mul.body[-1].append(val)
        return matrix_mul

    def transpose(self, mode):
        if mode == "main" or mode == "side":
            matrix_trans = Matrix([str(self.sizes[1]), str(self.sizes[0])], True)
        else:
            matrix_trans = Matrix([str(self.sizes[0]), str(self.sizes[1])], True)
        for row in range(matrix_trans.sizes[0]):
            matrix_trans.body.append(list())
            for col in range(matrix_trans.sizes[1]):
                if mode == "main":
                    matrix_trans.body[-1].append(self.body[col][row])
                elif mode == "side":
                    matrix_trans.body[-1].append(self.body[-(col + 1)][-(row + 1)])
                elif mode == "vertical":
                    matrix_trans.body[-1].append(self.body[row][-(col + 1)])
                elif mode == "horizontal":
                    matrix_trans.body[-1].append(self.body[-(row + 1)][col])
                else:
                    pass  # BOOM
        return matrix_trans

    def determinant(self):
        return self.calc_det(self.body, 0)

    def calc_det(self, body, row_det):
        if len(body) == 1:
            return body[0][0]
        if len(body) == 2:
            return body[0][0] * body[1][1] - body[0][1] * body[1][0]
        else:
            tot = 0
            for el_first_row in enumerate(body[row_det]):
                redux = []
                for row in enumerate(body):
                    if row[0] != row_det:
                        redux.append(list())
                        for col in enumerate(row[1]):
                            if col[0] != el_first_row[0]:
                                redux[-1].append(col[1])
                tot += el_first_row[1] * ((-1) ** el_first_row[0]) * self.calc_det(redux, 0)
            return tot

    def inverse(self):
        matrix_cofactors = self.cofactors()
        matrix_cofactors_trans = matrix_cofactors.transpose("main")
        determinant = self.determinant()
        return matrix_cofactors_trans.mconst(1 / determinant)

    def cofactors(self):
        matrix_cofactors = Matrix([str(self.sizes[0]), str(self.sizes[1])], True)
        for row_mat in range(self.sizes[0]):
            matrix_cofactors.body.append(list())
            for col_mat in range(self.sizes[1]):
                el_first_row = (col_mat, self.body[row_mat][col_mat])
                redux = []
                for row in enumerate(self.body):
                    if row[0] != row_mat:
                        redux.append(list())
                        for col in enumerate(row[1]):
                            if col[0] != el_first_row[0]:
                                redux[-1].append(col[1])
                matrix_cofactors.body[-1].append(self.calc_det(redux, 0) * (-1 if (row_mat + col_mat) % 2 != 0 else 1))
        return matrix_cofactors


menu = '''1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit'''

transpose_menu = '''1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line'''


def add_matrices():
    sizes = input("Enter size of first matrix: ").split()
    print("Enter first matrix:")
    # Generate first
    matrix_1 = Matrix(sizes)

    sizes = input("Enter size of second matrix: ").split()
    print("Enter second matrix:")
    # Generate second
    matrix_2 = Matrix(sizes)

    print("The result is:")
    if matrix_1.sizes == matrix_2.sizes:
        matrix_sum = matrix_1.add(matrix_2)
        print(matrix_sum)
    else:
        print("The operation cannot be performed")


def multiply_constant():
    sizes = input("Enter size of matrix: ").split()
    print("Enter matrix:")
    matrix = Matrix(sizes)
    constant = float(input("Enter constant: "))
    print("The result is:")
    matrix_mul = matrix.mconst(constant)
    print(matrix_mul)


def multiply_matrices():
    sizes = input("Enter size of first matrix: ").split()
    print("Enter first matrix:")
    # Generate first
    matrix_1 = Matrix(sizes)

    sizes = input("Enter size of second matrix: ").split()
    print("Enter second matrix:")
    # Generate second
    matrix_2 = Matrix(sizes)

    print("The result is:")
    if matrix_1.sizes[1] == matrix_2.sizes[0]:
        matrix_mul = matrix_1.mul(matrix_2)
        print(matrix_mul)
    else:
        print("The operation cannot be performed")


def transpose_matrix():
    print(transpose_menu)
    choice = input("Your choice: ")
    sizes = input("Enter size of matrix: ").split()
    print("Enter matrix:")
    matrix = Matrix(sizes)
    print("The result is:")
    matrix_trans = matrix.transpose(Matrix.TRANSPOSITIONS[int(choice) - 1])
    print(matrix_trans)


def determinant_matrix():
    sizes = input("Enter matrix size: ").split()
    print("Enter matrix:")
    matrix = Matrix(sizes)
    print("The result is:")
    determinant = matrix.determinant()
    print(determinant)


def inverse_matrix():
    sizes = input("Enter matrix size: ").split()
    print("Enter matrix:")
    matrix = Matrix(sizes)
    print("The result is:")
    if matrix.determinant() != 0:
        inverse = matrix.inverse()
        print(inverse)
    else:
        print("This matrix doesn't have an inverse")


def choices(choice):
    if choice == "1":
        add_matrices()
    elif choice == "2":
        multiply_constant()
    elif choice == "3":
        multiply_matrices()
    elif choice == "4":
        transpose_matrix()
    elif choice == "5":
        determinant_matrix()
    elif choice == "6":
        inverse_matrix()
    elif choice == "0":
        exit()
    else:
        print("Invalid option")


while True:
    print(menu)
    choices(input("Your choice: "))
