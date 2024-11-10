#pragma once
#include "SortedIndexedList.h"


//DO NOT CHANGE THIS PART
class ListIterator{
    friend class SortedIndexedList;
private:
    const SortedIndexedList& list;
    ListIterator(const SortedIndexedList& list);

    int* stack;
    int top;
    TComp current;

public:
    void first();
    void next();
    bool valid() const;
    TComp getCurrent() const;

    ~ListIterator();
};

