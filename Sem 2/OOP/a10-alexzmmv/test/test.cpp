#include "test.h"

void test::testall() {
    testDomain();
    testRepository();
    testController();
    testUserPlanner();
}

void test::testDomain() {
    auto a=Activity();
    assert(a.getTitle()=="");
    assert(a.getDescription()=="");
    assert(a.getLink()=="");
    assert(a.getDateTime().getYear()==0);
    assert(a.getDateTime().getMonth()==0);
    assert(a.getDateTime().getDay()==0);
    assert(a.getDateTime().getHour()==0);
    assert(a.getDateTime().getMinute()==0);
    assert(a.getPeopleGoing()==0);
    assert(a.getDuration()==0);
    a.setTitle("title");
    a.setDescription("description");
    a.setLink("link");
    a.setDateTime(DateTime(2021, 5, 10, 12, 30));
    a.setPeopleGoing(10);
    a.setDuration(100);
    assert(a.getTitle()=="title");
    assert(a.getDescription()=="description");
    assert(a.getLink()=="link");
    assert(a.getDateTime().getYear()==2021);
    assert(a.getDateTime().getMonth()==5);
    assert(a.getDateTime().getDay()==10);
    assert(a.getDateTime().getHour()==12);
    assert(a.getDateTime().getMinute()==30);
    assert(a.getPeopleGoing()==10);
    assert(a.getDuration()==100);
    a.incPeopleGoing();
    assert(a.getPeopleGoing()==11);
    a.decPeopleGoing();
    assert(a.getPeopleGoing()==10);
    auto b=Activity("title", "description", "link", DateTime(2021, 5, 10, 12, 30), 100, 10);
    assert(a==b);
}

void test::testRepository() {
    assert(true);
}

void test::testController() {
    assert(true);
}

void test::testUserPlanner() {
    assert(true);
}