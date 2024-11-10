import datetime


class Activity:
    def __init__(self, id, persons, date, start_time, end_time, description):
        self.__id = int(id)
        self.persons = persons
        self.date = datetime.datetime.strptime(date, "%Y.%m.%d")
        self.start_time = datetime.datetime.strptime(start_time, "%H:%M")
        self.end_time = datetime.datetime.strptime(end_time, "%H:%M")
        if self.start_time>self.end_time:
            raise ValueError("Start time must be before end time!")
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time!")
        self.description = description

    @property
    def id(self):
        return self.__id

    def delete_personn(self, person_id_to_delete):
        if person_id_to_delete not in self.persons:
            raise ValueError("Person id does not exist!")
        self.persons.remove(person_id_to_delete)

    def update(self, persons, date, start_time, end_time, description):
        self.persons = persons
        self.date = datetime.datetime.strptime(date, "%Y.%m.%d")
        self.start_time = datetime.datetime.strptime(start_time, "%H:%M")
        self.end_time = datetime.datetime.strptime(end_time, "%H:%M")
        self.description = description

    @property
    def duration(self):
        duration=self.end_time - self.start_time
        return duration.seconds//60

    def is_time_conflict(self,other=None, date=None, start_time=None, end_time=None,time=None):
        if other is not None:
            if self.date != other.date:
                return False
            if self.start_time <= other.start_time <= self.end_time:
                return True
            if self.start_time <= other.end_time <= self.end_time:
                return True
            if other.start_time <= self.start_time <= other.end_time:
                return True
            if other.start_time <= self.end_time <= other.end_time:
                return True
            return False
        if  time is None and start_time is not None and end_time is not None:
            if date is None:
                date=self.date
            if not isinstance(start_time, datetime.datetime):
                start_time = datetime.datetime.strptime(start_time, "%H:%M")
            if not isinstance(end_time, datetime.datetime):
                end_time = datetime.datetime.strptime(end_time, "%H:%M")

            if self.date != date:
                return False
            if self.start_time <= start_time <= self.end_time:
                return True
            if self.start_time <= end_time <= self.end_time:
                return True
            if start_time <= self.start_time <= end_time:
                return True
            if start_time <= self.end_time <= end_time:
                return True
            return False
        if time is not None:
            if date is None:
                date=self.date
            if not isinstance(date, datetime.datetime):
                date = datetime.datetime.strptime(date, "%Y.%m.%d")
            if not isinstance(time, datetime.datetime):
                time = datetime.datetime.strptime(time, "%H:%M")
            if self.date != date:
                return False
            if self.start_time <= time <= self.end_time:
                return True
            return False

    def __str__(self):
        return str(self.__id) + " " + str(self.persons) + " " + self.date.strftime("%Y.%m.%d") + " " + self.start_time.strftime("%H:%M") + " " + self.end_time.strftime("%H:%M") + " " + self.description
    def __deepcopy__(self, memodict={}):
        return Activity(self.id, self.persons, self.date.strftime("%Y.%m.%d"), self.start_time.strftime("%H:%M"), self.end_time.strftime("%H:%M"), self.description)