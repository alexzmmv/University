def generate_all_possible_person_placements(number_of_chairs: int, configuration_of_persons=[]):
    if len(configuration_of_persons) == number_of_chairs:
        print(configuration_of_persons)
        return

    for person in range(1, number_of_chairs + 1):
        configuration_of_persons.append(person)

        if is_next_person_safe(configuration_of_persons):
            generate_all_possible_person_placements(number_of_chairs, configuration_of_persons)

        configuration_of_persons.pop()


def is_next_person_safe(configuration_of_persons):
    length_of_configuration = len(configuration_of_persons)
    for i in range(0, length_of_configuration-1):
        if configuration_of_persons[length_of_configuration-1] == configuration_of_persons[i] or abs( configuration_of_persons[i]-configuration_of_persons[i+1])==1  :
            return False

    if length_of_configuration < 2:
        return True

    last_person = configuration_of_persons[-1]
    second_last_person = configuration_of_persons[-2]

    if(length_of_configuration<3):
        return (abs(last_person - second_last_person)!=1 )
    elif length_of_configuration>2:
        before_second_last_person=configuration_of_persons[-3]
        return (abs(last_person - second_last_person)!=1 or abs(last_person-before_second_last_person)!=1 )

number_of_persons = int(input("Enter the number of persons (number_of_chairs): "))
generate_all_possible_person_placements(number_of_persons)

"""
[1, 3, 5, 2, 4]14
[1, 4, 2, 5, 3]13
[2, 4, 1, 3, 5]12
[2, 4, 1, 5, 3]11
[2, 5, 3, 1, 4]10
[3, 1, 4, 2, 5]9
[3, 1, 5, 2, 4]8
[3, 5, 1, 4, 2]7
[3, 5, 2, 4, 1]6
[4, 1, 3, 5, 2]5
[4, 2, 5, 1, 3]4
[4, 2, 5, 3, 1]3
[5, 2, 4, 1, 3]2
[5, 3, 1, 4, 2]1
"""