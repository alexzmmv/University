
#include "Repository.h"

class command {
private:
public:
    command()=default;
    virtual void execute() = 0;
    virtual void undo() = 0;
    virtual void redo() = 0;
    virtual ~command() = default;
};

class addCommand{
private:
    Repository& repo;
    Activity activity;
public:
addCommand(Repository& repo, Activity activity) : repo{ repo }, activity{ activity } {};
    void execute() {
        repo.addActivity(activity.getTitle(), activity.getDescription(), activity.getLink(), activity.getDateTime(), activity.getPeopleGoing(), activity.getDuration());
    }
    void undo() {
        repo.removeActivity(activity.getTitle());
    }
    void redo() {
        repo.addActivity(activity.getTitle(), activity.getDescription(), activity.getLink(), activity.getDateTime(), activity.getPeopleGoing(), activity.getDuration());
    }
};

class removeCommand {
private:
    Repository& repo;
    Activity activity;
public:
    removeCommand(Repository& repo, Activity activity) : repo{ repo }, activity{ activity } {};
    void execute() {
        repo.removeActivity(activity.getTitle());
    }
    void undo() {
        repo.addActivity(activity.getTitle(), activity.getDescription(), activity.getLink(), activity.getDateTime(), activity.getPeopleGoing(), activity.getDuration());
    }
    void redo() {
        repo.removeActivity(activity.getTitle());
    }
};

class updateCommand {
private:
    Repository& repo;
    Activity activity;
    Activity newActivity;
public:
    updateCommand(Repository& repo, Activity activity, Activity newActivity) : repo{ repo }, activity{ activity }, newActivity{ newActivity } {};
    void execute() {
        repo.updateActivity(newActivity.getTitle(), newActivity.getDescription(), newActivity.getLink(), newActivity.getDateTime(), newActivity.getPeopleGoing(), newActivity.getDuration());
    }
    void undo() {
        repo.updateActivity(activity.getTitle(), activity.getDescription(), activity.getLink(), activity.getDateTime(), activity.getPeopleGoing(), activity.getDuration());
    }
    void redo() {
        repo.updateActivity(newActivity.getTitle(), newActivity.getDescription(), newActivity.getLink(), newActivity.getDateTime(), newActivity.getPeopleGoing(), newActivity.getDuration());
    }
};
