
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

class addCommand:public command{
    private:
        Repository& repo;
        Activity activity;
    public:
        addCommand(Repository& repo, Activity activity) : repo{ repo }, activity{ activity } {};
        void execute() override {
            repo.addActivity(activity.getTitle(), activity.getDescription(), activity.getLink(), activity.getDateTime(), activity.getPeopleGoing(), activity.getDuration());
        }
        void undo() override{
            repo.removeActivity(activity.getTitle());
        }
        void redo() override{
            repo.addActivity(activity.getTitle(), activity.getDescription(), activity.getLink(), activity.getDateTime(), activity.getPeopleGoing(), activity.getDuration());
        }
        ~addCommand() override {

        }

};

class removeCommand:public command{
    private:
        Repository& repo;
        Activity activity;
    public:
        removeCommand(Repository& repo, Activity activity) : repo{ repo }, activity{ activity } {};
        void execute() override{
            repo.removeActivity(activity.getTitle());
        }
        void undo() override{
            repo.addActivity(activity.getTitle(), activity.getDescription(), activity.getLink(), activity.getDateTime(), activity.getPeopleGoing(), activity.getDuration());
        }
        void redo() override{
            repo.removeActivity(activity.getTitle());
        }
        ~removeCommand() override {

        }
};

class updateCommand : public command{
    private:
        Repository& repo;
        Activity activity;
        Activity newActivity;
    public:
        updateCommand(Repository& repo,Activity newActivity) : repo{ repo }, newActivity{ newActivity } {};
        void execute() override{
            activity=repo.getActivityByTitle(newActivity.getTitle());
            repo.updateActivity(newActivity.getTitle(), newActivity.getDescription(), newActivity.getLink(), newActivity.getDateTime(), newActivity.getPeopleGoing(), newActivity.getDuration());
        }
        void undo() override{
            repo.updateActivity(activity.getTitle(), activity.getDescription(), activity.getLink(), activity.getDateTime(), activity.getPeopleGoing(), activity.getDuration());
        }
        void redo() override{
            repo.updateActivity(newActivity.getTitle(), newActivity.getDescription(), newActivity.getLink(), newActivity.getDateTime(), newActivity.getPeopleGoing(), newActivity.getDuration());
        }
        ~updateCommand() override {

        }
};
