from colorama import Fore, init

init(autoreset=True)


def find_max_snake_sequence (matrix):
    def max_path_from_specifiv_element_of_matrix (current_row, current_column):
        if current_row < 0 or current_row >= matrix_size or current_column < 0 or current_column >= matrix_size:
            return 0, []

        max_length = 1
        max_path = [(current_row, current_column)]

        for next_column_pozition, next_row_pozition in [(0, 1), (1, 0)]:
            if current_row + next_column_pozition < matrix_size and current_column + next_row_pozition < matrix_size and abs(matrix[current_row + next_column_pozition][current_column + next_row_pozition] - matrix[current_row][current_column]) == 1:
                length, path = max_path_from_specifiv_element_of_matrix(current_row + next_column_pozition, current_column + next_row_pozition)
                length += 1
                if length > max_length:
                    max_length = length
                    max_path = [(current_row, current_column)] + path

        return max_length, max_path

    matrix_size = len(matrix)
    max_length = 0
    max_path = []

    for j in range(matrix_size):
        length, path = max_path_from_specifiv_element_of_matrix(0, j)
        if length > max_length:
            max_length = length
            max_path = path

    return max_length, max_path

while True:
    print("Choose an option:")
    print("1. Enter your own matrix")
    print("2. Use a predefined matrix")
    print("3. Exit")
    menu_option = input(">")

    if menu_option == '1':
        print("Please enter the n that represents the size of the n*n matrix")
        matrix_size = int(input("n="))
        print("Now enter the elements of the matrix one by one:")
        matrix = []
        for i in range(matrix_size):
            row_of_matrix = []
            for j in range(matrix_size):
                element = int(input(f"M[{i}][{j}] = "))
                row_of_matrix.append(element)
            matrix.append(row_of_matrix)

    elif menu_option == '2':
        matrix_size = 4
        matrix = [
            [1, 2, 3, 4],
            [2, 3, 4, 5],
            [3, 4, 5, 6],
            [4, 5, 6, 7]
        ]

    elif menu_option == '3':
        break

    else:
        print("Not a valid option")

    print("Here is the matrix:")
    print(f"Size: {matrix_size}x{matrix_size}")
    for row in matrix:
        print(row)

    snake_length, snake_path = find_max_snake_sequence(matrix)
    print(f"Maximum snake length: {snake_length}")

    while True:
        print("How to show the path?")
        print("1. Lame way")
        print("2. Cool way")
        print("3. Don't show it")
        submenu_option = input('>')

        if submenu_option == '1':
            print("Snake path:")
            for coordinate in snake_path[:-1]:
                print(coordinate, "->", end='')
            print(snake_path[-1])
            print()
        elif submenu_option == '2':
            for i, row in enumerate(matrix):
                for j, element in enumerate(row):
                    if (i, j) in snake_path:
                        print(Fore.RED + str(element), end=' ')
                    else:
                        print(Fore.RESET + str(element), end=' ')
                print()

        elif submenu_option == '3':
            break
        else:
            print("Invalid option, try again!")
