from src.domain.Activity import Activity
from src.domain.Person import Person
from regex import match
from copy import copy
from datetime import datetime

class Repository_error(Exception):
    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message

    def __str__(self):
        return self.__message


class MemoryRepository:
    def __init__(self):
        self.__persons = {}
        self.__activities = {}


    @property
    def persons_list(self):
        person_list = []
        for person_id in self.__persons.keys():
            person_list.append(self.__persons[person_id])
        return person_list
    @property
    def activities_list(self):
        activity_list = []
        for activity_id in self.__activities.keys():
            activity_list.append(self.__activities[activity_id])
        return activity_list

    @property
    def persons_id(self):
        return list(self.__persons.keys())

    @property
    def activities_id(self):
        return list(self.__activities.keys())

    @property
    def persons(self):
        return self.__persons

    @property
    def activities(self):
        return self.__activities

    def add_person(self, person_id, name, phone_number):
        if person_id in self.__persons.keys():
            raise Repository_error("Person id already exists!")
        self.__persons[person_id] = Person(person_id, name, phone_number)

    def add_activity(self, activity_id, persons_id, date, start_time, end_time, description,valid=False):
        if not valid:
            if activity_id in self.__activities.keys():
                raise Repository_error("Activity id already exists!")
            persons_id_int=[]
            if persons_id!=[]:
                for person_id in persons_id:
                    try:
                        persons_id_int.append(int(person_id))
                    except:
                        raise Repository_error("Person id must be an integer!")
                persons_id=persons_id_int

                for person_id in persons_id:
                    if person_id not in self.__persons.keys():
                        raise Repository_error(f"Person with id {person_id} does not exist in the memory!")

            activity_to_add=Activity(activity_id, persons_id, date, start_time, end_time, description)
            for activity_key in self.__activities.keys():
                if activity_to_add.is_time_conflict(self.__activities[activity_key]):
                    raise Repository_error("Time conflict!")
        activity_to_add = Activity(activity_id, persons_id, date, start_time, end_time, description)
        self.__activities[activity_id] = activity_to_add
    def update_person(self, person_id, name, phone_number,valid=False):
        try:
            person_id=int(person_id)
        except:
            raise Repository_error("Person id must be an integer!")
        if not valid:
            if person_id not in self.__persons.keys():
                raise Repository_error("Person id does not exist!")
        self.__persons[person_id].update(name, phone_number)

    def update_activity(self, activity_id, persons_id, date, start_time, end_time, description,valid=False):
        if not valid:
            try:
                activity_id=int(activity_id)
            except:
                raise Repository_error("Activity id must be an integer!")
            if activity_id not in self.__activities.keys():
                raise Repository_error("Activity id does not exist!")
            for activity_key in self.__activities.keys():
                if activity_id!=activity_key and self.__activities[activity_key].is_time_conflict(date=date, start_time=start_time, end_time=end_time):
                    raise Repository_error("Time conflict!")
            if persons_id==[]:
                persons_id=[]
            else:

                for person_id in persons_id:
                    if person_id not in self.__persons.keys():
                        raise Repository_error(f"Person with id {person_id} does not exist in the memory!")

        self.__activities[activity_id].update(persons_id, date, start_time, end_time, description)

    def delete_person(self, person_id):
        try:
            person_id=int(person_id)
        except:
            raise Repository_error("Person id must be an integer!")
        if person_id not in self.__persons.keys():
            raise Repository_error("Person id does not exist!")
        for activity_key in self.__activities.keys():
            if person_id in self.__activities[activity_key].persons:
                self.__activities[activity_key].delete_personn(person_id)
        del self.__persons[person_id]

    def delete_activity(self, activity_id):
        try:
            activity_id=int(activity_id)
        except:
            raise Repository_error("Activity id must be an integer!")
        if activity_id not in self.__activities.keys():
            raise Repository_error("Activity id does not exist!")
        del self.__activities[activity_id]

    def get_person_by_id(self, person_id):
        try:
            person_id=int(person_id)
        except:
            raise Repository_error("Person id must be an integer!")
        if person_id not in self.__persons.keys():
            raise Repository_error("Person id does not exist!")
        return self.__persons[person_id]

    def get_activity_by_id(self, activity_id):
        try:
            activity_id=int(activity_id)
        except:
            raise Repository_error("Activity id must be an integer!")
        if activity_id not in self.__activities.keys():
            raise Repository_error("Activity id does not exist!")
        return copy(self.__activities[activity_id])

    def get_persons_by_name(self, name):
        persons_list = []
        name=name.lower()
        for person_id in self.__persons.keys():
            if match(name, self.__persons[person_id].name.lower()):
                persons_list.append(copy(self.__persons[person_id]))
        return persons_list

    def get_person_by_phone_number(self, phone_number):
        persons_list = []
        for person_id in self.__persons.keys():
            if match(self.__persons[person_id].phone_number,phone_number):
                persons_list.append(copy(self.__persons[person_id]))
        return persons_list

    def get_activities_by_date_time(self, date):
        try:
            date=datetime.strptime(date, "%Y.%m.%d").date()
        except:
            raise Repository_error("Date must be in the format YYYY.MM.DD and time in the format HH:MM!")
        activities_list = []
        for activity_id in self.__activities.keys():
            if  self.__activities[activity_id].date.date()==date.date():
                activities_list.append(self.__activities[activity_id])
                print(self.__activities[activity_id])
        return activities_list

    def get_activity_by_description(self, description):
        activities_list = []
        for activity_id in self.__activities.keys():
            if match(description, self.__activities[activity_id].description):
                activities_list.append(copy(self.__activities[activity_id]))
        return activities_list

    def get_activities_by_person_id(self, person_id):
        if person_id=="":
            return self.activities_list
        try:
            person_id=int(person_id)
        except:
            raise Repository_error("Person id must be an integer!")
        activities_list = []
        for activity_id in self.__activities.keys():
            if person_id in self.__activities[activity_id].persons:
                activities_list.append(copy(self.__activities[activity_id]))
        return activities_list

    def get_activities_by_duration(self, minutes):
        try:
            minutes=int(minutes)
        except:
            raise Repository_error("Duration must be an integer!")
        activities_list = []
        for activity_id in self.__activities.keys():
            if self.__activities[activity_id].duration==minutes:
                activities_list.append(copy(self.__activities[activity_id]))
        return activities_list

    def is_it_free(self, date=None, start_time=None, end_time=None, time=None):
        for activity_id in self.__activities.keys():
            if self.__activities[activity_id].is_time_conflict(date=date, start_time=start_time, end_time=end_time,time=time):
                return False
        return True