def is_next_person_safe(configuration_of_persons, person):
    length_of_configuration = len(configuration_of_persons)
    for some_person in configuration_of_persons:
        if some_person==person:
            return False

    for i in range(0, length_of_configuration-1):
        if person == configuration_of_persons[i] or abs( configuration_of_persons[i]-configuration_of_persons[i+1])==1  :
            return False

    last_person = person
    second_last_person = configuration_of_persons[-1]
    if abs(last_person-second_last_person) == 1:
        return False

    if (length_of_configuration < 2):
        return (abs(last_person - second_last_person) != 1)
    else:
        before_second_last_person = configuration_of_persons[-2]
        return (abs(last_person - second_last_person) != 1 or abs(last_person - before_second_last_person) != 1)


def generate_all_possible_person_placements(number_of_chairs: int):
    valid_placements = []
    stack = []

    for person in range(1, number_of_chairs + 1):
        stack.append([person])

    while stack:
        current_arrangement = stack.pop()
        if len(current_arrangement) == number_of_chairs:
            valid_placements.append(current_arrangement)
        else:
            for person in range(1, number_of_chairs + 1):
                if is_next_person_safe(current_arrangement, person):
                    new_arrangement = current_arrangement + [person]
                    stack.append(new_arrangement)

    return valid_placements

number_of_persons = int(input("Enter the number of persons (number_of_chairs): "))
solutions = generate_all_possible_person_placements(number_of_persons)

d=14
for solution in solutions:
    print(solution,end="")
    print(d)
    d-=1

"""
[5, 3, 1, 4, 2]1
[5, 2, 4, 1, 3]2
[4, 2, 5, 3, 1]3
[4, 2, 5, 1, 3]4
[4, 1, 5, 3, 2]5
[4, 1, 5, 2, 3]6
[4, 1, 3, 5, 2]7
[3, 5, 2, 4, 1]8
[3, 5, 1, 4, 2]9
[3, 1, 5, 2, 4]10
[3, 1, 4, 2, 5]11
[2, 5, 3, 1, 4]12
[2, 5, 1, 4, 3]13
[2, 5, 1, 3, 4]14
[2, 4, 1, 5, 3]15
[2, 4, 1, 3, 5]16
[1, 4, 2, 5, 3]17
[1, 3, 5, 2, 4]18
"""