import random
import math

ADD_NUMBER='1'
DISPLAY_NUMBERS='2'
LONGEST_INCREASING_MODULUS_ARRAY='3'
LONGEST_ALTERNATING_SUBSEQUENCE='4'
EXIT='0'
REAL_PART=0
IMAGINARY_PART=1


def string_to_tuple(string_complex_number):
    complex_number_parts = string_complex_number.replace(" ", "").split("+")
    real_part = int(complex_number_parts[REAL_PART]) if complex_number_parts[REAL_PART] else 0
    imaginary_part = int(complex_number_parts[1][:-1]) if len(complex_number_parts) > 1 else 0
    complex_tuple = (real_part, imaginary_part)
    return complex_tuple
def add_complex_number_to_list(complex_numbers: list, complex_number: tuple):
    complex_numbers.append(complex_number)


def tuple_to_string(complex_number_tuple):
    real_part, imaginary_part = complex_number_tuple

    # Build the string representation
    complex_number_string = f"{real_part}"
    if imaginary_part != 0:
        complex_number_string += f"{'+' if imaginary_part > 0 else ''}{imaginary_part}i"
    return complex_number_string

def initiate_complex_numbers_list():
    complex_list = []
    for _ in range(10):
        complex_list.append((random.randint(0, 30), random.randint(0, 30)))
    return complex_list

def modulus(complex_number: tuple) -> float:
    return math.sqrt(complex_number[REAL_PART] ** 2 + complex_number[IMAGINARY_PART] ** 2)

def longest_alternating_subsequence(complex_numbers):
    if not complex_numbers:
        return 0, []

    length = len(complex_numbers)
    lengths = [1] * length
    longest_subsequence = [complex_numbers[0]]

    for i in range(1, length):
        for j in range(i):
            real_current = complex_numbers[i][REAL_PART]
            real_previous = complex_numbers[j][IMAGINARY_PART]

            if (real_current > real_previous and i % 2 == 1) or (real_current < real_previous and i % 2 == 0):
                lengths[i] = max(lengths[i], lengths[j] + 1)

        if lengths[i] > len(longest_subsequence):
            longest_subsequence = [complex_numbers[j] for j in range(i + 1 - lengths[i], i + 1)]

    return len(longest_subsequence), longest_subsequence

def naive_longest_increasing_modulus_subarray(complex_numbers):
    if not complex_numbers:
        return 0, []

    longest_length = 1
    longest_subarray = [complex_numbers[0]]

    for i in range(len(complex_numbers)):
        current_length = 1
        current_subarray = [complex_numbers[i]]
        for j in range(i + 1, len(complex_numbers)):
            modulus_current = modulus(complex_numbers[j])
            modulus_previous = modulus(complex_numbers[j - 1])

            if modulus_current > modulus_previous:
                current_length += 1
                current_subarray.append(complex_numbers[j])
            else:
                break

        if current_length > longest_length:
            longest_length = current_length
            longest_subarray = current_subarray

    return longest_subarray

def print_menu():
    print('Options:')
    print('1. Enter a complex number')
    print('2. Display the entire list of numbers on the console ')
    print('3. Length and elements of longest subarray of numbers having increasing modulus')
    print('4. The length and elements of longest alternating subsequence, when considering each number\'s real part')
    print('0. Exit')

def add_complex_number_string_form(complex_numbers):
    print('Read a  complex number (a+bi form)')
    str_number = input("z=")
    tuple_complex = string_to_tuple(str_number)
    add_complex_number_to_list(complex_numbers, tuple_complex)

def display_list_of_complex_numbers(complex_numbers):
    for complex_number in complex_numbers:
        print(tuple_to_string(complex_number), end='; ')
    print()

def longest_increasing_subarray_by_modulus_display(complex_numbers):
    subarray = naive_longest_increasing_modulus_subarray(complex_numbers)
    length = len(subarray)
    print(f"Length of the longest subarray: {length}")
    for number in subarray:
        print(tuple_to_string(number), end='; ')
    print()

def longest_alternating_subsequence_display(complex_numbers):
    length, subsequence = longest_alternating_subsequence(complex_numbers)
    print(f"Length of the longest alternating subsequence based on real parts: {length}")
    print("Elements of the longest alternating subsequence:")
    for number in subsequence:
        print(tuple_to_string(number), end=", ")
    print()

def User_Interface():
    complex_numbers_list = initiate_complex_numbers_list()
    while True:
        print_menu()
        menu_option = input('>')
        if menu_option == ADD_NUMBER:
            add_complex_number_string_form(complex_numbers_list)
        elif menu_option == DISPLAY_NUMBERS:
            display_list_of_complex_numbers(complex_numbers_list)
        elif menu_option == LONGEST_INCREASING_MODULUS_ARRAY:
            longest_increasing_subarray_by_modulus_display(complex_numbers_list)
        elif menu_option == LONGEST_ALTERNATING_SUBSEQUENCE:
            longest_alternating_subsequence_display(complex_numbers_list)
        elif menu_option == EXIT:
            break
        else:
            print("No such option. Try again!")

if __name__ == "__main__":
    print("Make magic happen")
    User_Interface()

