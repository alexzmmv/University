#include "SMMIterator.h"
#include "SortedMultiMap.h"

SMMIterator::SMMIterator(const SortedMultiMap& d) : map(d){
    this->currentNode = map.head;
}

void SMMIterator::first(){
    currentNode = map.head;
}

void SMMIterator::next(){
    if (this->valid())
        currentNode = currentNode->next;
    else
        throw std::exception();
}

bool SMMIterator::valid() const{
	return currentNode != nullptr;
}

TElem SMMIterator::getCurrent() const{
    if (!this->valid())
        throw std::exception();
    return currentNode->elem;
}
