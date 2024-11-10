
#pragma once
#include <vector>
class Observer {
public:
    virtual void update() = 0;
    virtual ~Observer() = default;
};

class Subject{
    std::vector<Observer*> obs;
public:
    void subscribe(Observer* observer){
        obs.push_back(observer);
    }
     void notify(){
        for(auto observer : obs){
            observer->update();
        }
    }
    ~Subject() = default;
};