"""
import random
import math

ADD_NUMBER='1'
DISPLAY_NUMBERS='2'
LONGEST_INCREASING_MODULUS_ARRAY='3'
LONGEST_ALTERNATING_SUBSEQUENCE='4'
EXIT='0'
REAL_PART=1


def str_to_tuple(s):
    parts = s.replace(" ", "").split("+")
    real_part = int(parts[0]) if parts[0] else 0
    imaginary_part = int(parts[1][:-1]) if len(parts) > 1 else 0
    complex_tuple = (real_part, imaginary_part)
    return complex_tuple

def add_complex_number(complex_dict, complex_number):
    real_part = complex_number[0]
    if real_part in complex_dict:
        complex_dict[real_part].append(complex_number)
    else:
        complex_dict[real_part] = [complex_number]

def tuple_complex_number_to_string(complex_tuple):
    real_part, imaginary_part = complex_tuple

    # Build the string representation
    result_str = f"{real_part}"

    if imaginary_part != 0:
        result_str += f"{'+' if imaginary_part > 0 else ''}{imaginary_part}i"
    return result_str

def initiate_complex_numbers_dictionary():
    complex_dict = {}
    for _ in range(10):
        complex_number = (random.randint(0, 30), random.randint(0, 30))
        add_complex_number(complex_dict, complex_number)
    return complex_dict

def modulus(complex_number):
    return math.sqrt(complex_number[0] ** 2 + complex_number[1] ** 2)

def longest_alternating_subsequence(complex_dict):
    if not complex_dict:
        return 0, []

    real_parts = sorted(complex_dict.keys())
    length = len(real_parts)
    lengths = [1] * length
    longest_subsequence = complex_dict[real_parts[0]]

    for i in range(1, length):
        current_real_part = real_parts[i]
        current_complex_numbers = complex_dict[current_real_part]

        for j in range(i):
            previous_real_part = real_parts[j]
            previous_complex_numbers = complex_dict[previous_real_part]

            if (current_real_part > previous_real_part and i % 2 == 1) or (current_real_part < previous_real_part and i % 2 == 0):
                lengths[i] = max(lengths[i], lengths[j] + 1)

        if lengths[i] > len(longest_subsequence):
            longest_subsequence = []
            for j in range(i + 1 - lengths[i], i + 1):
                longest_subsequence.extend(complex_dict[real_parts[j]])

    return len(longest_subsequence), longest_subsequence

def naive_longest_increasing_modulus_subarray(complex_dict):
    if not complex_dict:
        return 0, []

    longest_length = 1
    longest_subarray = list(complex_dict.values())[0]

    real_parts = sorted(complex_dict.keys())
    for i in range(len(real_parts)):
        current_real_part = real_parts[i]
        current_complex_numbers = complex_dict[current_real_part]

        current_length = 1
        current_subarray = current_complex_numbers

        for j in range(i + 1, len(real_parts)):
            next_real_part = real_parts[j]
            next_complex_numbers = complex_dict[next_real_part]

            modulus_current = modulus(next_complex_numbers[0])
            modulus_previous = modulus(current_subarray[-1])

            if modulus_current > modulus_previous:
                current_length += 1
                current_subarray.extend(next_complex_numbers)
            else:
                break

        if current_length > longest_length:
            longest_length = current_length
            longest_subarray = current_subarray

    return longest_subarray

def print_menu():
    print('Options:')
    print('1. Enter a complex number - Add')
    print('2. Display the entire list of numbers on the console - Display')
    print('3. Length and elements of a longest subarray of numbers having increasing modulus - Problem 1')
    print('4. The length and elements of a longest alternating subsequence, when considering each number\'s real part - Problem 2')
    print('0. Exit')

def add_complex_number_string_to_dictionary(complex_dict):
    print('Read a complex number (a+bi form)')
    str_number = input("z=")
    tuple_complex = str_to_tuple(str_number)
    add_complex_number(complex_dict, tuple_complex)

def display_complex_numbers_dictionary(complex_dict):
    for real_part, complex_numbers in complex_dict.items():
        for number in complex_numbers:
            print(tuple_complex_number_to_string(number), end='; ')
        print()

def longest_increasing_modulus_subbaray_display(complex_dict):
    subarray = naive_longest_increasing_modulus_subarray(complex_dict)
    length = len(subarray)
    print(f"Length of the longest subarray: {length}")
    for number in subarray:
        print(tuple_complex_number_to_string(number), end='; ')
    print()

def longest_alternating_subsequence_display(complex_dict):
    length, subsequence = longest_alternating_subsequence(complex_dict)
    print(f"Length of the longest alternating subsequence based on real parts: {length}")
    print("Elements of the longest alternating subsequence:")
    for number in subsequence:
        print(tuple_complex_number_to_string(number), end=",")
    print()


def User_Interface():
    dictionary_complex_numbers = initiate_complex_numbers_dictionary()
    while True:
        print_menu()
        menu_option = input('>')
        if menu_option == ADD_NUMBER:
            add_complex_number_string_to_dictionary(dictionary_complex_numbers)
        elif menu_option == DISPLAY_NUMBERS:
            display_complex_numbers_dictionary(dictionary_complex_numbers)
        elif menu_option == LONGEST_INCREASING_MODULUS_ARRAY:
            longest_increasing_modulus_subbaray_display(dictionary_complex_numbers)
        elif menu_option == LONGEST_ALTERNATING_SUBSEQUENCE:
            longest_alternating_subsequence_display(dictionary_complex_numbers)
        elif menu_option == EXIT:
            break
        else:
            print("No such option. Try again!")

if __name__ == "__main__":
    print("Make magic happen")
    User_Interface()
"""