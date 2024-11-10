#include <exception>
#include "SetIterator.h"
#include "Set.h"


SetIterator::SetIterator(const Set& m) : set(m)
{
    head = m.head;
    current = head;
}


void SetIterator::first() {
    current = head;
}


void SetIterator::next() {
    if (!valid()) {
        throw std::exception();
    }
    current = set.elements[current].next;
}


TElem SetIterator::getCurrent()
{
    if (!valid()) {
        throw std::exception();
    }
    return set.elements[current].value;
}

bool SetIterator::valid() const {
	    return current != -1;
}



