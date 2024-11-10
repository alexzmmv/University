import random


def generate_list_specific_size_of_random_numbers (sizeof_list: int) -> list:
    random_ints = list()
    for iterator in range(sizeof_list):
        random_number = random.randint(0, 100)
        random_ints += [random_number]
    return random_ints


def print_list_of_numbers (numbers: list) -> None:
    for number in numbers:
        print(number, end=" ")
    print()


def swap_elements_of_list (array: list, iterator1: int, iterator2: int) -> None:
    array[iterator1], array[iterator2] = array[iterator2], array[iterator1]


def ExchangeSort (unsorted_list: list, step_: int, ) -> int:
    counter: int = 0
    swapped = True
    list_size_ = len(unsorted_list)
    while swapped:
        swapped = False
        for iterator in range(1, list_size_):
            if unsorted_list[iterator - 1] > unsorted_list[iterator]:
                swap_elements_of_list(unsorted_list, iterator, iterator - 1)
                swapped = True
                counter += 1
                if counter % step_ == 0:
                    print_list_of_numbers(unsorted_list)
    return counter


def StoogeSort (unsorted_list: list, left: int, right: int, step_: int, swap_counter=0) -> int:
    if left < right:
        if unsorted_list[left] > unsorted_list[right]:
            swap_elements_of_list(unsorted_list, left, right)
            swap_counter += 1
            if swap_counter % step_ == 0:
                print_list_of_numbers(unsorted_list)

        if right > left + 1:
            third = (right - left + 1) // 3
            swap_counter = StoogeSort(unsorted_list, left, right - third, step_, swap_counter)
            swap_counter = StoogeSort(unsorted_list, left + third, right, step_, swap_counter)
            swap_counter = StoogeSort(unsorted_list, left, right - third, step_, swap_counter)

        return swap_counter


print("Assigment 2 sorting algorithms \nFor this assigment I had Exchange Sort and Stooge sort \n")

main_menu_loop: bool = True

while main_menu_loop:
    unsorted_int_list = list()

    is_list_agreed_by_the_user = False
    while not(is_list_agreed_by_the_user):
        print("Generating a list of n random numbers from 0 to 100")

        list_size = int(input("Enter the size of the list:"))

        unsorted_int_list = generate_list_specific_size_of_random_numbers(list_size)
        print_list_of_numbers(unsorted_int_list)
        is_list_agreed = input("Is the list ok? y/n: ")
        if is_list_agreed == "y":
            is_list_agreed_by_the_user = True
        else:
            print()

    stay_in_sort_menu_loop = True

    while stay_in_sort_menu_loop:
        print("1.Sort using Exchange Sort")
        print("2.Sort using Stooge Sort")
        print("9.Exit")

        menu_option = input(">")
        stay_in_sort_menu_loop=False
        if menu_option == "1":
            step: int = int(input("Please enter the step value at witch to show the partially sorted list:"))
            operation_counter = ExchangeSort(unsorted_int_list, step)
            print("Final sorted list with "+str(operation_counter)+" operations:")
            print_list_of_numbers(unsorted_int_list)

        elif menu_option == "2":
            step: int = int(input("Please enter the step value at witch to show the partially sorted list:"))
            operation_counter = StoogeSort(unsorted_int_list, 0, list_size - 1, step, 0)
            print("Final sorted list with "+str(operation_counter)+" operations:")
            print_list_of_numbers(unsorted_int_list)

        elif menu_option == "9":
            pass
        else:
            stay_in_sort_menu_loop = True
            print("No such option, try again!")

    menu_option = input("Continue with another list? y/n : ")
    if menu_option == "y":
        print()
    else:
        main_menu_loop = False
