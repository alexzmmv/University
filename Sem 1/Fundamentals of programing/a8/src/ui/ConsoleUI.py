from src.services.Services import Services


class ActivityPlannerUI:
    MENU_MANAGE_PERSONS = "1"
    MENU_MANAGE_ACTIVITIES = "2"
    MENU_SEARCH = "3"
    MENU_STATISTICS = "4"
    HELP = "h"
    MENU_EXIT = "0"
    ADD_PERSON="1"
    REMOVE_PERSON="2"
    UPDATE_PERSON="3"
    LIST_PERSONS="4"
    ADD_ACTIVITY="1"
    REMOVE_ACTIVITY="2"
    UPDATE_ACTIVITY="3"
    LIST_ACTIVITIES="4"
    SEARCH_PERSON_BY_ID = "1"
    SEARCH_ACTIVITY_BY_ID = "2"
    SEARCH_PERSONS_BY_NAME = "3"
    SEARCH_PERSON_BY_PHONE_NUMBER = "4"
    SEARCH_ACTIVITIES_BY_DATE_TIME = "5"
    SEARCH_ACTIVITY_BY_DESCRIPTION = "6"
    SEARCH_ACTIVITIES_BY_PERSON_ID = "7"
    SEARCH_ACTIVITIES_BY_DURATION = "8"
    BUSIEST_DAY="1"
    ACTIVITIES_FOR_A_GIVEN_DATE="2"

    def __init__(self):
        self.service = Services()

    def display_main_menu(self):
        print("\nActivity Planner Menu:")
        print(f"{self.MENU_MANAGE_PERSONS}. Manage Persons")
        print(f"{self.MENU_MANAGE_ACTIVITIES}. Manage Activities")
        print(f"{self.MENU_SEARCH}. Search")
        print(f"{self.MENU_STATISTICS}. Statistics")
        print(f"{self.MENU_EXIT}. Exit")

    def run(self):
        while True:
            self.display_main_menu()
            choice = input("Enter your choice: ")
            if choice == self.MENU_MANAGE_PERSONS:
                self.manage_persons()
            elif choice == self.MENU_MANAGE_ACTIVITIES:
                self.manage_activities()
            elif choice == self.MENU_SEARCH:
                self.search()
            elif choice == self.MENU_STATISTICS:
                self.statistics()
            elif choice == self.MENU_EXIT:
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_persons(self):
        while True:
            print("\nManage Persons:")
            print("1. Add Person")
            print("2. Remove Person")
            print("3. Update Person")
            print("4. List Persons")
            print("0. Back")
            option = input("Enter your option: ")
            if option == self.ADD_PERSON:
                self.add_person()
            elif option == self.REMOVE_PERSON:
                self.remove_person()
            elif option == self.UPDATE_PERSON:
                self.update_person()
            elif option == self.LIST_PERSONS:
                self.list_persons()
            elif option == self.MENU_EXIT:
                return
            else:
                print("Invalid option. Please try again.")
    def add_person(self):
        person_id = input("Enter Person ID: ")
        name = input("Enter Name: ")
        phone_number = input("Enter Phone Number: ")
        try:
            person_id = int(person_id)
            self.service.add_person(person_id, name, phone_number)
            print("Person added successfully!")
        except Exception as Error:
            print("Services Error:\n" + str(Error))

    def remove_person(self):
        person_id = input("Enter Person ID to remove: ")
        try:
            person_id = int(person_id)
            self.service.remove_person(person_id)
            print("Person removed successfully!")
        except Exception as Error:
            print("Services Error:\n" + str(Error))
    def update_person(self):
        person_id = input("Enter Person ID to update: ")
        name = input("Enter New Name: ")
        phone_number = input("Enter New Phone Number: ")
        try:
            person_id = int(person_id)
            self.service.update_person(person_id, name, phone_number)
            print("Person updated successfully!")
        except Exception as Error:
            print("Services Error:\n" + str(Error))
    def list_persons(self):
        persons = self.service.persons_string
        print("List of Persons:")
        print(persons)

    def manage_activities(self):
        while True:
            print("\nManage Activities:")
            print("1. Add Activity")
            print("2. Remove Activity")
            print("3. Update Activity")
            print("4. List Activities")
            print("0. Back")
            option = input("Enter your option: ")
            if option == self.ADD_ACTIVITY:
                self.add_activity()
            elif option == self.REMOVE_ACTIVITY:
                self.remove_activity()
            elif option == self.UPDATE_ACTIVITY:
                self.update_activity()
            elif option == self.LIST_ACTIVITIES:
                self.list_activities()
            elif option == self.MENU_EXIT:
                return
            else:
                print("Invalid option. Please try again.")

    def add_activity(self):
        activity_id = input("Enter Activity ID: ")
        persons_id = input("Enter Person IDs (comma-separated): ").split(',')
        if persons_id == ['']:
            persons_id = []
        else:
            for person in persons_id:
                try:
                    int(person)
                except:
                    raise ValueError("Person id must be an integer!")
        date = input("Enter Date (YYYY.MM.DD): ")
        start_time = input("Enter Start Time (HH:MM): ")
        end_time = input("Enter End Time (HH:MM): ")
        description = input("Enter Description: ")
        try:
            activity_id = int(activity_id)
            self.service.add_activity(activity_id, persons_id, date, start_time, end_time, description)
            print("Activity added successfully!")
        except Exception as Error:
            print("Services Error:\n" + str(Error))

    def remove_activity(self):
        activity_id = input("Enter Activity ID to remove: ")
        try:
            activity_id = int(activity_id)
            self.service.remove_activity(activity_id)
            print("Activity removed successfully!")
        except Exception as Error:
            print("Services Error:\n" + str(Error))

    def update_activity(self):
        activity_id = input("Enter Activity ID to update: ")
        persons_id = input("Enter New Person IDs (comma-separated): ").split(',')
        date = input("Enter New Date (YYYY.MM.DD): ")
        start_time = input("Enter New Start Time (HH:MM): ")
        end_time = input("Enter New End Time (HH:MM): ")
        description = input("Enter New Description: ")
        try:
            activity_id = int(activity_id)
            self.service.update_activity(activity_id, persons_id, date, start_time, end_time, description)
            print("Activity updated successfully!")
        except Exception as Error:
            print("Services Error:\n" + str(Error))

    def list_activities(self):
        activities = self.service.activities_string
        print("List of Activities:")
        print(activities)

    def search(self):

        while True:
            print("\nSearch:")
            print("1. Search Person by ID")
            print("2. Search Activity by ID")
            print("3. Search Persons by Name")
            print("4. Search Person by Phone Number")
            print("5. Search Activities by Date/Time")
            print("6. Search Activity by Description")
            print("7. Search Activities by Person ID")
            print("8. Search Activities by Duration")
            print("0. Back")
            option = input("Enter your option: ")
            if option == self.SEARCH_PERSON_BY_ID:
                self.search_person_by_id()
            elif option == self.SEARCH_ACTIVITY_BY_ID:
                self.search_activity_by_id()
            elif option == self.SEARCH_PERSONS_BY_NAME:
                self.search_persons_by_name()
            elif option == self.SEARCH_PERSON_BY_PHONE_NUMBER:
                self.search_person_by_phone_number()
            elif option == self.SEARCH_ACTIVITIES_BY_DATE_TIME:
                self.search_activities_by_date_time()
            elif option == self.SEARCH_ACTIVITY_BY_DESCRIPTION:
                self.search_activity_by_description()
            elif option == self.SEARCH_ACTIVITIES_BY_PERSON_ID:
                self.search_activities_by_person_id()
            elif option == self.SEARCH_ACTIVITIES_BY_DURATION:
                self.search_activities_by_duration()
            elif option == self.MENU_EXIT:
                return
            else:
                print("Invalid option. Please try again.")

    def search_person_by_id(self):
        person_id = input("Enter Person ID to search: ")
        try:
            person_id = int(person_id)
            person = self.service.search_person_by_id(person_id)
            print(f"Person found:\n{person}")
        except Exception as Error:
            print(f"Repository Error:\n{Error}")

    def search_activity_by_id(self):
        activity_id = input("Enter Activity ID to search: ")
        try:
            activity_id = int(activity_id)
            activity = self.service.search_activity_by_id(activity_id)
            print(f"Activity found:\n{activity}")
        except Exception as Error:
            print(f"Repository Error:\n{Error}")

    def search_persons_by_name(self):
        name = input("Enter Name to search: ")
        persons = self.service.search_persons_by_name(name)
        print("Persons found:")
        print(persons)

    def search_person_by_phone_number(self):
        phone_number = input("Enter Phone Number to search: ")
        persons = self.service.search_person_by_phone_number(phone_number)
        print("Persons found:")
        print(persons)

    def search_activities_by_date_time(self):
        date = input("Enter Date (YYYY.MM.DD) to search:")
        activities = self.service.search_activities_by_date_time(date)
        print("Activities found:")
        print(activities)

    def search_activity_by_description(self):
        description = input("Enter Description to search: ")
        activities = self.service.search_activity_by_description(description)
        print("Activities found:")
        print(activities)

    def search_activities_by_person_id(self):
        person_id = input("Enter Person ID to search activities: ")
        activities = self.service.search_activities_by_person_id(person_id)
        print("Activities found:")
        print(activities)

    def search_activities_by_duration(self):
        minutes = input("Enter Duration in minutes to search activities: ")
        activities = self.service.search_activities_by_duration(minutes)
        print("Activities found:")
        print(activities)

    def statistics(self):
        while True:
            print("\nStatistics:")
            print("1. Busiest Day")
            print("2. Activities for a given day sorted by start time")
            print("0.Back")
            option = input("Enter your option: ")
            if option == self.BUSIEST_DAY:
                self.busiest_days()
            elif option == self.ACTIVITIES_FOR_A_GIVEN_DATE:
                self.activities_for_a_given_date()
            elif option == self.MENU_EXIT:
                return
            else:
                print("Invalid option. Please try again.")

    def busiest_days(self):
        print("Busiest Day:")
        print(self.service.busiest_days())

    def activities_for_a_given_date(self):
        date = input("Enter Date (YYYY.MM.DD) to search:")
        activities = self.service.activities_for_a_given_date(date)
        print("Activities found:")
        print(activities)

a=ActivityPlannerUI()
a.run()