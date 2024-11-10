import random
import timeit


def generate_list_specific_size_of_random_numbers(sizeof_list: int) -> list:
    random_ints = list()
    for iterator in range(sizeof_list):
        random_number = random.randint(0, 100)
        random_ints += [random_number]
    return random_ints


def print_list_of_numbers(numbers: list) -> None:
    for number in numbers:
        print(number, end=" ")
    print()


def swap_elements_of_list(array: list, iterator1: int, iterator2: int) -> None:
    array[iterator1], array[iterator2] = array[iterator2], array[iterator1]


def ExchangeSort(unsorted_list: list,left:int,right:int) -> None:
    swapped = True
    while swapped:
        swapped = False
        for iterator in range(left+1, right):
            if unsorted_list[iterator - 1] > unsorted_list[iterator]:
                swap_elements_of_list(unsorted_list, iterator, iterator - 1)
                swapped = True


def Stooge_Sort (arr, low, high):
    if low >= high:
        return

    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]

    if high - low + 1 > 2:
        third = (high - low + 1) // 3

        Stooge_Sort(arr, low, high - third)
        Stooge_Sort(arr, low + third, high)
        Stooge_Sort(arr, low, high - third)


def sorting_algorithm_menu(sorting_algorithm)->None:
    def best_case(length:int)->list:
        return list(range(length))
    def worst_case(length:int)->list:
        return list(range(length, 0, -1))
    def average_case(length):
        return generate_list_specific_size_of_random_numbers(length)

    def menu_option_calculation(case_function, data_length:int)->list:
        data_length_duration_of_sort=list()
        for i in range(5):
            print("...",end=" ")
            case_list = case_function(data_length)
            duration_of_sort = timeit.timeit(lambda:sorting_algorithm(case_list,0,len(case_list)-1), number=3)
            data_length_duration_of_sort.append((data_length, duration_of_sort))
            data_length *= 2
        return data_length_duration_of_sort
    print()


    stop_menu_loop=False
    while not stop_menu_loop:
        print("1.Best case")
        print("2.Worst case")
        print("3.Average case")
        print("9.Exit")
        menu_option = input(">")

        if menu_option=='1':
            data_length = int(input("Enter a data length: "))

            print("Printing the data length and duration")
            data_length_and_duration=menu_option_calculation(best_case,data_length)

            for data_and_duration in data_length_and_duration:
                print(f'For {data_and_duration[0]} elements it takes {data_and_duration[1] * 100}ms to run')


        elif menu_option=='2':
            data_length = int(input("Enter a data length: "))
            print("Printing the data length and duration")
            data_length_and_duration = menu_option_calculation(worst_case, data_length)

            for data_and_duration in data_length_and_duration:
                print(f'For {data_and_duration[0]} elements it takes {data_and_duration[1] * 100}ms to run')

        elif menu_option=='3':
            data_length = int(input("Enter a data length: "))
            print("Printing the data length and duration")
            data_length_and_duration = menu_option_calculation(average_case, data_length)

            for data_and_duration in data_length_and_duration:
                print(f'For {data_and_duration[0]} elements it takes {data_and_duration[1] * 100}ms to run')

        elif menu_option=='9':
            stop_menu_loop=True
        else:
            print("Option not available.Try again!")


print("Assigment 3 sorting algorithms \nFor this assigment I had Exchange Sort and Stooge sort \n")

while True:
        print("1.Sort using Exchange Sort")
        print("2.Sort using Stooge Sort")
        print("9.Exit")


        main_menu_choice=input(">")
        if main_menu_choice=='1':
            sorting_algorithm_menu(ExchangeSort)
        elif main_menu_choice=='2':
            sorting_algorithm_menu(Stooge_Sort)
        elif main_menu_choice=='9':
            break
        else:
            print("Try again")