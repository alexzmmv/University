from src.repository.MemoryRepo import MemoryRepository, Repository_error
from src.repository.BinaryFileRepo import BinaryFileRepository
from datetime import datetime

BUSY_TIME=1

class Service_error(Exception):
    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message

    def __str__(self):
        return self.__message


class Services:
    @staticmethod
    def list_to_string(items):
        string = ""
        for element in items:
            string += str(element) + "\n"
        return string

    @staticmethod
    def __read_settings():
        settings = {}
        with open("../Data/settings.properties", 'r') as file:
            for line in file:
                # Skip comments and empty lines
                if not line.strip() or line.strip().startswith('#'):
                    continue
                key, value = line.strip().split('=')
                settings[key.strip()] = value.strip()
        return settings

    def __init__(self):
        settings = self.__read_settings()
        try:
            repository_type = settings['repository']
        except KeyError:
            raise Service_error("Invalid settings file")

        try:
            if repository_type == 'Memory':
                self.__repository = MemoryRepository()
            elif repository_type == 'BinaryFile':
                self.__repository = BinaryFileRepository(settings['persons'], settings['activities'])
            else:
                raise Service_error("Invalid repository type")
        except Repository_error as Error:
            raise Service_error("Services Error:\n" + str(Error))

    def add_person(self, person_id, name, phone_number):
        self.__repository.add_person(person_id, name, phone_number)

    def add_activity(self, activity_id, persons_id, date, start_time, end_time, description):
        self.__repository.add_activity(activity_id, persons_id, date, start_time, end_time, description)

    def update_person(self, person_id, name, phone_number):
        self.__repository.update_person(person_id, name, phone_number)

    def update_activity(self, activity_id, persons_id, date, start_time, end_time, description):
        self.__repository.update_activity(activity_id, persons_id, date, start_time, end_time, description)

    def remove_person(self, person_id):
        self.__repository.delete_person(person_id)

    def remove_activity(self, activity_id):
        self.__repository.delete_activity(activity_id)

    @property
    def persons_string(self):
        persons_str=""
        persons=self.__repository.persons
        for person_id in persons.keys():
            persons_str+=str(persons[person_id])+"\n"
        return persons_str
    @property
    def activities_string(self):
        return Services.list_to_string(self.__repository.activities_list)

    def search_person_by_id(self, person_id):
        return self.__repository.get_person_by_id(person_id)

    def search_activity_by_id(self, activity_id):
        return self.__repository.get_activity_by_id(activity_id)

    def search_persons_by_name(self, name):
        return Services.list_to_string(self.__repository.get_persons_by_name(name))

    def search_person_by_phone_number(self, phone_number):
        return Services.list_to_string(self.__repository.get_person_by_phone_number(phone_number))

    def search_activities_by_date_time(self, date):
        return Services.list_to_string(self.__repository.get_activities_by_date_time(date))

    def search_activity_by_description(self, description):
        return Services.list_to_string(self.__repository.get_activity_by_description(description))

    def search_activities_by_person_id(self, person_id):
        return Services.list_to_string(self.__repository.get_activities_by_person_id(person_id))

    def search_activities_by_duration(self, minutes):
        return Services.list_to_string(self.__repository.get_activities_by_duration(minutes))

    def activities_for_a_given_date(self, date_str):
        activities_list = self.__repository.get_activities_by_date_time(date_str)
        activities_list.sort(key=lambda activity: activity.start_time)
        return self.list_to_string(activities_list)
    def busiest_days(self):
        activities_list = self.__repository.activities_list
        days = {}
        for activity in activities_list:
            if activity.date in days.keys():
                days[activity.date] += activity.duration
            else:
                days[activity.date] = activity.duration
        days_list = []
        for day_key in days.keys():
            days_list.append((day_key, days[day_key]))
        days_list.sort(key=lambda day: day[BUSY_TIME])
        days_string = ""
        for day in days_list:
            days_string += str(day[0].date()) + " - " + str(day[1]) + " minutes\n"
        return days_string
    def activities_with_person(self, person_id):
        return Services.list_to_string(self.__repository.get_activities_by_person_id(person_id))