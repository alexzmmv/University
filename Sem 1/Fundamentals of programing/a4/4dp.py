from colorama import Fore, init

init(autoreset=True)


def find_max_snake_sequence (matrix):
    matrix_len = len(matrix)
    length_to_first_row_matrix = [[1] * matrix_len for _ in range(matrix_len)]

    max_length = 1
    max_length_end = (0, 0)

    for current_row in range(matrix_len - 1, -1, -1):
        for current_column in range(matrix_len - 1, -1, -1):
            if current_row < matrix_len - 1 and abs(matrix[current_row][current_column] - matrix[current_row + 1][current_column]) == 1:
                length_to_first_row_matrix[current_row][current_column] = max(length_to_first_row_matrix[current_row][current_column], 1 + length_to_first_row_matrix[current_row + 1][current_column])
            if current_column < matrix_len - 1 and abs(matrix[current_row][current_column] - matrix[current_row][current_column + 1]) == 1:
                length_to_first_row_matrix[current_row][current_column] = max(length_to_first_row_matrix[current_row][current_column], 1 + length_to_first_row_matrix[current_row][current_column + 1])

            if length_to_first_row_matrix[current_row][current_column] >= max_length and  current_column==0:
                max_length = length_to_first_row_matrix[current_row][current_column]
                max_length_end = (current_row, current_column)

    max_sequence = []
    current_row, current_column = max_length_end

    while max_length > 0:
        max_sequence.append((current_row, current_column))
        if current_row < matrix_len - 1 and abs(matrix[current_row][current_column] - matrix[current_row + 1][current_column]) == 1 and length_to_first_row_matrix[current_row][current_column] == length_to_first_row_matrix[current_row + 1][current_column] + 1:
            current_row += 1
        elif current_column < matrix_len - 1 and abs(matrix[current_row][current_column] - matrix[current_row][current_column + 1]) == 1 and length_to_first_row_matrix[current_row][current_column] == length_to_first_row_matrix[current_row][current_column + 1] + 1:
            current_column += 1
        max_length -= 1

    return  length_to_first_row_matrix,max_sequence


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

    memorization_matrix,final_result_path = find_max_snake_sequence(matrix)
    final_result_path_length=len(final_result_path)
    print(f"Maximum snake length: {final_result_path_length}")

    while True:
        print("How to show the path?")
        print("1.Lame way")
        print("2.Cool way")
        print("3.Memorization matrix")
        print("4.Don't show it")
        submenu_option=input('>')
        print()
        if submenu_option=='1':
            print("Snake path:")
            for coordinate in final_result_path[:-1]:
                print(coordinate,"->",end='')
            print(final_result_path[-1])
            print()
        elif submenu_option=='2':
            for i, row in enumerate(matrix):
                for j, element in enumerate(row):
                    if (i, j) in final_result_path:
                        print(Fore.RED + str(element), end=' ')
                    else:
                        print(Fore.RESET + str(element), end=' ')
                print()

        elif submenu_option=='3':
            for row in memorization_matrix:
                print(row)
        elif submenu_option=='4':
            break
        else:
            print("Invalid  option,try again!")
