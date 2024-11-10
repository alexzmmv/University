class Action:
    def __call__(self, service):
        pass

    def undo(self, service):
        pass

    def redo(self, service):
        pass


class AddActivity(Action):
    def __init__(self, activity_id, persons_id, date, start_time, end_time, description):
        super().__init__()
        self.__activity_id = activity_id
        self.__persons_id = persons_id
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__description = description

    def __call__(self, service):
        service.add_activity(self.__activity_id,
                             self.__persons_id,
                             self.__date,
                             self.__start_time,
                             self.__end_time,
                             self.__description)

    def undo(self, service):
        service.remove_activity(self.__activity_id)

    def redo(self, service):
        self.__call__(service)


class UpdateActivity(Action):
    def __init__(self, activity_id, persons_id, date, start_time, end_time, description):
        super().__init__()
        self.__activity_id = activity_id
        self.__persons_id = persons_id
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__description = description
        self.__original_state = None

    def __call__(self, service):
        self.__original_state = service.search_activity_by_id(self.__activity_id)
        service.update_activity(self.__activity_id,
                                self.__persons_id,
                                self.__date,
                                self.__start_time,
                                self.__end_time,
                                self.__description)

    def undo(self, service):
        if self.__original_state:
            service.update_activity(self.__activity_id,
                                    self.__original_state.persons,
                                    self.__original_state.date,
                                    self.__original_state.start_time,
                                    self.__original_state.end_time,
                                    self.__original_state.description)

    def redo(self, service):
        self.__call__(service)


class RemoveActivity(Action):
    def __init__(self, activity_id):
        super().__init__()
        self.__activity_id = activity_id
        self.__removed_activity = None

    def __call__(self, service):
        self.__removed_activity = service.search_activity_by_id(self.__activity_id)
        service.remove_activity(self.__activity_id)

    def undo(self, service):
        if self.__removed_activity:
            service.add_activity(
                self.__removed_activity.activity_id,
                self.__removed_activity.persons_id,
                self.__removed_activity.date,
                self.__removed_activity.start_time,
                self.__removed_activity.end_time,
                self.__removed_activity.description
            )

    def redo(self, service):
        self.__call__(service)


class AddPerson(Action):
    def __init__(self, person_id, name, phone_number):
        super().__init__()
        self.__person_id = person_id
        self.__name = name
        self.__phone_number = phone_number

    def __call__(self, service):
        service.add_person(self.__person_id, self.__name, self.__phone_number)

    def undo(self, service):
        service.remove_person(self.__person_id)

    def redo(self, service):
        self.__call__(service)


class UpdatePerson(Action):
    def __init__(self, person_id, name, phone_number):
        super().__init__()
        self.__person_id = person_id
        self.__name = name
        self.__phone_number = phone_number
        self.__original_state = None

    def __call__(self, service):
        self.__original_state = service.search_person_by_id(self.__person_id)
        service.update_person(self.__person_id, self.__name, self.__phone_number)

    def undo(self, service):
        if self.__original_state:
            service.update_person(self.__person_id, self.__original_state.name, self.__original_state.phone_number)

    def redo(self, service):
        self.__call__(service)


class RemovePerson(Action):
    def __init__(self, person_id):
        super().__init__()
        self.__person_id = person_id
        self.__removed_person = None
        self.__removed_person_activities = None

    def __call__(self, service):
        self.__removed_person_activities = service.search_activities_by_person_id(self.__person_id)
        self.__removed_person = service.search_person_by_id(self.__person_id)
        service.remove_person(self.__person_id)

    def undo(self, service):
        if self.__removed_person:
            service.add_person(
                self.__removed_person.id,
                self.__removed_person.name,
                self.__removed_person.phone_number
            )
            for activity in self.__removed_person_activities:
                activity.persons.append(self.__person_id)
                service.update_activity(activity.id,
                                        activity.persons,
                                        activity.date,
                                        activity.start_time,
                                        activity.end_time,
                                        activity.description
                                        )

    def redo(self, service):
        if self.__removed_person:
            service.remove_person(self.__person_id)


class UndoRedoManager:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def do(self, action, service):
        action(service)
        self._undo_stack.append(action)
        self._redo_stack = []

    def undo(self, service):
        if self._undo_stack:
            action = self._undo_stack.pop()
            action.undo(service)
            self._redo_stack.append(action)

    def redo(self, service):
        if self._redo_stack:
            action = self._redo_stack.pop()
            action.redo(service)
            self._undo_stack.append(action)
